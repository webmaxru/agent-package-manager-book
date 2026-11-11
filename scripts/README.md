# Running the book workflow

Launch one driver; it reuses the existing custom agents and skills. No additional agent fleet or
scheduled release bot is required.

| Goal | Saved prompt | Launcher |
|---|---|---|
| Check upstream and assess chapter impact | `/update-book` with `Mode: check` | `-UpdateBook -CheckOnly` |
| Prepare an incremental, reviewed update | `/update-book` (default: prepare) | `-UpdateBook` |
| Bootstrap the entire book from scratch | `/run-playbook` | No mode flag |
| Add one genuinely new chapter | `/new-chapter` | Supply its prompt with `-PromptPath` |
| Prepare or explicitly publish reviewed content | `/release-content` | Prefer an interactive, scoped invocation |

## Incremental update

```powershell
# Preview without requiring Copilot, network access, or installs
pwsh .\scripts\run-fleet.ps1 -UpdateBook -CheckOnly -DryRun

# Read-only release-gap research and impact report
pwsh .\scripts\run-fleet.ps1 -UpdateBook -CheckOnly

# Prepare only affected chapters against latest stable at discovery
pwsh .\scripts\run-fleet.ps1 -UpdateBook

# Or freeze a specific stable target for this run
pwsh .\scripts\run-fleet.ps1 -UpdateBook -ApmVersion 0.31.0
```

The update prompt defaults to `prepare`, not publish. It reads the full stable APM release gap,
maps it onto the TOC/actual claims, verifies affected examples against an isolated pinned CLI,
requires chapter and integration ACCEPT, and hands off to release preparation. The result is
locally committed, review-ready content with durable reports, not a published edition.

For just the metadata/release notes, without agents or APM installed:

```powershell
python .\scripts\check_upstream.py
python .\scripts\check_upstream.py --target 0.31.0
```

Python + PyYAML are required. The helper prints JSON and writes nothing. It uses public GitHub
metadata without tokens, paginates the complete release list, excludes drafts/prereleases, and
fails rather than claiming "current" on a network or incomplete-range error. Its baseline comes
from `content/version.yml`'s `apm_version`, not the author's root dependency lockfile.

## Initial production or custom prompt

```powershell
pwsh .\scripts\run-fleet.ps1 -DryRun
pwsh .\scripts\run-fleet.ps1
pwsh .\scripts\run-fleet.ps1 -PromptPath ".github\prompts\new-chapter.prompt.md" -DryRun
```

The default is the real `.github\prompts\run-playbook.prompt.md` file. It runs architecture and
scaffolding and is **not** the routine update path. Custom prompts still need their required
inputs filled in; `-PromptPath` and `-UpdateBook` are mutually exclusive.

The launcher calls `copilot -p <prompt> --allow-all-tools` and propagates Copilot's exit code.
Dry-run validates the prompt path and reports the resolved mode/target without launching agents.
`-ApmVersion` accepts only an exact stable `X.Y.Z` (optional leading `v`); a moving "latest"
lookup is performed once by the default update flow, not independently by each agent.

## State, evidence, and release boundary

Session todos and local Git checkpoints track chapter progress. Keep the frozen discovery JSON
and working impact matrix in session artifacts; persist final verifier/reviewer reports under
`content/research/updates/<edition>/`. Resume only with unchanged inputs/target; later edits
invalidate affected verdicts. Separate chapter scratch projects prevent concurrent agents from
overwriting each other's examples.

`/release-content` defaults to **prepare**: content-only edition metadata/changelog, strict
preflight, required HTML/PDF build, and a local commit. Publishing requires an explicit request
and the exact reviewed commit already merged into remote `main`.

```powershell
python .\site\validate_release.py --base-ref v1.1
python .\site\extract_release_notes.py 1.2
python -m unittest discover -s tests -v
```

An owner-approved content PR can be merged and published by **Release approved book**.
For owner-authored PRs, GitHub prohibits self-approval; post `/release-book <full-head-sha>`.
The controller checks the current head, owner approval, checks, content-only paths and base,
then builds HTML/PDF read-only before merging. It explicitly dispatches publication for the
resulting merge SHA, and publication explicitly dispatches Pages. Mixed infrastructure changes
are excluded. Tag pushes alone do not publish; existing published tags are never moved.

## Edition evidence

For a new edition, retain the actual `chNN-review.md`, `chNN-verification.md` and
`integration-review.md` files from the verifier and reviewers. Each needs an explicit
`Verdict: ACCEPT` (reviews) or `Verdict: PASS` (verification), and must name the exact
reviewed APM version. Create `content/research/updates/<edition>/commit-binding.json`
after the reviewed files are final. Example for one affected chapter:

```json
{
  "book_edition": "1.3",
  "reviewed_apm_version": "0.32.0",
  "result": "PASS",
  "affected_chapters": [1],
  "removed_paths": [],
  "example_results": [
    {"chapter": 1, "id": "chapter-example-id", "status": "PASS"}
  ],
  "bound_paths": [
    {"path": "content/chapters/the-context-problem.html", "git_blob_oid": "<git-blob-id>"},
    {"path": "content/research/updates/1.3/ch01-review.md", "git_blob_oid": "<git-blob-id>"},
    {"path": "content/research/updates/1.3/ch01-verification.md", "git_blob_oid": "<git-blob-id>"},
    {"path": "content/research/updates/1.3/integration-review.md", "git_blob_oid": "<git-blob-id>"}
  ]
}
```

Replace placeholders with the actual `git hash-object -- <path>` outputs. Bind every changed
chapter, semantic TOC and backend example file and all required reports; list removed inputs in
`removed_paths`. Declare each affected chapter and all its actual example results. A
`SKIPPED-needs-network` entry also needs a nonempty `reason`. Do not invent a PASS or ACCEPT:
If a chapter has no affected examples, use
`"no_examples": [{"chapter": 1, "reason": "No executable examples were affected."}]`
instead of fabricating an example result. These structured fields point to real independent
evidence, not a substitute for it. Verify with
`python .\site\validate_evidence.py --base-ref <base-sha>`; any later edit to a bound file
requires fresh review/verification and a new binding.

## Safety

`--allow-all-tools` grants Copilot the same access you have; the prompt's scope is a workflow
instruction, not an OS sandbox. Use an appropriately isolated environment for unattended work.
The default update run never merges, pushes, tags, or publishes. Public examples avoid private
credentials and live publishing; any skipped example must have a specific, visible reason.
Do not change global APM configuration or upgrade the book's authoring skills while studying a
new CLI release. Preserve unrelated work and stage only the update's files.
