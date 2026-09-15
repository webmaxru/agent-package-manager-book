from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

import extract_release_notes
import generate
import validate_release
from release_metadata import ReleaseError, read_changelog, read_edition, release_notes, validate_metadata


class ReleaseMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "content").mkdir()
        self.version = self.root / "content" / "version.yml"
        self.changelog = self.root / "content" / "CHANGELOG.md"
        self.version.write_text(
            'version: "1.2"\ndate: "2026-09-15"\napm_version: "0.31.0"\n', encoding="utf-8"
        )
        self.notes = "## [1.2] \u2014 2026-09-15\n\n### Changed\n- Revised Chapter 5.\n"
        self.changelog.write_text(
            "# Changelog\n\n" + self.notes
            + "\n## [1.1] - 2026-07-08\n\n### Added\n- Added gh-aw guidance.\n",
            encoding="utf-8",
        )

    def test_current_metadata_and_exact_note_boundaries(self):
        edition, entries = validate_metadata(self.root)
        self.assertEqual((edition.version, edition.date, edition.apm_version),
                         ("1.2", "2026-09-15", "0.31.0"))
        self.assertEqual([entry.version for entry in entries], ["1.2", "1.1"])
        self.assertEqual(release_notes("1.2", self.changelog), self.notes)
        self.assertEqual(release_notes("v1.2", self.changelog), self.notes)
        self.assertNotIn("Revised Chapter 5", release_notes("1.1", self.changelog))

    def test_missing_version_file_blocks_generator_instead_of_defaulting(self):
        self.version.unlink()
        with patch.object(generate, "VERSION_PATH", self.version):
            with self.assertRaisesRegex(ReleaseError, "Cannot read"):
                generate.load_content_edition()

    def test_invalid_metadata(self):
        invalid = [
            "", "[]", "version: [",
            'version: 1.2\ndate: "2026-09-15"\napm_version: "0.31.0"',
            'version: "v1.2"\ndate: "2026-09-15"\napm_version: "0.31.0"',
            'version: "1.2.0"\ndate: "2026-09-15"\napm_version: "0.31.0"',
            'version: "1.02"\ndate: "2026-09-15"\napm_version: "0.31.0"',
            'version: "1.2"\ndate: "2026-02-30"\napm_version: "0.31.0"',
            'version: "1.2"\ndate: 2026-02-30\napm_version: "0.31.0"',
            'version: "1.2"\ndate: "2026-9-15"\napm_version: "0.31.0"',
            'version: "1.2"\ndate: 2026-09-15T00:00:00Z\napm_version: "0.31.0"',
            'version: "1.2"\ndate: "2026-09-15"',
            'version: "1.2"\ndate: "2026-09-15"\napm_version: "latest"',
            'version: "1.2"\ndate: "2026-09-15"\napm_version: "0.31.0-rc.1"',
        ]
        for text in invalid:
            with self.subTest(text=text):
                self.version.write_text(text, encoding="utf-8")
                with self.assertRaises(ReleaseError):
                    read_edition(self.version)

    def test_yaml_date_is_accepted(self):
        self.version.write_text(
            'version: "1.2"\ndate: 2026-09-15\napm_version: "0.31.0"', encoding="utf-8"
        )
        self.assertEqual(read_edition(self.version).date, "2026-09-15")

    def test_missing_notes_fail_with_no_success_shaped_stdout(self):
        with patch.object(extract_release_notes, "CHANGELOG", self.changelog):
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = extract_release_notes.main(["extract_release_notes.py", "1.3"])
        self.assertEqual(result, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("no changelog entry for v1.3", stderr.getvalue())

    def test_missing_changelog_is_an_error(self):
        self.changelog.unlink()
        with self.assertRaisesRegex(ReleaseError, "Cannot read"):
            release_notes("1.2", self.changelog)

    def test_empty_duplicate_and_malformed_entries_are_rejected(self):
        invalid = [
            "# Changelog\n",
            "## [1.2] - 2026-09-15\n",
            "## [1.2] - 2026-09-15\n\n### Added\n<!-- fill this in -->\n",
            self.notes + "\n" + self.notes,
            "## [1.2] - yesterday\n- Changed.\n",
            "## [1.2] - 2026-02-30\n- Changed.\n",
            "## [v1.2] - 2026-09-15\n- Changed.\n",
        ]
        for text in invalid:
            with self.subTest(text=text):
                self.changelog.write_text(text, encoding="utf-8")
                with self.assertRaises(ReleaseError):
                    read_changelog(self.changelog)

    def test_unreleased_is_not_mixed_into_release_notes(self):
        text = self.changelog.read_text(encoding="utf-8")
        self.changelog.write_text(
            "## [Unreleased]\n- Not released.\n\n" + text, encoding="utf-8"
        )
        self.assertEqual(release_notes("1.2", self.changelog), self.notes)

    def test_date_and_first_edition_must_match(self):
        for source, replacement in [("2026-09-15", "2026-09-14"), ('"1.2"', '"1.3"')]:
            with self.subTest(source=source):
                self.version.write_text(
                    'version: "1.2"\ndate: "2026-09-15"\napm_version: "0.31.0"\n'.replace(
                        source, replacement
                    ), encoding="utf-8",
                )
                with self.assertRaises(ReleaseError):
                    validate_metadata(self.root)

    def test_editions_must_be_in_descending_order(self):
        with self.changelog.open("a", encoding="utf-8") as handle:
            handle.write("\n## [1.3] - 2026-09-16\n- Misplaced edition.\n")
        with self.assertRaisesRegex(ReleaseError, "newest first"):
            validate_metadata(self.root)

    def test_invalid_requested_versions_do_not_match(self):
        for value in ["vv1.2", "1", "1.2.0", "1.2; echo bad"]:
            with self.subTest(value=value):
                with self.assertRaises(ReleaseError):
                    release_notes(value, self.changelog)

    def test_cli_preflight_returns_one_on_invalid_metadata(self):
        self.version.write_text("[]", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(validate_release.main(["--root", str(self.root)]), 1)

    def test_sitemap_uses_edition_date_not_the_rebuild_date(self):
        with patch.object(generate, "CONTENT_DATE", "2026-07-08"):
            sitemap = generate.render_sitemap([])
        self.assertEqual(sitemap.count("<lastmod>2026-07-08</lastmod>"), 3)


if __name__ == "__main__":
    unittest.main()
