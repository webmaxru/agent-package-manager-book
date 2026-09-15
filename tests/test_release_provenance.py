from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

from release_metadata import ReleaseError
from validate_release import validate_change, validate_tag


class ReleaseProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "--quiet", "--initial-branch=main")
        for key, value in {
            "user.name": "Book tooling tests",
            "user.email": "book-tests@example.invalid",
            "commit.gpgsign": "false",
            "tag.gpgsign": "false",
            "core.autocrlf": "false",
            "core.hooksPath": str(self.root / "no-hooks"),
        }.items():
            self.git("config", "--local", key, value)
        (self.root / "content" / "chapters").mkdir(parents=True)
        self.chapter = self.root / "content" / "chapters" / "example.html"
        self.chapter.write_text("<p>Original chapter.</p>\n", encoding="utf-8")
        self.version = self.root / "content" / "version.yml"
        self.changelog = self.root / "content" / "CHANGELOG.md"
        self.version.write_text(
            'version: "1.1"\ndate: "2026-07-08"\napm_version: "0.23.1"\n', encoding="utf-8"
        )
        self.old_notes = "## [1.1] - 2026-07-08\n\n- Original edition.\n"
        self.changelog.write_text(self.old_notes, encoding="utf-8")
        self.commit()
        self.git("tag", "v1.1")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True,
            text=True, encoding="utf-8",
        ).stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Test fixture")

    def prepare(self, *, content=True):
        self.version.write_text(
            'version: "1.2"\ndate: "2026-09-15"\napm_version: "0.31.0"\n', encoding="utf-8"
        )
        self.changelog.write_text(
            "## [1.2] - 2026-09-15\n\n- Revised chapter.\n\n" + self.old_notes, encoding="utf-8"
        )
        if content:
            self.chapter.write_text("<p>Revised chapter.</p>\n", encoding="utf-8")

    def publish_fixture(self):
        self.prepare()
        self.commit()
        self.git("tag", "v1.2")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def test_tooling_only_without_bump_is_allowed(self):
        (self.root / "README.md").write_text("Tooling documentation.\n", encoding="utf-8")
        validate_change(self.root, "v1.1")

    def test_changed_chapter_without_bump_is_blocked(self):
        self.chapter.write_text("<p>Changed.</p>\n", encoding="utf-8")
        with self.assertRaisesRegex(ReleaseError, "without a new edition"):
            validate_change(self.root, "v1.1")

    def test_untracked_chapter_without_bump_is_blocked(self):
        (self.chapter.parent / "new.html").write_text("<p>New.</p>\n", encoding="utf-8")
        with self.assertRaisesRegex(ReleaseError, "without a new edition"):
            validate_change(self.root, "v1.1")

    def test_tooling_only_bump_is_blocked(self):
        self.prepare(content=False)
        with self.assertRaisesRegex(ReleaseError, "require chapter or TOC"):
            validate_change(self.root, "v1.1")

    def test_content_bump_prepares_without_a_tag(self):
        self.prepare()
        validate_change(self.root, "v1.1")

    def test_changing_baseline_alone_is_blocked(self):
        self.version.write_text(
            'version: "1.1"\ndate: "2026-07-08"\napm_version: "0.31.0"\n', encoding="utf-8"
        )
        with self.assertRaisesRegex(ReleaseError, "baseline requires a new content edition"):
            validate_change(self.root, "v1.1")

    def test_metadata_adoption_does_not_require_a_content_bump(self):
        self.version.write_text('version: "1.1"\ndate: "2026-07-08"\n', encoding="utf-8")
        self.commit()
        base = self.git("rev-parse", "HEAD")
        self.version.write_text(
            'version: "1.1"\ndate: "2026-07-08"\napm_version: "0.23.1"\n', encoding="utf-8"
        )
        validate_change(self.root, base)

    def test_legacy_tag_without_metadata_is_supported_as_comparison_base(self):
        self.version.unlink()
        self.commit()
        self.git("tag", "v1.0")
        self.prepare()
        validate_change(self.root, "refs/tags/v1.0")

    def test_unknown_base_without_metadata_is_blocked(self):
        self.version.unlink()
        self.commit()
        base = self.git("rev-parse", "HEAD")
        self.prepare()
        with self.assertRaisesRegex(ReleaseError, "cannot establish its edition"):
            validate_change(self.root, base)

    def test_merged_tag_matches_edition_and_content(self):
        self.publish_fixture()
        validate_tag(self.root, "v1.2")

    def test_unmerged_tag_is_blocked(self):
        self.prepare()
        self.commit()
        self.git("tag", "v1.2")
        with self.assertRaisesRegex(ReleaseError, "not merged into origin/main"):
            validate_tag(self.root, "v1.2")

    def test_wrong_tag_or_non_edition_ref_is_blocked(self):
        self.publish_fixture()
        for tag in ["v1.3", "main", "v1.2.0", "v1.2\nbad", "v1.2;echo bad"]:
            with self.subTest(tag=tag):
                with self.assertRaises(ReleaseError):
                    validate_tag(self.root, tag)

    def test_branch_with_tag_name_cannot_substitute_for_tag(self):
        self.prepare()
        self.commit()
        self.git("branch", "v1.2")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        with self.assertRaises(ReleaseError):
            validate_tag(self.root, "v1.2")

    def test_tag_must_be_checked_out(self):
        self.publish_fixture()
        (self.root / "README.md").write_text("Later tooling.\n", encoding="utf-8")
        self.commit()
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        with self.assertRaisesRegex(ReleaseError, "Check out v1.2"):
            validate_tag(self.root, "v1.2")

    def test_dirty_tag_checkout_is_blocked(self):
        self.publish_fixture()
        self.chapter.write_text("Unreviewed change.\n", encoding="utf-8")
        with self.assertRaisesRegex(ReleaseError, "clean worktree"):
            validate_tag(self.root, "v1.2")

    def test_no_reader_change_cannot_be_tagged_as_new_edition(self):
        self.prepare(content=False)
        self.commit()
        self.git("tag", "v1.2")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        with self.assertRaisesRegex(ReleaseError, "require chapter or TOC"):
            validate_tag(self.root, "v1.2")

    def test_previous_tag_is_required(self):
        self.prepare()
        self.changelog.write_text(
            "## [1.2] - 2026-09-15\n- Revision.\n\n## [1.0] - 2026-07-03\n- Original.\n",
            encoding="utf-8",
        )
        self.commit()
        self.git("tag", "v1.2")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        with self.assertRaisesRegex(ReleaseError, "Preserve the previous edition"):
            validate_tag(self.root, "v1.2")

    def test_deleting_history_does_not_bypass_content_only_gate(self):
        self.prepare(content=False)
        self.changelog.write_text("## [1.2] - 2026-09-15\n- Tooling only.\n", encoding="utf-8")
        self.commit()
        self.git("tag", "v1.2")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        with self.assertRaisesRegex(ReleaseError, "Preserve the previous edition"):
            validate_tag(self.root, "v1.2")

    def test_new_edition_cannot_lower_reviewed_upstream_baseline(self):
        self.prepare()
        self.version.write_text(
            'version: "1.2"\ndate: "2026-09-15"\napm_version: "0.22.0"\n', encoding="utf-8"
        )
        with self.assertRaisesRegex(ReleaseError, "cannot go backwards"):
            validate_change(self.root, "v1.1")


if __name__ == "__main__":
    unittest.main()
