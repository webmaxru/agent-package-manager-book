---
description: Kick off authoring a single APM book chapter end-to-end through the agent team.
---

# New Chapter

Produce one complete, reviewed chapter of the APM interactive book.

**Chapter:** <chapter number + title>
**Learning objective:** <what the reader can do afterward>
**APM features to cover:** <list, or "decide from the architect's spec">

Run the per-chapter pipeline from the `book-orchestration` skill:

1. Confirm/create the chapter spec with `book-architect` (objective, sections, dependencies).
2. In parallel:
   - `theory-researcher` → cited concept brief.
   - `apm-cli-explorer` → feature notes + minimal examples (introspect the installed `apm` CLI;
     record the version).
3. `chapter-author` → write the chapter weaving theory + tool reference, following
   `.github/instructions/book-content.instructions.md`.
4. `code-verifier` → validate/run every example until PASS (or SKIPPED-needs-network). Loop fixes back.
5. `chapter-reviewer` → ACCEPT/REVISE with ranked findings; route must-fixes to the author.
6. `frontend-builder` → wire the accepted chapter into the site navigation.
7. Checkpoint: commit chapter content, examples, and the review verdict.

Do not ship the chapter until all examples PASS/are-marked and the reviewer returns ACCEPT.
