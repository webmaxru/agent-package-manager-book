# Final integration review - book 1.2

**Date:** 2026-09-16

**Reviewer:** chapter-reviewer (`review-full-integration`)

**Verdict: ACCEPT. Open findings and must-fix list: none.**

This records the reviewer's completed full cross-chapter assessment and final
F1-F3/G1 delta closure. Unchanged chapters and examples were not reviewed or
executed again during closure. Scope: the existing twelve-chapter structure,
reviewed baseline APM 0.23.1 through exactly 0.31.0, upstream source
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`.

The review was read-only: no executions, edits, commits, agent dispatches,
or publication.

## Findings closed

| Former finding | Final disposition and evidence |
| --- | --- |
| HIGH F1 - raw-download versus checkout checksum | CLOSED. Producer reference section 9 uses raw Git/LF digest `fb036a7a688eb24d0fb9fa0749dbf1840bd9e7c025ab95ca7546859f150727d8` for the download and identifies `6ebe127ee1ae527249b81239a8fa52f3a3ead298042b2d43122d6a68faf0f3ae` as the CRLF scratch-copy digest. The Ch11 verification appendix corroborates both against the pinned receipt. |
| MEDIUM F2 - Meridian carry-forward | CLOSED. Ch10 makes the standards requirement prospective and labels ex16 a reduced historical illustration, preserving earlier packages, `local-fetch` MCP, and the review script unless removal is separately reviewed. Ch10's delta confirms twenty unchanged code blocks and 38 fixture files. |
| MEDIUM F3 - inaccurate Chapter 11 back-reference | CLOSED. Ch12 points to the frozen upstream gh-aw guide as a source-only alternative requiring separate validation. Its appendix confirms one prose/link replacement, unchanged IDs, and zero executable blocks. |
| MEDIUM G1 - current Chapter 5 provenance | CLOSED. The privacy delta binds current `286f2d6a...` to accepted `c06627ac...`: only opening-comment lines 16/20 changed; every subsequent byte, sixteen code blocks, and eight Core files are unchanged. |

These closures add zero APM invocations, downloads, or gh-aw compilations.
They preserve original evidence rather than restamp it. Ch7's earlier closure
also stands: the canonical `./package` control scanned three files, whereas
`_local/package` retains its explicit no-files outcome. Seven blocks and
47 inputs were unchanged.

## Accepted current source identities

These are recorded raw Windows working-tree SHA256 values, not hashes computed
by the reviewer or final publication-commit identities.

| Chapter | Accepted SHA256 |
| --- | --- |
| 01 | `61b7d7e0b15f5f9b36c2bb013aeb9cad61578a2409bf5bcd6c8f5675e8713c89` |
| 02 | `a4e626f634b7a930483e233023e79bf61f092bbd95e316c33f91f253f8260ff7` |
| 03 | `cd9c17d28a240a3cf82f34239d6eec05faa11215825c8a400fca7231e7362741` |
| 04 | `c0f3d81788556838e3f55b1adc225b9716231786040544aa98ab098e73c41005` |
| 05 | `286f2d6a873b7152a09033a0e5c2330bbef8004a42818e103e6b7e594e9c3d1a` |
| 06 | `45aa09e83b7d2b64353921c8b7f13b37d6b68dffa71181ad1659432aaf6662e2` |
| 07 | `e45b3d6410caf0b030fe90da58660008c8ce088d6b1f2656f5af94620fe75c72` |
| 08 | `21efe99d2991b10b85e8ce00c0d569bccbe66ff71422756172eeb902d04af450` |
| 09 | `11391907af254a6c13866d431d40100043d1b43f6857dd4dc3e3e70091dbd01a` |
| 10 | `f42b35736a232965057c72b754b87bbe9e105f759b03de01ef2f66ef80b10dee` |
| 11 | `4a77f11386578721414e4797077d4eb17073919b55cc56b351141660e970ede5` |
| 12 | `4de95a5d3d756c538d1137e0b42c4516f915b23d47bee9288d828ed997efc1fa` |

Reviewed TOC SHA256:
`b46c306d6781692d40e5a9b4eef3b86225f815232abfcf4d476150b157ac80ed`.
Producer-reference SHA256:
`6a8bac3280c02b5340df845baf3db7f11b5cf8eeb356ef0179015c9539b0cc0c`.

[source-identities.json](source-identities.json) separates previous review
identities, current sources, canonical LF hashes, and expected Git object IDs.
Ch5/10/12 acceptance extends their prior reviews through the examined deltas;
older hashes retain their historical scope. The publication controller must
still compare committed blobs with this bridge.

## Matrix coverage and consistency

The ten-release impact-ledger reconciliation stands without unresolved
integration findings.

- **Ch1-5:** concept-before-command holds. Four properties versus three
  promises, primitive/package/harness distinctions, discovery/apply, target
  selection, bootstrap persistence, and classification align.
- **Ch2/4-8/11:** source identities remain distinct. Frozen's local-path
  exception propagates. Timestamp omission, legacy timestamps, semver/SBOM
  clocks, deployed-text normalization, and raw package-tree hashes are scoped.
- **Ch3/7/8/11:** freshness, consent, and integrity remain separate. Hooks,
  lifecycle scripts, bin consent, MCP depth, scanning, ownership, and audit
  modes agree.
- **Ch9/11:** schema diagnostics, local inheritance, cache restrictions,
  direct-only pins, plural-target coverage, consumer fetch posture, and
  environment bypass are accurately qualified.
- **Ch10-12:** default versus Agent Plugins output, one-shot ZIP deployment,
  catalog checks, registries/proxies, and isolated gh-aw imports are distinct.
  Concrete targets and explicit 0.31.0 reach both stages without blanket
  compatibility claims.

Twelve slugs, objectives, prerequisites, and six slots remain intact; TOC changes
stay within feature coverage. Meridian's accumulated decisions survive producer
extraction explicitly. Leadership guidance preserves ownership, risk, rollout,
and measurement without turning historical timings into current benchmarks.

Historical 0.23.1 examples and the July competitor snapshot remain historical.
Current fixtures do not silently replace old full graphs or runtime recordings.
Deferred target walkthroughs, global/admin execution, LSP/container details,
external scanners, exhaustive references, registry administration, and private
authorization matrices do not require expanding this edition.

## Evidence limits and publication handoff

Acceptance concerns accurate teaching and attribution, not repaired upstream
guarantees. Frozen exceptions, native/legacy replay, local MCP and parked-hook
behavior, native audit gaps, registry cache contamination, Windows cleanup,
policy bypass/fetch/target/freshness gaps, and legacy shared-skill omission remain
bounded disclosures. **Claim-gate PASS means the stated outcome, including
failure, was reproduced. It is not upstream security certification.**

[checkout-verification.md](checkout-verification.md) separately records five
primary fixtures and a representative ZIP round-trip: 31 invocations, actual
Git/LF inputs, unchanged original locks. This is native Windows execution with
LF sources, not Linux/WSL/POSIX or universal cross-platform verification. The
generated-lock/catalog LF attributes are appropriately scoped.

Private services, paid runtimes, Actions/rulesets, SARIF upload, gh-aw compilation,
and package publication retain specific example-execution exclusions. Those
exclusions do not prohibit publishing the reviewed book.

The content gate is clear. Remaining preparation/publication steps are to
advance metadata/changelog, require the frontend HTML/PDF build and preflight,
assert committed chapter/TOC identities, and publish only through the separately
authorized operation. The old edition metadata at review time was intentionally
not a content-review blocker.

**Final decision: ACCEPT at the recorded identities. No further author fixes or
duplicate full review are required.**
