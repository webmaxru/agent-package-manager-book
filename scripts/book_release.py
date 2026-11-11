"""Trusted controller for approved book updates. Run only from the default branch."""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import PurePosixPath

OWNER = "webmaxru"
SHA = re.compile(r"[0-9a-f]{40}\Z")
TAG = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")


class GateError(ValueError):
    pass


class APIError(RuntimeError):
    pass


class GitHub:
    def __init__(self):
        self.repo = os.environ["GITHUB_REPOSITORY"]
        self.token = os.environ["GH_TOKEN"]
        self.api = os.environ.get("GITHUB_API_URL", "https://api.github.com")

    def request(self, method, path, data=None, *, missing=False):
        body = json.dumps(data).encode() if data is not None else None
        request = urllib.request.Request(
            f"{self.api}/repos/{self.repo}/{path}", body, method=method,
            headers={"Authorization": f"Bearer {self.token}",
                     "Accept": "application/vnd.github+json",
                     "Content-Type": "application/json",
                     "X-GitHub-Api-Version": "2022-11-28"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as error:
            if missing and error.code == 404:
                return None
            raise APIError(f"GitHub {method} {path}: HTTP {error.code}") from error

    def pages(self, path):
        result = []
        for page in range(1, 1001):
            batch = self.request("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
            if not isinstance(batch, list):
                raise GateError(f"Expected a list from {path}.")
            result.extend(batch)
            if len(batch) < 100:
                return result
        raise GateError(f"Pagination limit exceeded for {path}.")


def full_sha(value):
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise GateError("Expected a full lowercase 40-character commit SHA.")
    return value


def allowed_path(path):
    parts = PurePosixPath(path).parts
    if not parts or ".." in parts or "\\" in path or path.startswith("/"):
        return False
    if path in {"content/version.yml", "content/CHANGELOG.md", "content/toc.yml"}:
        return True
    if path.startswith(("content/chapters/", "content/research/", "backend/examples/")):
        return True
    if path in {"site/index.html", "site/llms.txt", "site/llms-full.txt",
                "site/sitemap.xml", "site/robots.txt", "site/site.webmanifest"}:
        return True
    return path.startswith("site/chapters/") and path.endswith(".html")


def content_files(files):
    if not files:
        raise GateError("No changed files.")
    paths = []
    for item in files:
        for path in (item["filename"], item.get("previous_filename", item["filename"])):
            if not allowed_path(path):
                raise GateError(f"Not an automatic content update: {path}")
        paths.append(item["filename"])
    if not any(path.startswith("content/chapters/") or path == "content/toc.yml" for path in paths):
        raise GateError("No reader-facing chapter/TOC changes.")
    if not {"content/version.yml", "content/CHANGELOG.md"}.issubset(paths):
        raise GateError("Changed edition metadata and changelog are required.")


def approval(pr, reviews, comments, timeline=()):
    head = full_sha(pr["head"]["sha"])
    formal = sorted(
        (r for r in reviews if r["user"]["login"] == OWNER
         and r["state"] in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}),
        key=lambda r: (r.get("submitted_at") or "", r["id"]),
    )
    latest = formal[-1] if formal else None
    if (pr["user"]["login"] != OWNER and latest and latest["state"] == "APPROVED"
            and latest["commit_id"] == head):
        return True
    if pr["user"]["login"] != OWNER:
        return False
    barrier = (latest.get("submitted_at") or "") if latest and latest["state"] != "APPROVED" else ""
    owner_reviews = {r["id"] for r in formal}
    for event in timeline:
        if (event.get("event") == "review_dismissed"
                and event.get("dismissed_review", {}).get("review_id") in owner_reviews):
            barrier = max(barrier, event.get("created_at") or "")
    return any(
        c["user"]["login"] == OWNER and c.get("body", "") == f"/release-book {head}"
        and c["created_at"] > barrier
        for c in comments
    )


def candidate(api, number, *, expected_head=None, expected_base=None, checks=False):
    pr = api.request("GET", f"pulls/{number}")
    head_repo = pr["head"].get("repo") or {}
    if (pr["base"]["ref"] != "main" or pr["base"]["repo"]["full_name"] != api.repo
            or head_repo.get("full_name") != api.repo or pr["draft"]
            or (pr["state"] != "open" and not pr.get("merged"))):
        raise GateError("Only same-repository, non-draft content PRs targeting main qualify.")
    head = full_sha(pr["head"]["sha"])
    if expected_head and head != full_sha(expected_head):
        raise GateError("PR head changed after preflight.")
    files = api.pages(f"pulls/{number}/files")
    if len(files) != pr["changed_files"]:
        raise GateError("Changed-file list is incomplete.")
    content_files(files)
    if not approval(pr, api.pages(f"pulls/{number}/reviews"), api.pages(f"issues/{number}/comments"),
                    api.pages(f"issues/{number}/timeline")):
        raise GateError("No current owner approval of this exact PR head.")
    base = full_sha(pr["base"]["sha"])
    if pr.get("merged"):
        commit = api.request("GET", f"git/commits/{full_sha(pr['merge_commit_sha'])}")
        base = full_sha(commit["parents"][0]["sha"])
    if expected_base and base != full_sha(expected_base):
        raise GateError("PR base changed after preflight.")
    if checks:
        response = api.request(
            "GET", f"actions/workflows/check-book.yml/runs?head_sha={head}&event=pull_request&per_page=100"
        )
        matches = [r for r in response["workflow_runs"]
                   if r["head_sha"] == head and r["head_branch"] == pr["head"]["ref"]
                   and r["head_repository"]["full_name"] == api.repo]
        latest = max(matches, key=lambda r: r["id"], default=None)
        if not latest or latest["status"] != "completed" or latest["conclusion"] != "success":
            raise GateError("Latest Check book update run for this head is not successful.")
    fresh = api.request("GET", f"pulls/{number}")
    if fresh["head"]["sha"] != head or fresh["base"]["sha"] != pr["base"]["sha"]:
        raise GateError("PR changed during authorization.")
    return pr, head, base


def output(values):
    for key, value in values.items():
        print(f"{key}={value}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as handle:
            for key, value in values.items():
                handle.write(f"{key}={value}\n")


def event_numbers(api, event):
    if "issue" in event and "pull_request" in event["issue"]:
        comment = event.get("comment", {})
        if (comment.get("user", {}).get("login") == OWNER
                and re.fullmatch(r"/release-book [0-9a-f]{40}", comment.get("body", ""))):
            return [event["issue"]["number"]]
        return []
    if event.get("inputs", {}).get("pr"):
        return [int(event["inputs"]["pr"])]
    run = event.get("workflow_run", {})
    if (run.get("head_repository") or {}).get("full_name") != api.repo:
        return []
    branch = run.get("head_branch")
    if not isinstance(branch, str) or not branch:
        return []
    head = urllib.parse.quote(f"{api.repo.split('/')[0]}:{branch}", safe="")
    return [p["number"] for p in api.pages(f"pulls?state=open&base=main&head={head}")]


def inspect(api, event):
    eligible = []
    for number in event_numbers(api, event):
        try:
            pr, head, base = candidate(api, number, checks=True)
            if pr.get("merged"):
                continue
        except GateError as error:
            print(f"PR {number} not eligible: {error}", file=sys.stderr)
            continue
        eligible.append({"pr": str(number), "head": head, "base": base})
    if len(eligible) > 1:
        raise GateError("Ambiguous signal; dispatch with one explicit PR number.")
    output({"eligible": "true", **eligible[0]} if eligible else {"eligible": "false"})


def merge(api, number, head, base):
    pr, _, _ = candidate(api, number, expected_head=head, expected_base=base, checks=True)
    if pr.get("merged"):
        merge_sha = full_sha(pr["merge_commit_sha"])
    else:
        main = api.request("GET", "git/ref/heads/main")["object"]["sha"]
        if main != base:
            raise GateError("Main advanced during preflight; update the branch and approve again.")
        result = api.request("PUT", f"pulls/{number}/merge", {"sha": head, "merge_method": "squash"})
        if not result.get("merged"):
            raise GateError("GitHub refused the SHA-conditional merge.")
        merge_sha = full_sha(result["sha"])
    api.request("POST", "actions/workflows/release-content.yml/dispatches", {
        "ref": "main", "inputs": {"pr": str(number), "head_sha": head,
                                 "base_sha": base, "merge_sha": merge_sha},
    })
    output({"merge_sha": merge_sha})


def release_plan(api, *, number=None, head=None, base=None, merge_sha=None, tag=None):
    existing = None
    if tag:
        if not TAG.fullmatch(tag):
            raise GateError("Recovery requires an exact vX.Y tag.")
        ref = api.request("GET", f"git/ref/tags/{tag}")["object"]
        while ref["type"] == "tag":
            ref = api.request("GET", f"git/tags/{ref['sha']}")["object"]
        merge_sha = full_sha(ref["sha"])
        existing = api.request("GET", f"releases/tags/{tag}", missing=True)
        associated = api.pages(f"commits/{merge_sha}/pulls")
        matches = [p for p in associated if p.get("merged_at") and p["merge_commit_sha"] == merge_sha]
        if len(matches) != 1:
            raise GateError("New tag publication requires one approved, merged content PR.")
        number = matches[0]["number"]
    if not number or not merge_sha:
        raise GateError("Provide approved PR provenance or an existing edition tag.")
    merge_sha = full_sha(merge_sha)
    pr, actual_head, actual_base = candidate(
        api, int(number), expected_head=head, expected_base=base, checks=True,
    )
    if not pr.get("merged") or pr["merge_commit_sha"] != merge_sha:
        raise GateError("Release SHA is not this PR's exact merge commit.")
    comparison = api.request("GET", f"compare/{merge_sha}...main")
    if comparison["merge_base_commit"]["sha"] != merge_sha:
        raise GateError("Release commit is not on main.")
    commit = api.request("GET", f"git/commits/{merge_sha}")
    source = api.request("GET", f"git/commits/{actual_head}")
    if commit["parents"][0]["sha"] != actual_base or source["tree"]["sha"] != commit["tree"]["sha"]:
        raise GateError("Merged tree or base differs from the approved preflight.")
    if tag:
        metadata = api.request("GET", f"contents/content/version.yml?ref={merge_sha}")
        if metadata.get("encoding") != "base64":
            raise GateError("Cannot verify the tagged edition metadata.")
        data = base64.b64decode(metadata["content"], validate=False).decode("utf-8")
        versions = re.findall(r'(?m)^version:\s*["\'](0|[1-9][0-9]*)\.(0|[1-9][0-9]*)["\']\s*$', data)
        if len(versions) != 1 or f"v{versions[0][0]}.{versions[0][1]}" != tag:
            raise GateError("Tag does not match the edition at the approved merge.")
    if existing and not existing["draft"]:
        assets = api.pages(f"releases/{existing['id']}/assets")
        if not any(a["name"] == f"apm-book-{tag}.pdf" and a["size"] > 5 for a in assets):
            raise GateError("Published release is incomplete; immutable assets were not overwritten.")
        output({"merge_sha": merge_sha, "tag": tag, "recovery": "true"})
        return
    output({"merge_sha": merge_sha, "head": actual_head, "base": actual_base,
            "pr": str(number), "tag": tag or "", "recovery": "false"})


def publish(api, tag, sha, pdf, notes):
    if not TAG.fullmatch(tag):
        raise GateError("Invalid edition tag.")
    full_sha(sha)
    if not os.path.isfile(pdf) or os.path.getsize(pdf) <= 5:
        raise GateError("Missing or empty PDF artifact.")
    with open(pdf, "rb") as handle:
        if handle.read(5) != b"%PDF-":
            raise GateError("Artifact is not a PDF.")
    if not os.path.isfile(notes) or not os.path.getsize(notes):
        raise GateError("Missing release notes.")
    ref = api.request("GET", f"git/ref/tags/{tag}", missing=True)
    if ref:
        obj = ref["object"]
        while obj["type"] == "tag":
            obj = api.request("GET", f"git/tags/{obj['sha']}")["object"]
        if obj["type"] != "commit" or obj["sha"] != sha:
            raise GateError("Existing edition tag points to another commit; never move it.")
    else:
        api.request("POST", "git/refs", {"ref": f"refs/tags/{tag}", "sha": sha})
    existing = api.request("GET", f"releases/tags/{tag}", missing=True)
    if existing and not existing["draft"]:
        assets = api.pages(f"releases/{existing['id']}/assets")
        if not any(a["name"] == f"apm-book-{tag}.pdf" and a["size"] > 5 for a in assets):
            raise GateError("Published release is incomplete; do not overwrite immutable assets.")
        print("Existing published edition preserved.")
        return
    releases = api.pages("releases")
    current = tuple(map(int, tag[1:].split(".")))
    newest = all(
        tuple(map(int, release["tag_name"][1:].split("."))) <= current
        for release in releases
        if not release["draft"] and not release["prerelease"] and TAG.fullmatch(release["tag_name"])
    )
    if not existing:
        subprocess.run(["gh", "release", "create", tag, "--verify-tag", "--draft",
                        "--latest=false", "--title", f"Book {tag}", "--notes-file", notes],
                       check=True)
    subprocess.run(["gh", "release", "upload", tag, pdf, "--clobber"], check=True)
    subprocess.run(["gh", "release", "edit", tag, "--draft=false",
                    f"--latest={'true' if newest else 'false'}"], check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["inspect", "merge", "release-plan", "publish"])
    parser.add_argument("--event")
    parser.add_argument("--pr", type=int)
    parser.add_argument("--head")
    parser.add_argument("--base")
    parser.add_argument("--merge-sha")
    parser.add_argument("--tag")
    parser.add_argument("--pdf")
    parser.add_argument("--notes")
    args = parser.parse_args(argv)
    try:
        api = GitHub()
        if args.operation == "inspect":
            with open(args.event or os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as handle:
                inspect(api, json.load(handle))
        elif args.operation == "merge":
            merge(api, args.pr, full_sha(args.head), full_sha(args.base))
        elif args.operation == "release-plan":
            release_plan(api, number=args.pr, head=args.head, base=args.base,
                         merge_sha=args.merge_sha, tag=args.tag)
        else:
            publish(api, args.tag, args.merge_sha, args.pdf, args.notes)
    except (APIError, GateError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"book release: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
