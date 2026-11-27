"""Check an untagged edition against its previous immutable tag."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from release_metadata import ReleaseError, validate_metadata
from validate_release import ROOT, git, previous_edition, validate_change


def validate_candidate(root: Path) -> str:
    edition, entries = validate_metadata(root)
    previous = previous_edition(root, edition, entries)
    ref = f"refs/tags/{previous}"
    if git(root, "merge-base", ref, "HEAD") != git(root, "rev-parse", f"{ref}^{{commit}}"):
        raise ReleaseError("Previous edition is not an ancestor of the proposed merge.")
    validate_change(root, f"refs/tags/{previous}")
    return f"v{edition.version}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        print(f"tag={validate_candidate(args.root)}")
    except ReleaseError as error:
        print(f"release candidate: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
