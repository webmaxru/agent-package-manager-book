---
description: Prepare a reviewed content edition, or explicitly publish its exact merged commit as a vX.Y GitHub Release with a versioned PDF.
---

# Release a content edition

Book editions version **reader-facing content**, independently of tooling and APM's own version.
Use `/update-book` first when upstream research and chapter changes are still needed.

## Inputs and boundary

- **Mode:** `prepare` by default. `publish` requires an explicit user request to publish.
- **Edition:** `X.Y`; minor for additions/corrections, major for a substantive restructuring.
- **Date:** `YYYY-MM-DD`, normally today.
- **Reviewed APM:** exact `X.Y.Z` from the completed verification, not whatever is on PATH.
- **Content changes:** reader-facing additions/fixes only.

Prepare means local files/commits only. It never merges, pushes, tags, creates a PR or release,
or dispatches a publishing workflow. A later owner approval on a qualifying content PR is the
explicit authorization for the automated merge and release.

## Prepare

1. **Establish the version story.** Read the latest published book release, local tags,
   `content/version.yml`, `content/CHANGELOG.md`, and the actual chapter/TOC diff.
   Fetch missing remote tags without force if needed. Do not infer the book edition from
   `package.json`, root `apm.yml`, or the root skills lockfile.

2. **Require the content gates.** Read the actual verifier and reviewer reports for each affected
   chapter and the integration pass, normally in `content/research/updates/<edition>/`.
   Every affected example must PASS or have a specific, visibly documented
   `SKIPPED-needs-network` reason; every chapter and integration review must ACCEPT.
   Check that reports cover the current inputs and exact target. No reports or stale reports
   means not ready, even if CI is green. Never invent verdicts. Tooling-only changes need no
   edition and must not be released as one. Produce `commit-binding.json` as documented in
   `scripts/README.md#edition-evidence`; bind the actual reviewed source and report blobs and
   enumerate the real example outcomes. Run `python .\site\validate_evidence.py --base-ref <base>`.

3. **Update the source metadata together:** edition, date, and reviewed `apm_version` in
   `content/version.yml`. Preserve the previous baseline until verification is complete.
   Add a matching top section to `content/CHANGELOG.md`:
   ```markdown
   ## [X.Y] - YYYY-MM-DD

   ### Changed
   - Reader-facing change and affected chapters.
   ```
   Match the existing style; the ASCII hyphen and existing em dash are both supported.
   Keep all previous edition entries. Mention the reviewed APM range where relevant.

4. **Run strict preflight and preview notes.** Substitute the real previous book tag:
   ```powershell
   python .\site\validate_release.py --base-ref v1.1
   python .\site\extract_release_notes.py 1.2
   ```
   Stop on a nonzero exit code. Missing/empty/duplicate notes, malformed metadata, mismatched
   dates, a content change without a version bump, or a tooling-only bump are errors, not warnings.

5. **Require a fresh HTML build and release PDF:**
   ```powershell
   python .\site\generate.py
   if ($LASTEXITCODE -ne 0) { throw "Book HTML build failed" }
   python .\site\generate_pdf.py
   if ($LASTEXITCODE -ne 0) { throw "Release PDF build failed" }
   ```
   If required dependencies are missing, install the documented Python/Playwright toolchain
   and rerun. Confirm the intended edition/date on the home hero, a chapter footer, and the
   PDF cover; check affected links/navigation. Never hand-edit generated version labels.

6. **Checkpoint locally.** Stage only reviewed source, examples, reports, metadata, and generated
   tracked output belonging to this update; include new files, not just `git commit -am`.
   Preserve unrelated work. Commit with the required co-author trailer. Report the prepared
   edition, upstream range, evidence, skips, and commit. In `prepare` mode, stop here.

## Approve and publish

1. Open a same-repository content-only PR targeting `main` when explicitly requested. Require
   **Book release preflight** and the actual editorial evidence. The owner `webmaxru` approves
   another author's PR through a GitHub review. Since GitHub does not allow author self-review,
   an owner-authored PR requires the exact owner comment `/release-book <full-head-sha>`.
   New commits invalidate approval. Do not authorize mixed workflow/tooling changes.

2. **Release approved book** rechecks the owner approval, PR scope and exact head, runs
   read-only HTML/PDF/evidence preflight, then SHA-conditionally squash-merges and explicitly
   dispatches **Publish content release**. The publisher verifies the exact merged tree,
   builds before creating the immutable `vX.Y` tag, uploads the PDF to a draft release, publishes
   and explicitly dispatches Pages. Tag pushes themselves do not publish. Never move a tag.

3. Confirm both completed successfully, inspect the live edition and PDF, and inspect:
   ```powershell
   gh release view v1.2 --repo webmaxru/agent-package-manager-book --json tagName,body,assets,url
   ```
   Confirm the exact tag, changelog notes, and versioned PDF asset. Only mark a release latest
   when it really is the newest content edition; rerunning an old edition must not promote it.

## Reruns and historical editions

- To retry before merge, dispatch **Release approved book** with the PR number. After merge,
  dispatch **Publish content release** with the PR number and exact merge SHA, or use the existing
  exact `vX.Y` tag. Recovery requires the same approved merged provenance; a published release
  is a successful no-op only if its versioned PDF is present. Releases lacking provenance or
  the PDF fail explicitly and are left unchanged.
- Correcting published content or its source changelog requires a **new edition and new tag**.
  Do not retag a public edition or replace its PDF with content from another commit.
- Historical `v1.0` and `v1.1` were published before version metadata/release tooling existed at
  those tags. Preserve their existing assets; they are comparison baselines, not rebuildable
  inputs for this workflow. Do not fake missing metadata to make a historical rerun green.
- Editing workflow files may require the token's workflow permission. Never change credentials
  or weaken these checks to get a release through.
