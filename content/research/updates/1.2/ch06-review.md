# Chapter 6 editorial review - book 1.2 / APM 0.31.0

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-ch06-ch07`)

**Verdict: ACCEPT. Findings and must-fix list: none.**

**Source:** `content/chapters/the-lockfile-and-reproducibility.html`

**SHA256:** `45aa09e83b7d2b64353921c8b7f13b37d6b68dffa71181ad1659432aaf6662e2`

The reviewer read the book guidance, impact matrix, edition theory/reference
notes, current chapters, and fresh verification reports. Frozen APM source:
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`. The Chapter 6/7 reports share
16 current blocks and 168 invocations, not separate totals per chapter.
Recorded outcomes and reproduced defects do not certify the upstream CLI.

## Evidence and assessment

- `ch6-identity` and `ch6-current-lock` distinguish Git commits, local paths,
  registry archives, dependency/workspace owners, canonical deployment rows,
  and compatible hash maps. The displayed lock excerpt is not a restore input.
- New-lock timestamp omission, retained legacy timestamps, Git-semver
  `resolved_at`, and SBOM timestamps remain distinct. The exercise compares
  complete lock bytes and six native outputs. Normalized deployed text does
  not imply normalized package-tree bytes or cross-harness equality.
- `ch6-frozen-boundary` distinguishes missing-lock/Git refusals from newly
  declared local dependencies that can deploy and rewrite an old lock.
  Equivalent refs, transitive promotion, native edits, and MCP cases retain
  their boundaries. CI guidance adds contract comparison and separate audit.
- Existing ownership survives the deleted-canary lock-only test; a fresh
  resolution-only lock has no deployment history. Cleanup belongs to install.
  Find is provenance lookup and SBOM export is inventory, not authentication.
- Public cold audit and failed acquisition are distinct. Warm/local and
  MCP-audit success do not become offline or universal native-integrity claims.

Evidence: [ch06-verification.md](ch06-verification.md) and operations OP06.1,
including fresh lock-only, provenance, restore, hash, and cold-acquisition
controls.

The concept-first progression, Priya's forgotten regenerated Git lock,
Meridian's three targets, and leader track remain intact. Chapter 7 correctly
follows replay with deliberate maintenance. The historical 0.23.1 provenance
snapshot is not restamped.

Impact surfaces E06-lock/frozen/lock-only/find are addressed without reopening
unrelated private/global/runtime or historical coverage. The reviewer ran no
commands and made no edits, agent dispatches, commits, or publication.
This is chapter acceptance, not whole-book integration approval.
