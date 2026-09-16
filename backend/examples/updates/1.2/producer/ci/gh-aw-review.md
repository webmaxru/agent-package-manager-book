---
# Documentation sample: SKIPPED-needs-network.
# Vendor the canonical shared/apm.md from APM v0.31.0, then compile with
# a separately reviewed gh-aw compiler. Neither compile nor a runner was run here.
on:
  workflow_dispatch:
engine: copilot
permissions:
  contents: read
imports:
  - uses: shared/apm.md
    with:
      apm-version: '0.31.0'
      target: copilot
      token-source: github-token
      packages:
        - microsoft/apm-sample-package/.apm/instructions/design-standards.instructions.md#fb2851683be0e0e7711421d518bd8dba23b0b1f6
---

# Review the standards

Summarize the installed design standards. Do not modify repository files.

<!--
This deliberately uses the one-instruction CLI compatibility control.
The shared import ignores the host apm.yml and builds its own dependency set.
This is NOT a general skills-bundle compatibility claim: the reference records
the legacy Copilot .agents/skills omission observed with APM 0.31.0.
-->
