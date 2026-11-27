"""Bound Actions storage without executing or downloading producer artifacts."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import sys
import urllib.error

from book_release import APIError, GateError, GitHub, find_release, release_plan, uploaded_pdf

PREVIEW = re.compile(r"book-preview-v1-(\d+)-([0-9a-f]{64})-(\d+)-(\d+)\Z")


def positive_id(value):
    if isinstance(value, bool) or not re.fullmatch(r"[1-9][0-9]*", str(value)):
        raise GateError("Missing or invalid Actions identity.")
    return int(value)


def ref_hash(ref):
    if not isinstance(ref, str) or not ref.startswith(("refs/heads/", "refs/tags/")):
        raise GateError("Preview requires a full branch or tag ref.")
    return hashlib.sha256(ref.encode("utf-8")).hexdigest()


def preview_name(repo_id, ref, run_id, attempt):
    return (f"book-preview-v1-{positive_id(repo_id)}-{ref_hash(ref)}-"
            f"{positive_id(run_id)}-{positive_id(attempt)}")


def collection(api, path, key):
    result = []
    for page in range(1, 1001):
        response = api.request("GET", f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        batch = response.get(key) if isinstance(response, dict) else None
        if not isinstance(batch, list) or type(response.get("total_count")) is not int:
            raise GateError(f"Invalid {key} collection.")
        result.extend(batch)
        if len(batch) < 100:
            if len(result) != response["total_count"]:
                raise GateError(f"Incomplete or changing {key} collection; retaining artifacts.")
            return result
    raise GateError(f"Pagination limit exceeded for {key}.")


def run(api, run_id, workflow, *, attempt=None):
    path = f"actions/runs/{positive_id(run_id)}"
    if attempt is not None:
        path += f"/attempts/{positive_id(attempt)}"
    value = api.request("GET", path)
    if (value.get("id") != run_id or value.get("path") != f".github/workflows/{workflow}"
            or value.get("event") != "workflow_dispatch"
            or (value.get("repository") or {}).get("full_name") != api.repo
            or (value.get("head_repository") or {}).get("full_name") != api.repo):
        raise GateError("Artifact producer does not match the trusted workflow/repository.")
    positive_id(value.get("run_attempt"))
    positive_id(value.get("workflow_id"))
    if attempt is not None and value["run_attempt"] != attempt:
        raise GateError("Artifact producer attempt does not match the requested attempt.")
    return value


def artifact_identity(artifact, producer, *, name=None):
    metadata = artifact.get("workflow_run") or {}
    if (type(artifact.get("id")) is not int or artifact["id"] <= 0
            or artifact.get("expired") is not False
            or metadata.get("id") != producer["id"]
            or metadata.get("repository_id") != producer["repository"]["id"]
            or metadata.get("head_repository_id") != producer["repository"]["id"]
            or metadata.get("head_branch") != producer.get("head_branch")
            or metadata.get("head_sha") != producer.get("head_sha")
            or (name is not None and artifact.get("name") != name)):
        raise GateError("Artifact identity/producer metadata is missing or changed.")


def created(artifact):
    try:
        stamp = datetime.datetime.fromisoformat(artifact["created_at"].replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("timezone missing")
        return stamp
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise GateError("Artifact creation time is invalid.") from error


def preview_identity(artifact, producer):
    match = PREVIEW.fullmatch(artifact.get("name", ""))
    if not match:
        raise GateError("Missing versioned preview identity.")
    repo_id, digest, run_id, attempt = match.groups()
    artifact_identity(artifact, producer)
    if (int(repo_id) != producer["repository"]["id"] or int(run_id) != producer["id"]
            or int(attempt) != producer["run_attempt"]
            or digest not in {ref_hash(f"refs/{kind}/{producer['head_branch']}")
                              for kind in ("heads", "tags")}):
        raise GateError("Preview namespace does not match its producing run/full ref.")
    return repo_id, digest, int(run_id), int(attempt)


def completed(producer, *, success=False):
    return producer.get("status") == "completed" and (
        not success or producer.get("conclusion") == "success")


def preview_uploaded(api, producer):
    jobs = collection(api, f"actions/runs/{producer['id']}/attempts/"
                      f"{producer['run_attempt']}/jobs", "jobs")
    matches = [j for j in jobs if j.get("name") == "preflight (ubuntu-24.04)"]
    if (len(matches) != 1 or matches[0].get("run_id") != producer["id"]
            or matches[0].get("run_attempt") != producer["run_attempt"]
            or not completed(matches[0], success=True)):
        raise GateError("Missing successful current-attempt preview job evidence; nothing deleted.")
    steps = matches[0].get("steps") or []
    uploads = [s for s in steps if s.get("name") == "Upload PDF preview"]
    if (len(uploads) != 1 or uploads[0].get("status") != "completed"
            or uploads[0].get("conclusion") not in {"success", "skipped"}):
        raise GateError("Missing successful/skipped current-attempt preview upload evidence; nothing deleted.")
    return uploads[0]["conclusion"] == "success"


def cleanup_preview(api, run_id):
    replacement_run = run(api, run_id, "ci.yml")
    if not completed(replacement_run, success=True):
        raise GateError("Replacement run has not completed successfully; nothing deleted.")
    if not preview_uploaded(api, replacement_run):
        print("::notice::Current-attempt preview upload was skipped; nothing deleted.")
        return
    artifacts = collection(api, f"actions/runs/{run_id}/artifacts", "artifacts")
    names = {preview_name(replacement_run["repository"]["id"],
                          f"refs/{kind}/{replacement_run['head_branch']}",
                          run_id, replacement_run["run_attempt"])
             for kind in ("heads", "tags")}
    matches = [a for a in artifacts if a.get("name") in names]
    if not matches:
        raise GateError("Missing replacement preview after successful current-attempt upload; nothing deleted.")
    if len(matches) != 1:
        raise GateError("Ambiguous replacement preview; nothing deleted.")
    replacement = matches[0]
    identity = preview_identity(replacement, replacement_run)
    replacement_time = created(replacement)
    candidates = collection(api, "actions/artifacts", "artifacts")
    for candidate in candidates:
        match = PREVIEW.fullmatch(candidate.get("name", ""))
        if (not match or match.groups()[:2] != identity[:2]
                or candidate.get("expired") is not False
                or candidate.get("id", replacement["id"]) == replacement["id"]
                or tuple(map(int, match.groups()[2:])) >= identity[2:]
                or created(candidate) > replacement_time):
            continue
        producer = run(api, int(match[3]), "ci.yml")
        if (producer["workflow_id"] != replacement_run["workflow_id"]
                or producer.get("head_branch") != replacement_run.get("head_branch")
                or not completed(producer) or producer["run_attempt"] < int(match[4])):
            continue
        attempt = (producer if producer["run_attempt"] == int(match[4]) else
                   run(api, producer["id"], "ci.yml", attempt=int(match[4])))
        if not completed(attempt) or attempt["workflow_id"] != producer["workflow_id"]:
            continue
        preview_identity(candidate, attempt)
        # Re-read both producers and exact IDs immediately before deletion, never just names.
        fresh_replacement = api.request("GET", f"actions/artifacts/{replacement['id']}")
        fresh_run = run(api, run_id, "ci.yml")
        if (fresh_replacement != replacement or fresh_run != replacement_run
                or not completed(fresh_run, success=True)):
            raise GateError("Replacement changed during cleanup; retaining remaining previews.")
        fresh = api.request("GET", f"actions/artifacts/{candidate['id']}")
        current = run(api, producer["id"], "ci.yml")
        if fresh != candidate or current != producer or not completed(current):
            print(f"::notice::Preview {candidate['id']} changed or is active; retained.")
            continue
        api.request("DELETE", f"actions/artifacts/{candidate['id']}")
        print(f"Deleted replaced preview artifact {candidate['id']}.")


def cleanup_release(api, run_id, artifact_id, tag, sha, digest):
    positive_id(artifact_id)
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise GateError("Missing expected PDF SHA-256; retaining staging.")
    producer = run(api, run_id, "release.yml")
    if (producer.get("head_branch") != "main"
            or producer["run_attempt"] != positive_id(os.environ["GITHUB_RUN_ATTEMPT"])):
        raise GateError("Staging cleanup must belong to this main release attempt.")
    artifact = api.request("GET", f"actions/artifacts/{artifact_id}")
    artifact_identity(artifact, producer, name=f"release-book-{sha}")
    jobs = collection(api, f"actions/runs/{run_id}/jobs?filter=latest", "jobs")
    for name in ("build", "publish", "deploy"):
        matches = [j for j in jobs if j.get("name") == name]
        if (len(matches) != 1 or matches[0].get("run_id") != run_id
                or matches[0].get("run_attempt") != producer["run_attempt"]
                or not completed(matches[0], success=True)):
            raise GateError(f"Release consumer {name} has not finished successfully; retaining staging.")
    plan = release_plan(api, merge_sha=sha, tag=tag, emit=False)
    if plan["recovery"] != "true":
        raise GateError("Publication is incomplete; retaining staging.")
    published = find_release(api, tag)
    if not published or published.get("draft") is not False or published.get("prerelease") is not False:
        raise GateError("Release is not published; retaining staging.")
    assets = api.pages(f"releases/{published['id']}/assets")
    expected = [a for a in assets if a.get("name") == f"apm-book-{tag}.pdf"]
    if (len(expected) != 1 or not uploaded_pdf(expected, tag)
            or expected[0].get("digest") != f"sha256:{digest}"):
        raise GateError("Published PDF integrity is not verified; retaining staging.")
    fresh = api.request("GET", f"actions/artifacts/{artifact_id}")
    current = run(api, run_id, "release.yml")
    if fresh != artifact or current["run_attempt"] != producer["run_attempt"]:
        raise GateError("Release staging changed during cleanup.")
    api.request("DELETE", f"actions/artifacts/{artifact_id}")
    print(f"Deleted verified release staging artifact {artifact_id}.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("preview-name", "preview", "release"))
    parser.add_argument("--run-id", type=int)
    parser.add_argument("--artifact-id", type=int)
    parser.add_argument("--tag")
    parser.add_argument("--merge-sha")
    parser.add_argument("--pdf-sha256")
    args = parser.parse_args(argv)
    try:
        if args.operation == "preview-name":
            print("name=" + preview_name(os.environ["GITHUB_REPOSITORY_ID"], os.environ["GITHUB_REF"],
                                         os.environ["GITHUB_RUN_ID"], os.environ["GITHUB_RUN_ATTEMPT"]))
        elif args.operation == "preview":
            cleanup_preview(GitHub(), positive_id(args.run_id))
        else:
            cleanup_release(GitHub(), positive_id(args.run_id), positive_id(args.artifact_id),
                            args.tag, args.merge_sha, args.pdf_sha256)
    except (APIError, GateError, KeyError, OSError, urllib.error.URLError) as error:
        print(f"::error::Artifact cleanup failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
