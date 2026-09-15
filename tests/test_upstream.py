from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_upstream
from release_metadata import ReleaseError


def release(version, **overrides):
    return {
        "tag_name": f"v{version}", "draft": False, "prerelease": False,
        "published_at": "2026-09-15T17:48:53Z", "body": f"Notes for {version}.",
        **overrides,
    }


class UpstreamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "content").mkdir()
        (self.root / "content" / "version.yml").write_text(
            'version: "1.1"\ndate: "2026-07-08"\napm_version: "0.23.1"\n', encoding="utf-8"
        )

    def test_complete_gap_is_numeric_sorted_not_publication_order(self):
        versions = ["0.31.0", "0.23.1", "0.30.10", "0.24.0", "0.30.9", "0.22.0", "0.32.0"]
        batch = [release(version) for version in versions]
        batch += [release("0.32.0-rc.1", prerelease=True), release("0.33.0", draft=True)]
        with patch.object(check_upstream, "fetch_json", side_effect=[release("0.31.0"), batch]):
            result = check_upstream.discover(self.root)
        self.assertEqual(
            [item["version"] for item in result["releases"]],
            ["0.24.0", "0.30.9", "0.30.10", "0.31.0"],
        )
        self.assertTrue(result["update_available"])
        self.assertEqual(result["baseline_apm_version"], "0.23.1")
        self.assertTrue(result["changelog_url"].endswith("/v0.31.0/CHANGELOG.md"))
        self.assertTrue(result["compare_url"].endswith("/v0.23.1...v0.31.0"))
        self.assertEqual(result["releases"][-1]["notes"], "Notes for 0.31.0.")

    def test_explicit_target_uses_tag_not_latest(self):
        with patch.object(check_upstream, "fetch_json", side_effect=[
            release("0.30.0"), [release("0.31.0"), release("0.30.0"), release("0.23.1")],
        ]) as fetch:
            result = check_upstream.discover(self.root, "v0.30.0")
        self.assertEqual(fetch.call_args_list[0].args, ("releases/tags/v0.30.0",))
        self.assertEqual([item["version"] for item in result["releases"]], ["0.30.0"])

    def test_pagination_does_not_stop_at_baseline_or_first_page(self):
        first = [release("0.31.0"), release("0.32.0-rc.1", prerelease=True)]
        first += [release(f"0.30.{n}") for n in range(98)]
        with patch.object(check_upstream, "fetch_json", side_effect=[
            release("0.31.0"), first, [release("0.23.1"), release("0.29.0")],
        ]) as fetch:
            result = check_upstream.discover(self.root)
        self.assertEqual(fetch.call_args_list[-1].args, ("releases?per_page=100&page=2",))
        self.assertEqual(len(result["releases"]), 100)
        self.assertEqual(result["releases"][0]["version"], "0.29.0")

    def test_equal_target_is_a_read_only_no_op(self):
        with patch.object(check_upstream, "fetch_json", return_value=release("0.23.1")) as fetch:
            result = check_upstream.discover(self.root, "0.23.1")
        self.assertEqual(fetch.call_count, 1)
        self.assertFalse(result["update_available"])
        self.assertEqual(result["releases"], [])
        self.assertEqual(len(list(self.root.rglob("*"))), 2)

    def test_older_or_prerelease_target_is_rejected(self):
        for selected in [release("0.22.0"), release("0.31.0", prerelease=True)]:
            with self.subTest(selected=selected):
                with patch.object(check_upstream, "fetch_json", return_value=selected):
                    with self.assertRaises(ReleaseError):
                        check_upstream.discover(self.root)
        with patch.object(check_upstream, "fetch_json") as fetch:
            with self.assertRaises(ReleaseError):
                check_upstream.discover(self.root, "0.31.0-rc.1")
            fetch.assert_not_called()

    def test_incomplete_and_duplicate_ranges_are_errors(self):
        for batch in [
            [release("0.31.0")], [release("0.23.1")],
            [release("0.31.0"), release("0.23.1"), release("0.31.0")],
            {"message": "Not a list"},
        ]:
            with self.subTest(batch=batch):
                with patch.object(check_upstream, "fetch_json", side_effect=[release("0.31.0"), batch]):
                    with self.assertRaises(ReleaseError):
                        check_upstream.discover(self.root)

    def test_mismatched_exact_target_is_an_error(self):
        with patch.object(check_upstream, "fetch_json", return_value=release("0.30.0")):
            with self.assertRaisesRegex(ReleaseError, "does not match"):
                check_upstream.discover(self.root, "0.31.0")

    def test_malformed_release_is_not_silently_treated_as_stable(self):
        for data in [[], {}, release("0.31.0", draft=None), release("0.31.0", body=[]),
                     release("0.31.0", published_at="2026-09-15"), release("latest")]:
            with self.subTest(data=data):
                with self.assertRaises(ReleaseError):
                    check_upstream.release_info(data)

    def test_public_lookup_does_not_forward_tokens(self):
        data = io.BytesIO(json.dumps(release("0.31.0")).encode())
        with patch.object(check_upstream.urllib.request, "urlopen", return_value=data) as open_url:
            check_upstream.fetch_json("releases/latest")
        request = open_url.call_args.args[0]
        self.assertFalse(request.has_header("Authorization"))
        self.assertEqual(request.full_url, check_upstream.API + "/releases/latest")
        self.assertEqual(open_url.call_args.kwargs["timeout"], 30)

    def test_http_error_is_a_blocker_not_no_update(self):
        error = urllib.error.HTTPError(check_upstream.API, 403, "Rate limited", {}, None)
        with patch.object(check_upstream.urllib.request, "urlopen", side_effect=error):
            with self.assertRaisesRegex(ReleaseError, "HTTP 403"):
                check_upstream.fetch_json("releases/latest")

    def test_cli_discovery_failure_writes_only_stderr(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(check_upstream, "fetch_json", side_effect=ReleaseError("Network unavailable")):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                status = check_upstream.main(["--root", str(self.root)])
        self.assertEqual(status, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("Network unavailable", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
