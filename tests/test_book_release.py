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


def pr(author="webmaxru"):
    return {
        "state": "open", "draft": False, "merged": False, "changed_files": 3,
        "user": {"login": author}, "head": {"sha": HEAD, "ref": "content",
                                             "repo": {"full_name": "webmaxru/book"}},
        "base": {"sha": BASE, "ref": "main", "repo": {"full_name": "webmaxru/book"}},
    }


def review(state="APPROVED", sha=HEAD):
    return {"id": 1, "user": {"login": "webmaxru"}, "state": state,
            "commit_id": sha, "submitted_at": "2026-01-02T00:00:00Z"}


def comment(sha=HEAD, author="webmaxru", date="2026-01-03T00:00:00Z"):
    return {"user": {"login": author}, "body": f"/release-book {sha}", "created_at": date}


class ApprovalTests(unittest.TestCase):
    def test_self_author_requires_exact_owner_command(self):
        self.assertTrue(release.approval(pr(), [], [comment()]))
        for item in [comment("d" * 40), comment(author="attacker"),
                     dict(comment(), body=f"/release-book {HEAD}\nextra")]:
            self.assertFalse(release.approval(pr(), [], [item]))
        self.assertFalse(release.approval(pr(), [review()], []))

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
        if path in {"pulls/7/reviews", "issues/7/timeline"}:
            return []
        if path == "issues/7/comments":
            return self.comments
        if path == "actions/workflows/check-book.yml/runs":
            return {"workflow_runs": [{"id": 3, "status": "completed", "conclusion": self.check_result,
                                        "head_sha": HEAD, "head_branch": "content",
                                        "head_repository": {"full_name": "webmaxru/book"},
                                        "pull_requests": []}]}
        if path == "git/ref/heads/main":
            return {"object": {"sha": BASE}}
        if path == "pulls/7/merge" and method == "PUT":
            if body != {"sha": HEAD, "merge_method": "squash"}:
                raise AssertionError(body)
            return {"merged": True, "sha": MERGE}
        if path == "actions/workflows/release-content.yml/dispatches" and method == "POST":
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

        def respond(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length)) if length else None
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
                       GITHUB_API_URL=api)
            return subprocess.run([sys.executable, str(ROOT / "scripts" / "book_release.py"), *args],
                                  env=env, text=True, capture_output=True, timeout=30)

    def test_approved_pr_merges_head_and_explicitly_dispatches_release(self):
        fixture = FixtureServer()
        result = self.run_controller(fixture, "merge", "--pr", "7", "--head", HEAD, "--base", BASE)
        self.assertEqual(result.returncode, 0, result.stderr)
        writes = [a for a in fixture.actions if a[0] != "GET"]
        self.assertEqual([a[0] for a in writes], ["PUT", "POST"])
        self.assertEqual(writes[-1][2]["inputs"]["merge_sha"], MERGE)
        self.assertEqual(writes[-1][2]["inputs"]["head_sha"], HEAD)

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
        with tempfile.TemporaryDirectory() as directory:
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


