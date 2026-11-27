from __future__ import annotations

import contextlib
import base64
import copy
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import book_release as release

HEAD = "a" * 40
BASE = "b" * 40
MERGE = "c" * 40
ANNOTATION = "e" * 40


def pr(author="webmaxru"):
    return {
        "state": "open", "draft": False, "merged": False, "mergeable": True, "changed_files": 3,
        "user": {"login": author}, "head": {"sha": HEAD, "ref": "content",
                                             "repo": {"full_name": "webmaxru/book"}},
        "base": {"sha": BASE, "ref": "main", "repo": {"full_name": "webmaxru/book"}},
    }


def review(state="APPROVED", sha=HEAD):
    return {"id": 1, "user": {"login": "webmaxru"}, "state": state,
            "commit_id": sha, "submitted_at": "2026-01-02T00:00:00Z"}


def comment(sha=HEAD, author="webmaxru", date="2026-01-03T00:00:00Z"):
    return {"user": {"login": author}, "body": f"/release-book {sha}",
            "created_at": date, "updated_at": date}


class ApprovalTests(unittest.TestCase):
    def test_self_author_requires_exact_owner_command(self):
        self.assertTrue(release.approval(pr(), [], [comment()]))
        for item in [comment("d" * 40), comment(author="attacker"),
                     dict(comment(), body=f"/release-book {HEAD}\nextra")]:
            self.assertFalse(release.approval(pr(), [], [item]))
        self.assertFalse(release.approval(pr(), [review()], []))

    def test_edited_or_deleted_command_revokes_approval(self):
        edited = dict(comment(), updated_at="2026-01-04T00:00:00Z")
        missing_timestamp = comment()
        missing_timestamp.pop("updated_at")
        for comments in ([], [edited], [missing_timestamp]):
            self.assertFalse(release.approval(pr(), [], comments))

    def test_review_approval_and_revocation_bind_current_head(self):
        other = pr("contributor")
        self.assertTrue(release.approval(other, [review()], []))
        self.assertFalse(release.approval(other, [review(sha="d" * 40)], []))
        self.assertFalse(release.approval(other, [review("DISMISSED")], []))
        dismissal = {"event": "review_dismissed", "created_at": "2026-01-04T00:00:00Z",
                     "dismissed_review": {"review_id": 1}}
        self.assertFalse(release.approval(pr(), [review("DISMISSED")], [comment()], [dismissal]))
        self.assertTrue(release.approval(pr(), [review("DISMISSED")],
                                         [comment(date="2026-01-05T00:00:00Z")], [dismissal]))

    def test_later_reviews_and_dismissals_are_revocation_barriers(self):
        earlier = review()
        later = dict(review("CHANGES_REQUESTED"), id=2, submitted_at="2026-01-04T00:00:00Z")
        for state in ("CHANGES_REQUESTED", "DISMISSED"):
            with self.subTest(state=state):
                self.assertFalse(release.approval(pr("other"), [earlier, dict(later, state=state)], []))
                self.assertFalse(release.approval(pr(), [earlier, dict(later, state=state)], [comment()]))
        renewed = dict(review(), id=3, submitted_at="2026-01-05T00:00:00Z")
        dismissal = {"event": "review_dismissed", "created_at": "2026-01-06T00:00:00Z",
                     "dismissed_review": {"review_id": 1}}
        self.assertFalse(release.approval(pr("other"), [earlier, renewed], [], [dismissal]))
        self.assertTrue(release.approval(pr("other"), [later, renewed], []))
        self.assertFalse(release.approval(pr(), [later, renewed], [comment()]))
        self.assertTrue(release.approval(pr(), [later, renewed],
                                       [comment(date="2026-01-07T00:00:00Z")], [dismissal]))

    def test_allowlist_rejects_mixed_infrastructure_and_renames(self):
        base = [{"filename": p} for p in
                ["content/chapters/a.html", "content/version.yml", "content/CHANGELOG.md"]]
        release.content_files(base + [{"filename": "backend/examples/new/apm.lock.yaml"}])
        for path in [".github/workflows/evil.yml", "site/generate.py", "site/assets/app.js",
                     "scripts/run-fleet.ps1", "package.json"]:
            with self.subTest(path=path), self.assertRaises(release.GateError):
                release.content_files(base + [{"filename": path}])
        with self.assertRaises(release.GateError):
            release.content_files(base + [{"filename": "content/chapters/x.html",
                                          "previous_filename": "site/generate.py"}])


