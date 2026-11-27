"""Exercise the public CLI against disposable Git objects and a loopback-only GitHub/gh."""
from __future__ import annotations

import base64
import copy
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from test_book_release import ROOT, comment, github_fixture, pr, review


class GitHubRepository:
    repo = "webmaxru/book"

    def __init__(self, folder):
        self.folder = folder
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        self.git("init", "-b", "main")
        self.write("content/version.yml", 'version: "1.2"\n')
        self.write("content/CHANGELOG.md", "## [1.2]\nOld edition.\n")
        self.write("content/chapters/intro.html", "<h1>Old edition</h1>\n")
        self.git("add", ".")
        self.git("commit", "-m", "Old edition")
        self.base = self.git("rev-parse", "HEAD")
        self.git("checkout", "-b", "content")
        self.write("content/version.yml", 'version: "1.3"\n')
        self.write("content/CHANGELOG.md", "## [1.3]\nNew edition.\n\n## [1.2]\nOld edition.\n")
        self.write("content/chapters/intro.html", "<h1>New edition</h1>\n")
        self.git("add", ".")
        self.git("commit", "-m", "Approved content")
        self.head = self.git("rev-parse", "HEAD")
        self.merge = self.git("commit-tree", f"{self.head}^{{tree}}", "-p", self.base, "-m", "Squash")
        self.git("checkout", "main")
        self.pull = pr()
        self.pull["head"]["sha"] = self.head
        self.pull["base"]["sha"] = self.base
        self.comments = [comment(self.head)]
        self.reviews = []
        self.timeline = []
        self.actions = []
        self.gh_calls = []
        self.releases = []
        self.assets = {}
        self.comparison_override = {}
        self.missing_compare_files = False
        self.main_reads = 0
        self.move_main_after_read = None
        self.skip_upload = False
        self.fail_upload = False
        self.latest = None

    def git(self, *args, input=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false",
             "-c", f"core.hooksPath={self.folder / 'disabled-hooks'}", *args],
            cwd=self.folder, env=self.env, input=input.encode("utf-8") if input is not None else None,
            check=True, capture_output=True, timeout=20,
        ).stdout.decode("utf-8").strip()

    def write(self, path, content):
        target = self.folder / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def add_main_commit(self, path, content):
        self.git("checkout", "-f", "main")
        self.write(path, content)
        self.git("add", "--", path)
        self.git("commit", "-m", f"Update {path}")
        return self.git("rev-parse", "HEAD")

    def merged(self):
        self.pull.update(state="closed", merged=True, merge_commit_sha=self.merge,
                         merged_by={"login": "github-actions[bot]"})
        self.git("update-ref", "refs/heads/main", self.merge)

    def released(self, tag, sha, *, draft=False, prerelease=False, pdf=False, annotated=False):
        if annotated:
            self.git("tag", "-a", tag, sha, "-m", tag)
        else:
            self.git("update-ref", f"refs/tags/{tag}", sha)
        item = {"id": len(self.releases) + 1, "tag_name": tag, "draft": draft,
                "prerelease": prerelease, "target_commitish": "main"}
        self.releases.append(item)
        self.assets[item["id"]] = (
            [{"name": f"apm-book-{tag}.pdf", "state": "uploaded", "size": 30}] if pdf else [])
        return item

    def route(self, method, url, data):
        self.actions.append((method, url, data))
        parsed = urlsplit(url)
        path = parsed.path.removeprefix(f"/repos/{self.repo}/")
        query = parse_qs(parsed.query)
        if path == "_fixture/gh" and method == "POST":
            return self.run_gh(data)
        if path.startswith("git/ref/"):
            name = path.removeprefix("git/ref/")
            if name == "heads/main":
                self.main_reads += 1
                if self.move_main_after_read and self.main_reads > self.move_main_after_read:
                    self.git("update-ref", "refs/heads/main", self.head)
            try:
                sha = self.git("show-ref", "--verify", "--hash", f"refs/{name}")
            except subprocess.CalledProcessError:
                raise AssertionError("missing ref") from None
            return {"object": {"sha": sha, "type": self.git("cat-file", "-t", sha)}}
        if path.startswith("git/tags/"):
            sha = path.rsplit("/", 1)[-1]
            obj = self.git("cat-file", "-p", sha)
            fields = dict(line.split(" ", 1) for line in obj.split("\n\n")[0].splitlines())
            return {"object": {"sha": fields["object"], "type": fields["type"]}}
        if path.startswith("git/commits/"):
            sha = path.rsplit("/", 1)[-1]
            return {"parents": [{"sha": p} for p in self.git("show", "-s", "--format=%P", sha).split()],
                    "tree": {"sha": self.git("show", "-s", "--format=%T", sha)}}
        if path == "git/tags" and method == "POST":
            tag = (f"object {data['object']}\ntype {data['type']}\ntag {data['tag']}\n"
                   f"tagger Fixture <fixture@example.invalid> 1760000000 +0000\n\n{data['message']}\n")
            return {"sha": self.git("mktag", input=tag)}
        if path == "git/refs" and method == "POST":
            self.git("update-ref", data["ref"], data["sha"], "0" * 40)
            return {"ref": data["ref"]}
        if path.startswith("compare/"):
            base, head = path.removeprefix("compare/").split("...")
            ancestor = self.git("merge-base", base, head)
            files = []
            for line in self.git("diff", "--name-status", "-M", base, head).splitlines():
                status, *names = line.split("\t")
                item = {"filename": names[-1], "status": status}
                if len(names) > 1:
                    item["previous_filename"] = names[0]
                files.append(item)
            result = {"merge_base_commit": {"sha": ancestor},
                      "status": "identical" if base == head else "ahead" if ancestor == base else "behind",
                      "files": files}
            result.update(self.comparison_override)
            if self.missing_compare_files:
                result.pop("files", None)
            return result
        if path == "pulls/7":
            return copy.deepcopy(self.pull)
        if path == "pulls":
            return [{"number": 7}]
        if path == "pulls/7/files":
            return [{"filename": p} for p in
                    ("content/version.yml", "content/CHANGELOG.md", "content/chapters/intro.html")]
        if path == "pulls/7/reviews":
            return self.reviews
        if path == "issues/7/comments":
            return self.comments
        if path == "issues/7/timeline":
            return self.timeline
        if path == "pulls/7/merge" and method == "PUT":
            assert data == {"sha": self.head, "merge_method": "squash"}
            self.merged()
            return {"merged": True, "sha": self.merge}
        if path == "actions/workflows/ci.yml/runs":
            assert query["head_sha"] == [self.head] and query["event"] == ["pull_request"]
            return {"workflow_runs": [{"id": 3, "status": "completed", "conclusion": "success",
                                      "event": "pull_request", "head_sha": self.head,
                                      "head_branch": "content", "head_repository": {"full_name": self.repo}}]}
        if path == "actions/runs/3/jobs":
            return {"total_count": 1, "jobs": [{"name": "Book release preflight", "head_sha": self.head,
                                               "status": "completed", "conclusion": "success"}]}
        if path == "actions/workflows/release.yml/dispatches" and method == "POST":
            assert data == {"ref": "main", "inputs": {"pr": "7", "head_sha": self.head,
                           "base_sha": self.base, "merge_sha": self.merge, "tag": "v1.3"}}
            return None
        if path == "contents/content/version.yml":
            text = self.git("show", f"{query['ref'][0]}:content/version.yml") + "\n"
            return {"encoding": "base64", "content": base64.b64encode(text.encode()).decode()}
        if path.startswith("commits/") and path.endswith("/pulls"):
            sha = path.split("/")[1]
            return ([{"number": 7, "merged_at": "2026-01-04T00:00:00Z", "merge_commit_sha": self.merge}]
                    if self.pull["merged"] and sha == self.merge else [])
        if path == "releases":
            return self.releases
        if path.startswith("releases/") and path.endswith("/assets"):
            return self.assets.get(int(path.split("/")[1]), [])
        raise AssertionError((method, url, data))

    def run_gh(self, args):
        self.gh_calls.append(args)
        assert args[0] == "release" and args[-2:] == ["--repo", self.repo]
        assert "--clobber" not in args
        operation, tag = args[1:3]
        item = next((r for r in self.releases if r["tag_name"] == tag), None)
        if operation == "create":
            assert not item and "--verify-tag" in args and "--draft" in args and "--latest=false" in args
            self.git("show-ref", "--verify", f"refs/tags/{tag}")
            item = {"id": len(self.releases) + 1, "tag_name": tag, "draft": True, "prerelease": False}
            self.releases.append(item)
            self.assets[item["id"]] = []
        elif operation == "upload":
            assert item and item["draft"]
            if self.fail_upload:
                return {"exit": 1}
            if not self.skip_upload:
                pdf = Path(args[3])
                assert pdf.read_bytes().startswith(b"%PDF-")
                self.assets[item["id"]].append({"name": pdf.name, "state": "uploaded",
                                                "size": pdf.stat().st_size})
        elif operation == "edit":
            assert item and item["draft"] and "--draft=false" in args
            assert self.assets[item["id"]]
            item["draft"] = False
            if "--latest=true" in args:
                self.latest = tag
        else:
            raise AssertionError(operation)
        return {"exit": 0}


