# Chapter 4 final editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-core-wave`)

**Verdict: ACCEPT. Open findings / must-fix list: none.**

**Source:** `content/chapters/the-manifest-apm-yml.html`

**SHA256:** `c0f3d81788556838e3f55b1adc225b9716231786040544aa98ab098e73c41005`

## Closed findings

- **F4.1:** `ch4-local-source-selection` visibly identifies audit exit 1 caused
  by missing `pkg/apm.yml`, preserving the narrower successful skill selection.
- **F4.2:** `ch4-includes-boundary` discloses combined-layout audit disagreement
  across shared and Claude skill paths. Successful packing remains distinct
  from failed replay and the clean single-layout instruction fixture.
- **F4.3:** the opening provenance comment uses a symbolic session-artifact
  location instead of a workstation-specific path.
- **Procedural hold:** [ch04-verification.md](ch04-verification.md) now supplies
  the required source-specific PASS.

The prior full review stands. Operation-specific includes, Meridian's local-only
v0.1.0 milestone, leader track, and Chapter 5 handoff remain intact. The main
instruction example retains its clean, source-specific evidence.

`decl-path-options-audit` and `pack2-source-audit` remain actual FAIL results.
Native-plugin/legacy-marker limitations and historical 0.23.1 stamps are
unchanged, not certified away.

## Closure evidence

The reviewer read the updated reports, corrected passages, source diffs, and
`RunRoot/verify-core-wave/prose-delta/check.json`. The receipt dated
`2026-09-16T02:32:57.436453Z` confirms exact reconstruction from the five
requested Chapter 3/4 corrections: 17 code blocks, 38 captured fixture files,
and operative control inputs unchanged; zero new APM invocations.

No further edits or reruns are requested. This closes the chapter verdict,
not edition-wide integration or publication.
