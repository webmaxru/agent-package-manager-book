# Chapter 9 editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-ch08-ch09`)

**Verdict: ACCEPT. Must-fix list: none.**

**Source:** `content/chapters/governance-and-policy.html`

**SHA256:** `11391907af254a6c13866d431d40100043d1b43f6857dd4dc3e3e70091dbd01a`

The reviewer read [ch09-verification.md](ch09-verification.md), assembled at
2026-09-16 02:26 UTC, edition theory and operations/core references, the impact
matrix, and policy fixtures. All twelve current code blocks are accounted for.
No commands were executed during this review.

## Findings and changed claims

No unresolved material chapter findings or author fixes remain. Documented
policy defects remain product limitations, not repaired guarantees.

- The schema uses `compilation.target.allow`. Unknown top-level keys warn
  without registering rules; malformed known types fail. Diagnostic exit 0
  is distinct from successful resolution and compliance.
- Local extends works. Parent block/deny/require restrictions survive empty
  and null child lists; empty extends-chain metadata is not mistaken for an
  absent merge. Warm HTTPS evidence preserves strict fields and TTL.
- Canonical GitHub/registry casing is not generalized to refs, subpaths,
  local paths, or MCP identities. Untested host discovery and policy-cache
  locations are described as source contracts.
- Explicit policy beats `--no-policy` but not `APM_POLICY_DISABLE=1`, even
  with consumer fail-closed configuration. Missing checks are an authority
  failure; bypass controls are explicitly not configurations to copy.
- First-fetch authority, raw policy-byte hashes, and policy freshness remain
  distinct. Default malformed/fetch/hash cases can skip enforcement with exit
  0; consumer block makes the tested failures fatal. Stale-rule compliance
  does not certify freshness.
- The negative pin test uses a genuinely direct unbounded constraint.
  Plural-target false-negative coverage and the singular control's additional
  failures remain visible. The primary warn/block rehearsal isolates one
  missing requirement against a clean baseline.

## Retained limits and consistency

Mandatory content-hash requirements can fail even in warn mode. Parsed but
unenforced `mcp.trust_transitive` is not a new guarantee. Status success,
baseline-only success without an authority, and loopback controls do not
certify production governance or private-host discovery.

Private GitHub/GHES, GitLab, ADO discovery, policy publication, private standards,
and live MCP retain specific unavailable scopes. Loopback HTTPS negatives are
real tested outcomes, not network excuses. Historical policies retain their
0.23.1 boundary.

Organizational authority precedes schema; effective inheritance precedes
rollout. Meridian keeps its three harnesses, valid `.github` authority location,
and two-sprint warn/measure/remediate/block beat. The leader track emphasizes
ownership and change management, not self-granted exceptions. Direct pinning,
protected CI inputs, fetch posture, and runtime handoffs agree with Chapters
7-8, 10, and 11. No in-scope breaking change is misleadingly deferred.

Acceptance is a chapter gate, not certification of private infrastructure,
every policy feature, whole-book integration, or publication.