class CLIBase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix=".book-release-test-", dir=ROOT)
        self.addCleanup(directory.cleanup)
        self.folder = Path(directory.name)
        self.repo = GitHubRepository(self.folder)
        context = github_fixture(self.repo)
        self.api_url = context.__enter__()
        self.addCleanup(context.__exit__, None, None, None)
        shim = self.repo.write("fixture-gh.py", """import json, os, sys, urllib.parse, urllib.request
api = os.environ["GITHUB_API_URL"]
assert urllib.parse.urlsplit(api).hostname == "127.0.0.1", "fixture gh only supports loopback"
request = urllib.request.Request(
    api + "/repos/webmaxru/book/_fixture/gh", method="POST",
    data=json.dumps(sys.argv[1:]).encode(), headers={"Content-Type": "application/json"})
with urllib.request.urlopen(request, timeout=10) as response:
    result = json.load(response)
sys.exit(result["exit"])
""")
        if os.name == "nt":
            launcher = self.repo.write("gh.cmd", f'@echo off\n"{sys.executable}" "{shim}" %*\nexit /b %errorlevel%\n')
        else:
            launcher = self.repo.write("gh", f"#!/bin/sh\nexec {shlex.quote(sys.executable)} "
                                      f'{shlex.quote(str(shim))} "$@"\n')
            launcher.chmod(0o755)
        self.output_path = self.folder / "outputs.txt"
        self.env = dict(os.environ, GITHUB_API_URL=self.api_url, GITHUB_REPOSITORY=self.repo.repo,
                        GH_REPO=self.repo.repo, GH_TOKEN="loopback-fixture", BOOK_RELEASE_GH=str(launcher),
                        GITHUB_TOKEN="loopback-fixture", GITHUB_OUTPUT=str(self.output_path),
                        NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")

    def cli(self, *args, succeeds=True):
        self.output_path.write_text("", encoding="utf-8")
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "book_release.py"), *args],
                                cwd=self.folder, env=self.env, text=True, capture_output=True, timeout=30)
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        values = dict(line.split("=", 1) for line in self.output_path.read_text(encoding="utf-8").splitlines())
        for key, value in values.items():
            self.assertIn(f"{key}={value}", result.stdout)
        return result, values

    def no_writes(self):
        self.assertFalse([a for a in self.repo.actions if a[0] != "GET"])
        self.assertFalse(self.repo.gh_calls)

    def artifacts(self):
        pdf = self.repo.write("apm-book-v1.3.pdf", "%PDF-1.7 fixture\n")
        notes = self.repo.write("notes.md", "New edition.\n")
        return ["--pdf", str(pdf), "--notes", str(notes)]