class FixtureServer:
    def __init__(self):
        self.pull = pr()
        self.comments = [comment()]
        self.files = [{"filename": p} for p in
                      ["content/chapters/a.html", "content/version.yml", "content/CHANGELOG.md"]]
        self.actions = []
        self.pull_reads = 0
        self.change_during_read = False
        self.check_result = "success"
        self.behind = False
        self.main = BASE
        self.reviews = []
        self.timeline = []
        self.job_result = "success"

    def route(self, method, path, body):
        self.actions.append((method, path, body))
        path = path.split("?")[0].removeprefix("/repos/webmaxru/book/")
        if path == "pulls/7":
            self.pull_reads += 1
            result = copy.deepcopy(self.pull)
            if self.change_during_read and self.pull_reads > 1:
                result["head"]["sha"] = "d" * 40
            return result
        if path == "pulls":
            return [{"number": 7}]
        if path == "pulls/7/files":
            return self.files
        if path == "pulls/7/reviews":
            return self.reviews
        if path == "issues/7/timeline":
            return self.timeline
        if path == "issues/7/comments":
            return self.comments
        if path == "actions/workflows/ci.yml/runs":
            return {"workflow_runs": [{"id": 3, "status": "completed", "conclusion": self.check_result,
                                        "event": "pull_request",
                                        "head_sha": HEAD, "head_branch": "content",
                                        "head_repository": {"full_name": "webmaxru/book"},
                                        "pull_requests": []}]}
        if path == "actions/runs/3/jobs":
            return {"total_count": 1, "jobs": [{"name": "Book release preflight",
                                               "head_sha": HEAD, "status": "completed",
                                               "conclusion": self.job_result}]}
        if path == "git/ref/heads/main":
            return {"object": {"sha": self.main}}
        if path == f"compare/{self.main}...{HEAD}":
            return {"merge_base_commit": {"sha": "d" * 40 if self.behind else BASE}}
        if path == "contents/content/version.yml":
            return {"encoding": "base64", "content": base64.b64encode(b'version: "1.3"\n').decode()}
        if path == "pulls/7/merge" and method == "PUT":
            if body != {"sha": HEAD, "merge_method": "squash"}:
                raise AssertionError(body)
            return {"merged": True, "sha": MERGE}
        if path == "actions/workflows/release.yml/dispatches" and method == "POST":
            return None
        raise AssertionError((method, path))


@contextlib.contextmanager
def github_fixture(fixture):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def do_GET(self):
            self.respond()

        def do_POST(self):
            self.respond()

        def do_PUT(self):
            self.respond()

        def do_DELETE(self):
            self.respond()

        def respond(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length)) if length else None
            if hasattr(fixture, "headers_seen"):
                fixture.headers_seen.append(
                    (self.command, self.path, {k.lower(): v for k, v in self.headers.items()}))
            try:
                data = fixture.route(self.command, self.path, body)
            except AssertionError:
                self.send_error(404)
                return
            encoded = json.dumps(data).encode() if data is not None else b""
            self.send_response(200 if encoded else 204)
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


