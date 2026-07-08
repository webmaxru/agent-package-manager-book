"""Print the CHANGELOG section for one content edition, as GitHub Release notes.

The book's ``content/CHANGELOG.md`` is the human-readable record of each content
edition. The ``release-content`` workflow calls this script to turn the section
for the edition being released into the body of the GitHub Release, so the notes
never drift from the changelog. It is also handy locally to preview notes:

    python site/extract_release_notes.py 1.1
    python site/extract_release_notes.py v1.1   # a leading "v" is accepted

Exit status is 0 even when the version is not found (a short placeholder is
printed instead), so a release is never blocked purely on notes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parents[1] / "content" / "CHANGELOG.md"

# A section header looks like: "## [1.1] — 2026-07-08"
_HEADER_RE = re.compile(r"^##\s+\[([^\]]+)\]")


def extract(version: str) -> str:
    """Return the changelog block for ``version`` (without the leading ``v``)."""
    version = version.strip().lstrip("v").strip()
    if not CHANGELOG.exists():
        return f"Release v{version}.\n"
    lines = CHANGELOG.read_text(encoding="utf-8").splitlines()

    start: int | None = None
    for i, line in enumerate(lines):
        match = _HEADER_RE.match(line)
        if match and match.group(1).strip() == version:
            start = i
            break
    if start is None:
        return f"Release v{version}.\n"

    body = [lines[start]]
    for line in lines[start + 1:]:
        if _HEADER_RE.match(line):
            break
        body.append(line)
    return "\n".join(body).strip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: extract_release_notes.py <version>", file=sys.stderr)
        return 2
    sys.stdout.write(extract(argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
