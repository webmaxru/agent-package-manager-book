"""Artifact lifecycle regressions; no live API, uploads, releases or deletions."""
from __future__ import annotations

import contextlib
import copy
import io
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import yaml

import test_book_release as release_tests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import artifact_storage as storage

REF = "refs/heads/topic/preview"
DIGEST = "f" * 64
MERGE = release_tests.MERGE


class API(release_tests.RecoveryTests.API):
    repo = "webmaxru/book"

    def __init__(self):
        super().__init__()
        self.runs = {}
        self.attempts = {}
        self.preview_jobs = {}
        self.artifacts = {}
        self.calls = []
        self.reads = {}
        self.mutate = None
        self.fail_delete = False
        self.incomplete = False
        self.jobs = []
        self.asset_digest = f"sha256:{DIGEST}"

    def producer(self, number, *, branch="topic/preview", workflow="ci.yml", attempt=1,
                 status="completed", conclusion="success"):
        value = {"id": number, "head_branch": branch, "head_sha": "a" * 40,
                 "repository": {"id": 42, "full_name": self.repo},
                 "head_repository": {"id": 42, "full_name": self.repo},
                 "workflow_id": 7 if workflow == "ci.yml" else 8,
                 "path": f".github/workflows/{workflow}", "event": "workflow_dispatch",
                 "run_attempt": attempt, "status": status, "conclusion": conclusion}
        self.runs[number] = value
        self.attempts[number, attempt] = copy.deepcopy(value)
        if workflow == "ci.yml":
            self.preview_job(value)
        return value

    def preview_job(self, producer, *, upload="success"):
        self.preview_jobs[producer["id"], producer["run_attempt"]] = [{
            "name": "preflight (ubuntu-24.04)", "run_id": producer["id"],
            "run_attempt": producer["run_attempt"], "status": "completed", "conclusion": "success",
            "steps": [{"name": "Upload PDF preview", "status": "completed", "conclusion": upload}],
        }]

    def artifact(self, number, producer, *, ref=REF, name=None, created=None):
        key = producer["id"], producer["run_attempt"]
        if key not in self.attempts:
            self.attempts[key] = copy.deepcopy(producer)
            self.preview_job(producer)
        value = {"id": number, "expired": False, "name": name or storage.preview_name(
                     42, ref, producer["id"], producer["run_attempt"]),
                 "created_at": created or f"2026-11-27T12:{number % 60:02d}:00Z",
                 "workflow_run": {"id": producer["id"], "repository_id": 42,
                                  "head_repository_id": 42, "head_sha": producer["head_sha"],
                                  "head_branch": producer["head_branch"]}}
        self.artifacts[number] = value
        return value

    def request(self, method, path, *args, **kwargs):
        self.calls.append((method, path))
        self.reads[path] = self.reads.get(path, 0) + 1
        if self.mutate:
            self.mutate(method, path, self.reads[path])
        parsed = urlsplit(path)
        parts = parsed.path.split("/")
        if parts[:2] == ["actions", "artifacts"] and len(parts) == 3:
            if method == "DELETE":
                if self.fail_delete:
                    raise storage.APIError("GitHub DELETE: HTTP 403")
                del self.artifacts[int(parts[2])]
                return None
            return copy.deepcopy(self.artifacts[int(parts[2])])
        if parts[:2] == ["actions", "runs"]:
            number = int(parts[2])
            if number not in self.runs:
                return super().request(method, path, *args, **kwargs)
            if len(parts) == 3:
                return copy.deepcopy(self.runs[number])
            if parts[3] == "attempts":
                attempt = int(parts[4])
                if len(parts) == 5:
                    return copy.deepcopy(self.attempts[number, attempt])
                values, key = self.preview_jobs[number, attempt], "jobs"
            elif parts[-1] == "jobs":
                values, key = self.jobs, "jobs"
            else:
                values = [a for a in self.artifacts.values() if a["workflow_run"]["id"] == number]
                key = "artifacts"
        elif parsed.path == "actions/artifacts":
            values, key = list(self.artifacts.values()), "artifacts"
        else:
            return super().request(method, path, *args, **kwargs)
        page = int(parse_qs(parsed.query)["page"][0])
        return {key: copy.deepcopy(values[(page - 1) * 100:page * 100]),
                "total_count": len(values) + int(self.incomplete)}

    def pages(self, path):
        values = copy.deepcopy(super().pages(path))
        if path == "releases/42/assets":
            for value in values:
                value["digest"] = self.asset_digest
        return values

    def deleted(self):
        return [int(path.rsplit("/", 1)[-1]) for method, path in self.calls if method == "DELETE"]

    def route(self, method, path, body):
        return self.request(method, path.removeprefix(f"/repos/{self.repo}/"), body)


