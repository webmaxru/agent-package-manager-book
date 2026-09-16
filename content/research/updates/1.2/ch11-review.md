# Chapter 11 editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-ch10-ch12`)

**Verdict: ACCEPT. Must-fix list: none.**

**Source:** `content/chapters/enterprise-at-fleet-scale.html`

**SHA256:** `4a77f11386578721414e4797077d4eb17073919b55cc56b351141660e970ede5`

The reviewer read the instructions, brief/TOC, impact matrix, theory/reference
notes, current fragments, and fresh verification reports, not a site build.
The reported digest agrees with `RunRoot/verify-ch10-ch12/final-source-checks.json`.
Frozen upstream source: `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`.

## Assessment

Fleet ownership and protected enforcement lead commands. Payments, Onboarding,
Merchant Dashboard, staged rollout, and leadership metrics remain coherent.
Cold audit permits scratch hydration and fails when acquisition is unavailable;
mandatory `--no-drift` advice is retired. Frozen restore, audit coverage,
direct-only pin rules, consumer fail-closed posture, and the environment-policy
bypass remain appropriately bounded.

`ch11-ci-current` separates setup-only CLI acquisition from explicit audit,
pinning CLI 0.31.0 and Action v1.10.0 at
`d723bb64ed70c135bbaf87d126b721dd2dae0439`. `ch11-ghaw-import` supplies a concrete
Copilot target matching the engine and overrides shared default 0.28.0 with
0.31.0 for both pack and restore. Isolation, absent automatic host
manifest/lock/policy carry-over, and current-repository-only token scope are
explicit.

Evidence: [ch11-verification.md](ch11-verification.md), operations
OP07.2/OP08.3/OP09.1-3, producer sections 8-10, and `integration-contract.json`.

## Retained findings and scope

- **HIGH retained F10.2:** `ch11-ghaw-compatibility` does not generalize the
  instruction's byte-matched local success to skills or full workflows.
  Shared-skill delivery remains FAIL, not a network skip.
- **HIGH retained F10.1:** `ch11-audit-coverage` does not represent native
  registration as successful audit replay.

No author correction is required. Preserve both disclosures; upstream
follow-up ownership is recorded in Chapter 10's review.

Current local recipes have fresh independent records, including the
frozen/audit pair rather than assumed Ch5 reuse. Actions/rulesets/SARIF upload,
private authority discovery, corporate proxy access, and gh-aw compilation and
runtime retain specific skips. Static validation is not execution.

The six sections, terminology, Meridian's harnesses, and leader track agree
across Chapters 10-12 and relevant Chapter 8/9 evidence. Acceptance covers
accurate teaching, not whole-book integration, publication, or skipped
infrastructure.