class ReleaseCLIEndToEndTests(CLIBase):
    def test_inspect_merge_plan_publish_recover_and_deploy(self):
        event = self.repo.write("event.json", json.dumps({"issue": {"number": 7, "pull_request": {}},
                                                         "comment": comment(self.repo.head)}))
        _, inspected = self.cli("inspect", "--event", str(event))
        self.assertEqual(inspected, {"eligible": "true", "pr": "7",
                                     "head": self.repo.head, "base": self.repo.base})
        _, merged = self.cli("merge", "--pr", "7", "--head", self.repo.head, "--base", self.repo.base)
        self.assertEqual(merged, {"merge_sha": self.repo.merge, "tag": "v1.3"})
        dispatch = [a for a in self.repo.actions if a[1].endswith("release.yml/dispatches")]
        self.assertEqual(len(dispatch), 1)
        _, plan = self.cli("release-plan", "--pr", "7", "--head", self.repo.head,
                           "--base", self.repo.base, "--merge-sha", self.repo.merge, "--tag", "v1.3")
        self.assertEqual(plan["recovery"], "false")
        self.assertEqual(plan["tag"], "v1.3")
        self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge, *self.artifacts())
        self.assertEqual([a[1] for a in self.repo.gh_calls], ["create", "upload", "edit"])
        self.assertEqual(self.repo.latest, "v1.3")
        self.assertEqual(self.repo.git("cat-file", "-t", "v1.3"), "tag")
        self.assertEqual(self.repo.git("rev-parse", "v1.3^{}"), self.repo.merge)
        self.repo.actions.clear()
        self.repo.gh_calls.clear()
        _, recovery = self.cli("release-plan", "--tag", "v1.3")
        self.assertEqual(recovery["recovery"], "true")
        self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge)
        _, deployment = self.cli("deploy-plan", "--ref", "v1.3")
        self.assertEqual(deployment, {"eligible": "true", "sha": self.repo.merge, "tag": "v1.3"})
        self.no_writes()

    def test_nonowner_approval_then_dismissal_or_push_revokes(self):
        self.repo.pull["user"]["login"] = "contributor"
        self.repo.reviews = [review(sha=self.repo.head)]
        event = self.repo.write("event.json", json.dumps({"inputs": {"pr": "7"}}))
        _, approved = self.cli("inspect", "--event", str(event))
        self.assertEqual(approved["eligible"], "true")
        later = dict(review("DISMISSED", self.repo.head), id=2, submitted_at="2026-01-05T00:00:00Z")
        self.repo.reviews.append(later)
        _, revoked = self.cli("inspect", "--event", str(event))
        self.assertEqual(revoked["eligible"], "false")
        self.repo.reviews = [review(sha=self.repo.base)]
        self.cli("merge", "--pr", "7", "--head", self.repo.head, "--base", self.repo.base, succeeds=False)
        self.no_writes()

    def test_complete_release_cannot_hide_forged_squash_tree(self):
        self.repo.merge = self.repo.git("commit-tree", f"{self.repo.base}^{{tree}}",
                                        "-p", self.repo.base, "-m", "Forged merge")
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge, pdf=True)
        for operation in ("release-plan", "publish"):
            result, _ = self.cli(operation, "--tag", "v1.3", "--merge-sha", self.repo.merge, succeeds=False)
            self.assertIn("Merged tree", result.stderr)
        self.no_writes()

    def test_manual_merge_and_off_main_merge_fail_before_publication(self):
        self.repo.merged()
        self.repo.pull["merged_by"] = {"login": "webmaxru"}
        result, _ = self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge, succeeds=False)
        self.assertIn("GitHub Actions controller", result.stderr)
        self.repo.pull["merged_by"] = {"login": "github-actions[bot]"}
        self.repo.git("update-ref", "refs/heads/main", self.repo.base)
        result, _ = self.cli("release-plan", "--pr", "7", "--merge-sha", self.repo.merge, succeeds=False)
        self.assertIn("not on main", result.stderr)
        self.no_writes()

    def test_incomplete_published_release_and_missing_tag_fail_without_writes(self):
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge)
        for operation in ("release-plan", "publish"):
            result, _ = self.cli(operation, "--tag", "v1.3", "--merge-sha", self.repo.merge, succeeds=False)
            self.assertIn("incomplete", result.stderr)
        self.repo.git("update-ref", "-d", "refs/tags/v1.3")
        result, _ = self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge, succeeds=False)
        self.assertIn("no matching stable edition tag", result.stderr)
        self.no_writes()

    def test_tag_never_overrides_supplied_merge_sha(self):
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge, annotated=True)
        for operation in ("release-plan", "publish"):
            result, _ = self.cli(operation, "--tag", "v1.3", "--merge-sha", self.repo.base, succeeds=False)
            self.assertIn("another commit", result.stderr)
        self.no_writes()

    def test_latest_ignores_drafts_prereleases_and_nonnumeric_tags(self):
        self.repo.merged()
        for tag, draft, prerelease in (("v1.2", False, False), ("v9.0", True, False),
                                       ("v10.0", False, True), ("v88.0-rc.1", False, False)):
            self.repo.released(tag, self.repo.base, draft=draft, prerelease=prerelease)
        self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge, *self.artifacts())
        self.assertEqual(self.repo.latest, "v1.3")

    def test_old_stable_is_published_without_stealing_latest(self):
        self.repo.merged()
        self.repo.released("v1.10", self.repo.base)
        self.repo.latest = "v1.10"
        self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge, *self.artifacts())
        self.assertEqual(self.repo.latest, "v1.10")
        self.assertIn("--latest=false", self.repo.gh_calls[-1])

    def test_partial_tag_and_draft_never_receive_recovery_writes(self):
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge, draft=True, pdf=True)
        for operation in ("release-plan", "publish"):
            result, _ = self.cli(operation, "--tag", "v1.3", "--merge-sha", self.repo.merge, succeeds=False)
            self.assertIn("draft release is incomplete", result.stderr)
        self.repo.releases.clear()
        result, _ = self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge, succeeds=False)
        self.assertIn("no complete published release", result.stderr)
        self.no_writes()

    def failed_upload(self, *, fail):
        self.repo.merged()
        self.repo.fail_upload, self.repo.skip_upload = fail, not fail
        self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge,
                 *self.artifacts(), succeeds=False)
        self.assertTrue(self.repo.releases[0]["draft"])
        self.assertEqual([a[1] for a in self.repo.gh_calls], ["create", "upload"])
        self.repo.actions.clear()
        self.repo.gh_calls.clear()
        self.cli("publish", "--tag", "v1.3", "--merge-sha", self.repo.merge,
                 *self.artifacts(), succeeds=False)
        self.no_writes()

    def test_failed_upload_does_not_publish_or_retry_partial_release(self):
        self.failed_upload(fail=True)

    def test_unconfirmed_upload_does_not_publish_or_retry_partial_release(self):
        self.failed_upload(fail=False)

    def test_prerelease_edition_tag_is_rejected_by_publication(self):
        self.repo.merged()
        for operation in ("release-plan", "publish"):
            self.cli(operation, "--tag", "v1.3-rc.1", "--merge-sha", self.repo.merge, succeeds=False)
        self.no_writes()