class PublishTests(unittest.TestCase):
    def test_conflicting_tag_or_invalid_pdf_never_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf, notes = Path(directory) / "book.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            class API:
                writes = []
                def request(self, method, path, data=None, **_kwargs):
                    if method != "GET":
                        self.writes.append((method, path))
                    return {"object": {"type": "commit", "sha": "d" * 40}}
            api = API()
            with self.assertRaisesRegex(release.GateError, "another commit"):
                release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
            self.assertEqual(api.writes, [])
            pdf.write_bytes(b"not a pdf")
            with self.assertRaisesRegex(release.GateError, "not a PDF"):
                release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
            self.assertEqual(api.writes, [])

    def test_draft_upload_failure_never_publishes(self):
        class API:
            def request(self, method, path, data=None, **_kwargs):
                if path.startswith("git/ref/"):
                    return {"object": {"type": "commit", "sha": MERGE}}
                if path.startswith("releases/tags/"):
                    return {"draft": True}
                raise AssertionError(path)
            def pages(self, _path):
                return []
        with tempfile.TemporaryDirectory() as directory:
            pdf, notes = Path(directory) / "book.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            with patch.object(release.subprocess, "run",
                              side_effect=subprocess.CalledProcessError(1, "gh")) as run:
                with self.assertRaises(subprocess.CalledProcessError):
                    release.publish(API(), "v1.3", MERGE, str(pdf), str(notes))
                self.assertEqual(run.call_count, 1)
                self.assertIn("upload", run.call_args.args[0])

    def test_duplicate_published_release_never_replaces_assets(self):
        class API:
            def request(self, method, path, data=None, **_kwargs):
                if path.startswith("git/ref/"):
                    return {"object": {"type": "commit", "sha": MERGE}}
                if path.startswith("releases/tags/"):
                    return {"draft": False, "id": 4}
                raise AssertionError(path)
            def pages(self, _path):
                return [{"name": "apm-book-v1.3.pdf", "size": 99, "state": self.state}]
        with tempfile.TemporaryDirectory() as directory:
            pdf, notes = Path(directory) / "book.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            api = API()
            api.state = "uploaded"
            with patch.object(release.subprocess, "run") as run:
                release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
                run.assert_not_called()
                api.state = "starter"
                with self.assertRaisesRegex(release.GateError, "incomplete"):
                    release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
                run.assert_not_called()

    def test_build_first_then_draft_upload_and_publish_without_promoting_old_edition(self):
        class API:
            def __init__(self):
                self.writes = []
            def request(self, method, path, data=None, **_kwargs):
                if method == "POST":
                    self.writes.append((path, data))
                    return {}
                return None
            def pages(self, _path):
                return [{"tag_name": "v1.4", "draft": False, "prerelease": False}]
        with tempfile.TemporaryDirectory() as directory:
            pdf, notes = Path(directory) / "apm-book-v1.3.pdf", Path(directory) / "notes.md"
            pdf.write_bytes(b"%PDF-1.7 fixture")
            notes.write_text("notes", encoding="utf-8")
            api = API()
            with patch.object(release.subprocess, "run") as run:
                release.publish(api, "v1.3", MERGE, str(pdf), str(notes))
            self.assertEqual(api.writes, [("git/refs", {"ref": "refs/tags/v1.3", "sha": MERGE})])
            calls = [call.args[0] for call in run.call_args_list]
            self.assertEqual([call[2] for call in calls], ["create", "upload", "edit"])
            self.assertIn("--draft", calls[0])
            self.assertIn("--draft=false", calls[2])
            self.assertIn("--latest=false", calls[2])


class RecoveryTests(unittest.TestCase):
    class API:
        repo = "webmaxru/book"
        def __init__(self, *, associated=True, assets=True):
            self.associated = associated
            self.assets = assets
            self.pull = pr()
            self.pull.update({"state": "closed", "merged": True, "merge_commit_sha": MERGE})

        def request(self, method, path, data=None, **_kwargs):
            if method != "GET":
                raise AssertionError("Recovery must be read-only")
            if path == "git/ref/tags/v1.3":
                return {"object": {"type": "commit", "sha": MERGE}}
            if path == "releases/tags/v1.3":
                return {"draft": False, "id": 42}
            if path == "pulls/7":
                return self.pull
            if path == f"git/commits/{MERGE}":
                return {"parents": [{"sha": BASE}], "tree": {"sha": "tree"}}
            if path == f"git/commits/{HEAD}":
                return {"tree": {"sha": "tree"}}
            if path.startswith("actions/workflows/check-book.yml/runs"):
                return {"workflow_runs": [{"id": 3, "status": "completed", "conclusion": "success",
                                            "head_sha": HEAD, "head_branch": "content",
                                            "head_repository": {"full_name": "webmaxru/book"}}]}
            if path == f"compare/{MERGE}...main":
                return {"merge_base_commit": {"sha": MERGE}}
            if path == f"contents/content/version.yml?ref={MERGE}":
                return {"encoding": "base64",
                        "content": base64.b64encode(b'version: "1.3"\n').decode()}
            raise AssertionError(path)

        def pages(self, path):
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
                return ([{"name": "apm-book-v1.3.pdf", "size": 99, "state": "uploaded"}]
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


if __name__ == "__main__":
    unittest.main()
