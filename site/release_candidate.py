"""Check an untagged edition against its previous immutable tag."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from release_metadata import EDITION_PATTERN, ReleaseError, validate_metadata, version_tuple
from validate_release import ROOT, git, validate_change


def validate_candidate(root: Path) -> str:
    edition, entries = validate_metadata(root)
    tags = [tag for tag in git(root, "tag", "--list", "v*").splitlines()
            if re.fullmatch(rf"v{EDITION_PATTERN}", tag)
            and version_tuple(tag[1:]) < version_tuple(edition.version)]
    previous = max(tags, key=lambda tag: version_tuple(tag[1:]), default=None)
    recorded = f"v{entries[1].version}" if len(entries) > 1 else None
    if previous != recorded or not previous:
        raise ReleaseError("The previous changelog edition and fetched tag must match.")
    if git(root, "merge-base", previous, "HEAD") != git(root, "rev-parse", f"{previous}^{{commit}}"):
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