class DeployCLIEndToEndTests(CLIBase):
    def setUp(self):
        super().setUp()
        # Deliberately no release-plan provenance, PDF assets, or novel metadata: legacy rollback.
        self.repo.released("v1.2", self.repo.base, annotated=True)

    def test_published_main_and_tooling_only_main_are_eligible(self):
        _, exact = self.cli("deploy-plan", "--sha", self.repo.base)
        self.assertEqual(exact, {"eligible": "true", "sha": self.repo.base, "tag": "v1.2"})
        main = self.repo.add_main_commit("site/generate.py", "# trusted tooling update\n")
        _, tooling = self.cli("deploy-plan", "--sha", main)
        self.assertEqual(tooling, {"eligible": "true", "sha": main, "tag": "v1.2"})
        self.no_writes()

    def test_unreleased_content_on_main_does_not_deploy(self):
        main = self.repo.add_main_commit("content/chapters/intro.html", "<h1>Unreleased</h1>\n")
        result, values = self.cli("deploy-plan", "--sha", main)
        self.assertEqual(values, {"eligible": "false", "sha": main, "tag": "v1.2"})
        self.assertIn("book content different", result.stderr)
        self.no_writes()

    def test_allowlist_is_shared_including_renamed_out_content(self):
        paths = ("content/version.yml", "content/CHANGELOG.md", "content/toc.yml",
                 "content/research/proof.json", "backend/examples/apm.yml", "site/index.html",
                 "site/chapters/intro.html", "site/llms-full.txt", "site/sitemap.xml")
        for path in paths:
            with self.subTest(path=path):
                self.repo.comparison_override = {"files": [{"filename": path}]}
                _, values = self.cli("deploy-plan", "--sha", self.repo.base)
                self.assertEqual(values["eligible"], "false")
        self.repo.comparison_override = {"files": [{"filename": "tools/intro.html",
                                                   "previous_filename": "content/chapters/intro.html"}]}
        _, renamed = self.cli("deploy-plan", "--sha", self.repo.base)
        self.assertEqual(renamed["eligible"], "false")
        self.no_writes()

    def test_rollback_tag_and_full_sha_keep_their_commit_when_main_moves(self):
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge)
        self.repo.add_main_commit("scripts/build.py", "# updated tooling\n")
        for ref in ("v1.2", self.repo.base):
            _, rollback = self.cli("deploy-plan", "--ref", ref)
            self.assertEqual(rollback, {"eligible": "true", "sha": self.repo.base, "tag": "v1.2"})
        _, newer = self.cli("deploy-plan", "--ref", "v1.3")
        self.assertEqual(newer["sha"], self.repo.merge)
        self.no_writes()

    def test_latest_stable_wins_over_newer_draft_and_prerelease(self):
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge)
        self.repo.released("v9.0", self.repo.base, draft=True)
        self.repo.released("v10.0", self.repo.base, prerelease=True)
        _, selected = self.cli("deploy-plan", "--sha", self.repo.merge)
        self.assertEqual(selected, {"eligible": "true", "sha": self.repo.merge, "tag": "v1.3"})
        for ref in ("v9.0", "v10.0"):
            _, denied = self.cli("deploy-plan", "--ref", ref, succeeds=False)
            self.assertEqual(denied["eligible"], "false")
        self.no_writes()

    def test_draft_content_cannot_authorize_main_or_manual_deploy(self):
        self.repo.merged()
        self.repo.released("v1.3", self.repo.merge, draft=True)
        _, main = self.cli("deploy-plan", "--sha", self.repo.merge)
        self.assertEqual(main["eligible"], "false")
        self.cli("deploy-plan", "--ref", "v1.3", succeeds=False)
        self.cli("deploy-plan", "--ref", self.repo.merge, succeeds=False)
        self.no_writes()

    def test_unreleased_refs_arbitrary_branches_and_bad_inputs_are_rejected(self):
        self.repo.git("update-ref", "refs/tags/v1.4", self.repo.head)
        for ref in ("v1.4", self.repo.head, "main", "content", "refs/tags/v1.2",
                    self.repo.base[:12], "v1.2-rc.1"):
            with self.subTest(ref=ref):
                self.cli("deploy-plan", "--ref", ref, succeeds=False)
        self.cli("deploy-plan", succeeds=False)
        self.cli("deploy-plan", "--sha", self.repo.base, "--ref", "v1.2", succeeds=False)
        self.cli("deploy-plan", "--sha", "main", succeeds=False)
        self.no_writes()

    def test_stale_push_and_main_race_fail_closed(self):
        self.cli("deploy-plan", "--sha", self.repo.head, succeeds=False)
        self.repo.main_reads = 0
        self.repo.move_main_after_read = 1
        result, values = self.cli("deploy-plan", "--sha", self.repo.base, succeeds=False)
        self.assertIn("Main moved", result.stderr)
        self.assertEqual(values, {"eligible": "false", "sha": "", "tag": ""})
        self.no_writes()

    def test_comparison_truncation_and_invalid_paths_fail_closed(self):
        overrides = (
            {"files": [{"filename": f"tooling/file-{i}.py"} for i in range(300)]},
            {"total_files": 1}, {"truncated": True}, {"files_truncated": True},
            {"files": [{"filename": "site/../content/chapters/intro.html"}]},
            {"files": [{"filename": r"content\chapters\intro.html"}]},
            {"files": [{}]},
        )
        for override in overrides:
            with self.subTest(override=list(override)):
                self.repo.comparison_override = override
                _, values = self.cli("deploy-plan", "--sha", self.repo.base, succeeds=False)
                self.assertEqual(values["eligible"], "false")
        self.repo.comparison_override = {}
        self.repo.missing_compare_files = True
        self.cli("deploy-plan", "--sha", self.repo.base, succeeds=False)
        self.no_writes()

    def test_release_off_main_is_not_a_push_deployment_baseline(self):
        self.repo.released("v1.3", self.repo.head)
        result, _ = self.cli("deploy-plan", "--sha", self.repo.base, succeeds=False)
        self.assertIn("not an ancestor", result.stderr)
        self.no_writes()

    def test_no_published_edition_does_not_deploy(self):
        self.repo.releases[0]["draft"] = True
        _, values = self.cli("deploy-plan", "--sha", self.repo.base)
        self.assertEqual(values, {"eligible": "false", "sha": self.repo.base, "tag": ""})
        self.no_writes()


if __name__ == "__main__":
    unittest.main()
