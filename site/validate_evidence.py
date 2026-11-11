"""Verify edition evidence and its Git-object binding to reviewed inputs."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

from release_metadata import ReleaseError, validate_metadata
from validate_release import ROOT, git, resolve_commit


def validate_evidence(root: Path, base_ref: str) -> None:
    edition, _ = validate_metadata(root)
    base = resolve_commit(root, base_ref)
    changed = set(git(root, "diff", "--name-only", "--no-renames", base, "--",
                      "content/chapters", "content/toc.yml", "backend/examples").splitlines())
    paths = {p for p in changed if (root / p).is_file()}
    if not paths:
        raise ReleaseError("No current reader-facing inputs to bind.")
    folder = root / "content" / "research" / "updates" / edition.version
    try:
        manifest = json.loads((folder / "commit-binding.json").read_text(encoding="utf-8"))
        toc = yaml.safe_load((root / "content" / "toc.yml").read_text(encoding="utf-8"))
        old_toc = yaml.safe_load(git(root, "show", f"{base}:content/toc.yml"))
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as error:
        raise ReleaseError(f"Cannot read edition evidence: {error}") from error
    if (manifest.get("book_edition") != edition.version
            or manifest.get("reviewed_apm_version") != edition.apm_version
            or manifest.get("result") != "PASS"):
        raise ReleaseError("Evidence edition, reviewed APM version or binding result is wrong.")
    entries = manifest.get("bound_paths")
    if not isinstance(entries, list):
        raise ReleaseError("Evidence must contain bound_paths.")
    bound = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ReleaseError("Malformed evidence binding.")
        name, oid = entry.get("path"), entry.get("git_blob_oid")
        if (not isinstance(name, str) or name in bound or name.startswith("/")
                or "\\" in name or ".." in Path(name).parts
                or not isinstance(oid, str) or not re.fullmatch(r"[0-9a-f]{40}", oid)):
            raise ReleaseError("Invalid or duplicate bound path or Git object ID.")
        file = root / name
        if not file.is_file() or git(root, "hash-object", "--", name) != oid:
            raise ReleaseError(f"Reviewed input does not match binding: {name}")
        bound[name] = oid
    if not paths.issubset(bound):
        raise ReleaseError("Changed inputs missing from evidence binding: " + ", ".join(sorted(paths - bound)))
    removed = changed - paths
    declared_removed = manifest.get("removed_paths", [])
    if not isinstance(declared_removed, list) or set(declared_removed) != removed:
        raise ReleaseError("Removed inputs must be listed exactly in removed_paths.")
    if (not isinstance(toc, dict) or not isinstance(toc.get("chapters"), list)
            or not isinstance(old_toc, dict) or not isinstance(old_toc.get("chapters"), list)):
        raise ReleaseError("Invalid table of contents.")
    chapters = old_toc["chapters"] + toc["chapters"]
    by_path = {f"content/chapters/{chapter['slug']}.html": chapter["number"] for chapter in chapters}
    changed_chapters = {p for p in changed if p.startswith("content/chapters/") and p.endswith(".html")}
    if not changed_chapters.issubset(by_path):
        raise ReleaseError("Changed chapters must be represented in the old or current TOC.")
    affected = {by_path[p] for p in changed_chapters}
    declared = manifest.get("affected_chapters")
    if not isinstance(declared, list) or not declared or any(type(n) is not int or n not in by_path.values() for n in declared):
        raise ReleaseError("Evidence must declare valid affected chapter numbers.")
    if len(set(declared)) != len(declared) or not affected.issubset(declared):
        raise ReleaseError("Evidence does not cover every changed chapter.")
    reports = [folder / "integration-review.md"]
    for number in declared:
        reports.extend([folder / f"ch{number:02d}-review.md", folder / f"ch{number:02d}-verification.md"])
    for report in reports:
        name = report.relative_to(root).as_posix()
        if name not in bound:
            raise ReleaseError(f"Evidence report is not bound: {name}")
        text = report.read_text(encoding="utf-8")
        verdict = "PASS" if name.endswith("-verification.md") else "ACCEPT"
        if not re.search(rf"(?i)\bverdict\s*:\s*(?:\*\*)?\s*{verdict}\b", text):
            raise ReleaseError(f"Missing explicit {verdict} verdict: {name}")
        if edition.apm_version not in text:
            raise ReleaseError(f"Evidence does not name target APM {edition.apm_version}: {name}")
    results = manifest.get("example_results")
    if not isinstance(results, list):
        raise ReleaseError("Evidence must enumerate affected example results.")
    seen = set()
    covered = set()
    for item in results:
        if (not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip()
                or item.get("chapter") not in declared
                or item.get("status") not in {"PASS", "SKIPPED-needs-network"}
                or (item.get("status") == "SKIPPED-needs-network"
                    and (not isinstance(item.get("reason"), str) or not item["reason"].strip()))
                or (item["chapter"], item["id"]) in seen):
            raise ReleaseError("Invalid example result or undocumented skip.")
        seen.add((item["chapter"], item["id"]))
        covered.add(item["chapter"])
    no_examples = manifest.get("no_examples", [])
    if not isinstance(no_examples, list):
        raise ReleaseError("Invalid no_examples list.")
    for item in no_examples:
        if (not isinstance(item, dict) or item.get("chapter") not in declared
                or item["chapter"] in covered or not isinstance(item.get("reason"), str)
                or not item["reason"].strip()):
            raise ReleaseError("Invalid no-examples disposition.")
        covered.add(item["chapter"])
    if covered != set(declared):
        raise ReleaseError("Every affected chapter must enumerate its example results.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--base-ref", required=True)
    args = parser.parse_args(argv)
    try:
        validate_evidence(args.root, args.base_ref)
    except (ReleaseError, KeyError, TypeError, OSError, UnicodeError) as error:
        print(f"evidence preflight: {error}", file=sys.stderr)
        return 1
    print("Evidence preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
