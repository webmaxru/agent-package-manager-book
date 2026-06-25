---
description: Kick off authoring a single playbook chapter end-to-end through the agent team.
---

# New Chapter

Produce one complete, reviewed chapter of the MAF interactive playbook.

**Chapter:** <chapter number + title>
**Learning objective:** <what the reader can do afterward>
**MAF components to cover:** <list, or "decide from the architect's spec">

Run the per-chapter pipeline from the `playbook-orchestration` skill:

1. Confirm/create the chapter spec with `playbook-architect` (objective, sections, dependencies).
2. In parallel:
   - `theory-researcher` → cited concept brief.
   - `maf-library-explorer` → component notes + minimal examples (introspect the installed
     `agent-framework`; record the version).
3. `chapter-author` → write the chapter weaving theory + library, following
   `.github/instructions/playbook-content.instructions.md`.
4. `code-verifier` → run every example until PASS (or SKIPPED-needs-creds). Loop fixes back.
5. `chapter-reviewer` → ACCEPT/REVISE with ranked findings; route must-fixes to the author.
6. `frontend-builder` → wire the accepted chapter into the site navigation.
7. Checkpoint: commit chapter content, examples, and the review verdict.

Do not ship the chapter until all examples PASS/are-marked and the reviewer returns ACCEPT.
