"""Trusted controller for approved book updates. Run only from the default branch."""
from __future__ import annotations

import argparse
import base64
import datetime
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import PurePosixPath

OWNER = "webmaxru"
SHA = re.compile(r"[0-9a-f]{40}\Z")
TAG = re.compile(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
CHECK_WORKFLOW = "ci.yml"
CHECK_JOB = "Book release preflight"
RELEASE_WORKFLOW = "release.yml"
DEPLOY_WORKFLOW = "deploy-pages.yml"
DEPLOY_JOB = "deploy"
DEPLOY_STEPS = ("Deploy to GitHub Pages", "Smoke test the released edition")
# The release job's timeout-minutes must exceed this wait so a timeout is reported, not killed.
DEPLOY_WAIT_SECONDS = 2700
# This REST version returns the created run's ID from a workflow dispatch.
DISPATCH_API_VERSION = "2026-03-10"
MERGER = "github-actions[bot]"


class GateError(ValueError):
    pass


class StaleBase(GateError):
    def __init__(self, base, main):
        super().__init__(f"approved, but its base {base[:12]} is behind main {main[:12]}. "
                         "Update the branch from main, then approve the new head.")


class APIError(RuntimeError):
    pass


class GitHub:
    def __init__(self):
        self.repo = os.environ["GITHUB_REPOSITORY"]
        self.token = os.environ["GH_TOKEN"]
        self.api = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")

    def request(self, method, path, data=None, *, missing=False, version="2022-11-28"):
        body = json.dumps(data).encode() if data is not None else None
        request = urllib.request.Request(
            f"{self.api}/repos/{self.repo}/{path}", body, method=method,
            headers={"Authorization": f"Bearer {self.token}",
                     "Accept": "application/vnd.github+json",
                     "Content-Type": "application/json",
                     "X-GitHub-Api-Version": version},
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


def uploaded_pdf(assets, tag):
    return any(
        asset.get("name") == f"apm-book-{tag}.pdf"
        and asset.get("state") == "uploaded"
        and type(asset.get("size")) is int and asset["size"] > 5
        for asset in assets
    )


def safe_path(path):
    return (isinstance(path, str) and bool(path) and "\\" not in path
            and path != "." and not path.startswith("/") and ".." not in PurePosixPath(path).parts
            and str(PurePosixPath(path)) == path)


def allowed_path(path):
    if not safe_path(path):
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
        (r for r in reviews if (r.get("user") or {}).get("login") == OWNER
         and r["state"] in {"APPROVED", "CHANGES_REQUESTED", "DISMISSED"}),
        key=lambda r: (r.get("submitted_at") or "", r["id"]),
    )
    latest = formal[-1] if formal else None
    barrier = max((r.get("submitted_at") or "" for r in reviews
                   if r["state"] in {"CHANGES_REQUESTED", "DISMISSED"}), default="")
    for event in timeline:
        if event.get("event") == "review_dismissed":
            barrier = max(barrier, event.get("created_at") or "")
    if pr["user"]["login"] != OWNER:
        return bool(latest and latest["state"] == "APPROVED" and latest["commit_id"] == head
                    and (latest.get("submitted_at") or "") > barrier)
    return any(
        (c.get("user") or {}).get("login") == OWNER
        and c.get("body", "") == f"/release-book {head}"
        and (c.get("created_at") or "") > barrier
        and c.get("updated_at") == c.get("created_at")
        for c in comments
    )


def checks_passed(api, pr, head):
    response = api.request(
        "GET", f"actions/workflows/{CHECK_WORKFLOW}/runs?head_sha={head}&event=pull_request&per_page=100"
    )
    matches = [r for r in response["workflow_runs"]
               if r["head_sha"] == head and r["head_branch"] == pr["head"]["ref"]
               and (r.get("head_repository") or {}).get("full_name") == api.repo
               and r.get("event") == "pull_request"]
    latest = max(matches, key=lambda r: r["id"], default=None)
    if not latest or latest["status"] != "completed" or latest["conclusion"] != "success":
        raise GateError("Latest Book CI run for this head is not successful.")
    response = api.request("GET", f"actions/runs/{latest['id']}/jobs?filter=latest&per_page=100")
    jobs = response["jobs"]
    if len(jobs) != response["total_count"]:
        raise GateError("Book CI job list is incomplete.")
    aggregate = [j for j in jobs if j["name"] == CHECK_JOB]
    if (len(aggregate) != 1 or aggregate[0].get("head_sha") != head
            or aggregate[0].get("status") != "completed"
            or aggregate[0].get("conclusion") != "success"):
        raise GateError(f"'{CHECK_JOB}' has not passed on this exact head.")


def main_sha(api):
    return full_sha(api.request("GET", "git/ref/heads/main")["object"]["sha"])


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
    if pr.get("merged"):
        if (pr.get("merged_by") or {}).get("login") != MERGER:
            raise GateError("Release requires a merge by the GitHub Actions controller.")
        commit = api.request("GET", f"git/commits/{full_sha(pr['merge_commit_sha'])}")
        if len(commit["parents"]) != 1:
            raise GateError("Release requires a squash merge with exactly one parent.")
        base = full_sha(commit["parents"][0]["sha"])
    else:
        if pr.get("mergeable") is not True:
            raise GateError("PR is not mergeable (or GitHub has not computed it yet).")
        base = full_sha(pr["base"]["sha"])
    if expected_base and base != full_sha(expected_base):
        raise GateError("PR base changed after preflight.")
    if checks:
        checks_passed(api, pr, head)
    if not approval(pr, api.pages(f"pulls/{number}/reviews"), api.pages(f"issues/{number}/comments"),
                    api.pages(f"issues/{number}/timeline")):
        raise GateError("No current owner approval of this exact PR head.")
    if not pr.get("merged"):
        tip = main_sha(api)
        if base != tip:
            raise StaleBase(base, tip)
        comparison = api.request("GET", f"compare/{tip}...{head}")
        ancestor = full_sha(comparison["merge_base_commit"]["sha"])
        if ancestor != tip:
            raise StaleBase(ancestor, tip)
    fresh = api.request("GET", f"pulls/{number}")
    if (any(fresh.get(key) != pr.get(key) for key in
            ("head", "base", "state", "draft", "merged", "merge_commit_sha", "merged_by", "user"))
            or (not pr.get("merged") and
                (fresh.get("mergeable") is not True or main_sha(api) != base))):
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
    if event.get("schedule"):
        # A fixed cap bounds API usage. Older PRs outside this window can still
        # be re-evaluated by the explicit PR-number dispatch.
        return [p["number"] for p in api.request(
            "GET", "pulls?state=open&base=main&sort=updated&direction=desc&per_page=30"
        )]
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
        except StaleBase as error:
            message = f"PR {number}: {error}"
            print(f"::warning::{message}")
            if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
                with open(summary, "a", encoding="utf-8") as handle:
                    print(message, file=handle)
            continue
        except GateError as error:
            print(f"PR {number} not eligible: {error}", file=sys.stderr)
            continue
        eligible.append({"pr": str(number), "head": head, "base": base})
    if len(eligible) > 1 and not event.get("schedule"):
        raise GateError("Ambiguous signal; dispatch with one explicit PR number.")
    if eligible:
        # Rotate across a stable backlog, rather than retrying one failing PR
        # indefinitely. Missed schedules are recoverable by explicit dispatch.
        index = int(datetime.datetime.now(datetime.timezone.utc).timestamp() // 1800) % len(eligible)
        output({"eligible": "true", **eligible[index]})
    else:
        output({"eligible": "false"})


def merge(api, number, head, base):
    pr, _, _ = candidate(api, number, expected_head=head, expected_base=base, checks=True)
    tag = edition_tag(api, head)
    if pr.get("merged"):
        merge_sha = full_sha(pr["merge_commit_sha"])
        verify_squash(api, merge_sha, head, base)
    else:
        if main_sha(api) != base:
            raise GateError("Main advanced during preflight; update the branch and approve again.")
        result = api.request("PUT", f"pulls/{number}/merge", {"sha": head, "merge_method": "squash"})
        if not result.get("merged"):
            raise GateError("GitHub refused the SHA-conditional merge.")
        merge_sha = full_sha(result["sha"])
    api.request("POST", f"actions/workflows/{RELEASE_WORKFLOW}/dispatches", {
        "ref": "main", "inputs": {"pr": str(number), "head_sha": head,
                                 "base_sha": base, "merge_sha": merge_sha, "tag": tag},
    })
    output({"merge_sha": merge_sha, "tag": tag})


def peel(api, ref):
    obj = ref["object"]
    for _ in range(10):
        if obj["type"] == "commit":
            return full_sha(obj["sha"])
        if obj["type"] != "tag":
            break
        obj = api.request("GET", f"git/tags/{full_sha(obj['sha'])}")["object"]
    raise GateError("Tag does not resolve to a commit within ten objects.")


def edition_tag(api, sha):
    metadata = api.request("GET", f"contents/content/version.yml?ref={full_sha(sha)}")
    if metadata.get("encoding") != "base64":
        raise GateError("Cannot verify the edition metadata.")
    data = base64.b64decode(metadata["content"]).decode("utf-8")
    versions = re.findall(
        r'(?m)^version:[ \t]*(["\'])((?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))\1[ \t]*\r?$', data)
    if len(versions) != 1 or len(re.findall(r"(?m)^version:", data)) != 1:
        raise GateError("Edition metadata must contain exactly one quoted X.Y version.")
    return f"v{versions[0][1]}"


def find_release(api, tag):
    # The tag lookup endpoint hides drafts; listing includes them for an authenticated publisher.
    matches = [r for r in api.pages("releases") if r.get("tag_name") == tag]
    if len(matches) > 1:
        raise GateError(f"Multiple releases use {tag}; resolve the conflict manually.")
    return matches[0] if matches else None


def stable_releases(releases):
    return [r for r in releases if r.get("draft") is False and r.get("prerelease") is False
            and isinstance(r.get("tag_name"), str) and TAG.fullmatch(r["tag_name"])]


def tag_key(tag):
    return tuple(map(int, tag[1:].split(".")))


def verify_squash(api, merge_sha, head, base):
    commit = api.request("GET", f"git/commits/{merge_sha}")
    source = api.request("GET", f"git/commits/{head}")
    if (len(commit["parents"]) != 1 or commit["parents"][0]["sha"] != base
            or source["tree"]["sha"] != commit["tree"]["sha"]):
        raise GateError("Merged tree or base differs from the approved squash preflight.")
    comparison = api.request("GET", f"compare/{merge_sha}...{main_sha(api)}")
    if comparison["merge_base_commit"]["sha"] != merge_sha:
        raise GateError("Release commit is not on main.")


def release_plan(api, *, number=None, head=None, base=None, merge_sha=None, tag=None, emit=True):
    if tag and (not isinstance(tag, str) or not TAG.fullmatch(tag)):
        raise GateError("Recovery requires an exact vX.Y tag.")
    ref = api.request("GET", f"git/ref/tags/{tag}", missing=True) if tag else None
    if ref:
        tagged = peel(api, ref)
        if merge_sha and full_sha(merge_sha) != tagged:
            raise GateError("Existing edition tag points to another commit; never move it.")
        merge_sha = tagged
    if not number:
        if not merge_sha:
            raise GateError("Provide approved PR provenance or an existing edition tag.")
        merge_sha = full_sha(merge_sha)
        associated = api.pages(f"commits/{merge_sha}/pulls")
        matches = [p for p in associated if p.get("merged_at") and p["merge_commit_sha"] == merge_sha]
        if len(matches) != 1:
            raise GateError("New tag publication requires one approved, merged content PR.")
        number = matches[0]["number"]
    pr, actual_head, actual_base = candidate(
        api, int(number), expected_head=head, expected_base=base, checks=True,
    )
    merge_sha = full_sha(merge_sha or pr.get("merge_commit_sha"))
    if not pr.get("merged") or pr["merge_commit_sha"] != merge_sha:
        raise GateError("Release SHA is not this PR's exact merge commit.")
    verify_squash(api, merge_sha, actual_head, actual_base)
    expected_tag = edition_tag(api, merge_sha)
    if (tag and tag != expected_tag) or edition_tag(api, actual_head) != expected_tag:
        raise GateError("Tag does not match the edition at the approved merge.")
    tag = expected_tag
    ref = api.request("GET", f"git/ref/tags/{tag}", missing=True)
    if ref and peel(api, ref) != merge_sha:
        raise GateError("Existing edition tag points to another commit; never move it.")
    existing = find_release(api, tag)
    recovery = "false"
    if ref and not existing:
        raise GateError("Existing edition tag has no complete published release; no recovery writes allowed.")
    if existing and (not ref or existing.get("prerelease") is not False):
        raise GateError("Existing release has no matching stable edition tag.")
    if existing and existing["draft"]:
        raise GateError("Existing draft release is incomplete; no recovery writes allowed.")
    if existing and not existing["draft"]:
        assets = api.pages(f"releases/{existing['id']}/assets")
        if not uploaded_pdf(assets, tag):
            raise GateError("Published release is incomplete; immutable assets were not overwritten.")
        recovery = "true"
    plan = {"merge_sha": merge_sha, "head": actual_head, "base": actual_base,
            "pr": str(number), "tag": tag, "recovery": recovery}
    if emit:
        output(plan)
    return plan


def publish(api, tag, sha, pdf, notes):
    if not isinstance(tag, str) or not TAG.fullmatch(tag):
        raise GateError("Invalid edition tag.")
    full_sha(sha)
    plan = release_plan(api, merge_sha=sha, tag=tag, emit=False)
    if plan["recovery"] == "true":
        print("Existing published edition preserved.")
        output({"published": "false"})
        return
    if not pdf or not os.path.isfile(pdf) or os.path.getsize(pdf) <= 5:
        raise GateError("Missing or empty PDF artifact.")
    with open(pdf, "rb") as handle:
        if handle.read(5) != b"%PDF-":
            raise GateError("Artifact is not a PDF.")
    if os.path.basename(pdf) != f"apm-book-{tag}.pdf":
        raise GateError("PDF filename must match the edition asset name.")
    if not notes or not os.path.isfile(notes) or not os.path.getsize(notes):
        raise GateError("Missing release notes.")
    existing = find_release(api, tag)
    if existing:
        raise GateError("Release appeared during preparation; rerun the read-only plan.")
    ref = api.request("GET", f"git/ref/tags/{tag}", missing=True)
    if ref:
        if peel(api, ref) != sha:
            raise GateError("Existing edition tag points to another commit; never move it.")
        raise GateError("Edition tag appeared during preparation; no recovery writes allowed.")
    annotation = api.request("POST", "git/tags", {"tag": tag, "message": tag,
                                                 "object": sha, "type": "commit"})
    api.request("POST", "git/refs", {"ref": f"refs/tags/{tag}", "sha": full_sha(annotation["sha"])})
    executable = os.environ.get("BOOK_RELEASE_GH", "gh")

    def gh(*args):
        subprocess.run([executable, "release", *args, "--repo", api.repo], check=True, timeout=120)

    gh("create", tag, "--verify-tag", "--draft", "--latest=false",
       "--title", f"Book {tag}", "--notes-file", notes)
    gh("upload", tag, pdf)
    existing = find_release(api, tag)
    if not existing or not existing["draft"]:
        raise GateError("Draft disappeared or was published concurrently; nothing overwritten.")
    if not uploaded_pdf(api.pages(f"releases/{existing['id']}/assets"), tag):
        raise GateError("PDF upload is incomplete; release remains a draft.")
    ref = api.request("GET", f"git/ref/tags/{tag}", missing=True)
    if not ref or peel(api, ref) != sha:
        raise GateError("Edition tag changed before publication.")
    newest = all(tag_key(r["tag_name"]) <= tag_key(tag) for r in stable_releases(api.pages("releases")))
    gh("edit", tag, "--draft=false", f"--latest={'true' if newest else 'false'}")
    output({"published": "true"})


def deployment_failure(run, jobs, run_id):
    """Explain why the exact deploy run does not prove deployment plus smoke success."""
    if run.get("conclusion") != "success":
        return f"run concluded {run.get('conclusion')!r}"
    if not isinstance(jobs, dict) or not isinstance(jobs.get("jobs"), list):
        return "job list is missing"
    if len(jobs["jobs"]) != jobs.get("total_count"):
        return "job list is incomplete"
    deploy = [j for j in jobs["jobs"] if isinstance(j, dict) and j.get("name") == DEPLOY_JOB]
    if len(deploy) != 1 or deploy[0].get("run_id") != run_id:
        return f"exactly one '{DEPLOY_JOB}' job is required"
    if deploy[0].get("status") != "completed" or deploy[0].get("conclusion") != "success":
        return f"'{DEPLOY_JOB}' job concluded {deploy[0].get('conclusion')!r}"
    steps = deploy[0].get("steps") if isinstance(deploy[0].get("steps"), list) else []
    for name in DEPLOY_STEPS:
        matches = [s for s in steps if isinstance(s, dict) and s.get("name") == name]
        if len(matches) != 1 or matches[0].get("status") != "completed" or matches[0].get("conclusion") != "success":
            return f"step '{name}' did not succeed"
    return None


def deliver(api, tag, sha, *, wait_seconds=DEPLOY_WAIT_SECONDS, poll_seconds=15):
    """Deploy a newly published edition only if it is the highest published stable edition."""
    if not isinstance(tag, str) or not TAG.fullmatch(tag):
        raise GateError("Invalid edition tag.")
    if not (0 < wait_seconds < float("inf") and 0 < poll_seconds < float("inf")):
        raise GateError("Deployment wait and poll intervals must be positive.")
    plan = release_plan(api, merge_sha=full_sha(sha), tag=tag, emit=False)
    if plan["recovery"] != "true":
        raise GateError("Edition is not a complete published release; nothing deployed.")
    newest = max(stable_releases(api.pages("releases")), key=lambda r: tag_key(r["tag_name"]), default=None)
    if not newest or newest["tag_name"] != tag:
        current = newest["tag_name"] if newest else "none"
        print(f"::notice title=Production not rolled back::{tag} is older than the highest published "
              f"stable edition {current}; no deployment was dispatched. Roll back deliberately with "
              f"gh workflow run {DEPLOY_WORKFLOW} -f ref={tag}")
        output({"deployment": "skipped", "run_id": "", "run_url": ""})
        return
    # Dispatch exactly once; an uncertain dispatch is never retried or matched to a recent run.
    dispatched = api.request("POST", f"actions/workflows/{DEPLOY_WORKFLOW}/dispatches",
                             {"ref": "main", "inputs": {"ref": tag}}, version=DISPATCH_API_VERSION)
    run_id = dispatched.get("workflow_run_id") if isinstance(dispatched, dict) else None
    if type(run_id) is not int or run_id <= 0:
        raise GateError("Deployment dispatch returned no workflow run ID; not guessing a run. "
                        "Inspect Actions before any manual deployment.")
    url = dispatched.get("html_url") if isinstance(dispatched.get("html_url"), str) else ""
    print(f"Waiting for {DEPLOY_WORKFLOW} run {run_id} {url}".rstrip())
    deadline = time.monotonic() + wait_seconds

    def remaining_wait():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise GateError(f"Deployment run {run_id} did not finish within {wait_seconds} seconds; "
                            f"{tag} is not confirmed live.")
        return remaining

    while True:
        remaining_wait()
        run = api.request("GET", f"actions/runs/{run_id}")
        remaining = remaining_wait()
        if (not isinstance(run, dict) or run.get("id") != run_id
                or run.get("path") != f".github/workflows/{DEPLOY_WORKFLOW}"
                or run.get("event") != "workflow_dispatch" or run.get("head_branch") != "main"):
            raise GateError(f"Run {run_id} is not the dispatched {DEPLOY_WORKFLOW} run on main.")
        if run.get("status") == "completed":
            break
        time.sleep(min(poll_seconds, remaining))
    jobs = api.request("GET", f"actions/runs/{run_id}/jobs?filter=latest&per_page=100")
    failure = deployment_failure(run, jobs, run_id)
    if failure:
        raise GateError(f"Deployment run {run_id} did not deliver {tag}: {failure}.")
    remaining_wait()
    output({"deployment": "success", "run_id": str(run_id), "run_url": url})


def deploy_plan(api, *, sha=None, ref=None):
    """Resolve a published edition without imposing new provenance rules on old releases."""
    if bool(sha) == bool(ref):
        raise GateError("deploy-plan requires exactly one of --sha or --ref.")
    if sha:
        sha = full_sha(sha)
        if main_sha(api) != sha:
            raise GateError("Push SHA is not the exact current main commit.")
    elif not (isinstance(ref, str) and (TAG.fullmatch(ref) or SHA.fullmatch(ref))):
        raise GateError("Manual deployment requires a released vX.Y tag or full commit SHA.")
    releases = stable_releases(api.pages("releases"))
    if sha:
        selected = max(releases, key=lambda r: tag_key(r["tag_name"]), default=None)
        if not selected:
            print("No published stable edition is available for main deployment.", file=sys.stderr)
            output({"eligible": "false", "sha": sha, "tag": ""})
            return
    else:
        matches = []
        for item in releases:
            if TAG.fullmatch(ref):
                if item["tag_name"] == ref:
                    matches.append(item)
            else:
                tagged = peel(api, api.request("GET", f"git/ref/tags/{item['tag_name']}"))
                if tagged == ref:
                    matches.append(item)
        if not matches:
            raise GateError("Ref is not a published non-draft stable edition.")
        selected = max(matches, key=lambda r: tag_key(r["tag_name"]))
    tag = selected["tag_name"]
    if sum(r["tag_name"] == tag for r in releases) != 1:
        raise GateError("Ambiguous published edition tag.")
    tagged = peel(api, api.request("GET", f"git/ref/tags/{tag}"))
    if not sha and SHA.fullmatch(ref) and tagged != ref:
        raise GateError("Edition tag moved during deployment planning.")
    eligible = True
    if sha:
        comparison = api.request("GET", f"compare/{tagged}...{sha}")
        if (comparison["merge_base_commit"]["sha"] != tagged
                or comparison.get("status") not in {"ahead", "identical"}):
            raise GateError("Published edition is not an ancestor of current main.")
        files = comparison.get("files")
        # GitHub's comparison API returns at most 300 files, even when commits are paginated.
        if (not isinstance(files, list) or len(files) >= 300
                or comparison.get("truncated") or comparison.get("files_truncated")
                or ("total_files" in comparison and comparison["total_files"] != len(files))):
            raise GateError("Comparison file list may be truncated; deployment denied.")
        for item in files:
            for path in (item.get("filename"), item.get("previous_filename", item.get("filename"))):
                if not safe_path(path):
                    raise GateError("Comparison contains an invalid path.")
                if allowed_path(path):
                    eligible = False
        if not eligible:
            print(f"Main contains book content different from published {tag}; no deployment.",
                  file=sys.stderr)
        if main_sha(api) != sha:
            raise GateError("Main moved during deployment planning.")
    current = find_release(api, tag)
    if (not current or current["id"] != selected["id"]
            or not stable_releases([current])
            or peel(api, api.request("GET", f"git/ref/tags/{tag}")) != tagged):
        raise GateError("Published edition changed during deployment planning.")
    if sha:
        latest = max(stable_releases(api.pages("releases")),
                     key=lambda r: tag_key(r["tag_name"]), default=None)
        if not latest or latest["tag_name"] != tag:
            raise GateError("Latest published edition changed during deployment planning.")
    output({"eligible": str(eligible).lower(), "sha": sha or tagged, "tag": tag})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["inspect", "merge", "release-plan", "publish",
                                              "deliver", "deploy-plan"])
    parser.add_argument("--event")
    parser.add_argument("--pr", type=int)
    parser.add_argument("--head")
    parser.add_argument("--base")
    parser.add_argument("--merge-sha")
    parser.add_argument("--tag")
    parser.add_argument("--pdf")
    parser.add_argument("--notes")
    parser.add_argument("--sha")
    parser.add_argument("--ref")
    parser.add_argument("--wait-seconds", type=float, default=DEPLOY_WAIT_SECONDS)
    parser.add_argument("--poll-seconds", type=float, default=15)
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
        elif args.operation == "deploy-plan":
            deploy_plan(api, sha=args.sha, ref=args.ref)
        elif args.operation == "deliver":
            deliver(api, args.tag, args.merge_sha,
                    wait_seconds=args.wait_seconds, poll_seconds=args.poll_seconds)
        else:
            publish(api, args.tag, args.merge_sha, args.pdf, args.notes)
    except (APIError, GateError, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        if args.operation == "deploy-plan":
            output({"eligible": "false", "sha": "", "tag": ""})
        print(f"book release: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
