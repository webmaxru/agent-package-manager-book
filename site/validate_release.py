"""Validate an edition, a proposed content change, or an existing release tag."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from release_metadata import (
    EDITION_PATTERN,
    ReleaseError,
    parse_metadata,
    validate_metadata,
    version_number,
    version_tuple,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATHS = ("content/chapters", "content/toc.yml")
LEGACY_TAGS = {"v1.0", "v1.1"}


def git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True,
            text=True, encoding="utf-8",
        )
    except FileNotFoundError as error:
        raise ReleaseError("Git is required for release provenance checks.") from error
    except subprocess.CalledProcessError as error:
        raise ReleaseError(f"git {' '.join(args)} failed: {error.stderr.strip()}") from error
    return result.stdout.strip()


def resolve_commit(root: Path, ref: str) -> str:
    return git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}")


def changed_content(root: Path, base: str) -> list[str]:
    tracked = git(root, "diff", "--name-only", "--no-renames", base, "--", *CONTENT_PATHS)
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "--", *CONTENT_PATHS)
    return sorted(set(tracked.splitlines()) | set(untracked.splitlines()))


def validate_change(root: Path, base_ref: str) -> None:
    edition, _ = validate_metadata(root)
    base = resolve_commit(root, base_ref)
    metadata_path = "content/version.yml"
    base_has_metadata = git(root, "ls-tree", "--name-only", base, "--", metadata_path)
    if base_has_metadata:
        data = parse_metadata(git(root, "show", f"{base}:{metadata_path}"), base_ref)
        base_version = version_number(data.get("version"))
        base_apm = data.get("apm_version")
        base_tag = base_ref.removeprefix("refs/tags/")
        if re.fullmatch(rf"v{EDITION_PATTERN}", base_tag) and base_tag != f"v{base_version}":
            raise ReleaseError(f"{base_ref} does not match its own content edition (v{base_version}).")
        if base_apm is not None:
            version_number(base_apm, apm=True)
            if version_tuple(edition.apm_version) < version_tuple(base_apm):
                raise ReleaseError("The reviewed APM baseline cannot go backwards.")
    else:
        # These two historical tags were published before edition metadata existed.
        legacy_tag = base_ref.removeprefix("refs/tags/")
        if legacy_tag not in LEGACY_TAGS:
            raise ReleaseError(f"{base_ref} has no content/version.yml; cannot establish its edition.")
        base_version = legacy_tag.removeprefix("v")
        base_apm = None

    changed = changed_content(root, base)
    if version_tuple(edition.version) < version_tuple(base_version):
        raise ReleaseError(f"Edition v{edition.version} is older than {base_ref} (v{base_version}).")
    if edition.version == base_version:
        if changed:
            raise ReleaseError(
                "Reader-facing content changed without a new edition: " + ", ".join(changed)
            )
        if base_apm is not None and base_apm != edition.apm_version:
            raise ReleaseError("Changing the reviewed APM baseline requires a new content edition.")
    elif not changed:
        raise ReleaseError("Edition bumps require chapter or TOC changes, not only tooling or metadata.")


def validate_tag(root: Path, tag: str, main_ref: str = "origin/main") -> None:
    if not re.fullmatch(rf"v{EDITION_PATTERN}", tag):
        raise ReleaseError("Release tags must have the exact form vX.Y.")
    edition, entries = validate_metadata(root)
    if tag != f"v{edition.version}":
        raise ReleaseError(f"Tag {tag} does not match content/version.yml (v{edition.version}).")
    commit = resolve_commit(root, f"refs/tags/{tag}")
    if commit != resolve_commit(root, "HEAD"):
        raise ReleaseError(f"Check out {tag} before validating or publishing it.")
    if git(root, "status", "--porcelain"):
        raise ReleaseError("Tag validation requires a clean worktree; commit the reviewed inputs first.")
    main = resolve_commit(root, main_ref)
    if git(root, "merge-base", commit, main) != commit:
        raise ReleaseError(f"Release tag {tag} is not merged into {main_ref}.")
    earlier_tags = [
        item for item in git(root, "tag", "--list", "v*").splitlines()
        if re.fullmatch(rf"v{EDITION_PATTERN}", item)
        and version_tuple(item[1:]) < version_tuple(edition.version)
    ]
    previous = max(earlier_tags, key=lambda item: version_tuple(item[1:]), default=None)
    recorded_previous = f"v{entries[1].version}" if len(entries) > 1 else None
    if previous != recorded_previous:
        raise ReleaseError(
            "Preserve the previous edition in CHANGELOG and fetch its tag; "
            f"latest earlier tag: {previous}, previous changelog edition: {recorded_previous}."
        )
    if previous is not None:
        previous_commit = resolve_commit(root, f"refs/tags/{previous}")
        if git(root, "merge-base", previous_commit, commit) != previous_commit:
            raise ReleaseError(f"Previous edition {previous} is not an ancestor of {tag}.")
        validate_change(root, f"refs/tags/{previous}")
    elif edition.version != "1.0" or not any((root / "content" / "chapters").glob("*.html")):
        raise ReleaseError("Only an initial v1.0 with chapter content can be released without a prior tag.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Book repository root.")
    parser.add_argument("--base-ref", help="Compare proposed content and edition with this Git ref.")
    parser.add_argument("--tag", help="Validate an existing tag at HEAD, merged into main.")
    parser.add_argument("--main-ref", default="origin/main", help="Published branch for --tag.")
    args = parser.parse_args(argv)
    try:
        edition, _ = validate_metadata(args.root)
        if args.base_ref:
            validate_change(args.root, args.base_ref)
        if args.tag:
            validate_tag(args.root, args.tag, args.main_ref)
    except ReleaseError as error:
        print(f"release preflight: {error}", file=sys.stderr)
        return 1
    print(f"Release preflight passed: book v{edition.version}, APM {edition.apm_version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
