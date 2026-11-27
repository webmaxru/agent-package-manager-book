# Releasing *Agent Package Manager: An Interactive Book*

A release is a Git tag `vX.Y` on the merge commit of an **owner-approved, content-only pull request**, with a GitHub Release carrying `apm-book-vX.Y.pdf`. Nothing else publishes: not a push, a tag, a label or a manual merge.

```text
/update-book ─► /release-content ─► content PR ─► Book release preflight (green)
        ─► owner approval of the exact head ─► Release approved book: squash merge
        ─► Publish content release: tag, draft + PDF, publish ─► GitHub Pages: apm.isainative.dev
```

The sections below explain each step. [Scenarios](#scenarios-what-to-do-when) walks through the situations you will actually meet, with commands. The tooling behind this page is documented in the [README](README.md#versioning--releases) ([update from an APM release](README.md#update-from-an-apm-release), [prepare, approve, then publish](README.md#prepare-approve-then-publish)) and in [`scripts/README.md`](scripts/README.md) ([state, evidence and release boundary](scripts/README.md#state-evidence-and-release-boundary), [edition evidence](scripts/README.md#edition-evidence)).

## Prepare the edition

Run [`/update-book`](.github/prompts/update-book.prompt.md) to follow an APM release (add `Mode: check` for a read-only impact report), or make the chapter edits yourself. Then run [`/release-content`](.github/prompts/release-content.prompt.md): it updates the edition and the CHANGELOG, requires a fresh HTML and PDF build, and commits locally. Review the result and open a content PR against `main`.

Only reader-visible chapter prose and meaningful TOC changes justify a new edition. Research, examples under `backend/`, build scripts and styling alone do not.

| Increment | When to use it |
| --- | --- |
| Major (`2.0`) | Structural rewrite or reordering of the book. |
| Minor (`1.3`) | Every other reader-visible update: new material, a refresh for a new APM release, corrections. |

Editions are `major.minor`, with no patch level. The edition lives in [`content/version.yml`](content/version.yml) next to the date and `apm_version`, the APM release the chapters were reviewed against. The book's `1.2` and APM's `0.31.0` are independent numbers. Changing `apm_version` needs a new edition, and it cannot go backwards.

**Book release preflight** (the **Check book update** workflow) is the gate. It runs the tooling tests on Linux and Windows, checks the edition, CHANGELOG and evidence, regenerates the site and builds the PDF. For a content PR:

- Change only [`content/`](content) (`version.yml`, `CHANGELOG.md`, `toc.yml`, `chapters/`, `research/`), `backend/examples/` and the generated site files (`site/index.html`, `site/chapters/*.html`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`, `site.webmanifest`). Anything else is tooling and belongs in a separate PR with no version bump.
- Set the edition above the one on `main` and add a matching `## [X.Y] - YYYY-MM-DD` section at the **top** of `content/CHANGELOG.md`. The checks fail in these cases:

  | You did | Preflight says |
  | --- | --- |
  | Edited a chapter, no bump | `Reader-facing content changed without a new edition: content/chapters/<file>.html` |
  | Bumped `version.yml`, no CHANGELOG entry | `The first released CHANGELOG entry must match content/version.yml.` |
  | Bumped and added a CHANGELOG entry, no chapter or TOC change | `Edition bumps require chapter or TOC changes, not only tooling or metadata.` |
  | No evidence for the edition | `evidence preflight: Cannot read edition evidence: …` |

- Add the evidence. Under `content/research/updates/<edition>/`, keep an `integration-review.md` (`Verdict: ACCEPT`), a `chNN-review.md` (`Verdict: ACCEPT`) and a `chNN-verification.md` (`Verdict: PASS`) for every changed chapter, each naming the `apm_version`, and a `commit-binding.json` that lists the affected chapters, every example result (or a reason there are none) and the Git blob ID of every changed chapter, TOC and example file and of every report. Get an ID with `git hash-object -- <path>`. The format is in [`scripts/README.md`](scripts/README.md#edition-evidence). **Any edit to a bound file afterwards needs a new binding.** The check proves the files exist, match the binding and carry the verdicts. It does not judge whether the prose or examples are right. You do.

## Authorize and publish

For someone else's non-draft PR, **webmaxru** submits an **Approve** review on its current head. For an owner-authored PR, post exactly `/release-book <full lowercase 40-character head SHA>` in a new PR conversation comment. An older SHA, another user's comment, or approval superseded by requested changes or dismissal does not count. A new commit needs new approval. Approving before the checks finish is fine: the controller waits for them.

The controller, **Release approved book**, runs on `main` with its own trusted validators. It reacts to the review or comment, to the completion of **Check book update**, to a scan of up to 30 recently updated open PRs every 30 minutes, and to **Run workflow → pr**. None of those triggers grants approval. It requires a non-draft, same-repository PR against `main` whose files are all on the content allowlist, a head that already contains the current `main`, and a successful **Check book update** run for exactly that head. It then repeats the preflight on its own build of the head, including the PDF, and merges with a **squash** that is conditional on the approved head. If `main` moved in the meantime it stops with `Main advanced during preflight; update the branch and approve again.`

Publication is a separate dispatch from the controller, because a merge made with `GITHUB_TOKEN` does not trigger other workflows. **Publish content release** receives the PR, head, base and merge SHAs and proves that the merge commit is the PR's merge on `main`, with the approved tree. It rebuilds the book from that commit, creates the tag `vX.Y` there, uploads `apm-book-vX.Y.pdf` to a **draft** release, publishes it, and marks it Latest only if no newer stable release exists. It then dispatches **Deploy book to GitHub Pages** for the merge commit. The website keeps its Substack gate in front of the PDF, so the PDF is downloaded from the GitHub release.

The repository has no branch protection or ruleset, so nothing enforces this gate: **manual merges bypass it**.

## Recovery and corrections

Pushing a tag no longer publishes. If the merge succeeded but publication failed, dispatch **Publish content release** for that merged PR. It rechecks the approval and provenance, and never moves a tag or overwrites a published file:

```sh
gh workflow run release-content.yml -f pr=N -f merge_sha=$(gh pr view N --json mergeCommit --jq .mergeCommit.oid)
```

| State found | What recovery does |
| --- | --- |
| Release published with the PDF | Nothing to do (no-op): `Existing published edition preserved.` |
| No tag | Creates the tag at the merge commit, then a draft, uploads the PDF, publishes. |
| Tag but no release, or a draft | Creates or completes the draft, uploads the PDF, publishes. |
| Published release without the PDF | Stops without changes: `Published release is incomplete; do not overwrite immutable assets.` |
| Tag points to another commit | Stops: `Existing edition tag points to another commit; never move it.` |

If the tag already exists, `-f tag=vX.Y` selects it instead. It must match `content/version.yml` at the approved merge commit. Releases that predate this automation, `v1.0` and `v1.1`, have no approval provenance, so they fail closed and stay as they are.

A correction needs a **new edition**, not a rebuild. Never move a tag or replace a published PDF. See [scenarios 11–13](#11-the-release-failed-after-the-merge).

## Scenarios: what to do when

Commands use the [GitHub CLI](https://cli.github.com/) (`gh`) from a clone of this repository and work in bash and PowerShell. `N` is the pull request number and `vX.Y` a tag. Replace `v1.2` in examples with the latest published tag shown by `gh release list`.

### What triggers what

| Event | What happens | Release? |
| --- | --- | --- |
| PR opened or pushed | **Check book update** runs the tests, edition and evidence checks, site generation and the PDF build. Its **Book release preflight** job is the gate. | No |
| Owner **Approve** review, or an owner `/release-book <SHA>` comment | **Release approved book** re-checks everything and squash-merges the approved head. **Publish content release** follows. | Yes, a few minutes later |
| **Check book update** finishes, or the 30-minute scan | The controller looks for an approved PR it missed. It never approves anything itself. | Only if a valid approval exists |
| **Release approved book → Run workflow** with `pr` | Same re-check for one PR. | Only if a valid approval exists |
| **Publish content release → Run workflow** | Recovery for an already merged PR or an existing tag. | Completes a release, never overwrites one |
| Push a tag, add a label, press **Merge** | Nothing in the release flow. | **No** |
| Any push to `main` | **Deploy book to GitHub Pages** validates the edition against the previous `main` and redeploys the site. | No |
| A new APM release | Nothing. There is no scheduled scout: look yourself with `python scripts/check_upstream.py` or `/update-book` with `Mode: check`. | No |

### 1. Routine update (your own PR)

1. See whether the book is behind APM. Read-only, needs only Python and PyYAML:

   ```sh
   python scripts/check_upstream.py
   ```

   If a newer stable release changes something readers see, run `/update-book`, or make your chapter edits. Then run `/release-content`. Do the review loop and keep its reports under `content/research/updates/<edition>/`.
2. Check locally what CI will check (see also [Before you open any PR](#before-you-open-any-pr)):

   ```sh
   git fetch --tags
   python site/validate_release.py --base-ref origin/main
   python site/validate_evidence.py --base-ref origin/main
   python site/release_candidate.py --root .     # prints tag=vX.Y
   ```

3. Push and open the PR against `main`:

   ```sh
   git push -u origin content/my-update
   gh pr create --base main --title "Update for APM X.Y.Z" --body "See content/CHANGELOG.md."
   ```

4. Wait for **Book release preflight** (`gh pr checks N --watch`). Read the CHANGELOG entry and the reports yourself.
5. Authorize **the exact head**. You wrote the PR, so GitHub will not let you approve it. Comment instead:

   ```sh
   gh pr comment N --body "/release-book $(gh pr view N --json headRefOid --jq .headRefOid)"
   ```

6. Watch it go through, normally within a few minutes:

   ```sh
   gh run list --workflow approved-book.yml -L 3
   gh run list --workflow release-content.yml -L 3
   gh run watch <run-id>
   gh release view vX.Y
   ```

**Result:** the PR is squash-merged, `vX.Y` is a tag on the merge commit, the release has `apm-book-vX.Y.pdf`, it is Latest if it is the highest stable edition, and the website shows the new edition.

### 2. Someone else's PR on a branch in this repository

A collaborator with write access opens a content PR. This is the normal case for contributions.

1. Read the diff. The PR must be non-draft, target `main`, change only content files and pass **Book release preflight**. A contributor usually does not know about the edition bump, the CHANGELOG section and the evidence, so preflight fails until they exist. Add them to the contributor's branch yourself, after reviewing the edit:

   ```sh
   gh pr checkout N
   # edit content/version.yml and content/CHANGELOG.md; add content/research/updates/<edition>/
   git add -A && git commit -m "Prepare book edition X.Y" && git push
   ```

2. When preflight is green, submit an **Approve** review on the current head and stop there:

   ```sh
   gh pr review N --approve
   ```

**Do not press Merge.** A manual merge publishes nothing (scenario 9). The pushes in step 1 change the head, so approve after them, not before. The evidence must be bound after the contributor's last chapter edit.

### 3. A pull request from a fork

The controller only merges PRs whose head branch is in this repository (`Only same-repository, non-draft content PRs targeting main qualify.`), so a fork PR is refused. Re-create it on a branch here and keep the contributor's commits:

```sh
gh pr checkout N
git switch -c content/from-pr-N
git push -u origin content/from-pr-N
gh pr create --base main --head content/from-pr-N --title "<title>" --body "Supersedes #N"
```

You now own the new PR, so continue with scenario 1: add the edition bump, CHANGELOG and evidence, then comment `/release-book <SHA>`. Close the original PR with a thank-you.

### 4. A new push after approval, requested changes or a dismissed review

An approval counts only for the head it was given on. A push after approval, a **Request changes** review or a dismissed review voids it. Nothing merges until you approve again: a new **Approve** review, or a new `/release-book <SHA>` with the new head SHA. An old SHA in an old comment is ignored.

### 5. The branch is behind `main`

Being behind `main` stops the merge on its own, even with no conflict: the head must already contain the current `main`, or the controller refuses with `PR head is behind main; update it and obtain fresh approval.` Update the branch, wait for preflight on the new head, and approve again:

```sh
gh pr update-branch N
gh pr checks N --watch
gh pr review N --approve    # or comment /release-book <new SHA> on your own PR
```

### 6. Approved, but the PR is still open

Look at the latest **Release approved book** run. Its `authorize` job prints `PR N not eligible: <reason>` for every open PR it declined. Typical causes: a failing or still-running preflight, a head that moved after approval, a head behind `main`, a file outside the allowlist, or a run that was replaced in GitHub's concurrency queue. The scan covers only the 30 most recently updated PRs. Fix the cause, or run the controller for this PR:

```sh
gh workflow run approved-book.yml -f pr=N
```

If the run died within a second with no steps, see [Runs that fail without starting](#10-runs-that-fail-without-starting).

### 7. Tooling, docs and workflow changes

A PR that touches only files outside the content allowlist (`scripts/`, `site/` generator code, `.github/`, `README.md`, `RELEASING.md`, tests) is **tooling-only**. It needs no edition bump, and a bump with no chapter change fails the checks. It never releases: the controller refuses it (`Not an automatic content update: <path>`). Merge it yourself when the checks are green. The push to `main` redeploys the website with the new tooling.

### 8. Mixed content and tooling

A PR that changes both content and tooling gets the same `Not an automatic content update: <path>` refusal and is never merged by the controller. Split it into two PRs: tooling first (merged by you), then the content PR.

### 9. A manual merge by mistake

Pressing **Merge** on a content PR, or merging from the command line, bypasses the controller. The repository has no branch protection or ruleset, so GitHub allows it. The effects:

- **No tag, no release, no PDF.**
- The push to `main` still runs **Deploy book to GitHub Pages**, which validates the edition against the previous `main`. If the PR carried a valid bump and CHANGELOG entry, **the unreleased edition goes live on the website** while the downloads stay on the old one. If it did not, the deploy fails and the site keeps the previous edition, while the content sits on `main` waiting for the catch-up.
- The edition the PR carried is now on `main` unreleased. The next PR must be above it, so that version number is stranded.

Fix it with a **catch-up PR**. For example, if `main` carries edition `1.3` but the latest tag is `v1.2`:

1. Branch from `main`. The catch-up must contain a **real chapter or TOC change** (a correction, a clarified paragraph, an added cross-reference). A PR that only bumps the version and CHANGELOG fails with `Edition bumps require chapter or TOC changes, not only tooling or metadata.`
2. Set `version` in `content/version.yml` to `"1.4"`, above the stranded `1.3`. Keeping `1.3` fails with `Reader-facing content changed without a new edition`.
3. **Fold the stranded notes into the new CHANGELOG section.** Add `## [1.4] - YYYY-MM-DD`, move the `1.3` bullets under it and delete the `## [1.3]` heading, so the headings read `[1.4]`, `[1.2]`, and so on. The release build requires the entry after the new one to equal the latest published tag.

   > **Trap.** If you leave `## [1.3]` in place, the PR passes every preflight check and can be approved and merged. The release then fails in the **Publish content release** build with `The previous changelog edition and fetched tag must match.` The content is merged but unreleased, and `1.4` is stranded too. Catch it before you push, with `release_candidate.py` below.
4. Add the evidence for the new edition: `content/research/updates/1.4/` with the reports and a `commit-binding.json` whose `book_edition` is `1.4`.
5. Check it. All three must pass, and the last one must print `tag=v1.4`:

   ```sh
   git fetch --tags
   python site/validate_release.py --base-ref origin/main
   python site/validate_evidence.py --base-ref origin/main
   python site/release_candidate.py --root .
   ```

6. Open the PR and authorize it as in scenario 1.

Recovery of a PR you merged by hand is not covered here. **Publish content release** rechecks approval provenance that only the controller's own merge has. Use the catch-up PR, which is the path that was rehearsed.

### 10. Runs that fail without starting

If **Release approved book** or **Check book update** runs end in about a second with no steps and the annotation *"The job was not started because recent account payments have failed or your spending limit needs to be increased"*, GitHub Actions is blocked by billing, not by this repository. Fix **Settings → Billing and plans**, then run `gh workflow run approved-book.yml -f pr=N` for each affected PR. A PR whose **Check book update** run failed this way needs a new run of it first: push a commit or use **Re-run all jobs**.

### 11. The release failed after the merge

The PR is merged but the release is missing or incomplete, or **Publish content release** failed. Find the run (`gh run list --workflow release-content.yml -L 3`) and read the failed job. If the cause was transient, or you fixed it, dispatch recovery:

```sh
gh workflow run release-content.yml -f pr=N -f merge_sha=$(gh pr view N --json mergeCommit --jq .mergeCommit.oid)
```

What it does is in [the table above](#recovery-and-corrections). If it stops with `Published release is incomplete; do not overwrite immutable assets.`, open the release on GitHub and inspect it: a published release is immutable, so never overwrite it. Ship the fix as the next edition through scenario 1, which needs a real chapter change. If it fails on `The previous changelog edition and fetched tag must match.`, the CHANGELOG was not folded: scenario 9 step 3. Never move a tag or overwrite a published PDF.

### 12. Only the website deploy failed

The release is published and complete but [apm.isainative.dev](https://apm.isainative.dev/) still shows the old edition. The last step of **Publish content release** dispatches the deploy for the merge commit and fails if `main` has moved on since. A push to `main` deploys by itself, so the site may already be current. Otherwise redeploy `main`:

```sh
gh workflow run deploy-pages.yml
```

Pass `-f sha=<current main commit>` to pin it. The workflow refuses any other commit. The same command redeploys after a tooling change or a failed Pages build.

### 13. A published release is wrong, or the site must go back

Do not edit the release or move its tag. Fix `main` through scenario 1 and release the next edition, for example `1.3`. The edition must be above the one on `main`, so there is no way to publish an older edition after a newer one. To pull a mistaken edition back, restore the content in a new PR with a higher edition number. This repository has no workflow that deploys the website from an old tag or reverts a release: the site always follows `main`.

### 14. Choosing the version

Follow the table in [Prepare the edition](#prepare-the-edition). When unsure, ask what a reader of the last edition would notice: a restructured book is major, everything else reader-visible is minor. The edition must be above the one on `main`, and the check tells you if it is not. A change that readers cannot see gets no new edition: it goes in a tooling PR, or into the next content edition.

### 15. Control center alerts

If you use the book control center, each alert has a fix on this page:

| Alert | Cause and fix |
| --- | --- |
| `PR #N is ready for your approval` | Preflight is green. Approve the head (scenario 2) or comment `/release-book <SHA>` (scenario 1). |
| `PR #N release preflight is failing` | Open the failed **Check book update** run. Fix the PR, or re-run failed jobs if the failure was transient. |
| `PR #N was approved but is still open` | Scenario 6. |
| `PR #N changed after your approval` | Scenario 4. Approve the new head. |
| `<workflow> failed` | Open the run. Re-run failed jobs, or use scenario 10 (billing), 11 (release) or 12 (deploy). |
| `<run> has been queued for N days` | An orphaned run, such as GitHub's own `pages build and deployment`. `gh run cancel <run-id>`; the site keeps serving. |
| `Edition X on main has no release yet`, `N content file(s) changed since vX.Y without a release` | Scenario 9: content reached `main` without the controller. |
| `Latest GitHub Pages build errored` or `Site is not responding` | Scenario 12. |

### Before you open any PR

```sh
python -m unittest discover -s tests
git fetch --tags
python site/validate_release.py --base-ref origin/main    # edition, CHANGELOG, tooling-only bumps
python site/validate_evidence.py --base-ref origin/main   # content PR: evidence matches the changed files
python site/release_candidate.py --root .                 # content PR: prints tag=vX.Y; catches an unfolded CHANGELOG
python site/extract_release_notes.py X.Y                  # release notes come out nonempty
python site/generate.py                                   # regenerate the site, commit the result
python site/generate_pdf.py                               # needs Playwright Chromium; CI does this too
```

`release_candidate.py` compares the CHANGELOG with the tags in your clone, so fetch them first. The tooling is described in [`scripts/README.md`](scripts/README.md#state-evidence-and-release-boundary).