class PreviewTests(unittest.TestCase):
    def fixture(self):
        api = API()
        api.artifact(10, api.producer(100))
        api.artifact(20, api.producer(200))
        return api

    def test_preview_name_binds_repo_full_ref_run_and_attempt(self):
        name = storage.preview_name(42, REF, 200, 1)
        for args in [(43, REF, 200, 1), (42, "refs/tags/topic/preview", 200, 1),
                     (42, "refs/heads/topic-preview", 200, 1), (42, REF, 201, 1),
                     (42, REF, 200, 2)]:
            self.assertNotEqual(name, storage.preview_name(*args))
        with self.assertRaises(storage.GateError):
            storage.preview_name(42, "topic/preview", 200, 1)

    def test_only_exact_older_preview_is_deleted_after_success(self):
        api = self.fixture()
        api.artifact(9, api.producer(90), name="diagnostics")
        api.artifact(8, api.producer(80), name=f"release-book-{MERGE}")
        api.artifact(7, api.producer(70), name="book-preview-legacy")
        api.artifact(6, api.producer(60, branch="other"), ref="refs/heads/other")
        api.artifact(5, api.producer(50), ref="refs/tags/topic/preview")
        api.artifact(4, api.producer(40, status="in_progress"))
        api.artifact(30, api.producer(300))
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10])
        self.assertIn(20, api.artifacts)

    def test_newer_artifact_on_older_rerun_is_preserved(self):
        api = self.fixture()
        api.artifacts[10]["created_at"] = "2026-11-27T12:30:00Z"
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])

    def test_older_preview_with_higher_artifact_id_is_pruned(self):
        api = self.fixture()
        older = api.artifacts.pop(10)
        older["id"] = 30
        api.artifacts[30] = older
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [30])
        self.assertIn(20, api.artifacts)

    def test_older_same_run_attempt_with_higher_artifact_id_is_pruned(self):
        api = self.fixture()
        older = api.artifacts.pop(20)
        older["id"] = 30
        api.artifacts[30] = older
        api.runs[200]["run_attempt"] = 2
        api.artifact(21, api.runs[200])
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10, 30])
        self.assertIn(21, api.artifacts)

    def test_newer_producer_with_earlier_upload_id_and_time_is_preserved(self):
        api = self.fixture()
        api.artifact(15, api.producer(300))
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10])
        self.assertIn(15, api.artifacts)

    def test_reversed_cleanup_completion_cannot_delete_newer_replacement(self):
        api = self.fixture()
        api.artifact(30, api.producer(300))
        storage.cleanup_preview(api, 200)
        storage.cleanup_preview(api, 300)
        self.assertEqual(api.deleted(), [10, 20])
        self.assertIn(30, api.artifacts)
        # A successful upload whose replacement has since disappeared fails closed.
        with self.assertRaisesRegex(storage.GateError, "Missing replacement"):
            storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10, 20])

    def test_failed_or_active_replacement_never_deletes_previous_preview(self):
        for change in ({"conclusion": "failure"}, {"status": "in_progress"},
                       {"conclusion": "cancelled"}, {"conclusion": None}):
            with self.subTest(change=change):
                api = self.fixture()
                api.runs[200].update(change)
                with self.assertRaises(storage.GateError):
                    storage.cleanup_preview(api, 200)
                self.assertEqual(api.deleted(), [])

    def test_missing_replacement_identity_or_ambiguous_upload_never_cleans(self):
        api = self.fixture()
        del api.artifacts[20]
        with self.assertRaisesRegex(storage.GateError, "Missing replacement"):
            storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])
        api = self.fixture()
        api.artifact(21, api.runs[200])
        with self.assertRaisesRegex(storage.GateError, "Ambiguous"):
            storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])

    def test_active_rerun_or_changed_artifact_immediately_before_delete_is_retained(self):
        for target in ("producer", "artifact"):
            with self.subTest(target=target):
                api = self.fixture()

                def mutate(method, path, count):
                    if path == "actions/runs/100" and count == 2:
                        if target == "producer":
                            api.runs[100].update(status="queued", run_attempt=2)
                        else:
                            api.artifacts[10]["expired"] = True
                    if path == "actions/artifacts/10" and target == "artifact":
                        api.artifacts[10]["expired"] = True

                api.mutate = mutate
                storage.cleanup_preview(api, 200)
                self.assertEqual(api.deleted(), [])

    def test_replacement_rerun_during_cleanup_fails_closed(self):
        api = self.fixture()

        def mutate(method, path, count):
            if path == "actions/runs/200" and count == 2:
                api.runs[200].update(status="queued", run_attempt=2)

        api.mutate = mutate
        with self.assertRaisesRegex(storage.GateError, "Replacement changed"):
            storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])

    def test_expired_previous_preview_is_retained(self):
        api = self.fixture()
        api.artifacts[10]["expired"] = True
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])

    def test_rerun_selects_current_upload_and_prunes_completed_older_attempts(self):
        api = self.fixture()
        api.runs[200]["run_attempt"] = 2
        api.artifact(21, api.runs[200])
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10, 20])
        self.assertIn(21, api.artifacts)

    def test_completed_previous_attempt_of_another_run_is_pruned(self):
        api = self.fixture()
        api.runs[100]["run_attempt"] = 2
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10])
        self.assertIn(("GET", "actions/runs/100/attempts/1"), api.calls)

    def test_skipped_current_upload_is_noop_even_with_previous_attempt_artifacts(self):
        api = self.fixture()
        api.runs[200]["run_attempt"] = 2
        api.preview_job(api.runs[200], upload="skipped")
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])
        self.assertIn(20, api.artifacts)

    def test_successful_upload_with_expired_replacement_fails_clearly(self):
        api = self.fixture()
        api.artifacts[20]["expired"] = True
        with self.assertRaisesRegex(storage.GateError, "expired|identity"):
            storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])

    def test_missing_failed_or_wrong_attempt_upload_evidence_never_cleans(self):
        for change in ("missing-job", "missing-step", "failed", "wrong-attempt"):
            with self.subTest(change=change):
                api = self.fixture()
                job = api.preview_jobs[200, 1][0]
                if change == "missing-job":
                    api.preview_jobs[200, 1] = []
                elif change == "missing-step":
                    job["steps"] = []
                elif change == "failed":
                    job["steps"][0]["conclusion"] = "failure"
                else:
                    job["run_attempt"] = 2
                with self.assertRaises(storage.GateError):
                    storage.cleanup_preview(api, 200)
                self.assertEqual(api.deleted(), [])

    def test_active_rerun_preserves_all_its_previous_attempts(self):
        for number in (100, 200):
            with self.subTest(number=number):
                api = self.fixture()
                api.runs[number].update(run_attempt=2, status="in_progress")
                if number == 200:
                    api.artifact(21, api.runs[number])
                    with self.assertRaisesRegex(storage.GateError, "not completed successfully"):
                        storage.cleanup_preview(api, 200)
                else:
                    storage.cleanup_preview(api, 200)
                self.assertEqual(api.deleted(), [])

    def test_repository_workflow_or_producer_mismatch_never_deletes(self):
        for change in ("repository", "workflow", "head", "event", "metadata", "namespace"):
            with self.subTest(change=change):
                api = self.fixture()
                if change == "repository":
                    api.runs[100]["repository"]["full_name"] = "other/book"
                elif change == "workflow":
                    api.runs[100]["path"] = ".github/workflows/other.yml"
                elif change == "head":
                    api.runs[100]["head_repository"]["full_name"] = "fork/book"
                elif change == "event":
                    api.runs[100]["event"] = "pull_request"
                elif change == "metadata":
                    api.artifacts[10]["workflow_run"]["id"] = 99
                else:
                    api.artifacts[20]["name"] = storage.preview_name(43, REF, 200, 1)
                with self.assertRaises(storage.GateError):
                    storage.cleanup_preview(api, 200)
                self.assertEqual(api.deleted(), [])

    def test_artifact_pagination_and_incomplete_lists_fail_closed(self):
        api = self.fixture()
        for index in range(1000, 1105):
            api.artifact(index, api.runs[200], name=f"diagnostic-{index}")
        storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [10])
        self.assertTrue(any("page=2" in path for _, path in api.calls))
        api = self.fixture()
        api.incomplete = True
        with self.assertRaisesRegex(storage.GateError, "Incomplete"):
            storage.cleanup_preview(api, 200)
        self.assertEqual(api.deleted(), [])

    def test_delete_api_failure_is_visible_nonzero_and_preserves_replacement(self):
        api = self.fixture()
        api.fail_delete = True
        with patch.object(storage, "GitHub", return_value=api), contextlib.redirect_stderr(io.StringIO()) as err:
            result = storage.main(["preview", "--run-id", "200"])
        self.assertEqual(result, 1)
        self.assertIn("::error::", err.getvalue())
        self.assertIn("403", err.getvalue())
        self.assertIn(20, api.artifacts)

    def test_real_api_client_against_loopback_deletes_exact_id_only(self):
        api = self.fixture()
        with release_tests.github_fixture(api) as url, patch.dict(
            os.environ, GITHUB_API_URL=url, GITHUB_REPOSITORY=api.repo, GH_TOKEN="fixture",
            NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost",
        ):
            self.assertEqual(storage.main(["preview", "--run-id", "200"]), 0)
        self.assertEqual(api.deleted(), [10])
        self.assertIn(20, api.artifacts)

    def test_loopback_api_error_is_a_visible_failed_cleanup(self):
        api = self.fixture()

        def missing(method, path, count):
            if method == "DELETE":
                raise AssertionError("simulate a missing artifact")

        api.mutate = missing
        with release_tests.github_fixture(api) as url, patch.dict(
            os.environ, GITHUB_API_URL=url, GITHUB_REPOSITORY=api.repo, GH_TOKEN="fixture",
            NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost",
        ), contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(storage.main(["preview", "--run-id", "200"]), 1)
        self.assertIn("HTTP 404", err.getvalue())
        self.assertIn("::error::", err.getvalue())
        self.assertIn(10, api.artifacts)
        self.assertIn(20, api.artifacts)


