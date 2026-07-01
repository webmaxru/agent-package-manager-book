---
name: book-orchestration
description: The wave-based workflow that coordinates the book agent team (book-architect, theory-researcher, apm-cli-explorer, chapter-author, code-verifier, chapter-reviewer, frontend-builder) to produce the APM interactive book end to end. Use to plan and run the production pipeline for one or more chapters.
---

# Book Orchestration

This skill describes **how the book agents work together** to build the Agent Package Manager (APM)
interactive book. It is the orchestration layer: who is dispatched, in what order, with what
hand-offs and checkpoints. (This is a starting scaffold — refine as the project evolves.)

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
   introspectable, plus a sample project to inspect.

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
