---
name: book-orchestration
description: Coordinates the existing book agents for initial production or targeted updates from upstream APM releases. Use to plan and run research, authoring, verification, review, and integration for one or more chapters.
---

# Book Orchestration

This skill describes **how the book agents work together** to build the Agent Package Manager (APM)
interactive book. It is the orchestration layer: who is dispatched, in what order, with what
hand-offs and checkpoints. Choose the entry point before dispatching any work:

- `/run-playbook`: initial production, using the architecture and shell phases below.
- `/new-chapter`: one new chapter through the per-chapter loop.
- `/update-book`: incremental upstream refresh, using **Incremental updates** below.
- `/release-content`: prepare/publish already reviewed content; does not research new APM behavior.

## The team
| Agent | Role |
|-------|------|
| `book-architect` | Designs TOC, chapter specs, navigation, wave plan |
| `theory-researcher` | Produces cited concept briefs from APM docs |
| `apm-cli-explorer` | Installs & introspects the `apm` CLI; feature notes + examples |
| `chapter-author` | Weaves theory + CLI reference into chapter content |
| `code-verifier` | Runs/validates every example; reports pass/fail |
| `chapter-reviewer` | Reviews chapters; ACCEPT/REVISE + ranked findings |
| `frontend-builder` | Builds the interactive HTML shell and wires content in |

## Pipeline (per the case-study methodology: draft → review → revise, in waves)

### Phase 0 — Architecture
1. Dispatch `book-architect` → TOC, chapter table, section breakdowns, wave plan.
2. Dispatch `frontend-builder` → scaffold the site shell + nav driven by the TOC.
3. Checkpoint: commit TOC + shell.

### Phase 1 — Environment
4. Run the `apm-environment-setup` skill (via `apm-cli-explorer`) → the `apm` CLI installed and
   introspectable at one exact stable release, plus a scratch sample project to inspect.

### Waves (repeat per wave; start with ONE pilot chapter, then widen)
For each chapter in the wave, run **research in parallel**, then author, verify, review:
5. **Research (parallel):**
   - `theory-researcher` → concept brief (`content/research/<ch>-theory.md`)
   - `apm-cli-explorer` → feature notes + draft examples (`content/research/<ch>-reference.md`)
6. **Author:** `chapter-author` → chapter draft, pulling both briefs together.
7. **Verify:** `code-verifier` → validate/run every example; loop with author/explorer until all PASS
   (or SKIPPED-needs-network with a clear marker).
8. **Review:** `chapter-reviewer` → ACCEPT or REVISE; on REVISE, route must-fixes to `chapter-author`.
9. **Integrate:** `frontend-builder` → wire the accepted chapter into the site nav.
10. Checkpoint: commit the chapter (draft + examples + review verdict).

### Integration pass (after all waves)
11. `chapter-reviewer` reads across chapters for cross-chapter consistency (terminology, ordering,
    duplicate/contradictory claims).
12. `chapter-author` applies cross-cutting fixes; `frontend-builder` finalizes nav/cross-links.

## Wave ordering guidance
- **Wave 0:** one pilot chapter (e.g. "Why a package manager for agents?") to validate the pipeline.
- **Wave 1:** chapters with the most existing source material (lowest risk).
- **Wave 2:** the hardest chapters (governance/policy, transitive MCP, enterprise ramp).
- **Wave 3:** integration chapters needing cross-references to earlier ones.

## Orchestration principles
- **One chapter, one author per wave** — keep scope inside an agent's context budget; split if too big.
- **Checkpoint discipline** — draft → review → revise → commit at each chapter.
- **Batch reviews** in later waves (one reviewer over several chapters) to cut dispatch overhead.
- **Fix the primitives, not the symptom** — when a recurring gap appears, update the relevant agent
  definition / instructions rather than hand-patching each chapter.
- **Verify before ship** — no chapter is "done" until its examples PASS and the reviewer ACCEPTs.

## Incremental updates

Do not run Architecture/Shell or the from-scratch driver for an existing-book refresh.
Preserve the book brief, structure, design, stable slugs, and the Meridian narrative.

### 1. Freeze the release range and impact