class ControllerEndToEndTests(unittest.TestCase):
    def run_controller(self, fixture, *args):
        with github_fixture(fixture) as api:
            env = dict(os.environ, GITHUB_REPOSITORY="webmaxru/book", GH_TOKEN="fixture",
                       GITHUB_TOKEN="fixture", GH_REPO="webmaxru/book", GITHUB_API_URL=api,
                       NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")
            env.pop("GITHUB_OUTPUT", None)
            return subprocess.run([sys.executable, str(ROOT / "scripts" / "book_release.py"), *args],
                                  env=env, text=True, capture_output=True, timeout=30)

    def test_approved_pr_merges_head_and_explicitly_dispatches_release(self):
        fixture = FixtureServer()
        result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
        self.assertEqual(result.returncode, 0, result.stderr)
        writes = [a for a in fixture.actions if a[0] != "GET"]
        self.assertEqual([a[0] for a in writes], ["PUT", "POST"])
        self.assertEqual(writes[-1][1], "/repos/webmaxru/book/actions/workflows/release.yml/dispatches")
        self.assertEqual(writes[-1][2], {"ref": "main", "inputs": {
            "pr": "7", "head_sha": HEAD, "base_sha": BASE, "merge_sha": MERGE, "tag": "v1.3"}})

    def test_stale_head_and_noncontent_never_merge(self):
        for stale in (False, True):
            fixture = FixtureServer()
            if stale:
                fixture.change_during_read = True
            else:
                fixture.files.append({"filename": ".github/workflows/evil.yml"})
                fixture.pull["changed_files"] += 1
            result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(any(action[0] != "GET" for action in fixture.actions))

    def test_workflow_run_with_empty_pull_requests_resolves_by_branch(self):
        fixture = FixtureServer()
        event = {"workflow_run": {"head_branch": "content",
                                  "head_repository": {"full_name": "webmaxru/book"},
                                  "pull_requests": []}}
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path = Path(directory) / "event.json"
            path.write_text(json.dumps(event), encoding="utf-8")
            result = self.run_controller(fixture, "inspect", "--event", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("eligible=true", result.stdout)
        self.assertIn(f"head={HEAD}", result.stdout)

    def test_pending_or_failed_check_cannot_merge(self):
        fixture = FixtureServer()
        fixture.check_result = "failure"
        result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any(action[0] != "GET" for action in fixture.actions))

    def test_head_behind_main_cannot_merge(self):
        fixture = FixtureServer()
        fixture.behind = True
        result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("behind main", result.stderr)
        self.assertFalse(any(action[0] != "GET" for action in fixture.actions))

    def test_live_main_not_stale_pull_base_is_authoritative(self):
        fixture = FixtureServer()
        fixture.main = "e" * 40
        result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(any("git/ref/heads/main" in a[1] for a in fixture.actions))
        self.assertFalse(any(a[0] != "GET" for a in fixture.actions))

    def test_mergeability_state_and_aggregate_fail_closed(self):
        for mutation in ({"mergeable": False}, {"mergeable": None}, {"mergeable": 1},
                         {"state": "closed"}, {"draft": True}):
            with self.subTest(mutation=mutation):
                fixture = FixtureServer()
                fixture.pull.update(mutation)
                result = self.run_controller(fixture, "merge", "--pr", "7",
                                             "--head", HEAD, "--base", BASE)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(any(a[0] != "GET" for a in fixture.actions))
        for conclusion in ("failure", "skipped", None):
            fixture = FixtureServer()
            fixture.job_result = conclusion
            result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Book release preflight", result.stderr)
            self.assertFalse(any(a[0] != "GET" for a in fixture.actions))

    def test_forks_wrong_base_and_missing_files_cannot_merge(self):
        for mutation in ("fork", "deleted-fork", "branch", "base-repository", "files"):
            with self.subTest(mutation=mutation):
                fixture = FixtureServer()
                if mutation == "fork":
                    fixture.pull["head"]["repo"]["full_name"] = "attacker/book"
                elif mutation == "deleted-fork":
                    fixture.pull["head"]["repo"] = None
                elif mutation == "branch":
                    fixture.pull["base"]["ref"] = "release"
                elif mutation == "base-repository":
                    fixture.pull["base"]["repo"]["full_name"] = "attacker/book"
                else:
                    fixture.pull["changed_files"] = 4
                self.assertNotEqual(self.run_controller(fixture, "merge", "--pr", "7",
                                    "--head", HEAD, "--base", BASE).returncode, 0)
                self.assertFalse(any(a[0] != "GET" for a in fixture.actions))

    def test_scheduled_scan_rotates_among_current_eligible_prs(self):
        class API:
            def request(self, method, path, data=None, **_kwargs):
                self.query = (method, path)
                return [{"number": 7}, {"number": 8}]
        api = API()
        with patch.object(release, "candidate", side_effect=lambda _api, number, **_kw:
                          ({"merged": False}, HEAD, BASE)) as gate:
            with patch.object(release, "output") as output:
                release.inspect(api, {"schedule": "17,47 * * * *"})
        self.assertIn("per_page=30", api.query[1])
        self.assertEqual(gate.call_count, 2)
        self.assertIn(output.call_args.args[0]["pr"], {"7", "8"})


class PublishTests(unittest.TestCase):
    def api(self, *, published=False, tagged=False, assets=False):
        class API(RecoveryTests.API):
            def request(self, method, path, data=None, **kwargs):
                if method == "POST" and path == "git/tags":
                    self.writes.append((path, data))
                    return {"sha": ANNOTATION}
                if method == "POST" and path == "git/refs":
                    self.writes.append((path, data))
                    self.tagged = True
                    return {}
                return super().request(method, path, data, **kwargs)
        api = API(assets=assets)
        api.writes = []
        api.tagged = tagged
        if not published and tagged:
            api.releases[0]["draft"] = True
        elif not published:
            api.releases = []
        return api

    def gh(self, api, calls):
        def run(args, **kwargs):
            self.assertTrue(kwargs["check"])
            calls.append(args)
            self.assertNotIn("--clobber", args)
            self.assertEqual(args[-2:], ["--repo", api.repo])
            if args[2] == "create":
                api.releases.append({"tag_name": "v1.3", "draft": True, "prerelease": False, "id": 42})
            elif args[2] == "upload":
                api.assets = True
            elif args[2] == "edit":
                next(r for r in api.releases if r["tag_name"] == args[3])["draft"] = False
        return run

    def test_conflicting_tag_or_invalid_pdf_never_writes(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            pdf, notes = Path(directory) / "apm-book-v1.3.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            api = self.api(published=True, tagged=True, assets=True)
            with self.assertRaisesRegex(release.GateError, "another commit"):
                release.publish(api, "v1.3", "d" * 40, str(pdf), str(notes))
            self.assertEqual(api.writes, [])
            pdf.write_bytes(b"not a pdf")
            api = self.api()
            with self.assertRaisesRegex(release.GateError, "not a PDF"):
                release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
            self.assertEqual(api.writes, [])

    def test_draft_upload_failure_never_publishes(self):
        api = self.api(tagged=True)
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            pdf, notes = Path(directory) / "apm-book-v1.3.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            with patch.object(release.subprocess, "run") as run:
                with self.assertRaisesRegex(release.GateError, "draft release is incomplete"):
                    release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
                run.assert_not_called()
        self.assertEqual(api.writes, [])
        self.assertTrue(api.releases[0]["draft"])

    def test_duplicate_published_release_never_replaces_assets(self):
        api = self.api(published=True, tagged=True, assets=True)
        with patch.object(release.subprocess, "run") as run:
            release.publish(api, "v1.3", MERGE, None, None)
            run.assert_not_called()
            api.assets = False
            with self.assertRaisesRegex(release.GateError, "incomplete"):
                release.publish(api, "v1.3", MERGE, None, None)
            run.assert_not_called()
        self.assertEqual(api.writes, [])

    def test_build_first_then_draft_upload_and_publish_without_promoting_old_edition(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            pdf, notes = Path(directory) / "apm-book-v1.3.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            api = self.api(tagged=False)
            api.releases = [{"tag_name": "v1.4", "draft": False, "prerelease": False, "id": 43}]
            calls = []
            with patch.object(release.subprocess, "run", side_effect=self.gh(api, calls)):
                release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
            self.assertEqual(api.writes, [
                ("git/tags", {"tag": "v1.3", "message": "v1.3", "object": MERGE, "type": "commit"}),
                ("git/refs", {"ref": "refs/tags/v1.3", "sha": ANNOTATION})])
            self.assertEqual([call[2] for call in calls], ["create", "upload", "edit"])
            self.assertIn("--draft", calls[0])
            self.assertIn("--draft=false", calls[2])
            self.assertIn("--latest=false", calls[2])

    def test_unverified_upload_and_existing_partial_asset_stay_drafts(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            pdf, notes = Path(directory) / "apm-book-v1.3.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            api = self.api()
            calls = []
            fake_gh = self.gh(api, calls)

            def run_without_upload(args, **kwargs):
                if args[2] != "upload":
                    fake_gh(args, **kwargs)

            with patch.object(release.subprocess, "run", side_effect=run_without_upload) as run:
                with self.assertRaisesRegex(release.GateError, "upload is incomplete"):
                    release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
                self.assertEqual(run.call_count, 2)
                api.writes.clear()
                api.asset_state = "starter"
                api.assets = True
                with self.assertRaisesRegex(release.GateError, "draft release is incomplete"):
                    release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
                self.assertEqual(run.call_count, 2)
            self.assertEqual(api.writes, [])


class RecoveryTests(unittest.TestCase):
    class API:
        repo = "webmaxru/book"
        def __init__(self, *, associated=True, assets=True):
            self.associated = associated
            self.assets = assets
            self.pull = pr()
            self.pull.update({"state": "closed", "merged": True, "merge_commit_sha": MERGE,
                              "merged_by": {"login": "github-actions[bot]"}})
            self.tagged = True
            self.releases = [{"draft": False, "prerelease": False, "id": 42, "tag_name": "v1.3"}]
            self.asset_state = "uploaded"

        def request(self, method, path, data=None, **_kwargs):
            if method != "GET":
                raise AssertionError("Recovery must be read-only")
            if path == "git/ref/tags/v1.3":
                return {"object": {"type": "commit", "sha": MERGE}} if self.tagged else None
            if path == "git/ref/heads/main":
                return {"object": {"type": "commit", "sha": MERGE}}
            if path == "pulls/7":
                return self.pull
            if path == f"git/commits/{MERGE}":
                return {"parents": [{"sha": BASE}], "tree": {"sha": "tree"}}
            if path == f"git/commits/{HEAD}":
                return {"tree": {"sha": "tree"}}
            if path.startswith("actions/workflows/ci.yml/runs"):
                return {"workflow_runs": [{"id": 3, "status": "completed", "conclusion": "success",
                                            "event": "pull_request",
                                            "head_sha": HEAD, "head_branch": "content",
                                            "head_repository": {"full_name": "webmaxru/book"}}]}
            if path.startswith("actions/runs/3/jobs"):
                return {"total_count": 1, "jobs": [{"name": "Book release preflight", "head_sha": HEAD,
                                                   "status": "completed", "conclusion": "success"}]}
            if path == f"compare/{MERGE}...{MERGE}":
                return {"merge_base_commit": {"sha": MERGE}}
            if path in {f"contents/content/version.yml?ref={MERGE}",
                        f"contents/content/version.yml?ref={HEAD}"}:
                return {"encoding": "base64",
                        "content": base64.b64encode(b'version: "1.3"\n').decode()}
            raise AssertionError(path)

        def pages(self, path):
            if path == "releases":
                return self.releases
            if path == f"commits/{MERGE}/pulls":
                return ([{"number": 7, "merged_at": "2026-01-03T00:00:00Z",
                          "merge_commit_sha": MERGE}] if self.associated else [])
            if path == "pulls/7/files":
                return [{"filename": p} for p in
                        ["content/chapters/a.html", "content/version.yml", "content/CHANGELOG.md"]]
            if path in {"pulls/7/reviews", "issues/7/timeline"}:
                return []
            if path == "issues/7/comments":
                return [comment()]
            if path == "releases/42/assets":
                return ([{"name": "apm-book-v1.3.pdf", "size": 99, "state": self.asset_state}]
                        if self.assets else [])
            raise AssertionError(path)

    def test_unrelated_tag_and_missing_published_pdf_fail(self):
        with self.assertRaisesRegex(release.GateError, "approved, merged content PR"):
            release.release_plan(self.API(associated=False), tag="v1.3")
        with self.assertRaisesRegex(release.GateError, "incomplete"):
            release.release_plan(self.API(assets=False), tag="v1.3")

    def test_complete_recovery_requires_current_approval_and_bound_tag(self):
        api = self.API()
        with patch.object(release, "output") as output:
            release.release_plan(api, tag="v1.3")
            self.assertEqual(output.call_args.args[0]["recovery"], "true")
        api.pull["user"]["login"] = "someone-else"
        with self.assertRaisesRegex(release.GateError, "approval"):
            release.release_plan(api, tag="v1.3")

    def test_asset_must_be_uploaded_and_have_valid_integer_size(self):
        for asset in [
            {"name": "apm-book-v1.3.pdf", "size": 99, "state": "starter"},
            {"name": "apm-book-v1.3.pdf", "size": True, "state": "uploaded"},
            {"name": "apm-book-v1.3.pdf", "size": "99", "state": "uploaded"},
            {"name": "apm-book-v1.3.pdf", "size": 0, "state": "uploaded"},
        ]:
            with self.subTest(asset=asset):
                self.assertFalse(release.uploaded_pdf([asset], "v1.3"))
                api = self.API()
                pages = api.pages
                api.pages = lambda path: [asset] if path == "releases/42/assets" else pages(path)
                with self.assertRaisesRegex(release.GateError, "incomplete"):
                    release.release_plan(api, tag="v1.3")

    def test_manual_merger_and_multiple_parents_reject_provenance(self):
        for actor in (None, {"login": "webmaxru"}, {"login": "contributor"}):
            api = self.API()
            api.pull["merged_by"] = actor
            with self.assertRaisesRegex(release.GateError, "GitHub Actions controller"):
                release.release_plan(api, tag="v1.3")
        api = self.API()
        request = api.request

        def multi_parent(method, path, *args, **kwargs):
            data = request(method, path, *args, **kwargs)
            if path == f"git/commits/{MERGE}":
                data["parents"].append({"sha": HEAD})
            return data

        api.request = multi_parent
        with self.assertRaisesRegex(release.GateError, "exactly one parent"):
            release.release_plan(api, tag="v1.3")


class CheckIdentityTests(unittest.TestCase):
    class API:
        repo = "webmaxru/book"

        def __init__(self):
            self.runs = [{"id": 1, "status": "completed", "conclusion": "success",
                          "event": "pull_request", "head_sha": HEAD, "head_branch": "content",
                          "head_repository": {"full_name": self.repo}}]
            self.jobs = [{"name": "Book release preflight", "head_sha": HEAD,
                          "status": "completed", "conclusion": "success"}]
            self.total = 1

        def request(self, method, path):
            assert method == "GET"
            if path.startswith("actions/workflows/ci.yml/runs"):
                return {"workflow_runs": self.runs}
            assert path.startswith(f"actions/runs/{self.runs[-1]['id']}/jobs")
            return {"jobs": self.jobs, "total_count": self.total}

    def test_latest_run_must_match_workflow_head_branch_event_and_repository(self):
        release.checks_passed(self.API(), pr(), HEAD)
        for mutation in ({"head_sha": BASE}, {"head_branch": "main"}, {"event": "push"},
                         {"head_repository": {"full_name": "attacker/book"}},
                         {"head_repository": None}, {"status": "in_progress"}, {"conclusion": "skipped"}):
            api = self.API()
            api.runs[0].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(release.GateError):
                release.checks_passed(api, pr(), HEAD)
        api = self.API()
        api.runs.append(dict(api.runs[0], id=2, conclusion="failure"))
        with self.assertRaises(release.GateError):
            release.checks_passed(api, pr(), HEAD)

    def test_aggregate_must_be_unique_complete_and_on_exact_head(self):
        for mutation in ("absent", "duplicate", "truncated", "head", "pending"):
            api = self.API()
            if mutation == "absent":
                api.jobs, api.total = [], 0
            elif mutation == "duplicate":
                api.jobs *= 2
                api.total = 2
            elif mutation == "truncated":
                api.total = 101
            elif mutation == "head":
                api.jobs[0]["head_sha"] = BASE
            else:
                api.jobs[0]["status"] = "in_progress"
            with self.subTest(mutation=mutation), self.assertRaises(release.GateError):
                release.checks_passed(api, pr(), HEAD)


class TagValidationTests(unittest.TestCase):
    def test_annotated_tag_requires_bounded_commit_resolution(self):
        class API:
            calls = 0

            def request(self, method, path):
                self.calls += 1
                return {"object": {"type": "tag", "sha": ANNOTATION}}
        api = API()
        for obj in ({"type": "tree", "sha": MERGE}, {"type": "commit", "sha": "short"},
                    {"type": "tag", "sha": ANNOTATION}):
            with self.subTest(obj=obj), self.assertRaises(release.GateError):
                release.peel(api, {"object": obj})
        self.assertEqual(api.calls, 10)

    def test_edition_metadata_is_unambiguous_and_supports_crlf(self):
        class API:
            def request(self, _method, _path):
                return {"encoding": "base64", "content": base64.b64encode(self.text.encode()).decode()}
        api = API()
        for text in ('version: "1.3"\n', "version: '1.3'\r\n"):
            api.text = text
            self.assertEqual(release.edition_tag(api, MERGE), "v1.3")
        for text in ('version: "1.3\'\n', 'version: "1.3-rc.1"\n',
                     'version: "1.3"\nversion: "1.4"\n', 'version: "01.3"\n'):
            api.text = text
            with self.subTest(text=text), self.assertRaises(release.GateError):
                release.edition_tag(api, MERGE)


if __name__ == "__main__":
    unittest.main()
