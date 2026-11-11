from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))
from release_metadata import ReleaseError
from validate_evidence import validate_evidence
from validate_release import validate_change


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "--quiet", "--initial-branch=main")
        for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid"),
                           ("core.autocrlf", "false"), ("commit.gpgsign", "false"),
                           ("core.hooksPath", str(self.root / "no-hooks"))):
            self.git("config", "--local", key, value)
        self.write("content/toc.yml", "chapters:\n- number: 1\n  slug: sample\n")
        self.write("content/chapters/sample.html", "<p>before</p>\n")
        self.write("content/version.yml", 'version: "1.2"\ndate: "2026-01-01"\napm_version: "0.31.0"\n')
        self.write("content/CHANGELOG.md", "## [1.2] - 2026-01-01\n- Before.\n")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Base")
        self.base = self.git("rev-parse", "HEAD")
        self.write("content/chapters/sample.html", "<p>after</p>\n")
        self.write("content/version.yml", 'version: "1.3"\ndate: "2026-01-02"\napm_version: "0.32.0"\n')
        self.write("content/CHANGELOG.md",
                   "## [1.3] - 2026-01-02\n- Updated.\n\n## [1.2] - 2026-01-01\n- Before.\n")
        self.folder = "content/research/updates/1.3"
        self.report_paths = [
            f"{self.folder}/integration-review.md", f"{self.folder}/ch01-review.md",
            f"{self.folder}/ch01-verification.md",
        ]
        for path in self.report_paths:
            verdict = "PASS" if "verification" in path else "ACCEPT"
            self.write(path, f"**Verdict: {verdict}**\nAPM 0.32.0\n")
        self.manifest = {
            "book_edition": "1.3", "reviewed_apm_version": "0.32.0", "result": "PASS",
            "affected_chapters": [1], "example_results": [{"chapter": 1, "id": "ex1", "status": "PASS"}],
            "bound_paths": [],
        }
        for path in ["content/chapters/sample.html", *self.report_paths]:
            self.manifest["bound_paths"].append({"path": path, "git_blob_oid": self.git("hash-object", "--", path)})
        self.save()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True,
                              text=True, encoding="utf-8").stdout.strip()

    def write(self, name, text):
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def save(self):
        self.write(f"{self.folder}/commit-binding.json", json.dumps(self.manifest))

    def test_valid_bound_evidence_passes(self):
        validate_change(self.root, self.base)
        validate_evidence(self.root, self.base)

    def test_changed_source_or_report_invalidates_binding(self):
        for path in ["content/chapters/sample.html", self.report_paths[0]]:
            with self.subTest(path=path):
                original = (self.root / path).read_text(encoding="utf-8")
                self.write(path, original + "late change\n")
                with self.assertRaisesRegex(ReleaseError, "does not match"):
                    validate_evidence(self.root, self.base)
                self.write(path, original)

    def test_bad_verdict_and_unjustified_skip_fail(self):
        self.manifest["example_results"][0]["status"] = "SKIPPED-needs-network"
        self.save()
        with self.assertRaisesRegex(ReleaseError, "undocumented skip"):
            validate_evidence(self.root, self.base)
        self.manifest["example_results"][0]["reason"] = "Private server unavailable."
        self.save()
        validate_evidence(self.root, self.base)
        path = self.report_paths[1]
        self.write(path, "Verdict: REVISE\nAPM 0.32.0\n")
        for entry in self.manifest["bound_paths"]:
            if entry["path"] == path:
                entry["git_blob_oid"] = self.git("hash-object", "--", path)
        self.save()
        with self.assertRaisesRegex(ReleaseError, "Missing explicit ACCEPT"):
            validate_evidence(self.root, self.base)

    def test_toc_comment_only_is_not_content_change(self):
        self.write("content/chapters/sample.html", "<p>before</p>\n")
        self.write("content/version.yml", 'version: "1.2"\ndate: "2026-01-01"\napm_version: "0.31.0"\n')
        self.write("content/CHANGELOG.md", "## [1.2] - 2026-01-01\n- Before.\n")
        self.write("content/toc.yml", "# Comment only\nchapters:\n- number: 1\n  slug: sample\n")
        validate_change(self.root, self.base)

    def test_no_examples_needs_explicit_reason(self):
        self.manifest["example_results"] = []
        self.manifest["no_examples"] = [{"chapter": 1, "reason": "No executable examples changed."}]
        self.save()
        validate_evidence(self.root, self.base)
        self.manifest["no_examples"][0]["reason"] = ""
        self.save()
        with self.assertRaisesRegex(ReleaseError, "no-examples"):
            validate_evidence(self.root, self.base)


if __name__ == "__main__":
    unittest.main()
