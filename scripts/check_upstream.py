"""Read the complete stable APM release gap without changing the book or installing APM."""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "site"))

from release_metadata import ReleaseError, read_edition, version_number, version_tuple  # noqa: E402

API = "https://api.github.com/repos/microsoft/apm"
REPO = "https://github.com/microsoft/apm"


def fetch_json(endpoint: str) -> Any:
    request = urllib.request.Request(
        f"{API}/{endpoint}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "agent-package-manager-book",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        # Public metadata needs no token; do not inherit an unrelated organization's credentials.
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise ReleaseError(
            f"Public APM release lookup returned HTTP {error.code} at {request.full_url}. "
            "Check GitHub availability/rate limits or use an authorized gh release lookup; "
            "do not guess the target version."
        ) from error
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeError) as error:
        raise ReleaseError(f"Cannot read public APM release metadata: {error}") from error


def release_info(data: Any) -> dict[str, str]:
    if not isinstance(data, dict):
        raise ReleaseError("GitHub returned a release that is not an object.")
    if data.get("draft") is not False or data.get("prerelease") is not False:
        raise ReleaseError("The selected APM release must be published and stable.")
    tag = data.get("tag_name")
    if not isinstance(tag, str) or not tag.startswith("v"):
        raise ReleaseError("The APM release has no canonical vX.Y.Z tag.")
    version = version_number(tag.removeprefix("v"), apm=True)
    published = data.get("published_at")
    if not isinstance(published, str):
        raise ReleaseError(f"{tag} has no publication date.")
    try:
        timestamp = datetime.datetime.fromisoformat(published.replace("Z", "+00:00"))
    except ValueError as error:
        raise ReleaseError(f"{tag} has an invalid publication date.") from error
    if timestamp.tzinfo is None:
        raise ReleaseError(f"{tag} has a publication date without a time zone.")
    body = data.get("body")
    if body is not None and not isinstance(body, str):
        raise ReleaseError(f"{tag} has malformed release notes.")
    return {
        "version": version,
        "tag": tag,
        "published_at": published,
        "url": f"{REPO}/releases/tag/{tag}",
        "notes": body or "",
    }


def discover(root: Path, target: str | None = None) -> dict[str, Any]:
    edition = read_edition(root / "content" / "version.yml")
    if target is None:
        selected = release_info(fetch_json("releases/latest"))
    else:
        target = version_number(target.removeprefix("v"), apm=True)
        selected = release_info(fetch_json(f"releases/tags/v{target}"))
        if selected["version"] != target:
            raise ReleaseError("The returned APM release does not match the requested target.")
    baseline = version_tuple(edition.apm_version)
    target_version = version_tuple(selected["version"])
    if target_version < baseline:
        raise ReleaseError("The selected APM release is older than the book's reviewed baseline.")

    releases: dict[str, dict[str, str]] = {}
    if target_version > baseline:
        page = 1
        while True:
            batch = fetch_json(f"releases?per_page=100&page={page}")
            if not isinstance(batch, list):
                raise ReleaseError("GitHub returned an invalid release list.")
            for item in batch:
                if isinstance(item, dict) and (item.get("draft") is True or item.get("prerelease") is True):
                    continue
                release = release_info(item)
                if release["version"] in releases:
                    raise ReleaseError("GitHub release pagination changed during lookup; retry discovery.")
                releases[release["version"]] = release
            if len(batch) < 100:
                break
            page += 1
        if edition.apm_version not in releases or selected["version"] not in releases:
            raise ReleaseError("The release list does not contain both endpoints; the gap is incomplete.")

    gap = [
        releases[version] for version in sorted(releases, key=version_tuple)
        if baseline < version_tuple(version) <= target_version
    ]
    return {
        "book_edition": edition.version,
        "baseline_apm_version": edition.apm_version,
        "target_apm_version": selected["version"],
        "target_release_url": selected["url"],
        "target_published_at": selected["published_at"],
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "update_available": target_version > baseline,
        "compare_url": f"{REPO}/compare/v{edition.apm_version}...{selected['tag']}",
        "changelog_url": f"{REPO}/blob/{selected['tag']}/CHANGELOG.md",
        "releases": gap,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Book repository root.")
    parser.add_argument("--target", help="Exact stable APM version; defaults to GitHub's latest release.")
    args = parser.parse_args(argv)
    try:
        result = discover(args.root, args.target)
    except ReleaseError as error:
        print(f"upstream check: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