class ReleaseStagingTests(unittest.TestCase):
    def fixture(self):
        api = API()
        producer = api.producer(200, workflow="release.yml", branch="main")
        producer["status"] = "in_progress"
        api.artifact(20, producer, name=f"release-book-{MERGE}")
        api.jobs = [{"name": name, "run_id": 200, "run_attempt": 1,
                     "status": "completed", "conclusion": "success"}
                    for name in ("build", "publish", "deploy")]
        return api

    def cleanup(self, api):
        with patch.dict(os.environ, GITHUB_RUN_ATTEMPT="1"):
            storage.cleanup_release(api, 200, 20, "v1.3", MERGE, DIGEST)

    def test_verified_publication_and_finished_consumers_delete_only_staging_id(self):
        api = self.fixture()
        api.artifact(21, api.runs[200], name="diagnostics")
        self.cleanup(api)
        self.assertEqual(api.deleted(), [20])
        self.assertIn(21, api.artifacts)
        self.assertFalse(any(path.startswith("releases/") for method, path in api.calls if method == "DELETE"))

    def test_failed_or_incomplete_publication_retains_recovery_artifact(self):
        for change in ("draft", "assets", "tag", "approval", "digest", "digest-missing"):
            with self.subTest(change=change):
                api = self.fixture()
                if change == "draft":
                    api.releases[0]["draft"] = True
                elif change == "assets":
                    api.assets = False
                elif change == "tag":
                    api.tagged = False
                elif change == "approval":
                    api.pull["user"]["login"] = "someone-else"
                elif change == "digest":
                    api.asset_digest = "sha256:" + "0" * 64
                else:
                    api.asset_digest = None
                with self.assertRaises(storage.GateError):
                    self.cleanup(api)
                self.assertEqual(api.deleted(), [])
                self.assertIn(20, api.artifacts)

    def test_each_consumer_must_have_finished_this_attempt_successfully(self):
        for job in ("build", "publish", "deploy"):
            for change in ({"conclusion": "failure"}, {"status": "in_progress"},
                           {"conclusion": "skipped"}, {"run_attempt": 2}):
                with self.subTest(job=job, change=change):
                    api = self.fixture()
                    next(j for j in api.jobs if j["name"] == job).update(change)
                    with self.assertRaisesRegex(storage.GateError, "consumer"):
                        self.cleanup(api)
                    self.assertEqual(api.deleted(), [])

    def test_staging_identity_missing_or_changed_is_not_deleted(self):
        for change in ("name", "run", "attempt", "missing-digest"):
            api = self.fixture()
            if change == "name":
                api.artifacts[20]["name"] = "unrelated"
            elif change == "run":
                api.artifacts[20]["workflow_run"]["id"] = 100
            elif change == "attempt":
                api.runs[200]["run_attempt"] = 2
            else:
                with self.assertRaises(storage.GateError):
                    storage.cleanup_release(api, 200, 20, "v1.3", MERGE, None)
                continue
            with self.assertRaises(storage.GateError):
                self.cleanup(api)
            self.assertEqual(api.deleted(), [])


