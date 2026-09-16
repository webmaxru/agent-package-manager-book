# Chapter 3 final editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-core-wave`)

**Verdict: ACCEPT. Open findings / must-fix list: none.**

**Source:** `content/chapters/primitives-and-harnesses.html`

**SHA256:** `cd9c17d28a240a3cf82f34239d6eec05faa11215825c8a400fca7231e7362741`

## Closed findings

- **F3.1:** `ch3-mcp-boundary` visibly records audit exit 1 and
  `nested-checkout-probe: in manifest but not in lockfile`. Correct depth-two
  withholding is distinct from an audit-clean result.
- **F3.2:** the MCP comment attributes the explorer observation correctly and
  links the independent verification report.
- **Procedural hold:** [ch03-verification.md](ch03-verification.md) now supplies
  the source-specific PASS required to close the withheld verdict.

The prior full review stands. Concept-first vocabulary, Meridian's typed
inventory, leader track, and Chapter 4 handoff are preserved. The current
onboard-skill example retains its narrow successful evidence.

`mcp-nested-audit` remains an actual FAIL, not a network skip. Native registration
does not certify runtime loading or audit cleanliness. Historical 0.23.1
material remains historical.

## Closure evidence

The reviewer read the updated reports, corrected passages, source diffs, and
`RunRoot/verify-core-wave/prose-delta/check.json`. The receipt dated
`2026-09-16T02:32:57.436453Z` confirms exact reconstruction from the five
requested Chapter 3/4 corrections: 17 code blocks, 38 captured fixture files,
and operative control inputs unchanged; zero new APM invocations.

No further edits or reruns are requested. This closes the chapter verdict,
not edition-wide integration or publication.
