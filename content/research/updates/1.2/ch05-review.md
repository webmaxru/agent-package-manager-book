# Chapter 5 final editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-ch05-final`)

**Verdict: ACCEPT**

**Reviewed source:** `content/chapters/install-and-restore.html`

**Current SHA-256, computed by the orchestrator after the author's final edit:**
`c06627ac2367a41f9d8a427a6021b695c4c4d28237ca4c3cda951a56effe1e25`

## Scope and evidence

This records the reviewer's returned final recheck of R1/R2, retaining the prior
full review's conclusion that no technical or code blocker remained. The reviewer
read the current chapter, `ch05-verification.md`, the edition theory/core
references, and relevant impact/deferred-scope decisions. This is Chapter 5 pilot
acceptance, not edition-wide integration or publication approval.

The reviewer did not compute the source hash; the caller supplied the current
identity above rather than reusing the prior reviewed hash.

## Findings resolved

**MEDIUM R1 - CLOSED.** The edition introduction and opening, frozen-boundary,
and current-restore comments no longer say delta verification/review are awaited.
The introduction records the independent check date. Comments retain the frozen
local-path exception, audit limitation, and successful literal-sequence evidence
without contradicting the completed code gate. No further author change.

**LOW R2 - IMPROVED / CLOSED.** The targeting passage introduces an eligible APM
package with a co-located legacy `plugin.json` marker before the marker-free
control. It states that only that marker was omitted before the control's first
install, and distinguishes the clean control from the marker-present audit
failure. No further author change.

**Open editorial findings: none.**

## Code gate and retained boundaries

- Existing independent code gate: **PASS**, covering unchanged executable inputs,
  16 code blocks, and eight canonical fixture files. The original evidence
  records 143 invocations and 562.791 seconds summed native runtime, including
  actual failures, not 143 blanket passes. All twelve displayed fixture-sequence
  commands have recorded exit 0. Status-only prose changes require an equivalence
  record, not rerecording those executions.
- Frozen installation still requires an existing lock but provides limited
  structural checks. A newly declared local dependency can deploy and rewrite
  the lock with exit 0. Exercise and closing guidance retain that exception and
  distinguish content audit.
- Native-plugin replay and the separate legacy-marker replay mismatch remain
  actual **FAIL** results, not network skips or repaired upstream behavior.
  The legacy case identifies mutation of `apm_modules/`, not authored sources,
  the lock, or deployed files.
- The full historical Meridian graph and live Copilot recording retain their
  0.23.1 stamps, hashes, and timings. Fictional/private clone access, live
  Copilot execution, and native-plugin loading retain their specific skips.

## Consistency

The six slots, concept-before-command progression, four-command habit, Meridian
v0.2.0 milestone, and engineering-leader track remain intact. Portability means
supported target-native context, not cross-harness byte equality. Stable links
and qualified Chapter 6/7 handoffs remain appropriate. Later cross-chapter
propagation and deferred depth are not certified by this pilot gate.

The reviewer performed no CLI executions, edits, commits, agent dispatches, or
publication and inferred no verification result from a site build.

**Final decision: ACCEPT. Must-fix list: none.**
