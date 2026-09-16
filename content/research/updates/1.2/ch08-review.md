# Chapter 8 editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-ch08-ch09`)

**Verdict: ACCEPT. Must-fix list: none.**

**Source:** `content/chapters/security-by-default.html`

**SHA256:** `21efe99d2991b10b85e8ce00c0d569bccbe66ff71422756172eeb902d04af450`

The reviewer read [ch08-verification.md](ch08-verification.md), assembled at
2026-09-16 02:26 UTC, edition theory and operations/core references, the impact
matrix, and current fixtures. All nine current code blocks and the corrected
inline audit control have fresh execution, validated independent reuse, or
explicit scope limitations. No commands were executed in review.

## Findings

No unresolved material chapter findings or author fixes remain. The scan
evidence error at `ch08-package-audit-scope` is resolved, not waived:
`_local/package` returned success without scanning files. The corrected
`audit ./package -f json` exited 0 and scanned three files, including a rerun
against the final source. The chapter explains why the earlier green exit
proved nothing about coverage.

## Changed-claim reconciliation

- Authorized deployable source is distinguished from the entire cache and a
  pre-any-write boundary. README/unselected-skill exclusion and partial
  deployment before an overall failure support the distinction.
- Character severity and integrity drift are separate. Correctly hashed
  Warning-only content produced bare/CI 2/0; ordinary deployed edits produced
  0/1. Stripping deployed copies is not a durable authored-source fix.
- LF-normalized deployed-text hashes and raw materialized package-tree hashes
  are distinct. Invalid ownership, unrecorded governed content, user-owned
  hooks, and APM-owned sidecars are not one drift rule.
- Direct/depth-two trust is distinct from executable approval. Actual local MCP
  configuration despite default denial and parked-hook replay failure remain
  visible. Approved-state success is not presented as a repair or workaround.
- Harness hooks, lifecycle execution, and bin consent remain distinct. Preview
  side effects and the source-only Windows admin path are bounded. The exact
  PE's NotSigned result is not displaced by signing release notes or checksums.

## Retained limits and consistency

Native MCP absence/argument edits can escape CI audit; frozen repairs the
tested absence but preserves the edit. Direct inspection remains necessary.
The additional nested configuration-consistency audit failure is not certified
away by the installation-depth table. Canonical approval is not publisher
authentication or an ordinary per-release grant. Cold hydration failures are
failures, not skips; credential-binding mismatch can still allow anonymous
requests.

Private Meridian services retain specific network skips. Harness runtime,
global bin deployment, and machine-admin policy were not exercised.
Historical evidence is not restamped. The older operations reference selector
is superseded by the fresh verification correction.

Six sections, the four-property vocabulary, concept-first progression,
Meridian's capability-review beat, and the leader track remain intact. Hash,
audit, and governance handoffs agree with Chapters 6-7 and 9. This acceptance
is a chapter gate, not whole-book integration or security certification.