class ArtifactWorkflowTests(unittest.TestCase):
    def workflow(self, name):
        return yaml.load((ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8"),
                         Loader=yaml.BaseLoader)

    def test_default_ci_builds_without_uploads_and_manual_preview_expires_in_one_day(self):
        ci = self.workflow("ci.yml")
        self.assertEqual(ci["on"]["workflow_dispatch"]["inputs"]["upload_preview"],
                         {"description": "Upload a PDF preview (expires after one day)",
                          "type": "boolean", "default": "false"})
        steps = ci["jobs"]["preflight"]["steps"]
        upload = [s for s in steps if s.get("uses", "").startswith("actions/upload-artifact@")]
        self.assertEqual(len(upload), 1)
        self.assertEqual(upload[0]["if"],
                         "runner.os == 'Linux' && github.event_name == 'workflow_dispatch' && inputs.upload_preview")
        self.assertEqual(upload[0]["with"]["retention-days"], "1")
        self.assertNotIn("continue-on-error", upload[0])
        pdf = next(s for s in steps if s.get("name") == "Build and verify PDF")
        self.assertEqual(pdf["if"], "runner.os == 'Linux'")
        approval = self.workflow("approved-book.yml")
        self.assertNotIn("upload-artifact@", str(approval))
        self.assertIn("generate_pdf.py", str(approval))

    def test_preview_cleanup_is_serial_trusted_main_and_never_checks_out_producer(self):
        workflow = self.workflow("cleanup-preview.yml")
        self.assertEqual(workflow["permissions"], {})
        self.assertEqual(workflow["on"], {"workflow_run": {"workflows": ["Book CI"], "types": ["completed"]}})
        job = workflow["jobs"]["cleanup"]
        self.assertIn("workflow_dispatch", job["if"])
        self.assertIn("conclusion == 'success'", job["if"])
        self.assertIn("github.ref == 'refs/heads/main'", job["if"])
        self.assertEqual(job["concurrency"]["cancel-in-progress"], "false")
        self.assertIn("head_branch", job["concurrency"]["group"])
        self.assertEqual(job["permissions"], {"contents": "read", "actions": "write"})
        checkout = job["steps"][0]
        self.assertEqual(checkout["with"], {"ref": "main", "persist-credentials": "false"})
        self.assertNotIn("download-artifact", str(job))
        self.assertEqual(self.workflow("ci.yml")["permissions"], {"contents": "read"})

    def test_staging_cleanup_waits_for_publication_and_delivery_and_keeps_recovery_window(self):
        workflow = self.workflow("release.yml")
        jobs = workflow["jobs"]
        upload = next(s for s in jobs["build"]["steps"] if s.get("id") == "staging")
        self.assertEqual(upload["with"]["retention-days"], "7")
        self.assertEqual(jobs["build"]["outputs"]["staging_id"], "${{ steps.staging.outputs.artifact-id }}")
        self.assertIn("sha256sum", str(jobs["build"]["steps"]))
        cleanup = jobs["cleanup-staging"]
        self.assertEqual(cleanup["needs"], ["authorize", "build", "publish", "deploy"])
        self.assertIn("needs.publish.outputs.published == 'true'", cleanup["if"])
        self.assertIn("needs.deploy.result == 'success'", cleanup["if"])
        self.assertNotIn("always()", cleanup["if"])
        self.assertIn("actions/download-artifact@v8", str(jobs["publish"]["steps"]))
        self.assertIn("release-plan", str(jobs["publish"]["steps"]))
        self.assertIn("book_release.py deliver", str(jobs["deploy"]["steps"]))
        pages = self.workflow("deploy-pages.yml")
        self.assertIn("python site/generate.py", str(pages))
        upload_pages = next(s for s in pages["jobs"]["build"]["steps"]
                            if s.get("uses", "").startswith("actions/upload-pages-artifact@"))
        self.assertEqual(upload_pages["with"]["retention-days"], "1")


if __name__ == "__main__":
    unittest.main()
