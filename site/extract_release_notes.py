"""Print the CHANGELOG section for one content edition, as GitHub Release notes.

The book's ``content/CHANGELOG.md`` is the human-readable record of each content
edition. The ``release-content`` workflow calls this script to turn the section
for the edition being released into the body of the GitHub Release, so the notes
never drift from the changelog. It is also handy locally to preview notes:

    python site/extract_release_notes.py 1.1
    python site/extract_release_notes.py v1.1   # a leading "v" is accepted

Missing, empty, duplicate, or malformed changelog entries fail with exit status 1.
"""
from __future__ import annotations

import sys
from pathlib import Path

from release_metadata import ReleaseError, release_notes

CHANGELOG = Path(__file__).resolve().parents[1] / "content" / "CHANGELOG.md"


def extract(version: str) -> str:
    """Return the changelog block for ``version`` (without the leading ``v``)."""
    return release_notes(version.strip(), CHANGELOG)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: extract_release_notes.py <version>", file=sys.stderr)
        return 2
    try:
        notes = extract(argv[1])
    except ReleaseError as error:
        print(f"release notes: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