Read the latest published book edition, `content/version.yml` (including its `apm_version`),
the changelog, TOC, and chapter evidence. Run `scripts/check_upstream.py` to discover the latest
stable APM release or resolve an explicit target. Its JSON includes **every stable release
after the baseline through the target**, plus pinned changelog and comparison links.
Treat network/discovery errors as blockers, never as "already current."

Keep discovery JSON and the working impact table in the session artifacts directory. Read the
release notes and relevant docs for the full gap, not only `releases/latest`. Map changes against
both the TOC's `apm_features` and existing prose/examples. Every change needs an action or an
explicit no-impact/out-of-scope rationale. Prioritize breaking changes, changed defaults,
security/governance claims, and obsolete caveats before adding features.

The existing `apm_version: "0.23.1"` baseline is grounded in the v1.1 chapter research. Do not
infer this value from the root skill lockfile or silently substitute an installed CLI version.
If an edition has inconsistent chapter baselines, inventory them and review from the oldest
relevant version; retain per-chapter evidence rather than pretending everything was reverified.
Freeze one target for the run; a newer release arriving mid-wave belongs to a later update.

`check` mode stops here, read-only. If the gap has no reader-facing impact, stop without changing
the edition, date, or reviewed baseline. Do not create a tooling-only content release.

### 2. Run only affected chapter waves

Seed session `todos` / `todo_deps` for impacted chapters and their cross-cutting dependencies.
Pass the frozen upstream range, chapter spec, impact rows, artifact paths, and an explicit
completion condition to each agent. Start with one representative affected chapter.

1. `book-architect` is conditional: use it only if scope, prerequisites, or the TOC must change.
2. `apm-cli-explorer` uses `apm-environment-setup` to prepare one **version-pinned** executable.
   Reuse it across waves; give each verifier a separate scratch project.
3. Run `theory-researcher` and `apm-cli-explorer` in parallel for the changed material.
   Preserve still-valid research and explicitly replace superseded claims.
4. `chapter-author` edits only affected source fragments and example files. New features must
   serve existing learning objectives or an architect-approved change, not turn into a flag dump.
5. `code-verifier` executes every affected example and the shared examples its changes can
   invalidate. Record exact commands, exit codes, relevant output, version, and PASS/FAIL or
   `SKIPPED-needs-network` with a specific reason. Private/publishing examples stay skipped;
   a real behavioral failure must not be relabeled as a network skip.
6. `chapter-reviewer` reads the updated chapter, research, and fresh verification report.
   Loop REVISE findings through author -> verifier -> reviewer until ACCEPT.
7. `frontend-builder` integrates accepted fragments and regenerates the existing site.
   Checkpoint only the accepted chapter, its examples, and evidence; never `git add -A` over
   unrelated work.

Persist final verification and review reports under
`content/research/updates/<book-edition>/`, with chapter IDs in filenames. Record the frozen
APM range, affected files, exact example IDs, statuses, and verdicts. Raw logs and temporary
projects remain in session artifacts. Do not write PASS or ACCEPT on another agent's behalf.

### 3. Integrate and prepare, without publishing

Run the cross-chapter review for terminology, version-specific guidance, prerequisites,
links, and shared examples. Reverify anything changed by integration. Leave unchanged examples'
old verification stamps intact; do not claim that a build proves CLI behavior.

Only after all affected chapters and integration ACCEPT, follow `/release-content` in **prepare**
mode. Set `content/version.yml`'s edition/date and reviewed `apm_version` together, and add the
matching content-only changelog section. A relevant unresolved breaking change blocks advancing
the baseline; explicitly out-of-scope features may be deferred with rationale.

Require release preflight and a successful HTML/PDF build. Commit the accepted update and
reports locally, then stop with the exact commit and remaining publication steps.
The PR/release workflows enforce metadata/provenance/build checks; they do not execute the
agent examples or judge prose. Actual verifier and reviewer evidence is still mandatory.

### Resume rules

Resume from the saved target, impact matrix, reports, and Git checkpoints, not a new "latest"
lookup. Skip completed work only while its chapter/example inputs and target are unchanged.
Any later edit invalidates the affected verification/review verdicts. If previous state cannot
be established, rediscover and reassess explicitly; do not manufacture a completed checkpoint.
