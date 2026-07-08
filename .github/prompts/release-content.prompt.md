---
description: Cut a new versioned edition of the book CONTENT and publish it as a GitHub Release (vX.Y tag → site + PDF + release notes).
---

# Release a content edition

Publish a new edition of the **book content** as a GitHub Release. The content is versioned
independently of the site tooling, so **only content changes bump the number** — build scripts,
analytics, styling, and other infrastructure never do.

**New edition:** <X.Y, e.g. 1.2 — bump the minor for new/revised chapters, the major for a rewrite>
**Date:** <YYYY-MM-DD, defaults to today>
**What changed (content only):** <1–3 bullets describing chapter additions/edits; omit tooling changes>

## Guardrails
- **Content-only.** If the changes since the last edition are purely tooling/infra, there is nothing
  to release — say so and stop. A release must correspond to a real change in the chapters a reader sees.
- **One source of truth.** The edition shown on the site, in the JSON-LD, in `llms.txt`, and on the
  PDF all come from `content/version.yml`. Never hand-edit those outputs — bump the source and rebuild.
- **Tag must equal the file version.** The `vX.Y` tag and `content/version.yml` must match, or the
  release workflow emits a warning and the notes won't line up.

## Steps

1. **Confirm the version story.** Check the latest tag and the top of
   [`content/CHANGELOG.md`](../../content/CHANGELOG.md); pick the next `X.Y` (minor for content
   additions/corrections, major for a restructuring/rewrite). Verify the changes being released are
   content, not tooling.

2. **Bump the source of truth** — [`content/version.yml`](../../content/version.yml):
   set `version: "X.Y"` and `date: "YYYY-MM-DD"`.

3. **Record the changes** — add a new section at the **top** of the change list in
   [`content/CHANGELOG.md`](../../content/CHANGELOG.md), matching the existing Keep-a-Changelog format:
   ```
   ## [X.Y] — YYYY-MM-DD

   ### Added
   - <what a reader gains in this edition>
   ### Changed / Fixed   (only the subsections that apply)
   - <...>
   ```
   The header format matters: `extract_release_notes.py` slices the release notes from the section
   whose header is `## [X.Y] …`, up to the next `## [` .

4. **Preview the release notes** that the workflow will publish:
   ```powershell
   python site/extract_release_notes.py X.Y
   ```
   It should print exactly your new changelog section. Fix the heading if nothing prints.

5. **Build + verify locally** (optional but recommended) so the edition renders before you tag:
   ```powershell
   $env:APM_PDF_REQUIRED = "1"; python site/generate.py
   ```
   Confirm `Edition vX.Y` appears on the home hero, a page footer, and the PDF cover
   (`site/apm-book.pdf`). The versioned `apm-book-vX.Y.pdf` is produced by CI, not locally.

6. **Commit, tag, and push** — pushing the tag is what triggers the release:
   ```powershell
   git commit -am "content: vX.Y — <short summary>"
   git tag vX.Y
   git push origin main --tags
   ```
   (Do this from the branch/PR that carries the content change once it's merged to `main`, so the
   tag points at the published content.)

7. **Let the automation finish.** Pushing `vX.Y` runs
   [`release-content.yml`](../../.github/workflows/release-content.yml), which rebuilds the site +
   PDF, turns the changelog section into the notes, and creates the **Book vX.Y** Release with
   `apm-book-vX.Y.pdf` attached.

8. **Verify the release:**
   ```powershell
   gh release view vX.Y --repo webmaxru/agent-package-manager-book
   ```
   Confirm the notes render and the PDF asset is attached. Mark the newest content edition as
   `--latest` if it isn't already.

## Re-running / fixing a release
- To rebuild an **existing** tag's release (e.g. after tweaking the changelog on `main`), trigger the
  workflow manually instead of retagging: **Actions → "Publish content release" → Run workflow**, and
  pass the tag (e.g. `v1.2`). Re-running updates the release and re-uploads the PDF in place.
- Only editing `.github/workflows/release-content.yml` itself requires a token with the `workflow`
  scope; tagging content and publishing releases do not.
