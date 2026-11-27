# Releasing *Agent Package Manager: An Interactive Book*

A release is a Git tag `vX.Y` on the merge commit of an **owner-approved, content-only pull request**, with a GitHub Release carrying `apm-book-vX.Y.pdf`. Nothing else publishes: not a push, a tag, a label or a manual merge.

```text
/update-book ─► /release-content ─► content PR ─► Book release preflight (green)
        ─► owner approval of the exact head ─► Release approved book: squash merge
        ─► Release book: tag, draft + PDF, publish ─► released tag → GitHub Pages: apm.isainative.dev
```

The sections below explain each step. [Scenarios](#scenarios-what-to-do-when) walks through the situations you will actually meet, with commands. The tooling behind this page is documented in the [README](README.md#versioning--releases) ([update from an APM release](README.md#update-from-an-apm-release), [prepare, approve, then publish](README.md#prepare-approve-then-publish)) and in [`scripts/README.md`](scripts/README.md) ([state, evidence and release boundary](scripts/README.md#state-evidence-and-release-boundary), [edition evidence](scripts/README.md#edition-evidence)).

## Book release flow contract v1

Every book repository follows the same release flow. A repository conforms when `tests/test_flow_contract.py` passes and each rule below is covered by a test in that repository's own suite.

1. **Workflow surface (same names everywhere).**
   `ci.yml` named "Book CI" with the aggregate job "Book release preflight"; `book-approval-signal.yml` named "Book approval signal"; `approved-book.yml` named "Release approved book"; `release.yml` named "Release book"; one deploy workflow, `deploy-swa.yml` or `deploy-pages.yml`.
2. **Controller.**
   Triggers: `workflow_run` of "Book approval signal" and "Book CI", `issue_comment`, schedule `17,47 * * * *`, and `workflow_dispatch` with the input `pr`. Jobs run only from `main`. Workflow `permissions: {}` with least privilege per job. Concurrency group `approved-book`, no cancel. Validators always run from `main`, never from the pull request.
3. **Eligibility.**
   The pull request is open, not a draft, from the same repository, targets `main`, is mergeable, and its head contains the current `main`. Its files are content-only under the book's allowlist. "Book release preflight" is green on the exact head, and the version, CHANGELOG and evidence checks pass.
4. **Authorization.**
   Someone else's pull request: the latest formal owner review is Approve on the current head; ordinary COMMENTED reviews neither authorize nor revoke. The owner's own pull request: any still-present, unedited owner comment with the exact whole body `/release-book <40-character lowercase head SHA>`; extra whitespace is invalid. A later push invalidates authorization for the old head. A CHANGES_REQUESTED or DISMISSED review from any reviewer, or any review-dismissal timeline event at its actual event time, requires fresh owner authorization strictly afterward. Editing or deleting an authorization comment removes that comment's authority, but unrelated, stale or invalid comments do not cancel another valid comment. A non-owner never authorizes. The identical `tests/test_approval_contract.py` exercises these decisions in all four books.
5. **Merge.**
   A squash merge conditioned on the approved head SHA. The controller then dispatches `release.yml`, because merges made with `GITHUB_TOKEN` trigger no workflows.
6. **Release.**
   `release.yml` is dispatch-only, with the inputs `pr`, `head_sha`, `base_sha`, `merge_sha` and `tag`, and the concurrency group `book-publish`. Steps: plan, build from the merge commit, annotated tag, draft release, upload assets, publish, deploy the released tag, smoke test. Never clobber assets and never move a tag. A complete published release is a no-op, including no redeployment. A partial release (tag-only, any existing draft, or incomplete published assets) or a provenance mismatch fails with no writes. Latest goes only to the highest published stable edition; bare tags, drafts and prereleases do not compete. A fix is a new version.
7. **Deploy.**
   Production serves only released editions. A push to `main` deploys only when the content equals the latest published stable release (the `published-source` job). After a new publication, the release automatically deploys its own tag only if it is the highest published stable edition; older editions and prereleases do not roll production back. The release waits for its exact deployment run and requires successful deployment and smoke-test steps; failure, timeout, missing credentials or skipped checks cannot be reported as a successful deployment. A manual deploy dispatch takes a published stable ref or sha, including an older edition, which is the explicit rollback path.
8. **No other publisher.**
   A tag push, a label or a branch name never publishes. A manual merge to `main` bypasses the controller; the fix is a catch-up pull request with a higher version.
9. **Pins.**
   Runner `ubuntu-24.04`. `actions/checkout@v7`, `actions/setup-python@v7`, `actions/upload-artifact@v7`, `actions/download-artifact@v8`.

### Per-book settings

These may differ between books and are documented in each repository: the format and build, the version file, scheme and tag format, the content allowlist, the evidence rules, the deploy target and domain, the catch-up pull request rules, and how upstream updates are scouted.

| Setting | Agent Package Manager book |
| --- | --- |
| Format/build | HTML from `content/toc.yml` and chapter fragments via `python site/generate.py`; release PDF via `python site/generate_pdf.py` (Python 3.12, PyYAML, Playwright Chromium). The sole release asset is `apm-book-vX.Y.pdf`; the website retains its Substack PDF gate. |
| Version file, scheme and tag | `content/version.yml`: quoted major.minor `X.Y`, date and independently pinned `apm_version` (`X.Y.Z`). Structural rewrites are major; other reader-visible updates are minor. Tags are stable-only `vX.Y`; no patch or prerelease editions. |
| Content allowlist | Trusted `scripts/book_release.py::allowed_path`: `content/version.yml`, `content/CHANGELOG.md`, `content/toc.yml`, `content/chapters/**`, `content/research/**`, `backend/examples/**`, generated `site/index.html`, `site/chapters/**/*.html`, `site/llms.txt`, `site/llms-full.txt`, `site/sitemap.xml`, `site/robots.txt`, `site/site.webmanifest`. Renames check both paths. The same policy defines the deploy content comparison; workflows carry no separate path list. |
| Evidence rules | `content/research/updates/<edition>/commit-binding.json` binds affected chapter/TOC/example inputs and reports to Git blob IDs, names every affected chapter and example result (or an explicit no-example reason). Integration and chapter reviews require ACCEPT; verification requires PASS or justified `SKIPPED-needs-network`, all at the pinned APM baseline. Trusted validators check structure and binding, not prose quality. |
| Deploy target/domain | GitHub Pages, `deploy-pages.yml`, `github-pages` environment, `https://apm.isainative.dev`. Pushes rebuild current main only if allowed content equals the latest published edition; release/manual deployments use a published tag or its full SHA. A new publication auto-deploys only when it is the highest published stable edition, and **Release book** waits for that exact Pages run (job `deploy`, steps `Deploy to GitHub Pages` and `Smoke test the released edition`, up to 45 minutes). Smoke checks verify the edition and discovery files. Existing `v1.2` remains deployable; historical `v1.0`/`v1.1` lack today's metadata/toolchain and are preserved, not rebuilt by this workflow. |
| Catch-up PR rules | Start at current main; choose an edition higher than main, make a real chapter/TOC change, and provide fresh bound evidence. Fold stranded untagged CHANGELOG entries into the new entry, leaving the latest fetched lower edition tag immediately below it (normally the latest published edition). Both PR preflight and release-candidate validation enforce the fold before merge. A partial tagged edition remains an immutable predecessor; retain its entry and choose a higher version. |
| Upstream-update scouting | No scheduled scout. `python scripts/check_upstream.py` or `/update-book` with `Mode: check` reads stable `microsoft/apm` releases against `content/version.yml`; an update freezes one explicit APM target and requires the chapter quality gates. The root skill lockfile is not the upstream baseline. |

The Linux runner is pinned to `ubuntu-24.04`; the existing extra Windows launcher regression lane is pinned to `windows-2025`. Both feed the single required aggregate check.

## Preview downloads and Actions storage

Ordinary pushes, PR checks and the approval controller still build and verify the full HTML
and PDF, but upload no book bundles. To request a downloadable PDF, select **Book CI ->
Run workflow**, choose the source branch/tag, and enable **upload_preview** (default `false`):

```sh
gh workflow run ci.yml --ref main -f upload_preview=true
```

The preview expires after **one day**. Its name is
`book-preview-v1-<repository ID>-<SHA256 of full source ref>-<run ID>-<attempt>`.
The hash distinguishes `refs/heads/feature` from `refs/tags/feature` and avoids unsafe or
overlong ref names. After successful manual CI, **Clean replaced book previews** runs trusted
code from `main`, without checking out or downloading producer code/artifacts. It uses the
exact replacement artifact ID, namespace, producing workflow/run/attempt, repository and
branch metadata, and creation order to delete only older previews of that same full ref.
Artifact IDs identify objects but are not chronological; age checks use creation timestamps
and producing run/attempt order, never numeric artifact-ID order.
Cleanup serializes by repository and source name without cancelling an executing cleanup;
branches/tags sharing a short name also serialize but never replace each other's previews.
It requires the current attempt's successful upload step and selects only that attempt's exact
namespace, so reruns can safely replace artifacts retained from earlier completed attempts.
A skipped upload is a no-op; a successful upload with missing or expired replacement data
fails clearly and retains previous previews. Cleanup rechecks the replacement and producer
immediately before deletion, preserves active runs,
newer uploads, other refs/workflows, diagnostics and release staging, and does nothing without
a successful replacement. Active runs and unverifiable historical attempts may leave overlap until a later
cleanup or one-day expiry. Cleanup failures are visible failed jobs, not hidden successes.

Release builds retain their PDF and notes transfer artifact for **seven days** for failure
inspection/recovery. Only `publish` downloads it; website deployment rebuilds released source
and uses its own required **one-day** Pages transfer artifact. Release staging is deleted by
a separate least-privilege cleanup job only after publication and delivery have succeeded,
all build/publish/deploy consumers are finished, the existing provenance/publication validator
passes again, and the published PDF's GitHub SHA-256 digest matches the built PDF. Missing
integrity metadata, failed/skipped delivery, drafts, incomplete publication or any uncertainty
retain staging. Existing immutable/no-write release recovery behavior is unchanged.
No release assets, releases, tags or deployed content are deleted.

The workflow YAML in this repository is the source of truth: there is no shared workflow
template/generator to regenerate. The prior CI and approval-preview uploads had no consumers.
The existing controller/deployment `actions: write` permissions remain necessary for dispatch;
new deletion privileges exist only in the trusted cleanup jobs. Fork PR checks remain read-only.

Retention settings affect **new artifacts only**, not existing expiration dates. At the
2026-11-27 inventory, this repository had ten unexpired legacy preview archives (32.33 MiB)
with the default **90-day** expiry, some in February 2027; they are not retroactively shortened
or purged by this change. Other repositories still consume the account's shared **500 MB**
included Actions artifact-storage allowance. Archive-size totals are not a billing calculation,
and storage accounting can lag deletion/expiry.

## Prepare the edition

Run [`/update-book`](.github/prompts/update-book.prompt.md) to follow an APM release (add `Mode: check` for a read-only impact report), or make the chapter edits yourself. Then run [`/release-content`](.github/prompts/release-content.prompt.md): it updates the edition and the CHANGELOG, requires a fresh HTML and PDF build, and commits locally. Review the result and open a content PR against `main`.

Only reader-visible chapter prose and meaningful TOC changes justify a new edition. Research, examples under `backend/`, build scripts and styling alone do not.

| Increment | When to use it |
| --- | --- |
| Major (`2.0`) | Structural rewrite or reordering of the book. |
| Minor (`1.3`) | Every other reader-visible update: new material, a refresh for a new APM release, corrections. |

Editions are `major.minor`, with no patch level. The edition lives in [`content/version.yml`](content/version.yml) next to the date and `apm_version`, the APM release the chapters were reviewed against. The book's `1.2` and APM's `0.31.0` are independent numbers. Changing `apm_version` needs a new edition, and it cannot go backwards.

**Book release preflight** (the **Book CI** workflow, `ci.yml`) is the gate. It runs the tooling tests on Linux and Windows, checks the edition, CHANGELOG and evidence with validators from `main`, regenerates the site and builds the PDF. For a content PR:

- Change only [`content/`](content) (`version.yml`, `CHANGELOG.md`, `toc.yml`, `chapters/`, `research/`), `backend/examples/` and the generated site files (`site/index.html`, `site/chapters/*.html`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `robots.txt`, `site.webmanifest`). Anything else is tooling and belongs in a separate PR with no version bump.
- Set the edition above the one on `main` and add a matching `## [X.Y] - YYYY-MM-DD` section at the **top** of `content/CHANGELOG.md`. The checks fail in these cases:

  | You did | Preflight says |
  | --- | --- |
  | Edited a chapter, no bump | `Reader-facing content changed without a new edition: content/chapters/<file>.html` |
  | Bumped `version.yml`, no CHANGELOG entry | `The first released CHANGELOG entry must match content/version.yml.` |
  | Bumped and added a CHANGELOG entry, no chapter or TOC change | `Edition bumps require chapter or TOC changes, not only tooling or metadata.` |
  | Left a stranded unpublished entry below the new CHANGELOG section | `The previous changelog edition and fetched tag must match.` |
  | No evidence for the edition | `evidence preflight: Cannot read edition evidence: …` |

- Add the evidence. Under `content/research/updates/<edition>/`, keep an `integration-review.md` (`Verdict: ACCEPT`), a `chNN-review.md` (`Verdict: ACCEPT`) and a `chNN-verification.md` (`Verdict: PASS`) for every changed chapter, each naming the `apm_version`, and a `commit-binding.json` that lists the affected chapters, every example result (or a reason there are none) and the Git blob ID of every changed chapter, TOC and example file and of every report. Get an ID with `git hash-object -- <path>`. The format is in [`scripts/README.md`](scripts/README.md#edition-evidence). **Any edit to a bound file afterwards needs a new binding.** The check proves the files exist, match the binding and carry the verdicts. It does not judge whether the prose or examples are right. You do.

## Authorize and publish

For someone else's non-draft PR, **webmaxru** submits an **Approve** review on its current head. For an owner-authored PR, post exactly `/release-book <full lowercase 40-character head SHA>` in a new, unedited PR conversation comment. An older SHA, another user's comment, an edited or deleted comment, or approval superseded by requested changes or dismissal does not count. A new commit needs new approval. Approving before the checks finish is fine: the controller waits for them.

The controller, **Release approved book**, runs on `main` with its own trusted validators. It reacts to the review or comment, to the completion of **Book CI**, to a scan of up to 30 recently updated open PRs at minutes 17 and 47, and to **Run workflow → pr**. None of those triggers grants approval. It requires an open, mergeable, non-draft, same-repository PR against `main` whose files are all on the content allowlist, a head that already contains the current `main`, and a successful **Book CI** run with **Book release preflight** green for exactly that head. It then repeats the preflight on its own build of the head, including the PDF, and merges with a **squash** that is conditional on the approved head. If `main` moved in the meantime it stops with `Main advanced during preflight; update the branch and approve again.`

Publication is a separate dispatch from the controller, because a merge made with `GITHUB_TOKEN` does not trigger other workflows. **Release book** receives `pr`, `head_sha`, `base_sha`, `merge_sha` and `tag`, and proves that the merge commit is the PR's merge on `main`, with the approved tree. It rebuilds the book from that commit, creates an annotated tag `vX.Y` there, uploads `apm-book-vX.Y.pdf` to a **draft** release, publishes it, and marks it Latest only if no newer stable release exists. Its final `deploy` job (`book_release.py deliver`) then rechecks that the release is complete and provenance-valid and compares the tag with every published stable release (bare tags, drafts and prereleases are ignored):

- **Highest published stable edition:** it dispatches **Deploy book to GitHub Pages** once with `ref=vX.Y` (independent of later changes to `main`), using the REST API version that returns the new run's ID, and follows only that run. It succeeds only when the run concluded `success` and its `deploy` job ran both `Deploy to GitHub Pages` and `Smoke test the released edition` successfully. A failed, cancelled (for example superseded in the `pages` queue) or timed-out run, a skipped `deploy` job, or a missing or skipped smoke step fails **Release book**. A dispatch without a run ID also fails: it never guesses a recent run and never re-dispatches.
- **Older edition** (a newer stable edition is already published): it publishes the release but dispatches nothing, and posts the notice `Production not rolled back` with the manual rollback command. Production keeps serving the newer edition.

A complete published release found by the plan is a no-op, including no redeployment. The website keeps its Substack gate in front of the PDF, so the PDF is downloaded from the GitHub release.

The repository has no branch protection or ruleset, so nothing enforces this gate: **manual merges bypass it**.

## Recovery and corrections

Pushing a tag no longer publishes. If the merge succeeded but publication failed before creating a tag or draft, dispatch **Release book** for that merged PR. It rechecks the approval and provenance, and never moves a tag or overwrites a published file:

```sh
gh workflow run release.yml --ref main -f pr=N -f merge_sha=$(gh pr view N --json mergeCommit --jq .mergeCommit.oid)
```

| State found | What recovery does |
| --- | --- |
| Release published with the PDF | Nothing to do (no-op, no redeploy): `Existing published edition preserved.` |
| No tag | Creates the tag at the merge commit, then a draft, uploads the PDF, publishes. |
| Tag but no release, or a draft | Stops without writes. An interrupted/partial edition is not repaired in place; prepare a new edition. |
| Published release without the PDF | Stops without changes. Prepare a new edition; never overwrite immutable assets. |
| Tag points to another commit | Stops: `Existing edition tag points to another commit; never move it.` |

If the tag already exists, `-f tag=vX.Y` selects it instead. It must match `content/version.yml` at the approved merge commit. Any historical release without this controller's approval/merge provenance fails closed and stays unchanged; this is separate from the published-tag deployment check, which supports `v1.2`.

A correction needs a **new edition**, not a rebuild. Never move a tag or replace a published PDF. See [scenarios 11–13](#11-the-release-failed-after-the-merge).

## Scenarios: what to do when

Commands use the [GitHub CLI](https://cli.github.com/) (`gh`) from a clone of this repository and work in bash and PowerShell. `N` is the pull request number and `vX.Y` a tag. Replace `v1.2` in examples with the latest published tag shown by `gh release list`.

### What triggers what

| Event | What happens | Release? |
| --- | --- | --- |
| PR opened or pushed | **Book CI** runs the tests, edition and evidence checks, site generation and the PDF build. Its **Book release preflight** job is the gate. | No |
| Owner **Approve** review, or an owner `/release-book <SHA>` comment | **Release approved book** re-checks everything and squash-merges the approved head. **Release book** follows, publishes, and deploys and smoke-tests the edition if it is the highest published stable edition. | Yes, a few minutes later |
| **Book CI** finishes, or the 30-minute scan | The controller looks for an approved PR it missed. It never approves anything itself. | Only if a valid approval exists |
| **Release approved book → Run workflow** with `pr` | Same re-check for one PR. | Only if a valid approval exists |
| **Release book → Run workflow** | Recovery for an approved merged PR or an existing tag. | Publishes only a fresh edition; complete editions are no-ops (no redeploy) and partial editions fail without writes |
| Push a tag, add a label, press **Merge** | Nothing in the release flow. | **No** |
| Any push to `main` | **Book CI** runs; **Deploy book to GitHub Pages** runs `published-source` and deploys only if allowed content equals the latest published release. Unreleased content leaves production unchanged. | No |
| **Deploy book to GitHub Pages → Run workflow**, `ref=vX.Y` (or its full SHA) | Verifies a published release and deploys that edition; an older released ref is rollback. An unreleased ref is refused. | No |
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
   gh run list --workflow release.yml -L 3
   gh run watch <run-id>
   gh release view vX.Y
   ```

**Result:** the PR is squash-merged, `vX.Y` is a tag on the merge commit, the release has `apm-book-vX.Y.pdf`, it is Latest if it is the highest stable edition, and the website shows the new edition. **Release book** turns green only after its `deploy` job has seen the exact Pages run deploy and smoke-test `vX.Y`.

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

Only the owner can authorize a release, but **any reviewer’s change request or dismissed review revokes earlier authorization**. A dismissal counts when it happens on the PR timeline, even if the original review was much earlier. An ordinary **Comment** review neither authorizes nor revokes. Pushing a new head invalidates approval of the old SHA; editing or deleting an authorization comment invalidates that comment.

To unblock the PR, the owner must authorize its current head **strictly after** the most recent change request or dismissal. For a contributor’s PR, submit a new **Approve** review. For your own PR, post a new, unedited `/release-book <SHA>` comment. An authorization with the same timestamp as the revocation does not count.

### 5. The branch is behind `main`

An approved PR with green preflight can fall behind when another PR merges into `main`. Even without a conflict, **Release approved book** skips the stale PR before rebuilding the book. Its `authorize` job emits a warning and writes the same message in the run summary: `PR N: approved, but its base <old SHA> is behind main <live SHA>. Update the branch from main, then approve the new head.` Rerunning the controller alone won't help. Update the branch, wait for preflight on the new head, and approve again:

```sh
gh pr update-branch N
gh pr checks N --watch
gh pr review N --approve    # or comment /release-book <new SHA> on your own PR
```

### 6. Approved, but the PR is still open

Look at the latest **Release approved book** run. Check the run summary for the stale-base warning from scenario 5 or the tooling and mixed-PR warnings from scenarios 7 and 8; for other rejections the `authorize` job prints `PR N not eligible: <reason>`. Typical causes include a failing or still-running preflight, a head that moved after approval, or a file outside the allowlist. A run can also be replaced in GitHub's concurrency queue. The scan covers only the 30 most recently updated PRs. Fix the cause, or run the controller for this PR:

```sh
gh workflow run approved-book.yml -f pr=N
```

If the run died within a second with no steps, see [Runs that fail without starting](#10-runs-that-fail-without-starting).

### 7. Tooling, docs and workflow changes

A PR that touches only files outside the content allowlist (`scripts/`, `site/` generator code, `.github/`, `README.md`, `RELEASING.md`, tests) is **tooling-only**. It needs no edition bump, and a bump with no chapter change fails the checks. It never releases. The owner's **Approve** on its current head, a `/release-book <SHA>` comment or `gh workflow run approved-book.yml -f pr=N` ends in a green **Release approved book** run with one warning, repeated in the run summary, and no merge or release:

```text
PR #N is tooling-only (no book content changed: <first up to 5 paths, comma-separated>); the release controller never merges or releases tooling PRs. Merge it yourself once its checks are green.
```

Merge it yourself when the checks are green. Scheduled scans, **Book CI** completions and other reviewers' reviews only log the quiet `PR N not eligible: <reason>` line. The push to `main` redeploys with the new tooling only if the allowed content still matches the latest published edition; otherwise `published-source` skips the build and deploy.

That comparison includes tracked generated HTML and discovery files, not just chapter sources. Previously regenerated output can therefore hold a tooling-only push behind the gate even when chapter prose is unchanged. The existing website remains live; deploy a published tag explicitly or prepare the next reviewed content edition rather than weakening the gate.

### 8. Mixed content and tooling

A PR that changes both content and tooling is never merged by the controller. The same owner requests end in a green run with one warning, also in the run summary:

```text
PR #N mixes book content with tooling (<first up to 5 non-allowlisted paths>); split it: merge the tooling PR yourself, then authorize the content PR.
```

Split it into two PRs: tooling first (merged by you), then the content PR.

### 9. A manual merge by mistake

Pressing **Merge** on a content PR, or merging from the command line, bypasses the controller. The repository has no branch protection or ruleset, so GitHub allows it. The effects:

- **No tag, no release, no PDF.**
- The push to `main` still runs **Deploy book to GitHub Pages**, but `published-source` sees content different from the latest published release and skips deployment. **Production stays on its released edition**, while the content sits on `main` waiting for the catch-up.
- The edition the PR carried is now on `main` unreleased. The next PR must be above it, so that version number is stranded.

Fix it with a **catch-up PR**. For example, if `main` carries edition `1.3` but the latest tag is `v1.2`:

1. Branch from `main`. The catch-up must contain a **real chapter or TOC change** (a correction, a clarified paragraph, an added cross-reference). A PR that only bumps the version and CHANGELOG fails with `Edition bumps require chapter or TOC changes, not only tooling or metadata.`
2. Set `version` in `content/version.yml` to `"1.4"`, above the stranded `1.3`. Keeping `1.3` fails with `Reader-facing content changed without a new edition`.
3. **Fold the stranded notes into the new CHANGELOG section.** Add `## [1.4] - YYYY-MM-DD`, move the untagged `1.3` bullets under it and delete the `## [1.3]` heading, so the headings read `[1.4]`, `[1.2]`, and so on. The entry after the new one must equal the latest fetched lower edition tag, `v1.2` here. If a failed publisher already created a partial `v1.3` tag, never move/delete it: keep its predecessor entry and prepare a higher edition instead.

   > **Preflight guard.** Leaving `## [1.3]` in place now fails **Book release preflight** with `The previous changelog edition and fetched tag must match.` Both PR CI and the trusted controller run the candidate check, so the mistake is caught before the automatic merge. Fetch tags before running the same check locally.
4. Add the evidence for the new edition: `content/research/updates/1.4/` with the reports and a `commit-binding.json` whose `book_edition` is `1.4`.
5. Check it. All three must pass, and the last one must print `tag=v1.4`:

   ```sh
   git fetch --tags
   python site/validate_release.py --base-ref origin/main
   python site/validate_evidence.py --base-ref origin/main
   python site/release_candidate.py --root .
   ```

6. Open the PR and authorize it as in scenario 1.

**Release book** requires owner authorization and controller merge provenance. It is not a bypass for a manual merge: use the catch-up PR, which is the path that was rehearsed.

### 10. Runs that fail without starting

If **Release approved book** or **Book CI** runs end in about a second with no steps and the annotation *"The job was not started because recent account payments have failed or your spending limit needs to be increased"*, GitHub Actions is blocked by billing, not by this repository. Fix **Settings → Billing and plans**, then run `gh workflow run approved-book.yml -f pr=N` for each affected PR. A PR whose **Book CI** run failed this way needs a new run of it first: push a commit or use **Re-run all jobs**.

### 11. The release failed after the merge

The PR is merged but the release is missing or incomplete, or **Release book** failed. Find the run (`gh run list --workflow release.yml -L 3`) and read the failed job. If it failed before any tag/release write, fix the cause and dispatch recovery:

```sh
gh workflow run release.yml --ref main -f pr=N -f merge_sha=$(gh pr view N --json mergeCommit --jq .mergeCommit.oid)
```

What it does is in [the table above](#recovery-and-corrections). A tag without a release, a draft, an incomplete asset, or mismatched provenance fails without writes. Inspect it, then ship the fix as the next edition through scenario 1, which needs a real chapter change. A complete edition is a no-op; that does not retry Pages, so if only the final `deploy` job failed use scenario 12. If an older run failed on `The previous changelog edition and fetched tag must match.`, follow scenario 9 step 3. Never move a tag or overwrite a PDF.

### 12. Only the website deploy failed

The release is published and complete, but **Release book** failed in its `deploy` job or [apm.isainative.dev](https://apm.isainative.dev/) still shows the old edition. The job names the exact Pages run it dispatched and why it was not accepted:

| Message | Meaning and next step |
| --- | --- |
| `Deployment run <id> did not deliver vX.Y: run concluded 'failure'` (or `'cancelled'`) | The Pages run failed (including `published-source` refusing the tag; read that job's log), or a newer Pages run replaced it while it was queued. Read it with `gh run view <id> --log-failed`. |
| `… did not deliver vX.Y: 'deploy' job concluded 'skipped'` | Defensive guard: the run finished without its `deploy` job running, so nothing was deployed or smoke-tested. Inspect the run before any manual deployment. |
| `… did not deliver vX.Y: step 'Smoke test the released edition' did not succeed` | Pages deployed but the edition or discovery-file check failed or did not run. |
| `Deployment run <id> did not finish within 2700 seconds` | Deployment and successful smoke-test evidence were not confirmed before the deadline. Even a successful response received after it is rejected; the run may still be going or may have finished. Check `gh run view <id>` before doing anything else. |
| `Deployment dispatch returned no workflow run ID` | It is unknown whether a run started. Check `gh run list --workflow deploy-pages.yml -L 5` first; the release never guesses a run or re-dispatches. |

Later main changes never substitute another edition. Dispatching **Release book** again is a no-op for a complete edition and does not redeploy. After you have fixed the cause and confirmed no deployment of this edition is still running, deploy the published tag yourself and watch the run:

```sh
gh workflow run deploy-pages.yml --ref main -f ref=v1.2
gh run list --workflow deploy-pages.yml -L 3
gh run watch <run-id>
```

Instead of the manual dispatch, and under the same conditions, you can use **Re-run failed jobs** on the **Release book** run. Its `deploy` job rechecks the release and the newest-edition rule, then dispatches and follows exactly one new run.

Use a published tag or its full 40-character commit SHA in `ref`. The workflow verifies that the release is non-draft and the tag resolves to that commit; an arbitrary main SHA, branch name or unpublished tag is refused. A push can rebuild newer tooling only after the trusted allowlist comparison proves the content still equals the latest release.

### 13. A published release is wrong, or the site must go back

Do not edit the release or move its tag. Fix `main` through scenario 1 and release the next edition, for example `1.3`. The edition must be above the one on `main`. **Release book** never rolls production back on its own: if a newer stable edition is already published, it publishes the older one without deploying it and posts the notice `Production not rolled back` with the command below. For an immediate website rollback, dispatch the earlier published tag yourself (for example `v1.2` after `v1.3`):

```sh
gh workflow run deploy-pages.yml --ref main -f ref=v1.2
```

This changes the website only, not Git history, release assets or GitHub Latest. A future qualifying push or release can deploy the newest edition again. `v1.0` and `v1.1` predate the required build metadata and cannot be rebuilt by today's workflow; preserve their assets and use a buildable published edition.

### 14. Choosing the version

Follow the table in [Prepare the edition](#prepare-the-edition). When unsure, ask what a reader of the last edition would notice: a restructured book is major, everything else reader-visible is minor. The edition must be above the one on `main`, and the check tells you if it is not. A change that readers cannot see gets no new edition: it goes in a tooling PR, or into the next content edition.

### 15. Control center alerts

If you use the book control center, each alert has a fix on this page:

| Alert | Cause and fix |
| --- | --- |
| `PR #N is ready for your approval` | Preflight is green. Approve the head (scenario 2) or comment `/release-book <SHA>` (scenario 1). |
| `PR #N release preflight is failing` | Open the failed **Book CI** run. Fix the PR, or re-run failed jobs if the failure was transient. |
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
