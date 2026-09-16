# Chapter 1 independent delta verification — book 1.2 / APM 0.31.0

**Verdict: PASS, within the historical-code / current-prose scope below.**
No historical illustration was executed or newly certified with 0.31.0.
No chapter or fixture was edited. This is a code-verification gate, not
reviewer acceptance or publication approval.

## Source identity and scope

| Item | Value |
| --- | --- |
| Chapter | `content/chapters/the-context-problem.html` |
| Source SHA256 | `61b7d7e0b15f5f9b36c2bb013aeb9cad61578a2409bf5bcd6c8f5675e8713c89` |
| Current behavior target | Exactly **0.31.0** |
| Historical illustration stamp | **0.23.1**, retained; no current execution |
| Verification date | 2026-09-16 UTC |
| Changed executable blocks | **0**; both original blocks retain their content and historical captions |

The two code blocks match their Git-HEAD predecessors after only Git's
LF-to-worktree-CRLF checkout conversion. There are no code-content changes.
The conceptual manifest is explicitly an illustration, not an installed
project. This preservation check does **not** establish a new schema/install
result for that sketch.

Read inputs: the four updated chapter sources and their IDs/comments;
`core-reference.md`, `theory.md`, `operations-reference.md`,
`producer-reference.md`, and `ch05-verification.md`. Original source bytes,
reference hashes, extracted blocks, and historical comparisons are retained.

## Execution and bounded reuse

Aliases avoid workstation identities in published artifacts:

| Alias | Meaning |
| --- | --- |
| `RunRoot` | Orchestrator's session artifact directory, `files/book-v1.2` |
| `Wave` / `N` | `RunRoot/verify-core-wave`; new logs are `N/logs/<id>.json` |
| `Prior` / `R` | `RunRoot/verify-ch05`; reused logs are `R/logs/<id>.json` |
| `Scratch` | This wave's owned short temporary root, recorded in `Wave/runtime-layout.json` |
| `Core` | `backend/examples/updates/1.2/core` |

Every command table gives exact arguments after `& $Apm`:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

The executable SHA256 is
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
It was invoked by its absolute path, never resolved from PATH.

Across the **entire Chapters 1–4 wave**, there were **78 new native
invocations**: **9 version guards**, **7 help commands**, and **62 narrowly
selected example/control commands**, totaling **241.350 s** native runtime.
The wave did not rerun the original explorer or 143-command Ch5 suite.
**53 existing independent Ch5 records**, with **13 original version guards**,
were read and checked instead. Their original command runtime is **239.435 s**,
not new execution time. Do not add the shared evidence tables across reports
as though each were a separate execution.

`Wave/reuse-evidence.json` verifies:

- All eight current Core fixture files, including complete locks, equal the
  independently captured `Prior/canonical-core.zip` bytes.
- Exact first-install input inventories, argv, subsequent state continuity,
  native stdout/stderr bytes, resulting ZIP snapshots, executable identity,
  and preceding version guards agree.
- Historical content stays historical. Explorer reports supply fixture
  provenance and hypotheses, **not independent PASS stamps**.

The read-only reuse check took **3.136 s**, exit **0**; final raw/source
integrity checks took **3.379 s**, exit **0**. New commands used short
**normal CWDs**, separate batch HOME/APM cache/config/temp directories,
allowlisted credential-free environments, disabled Git credential helpers,
and no host `gh` or agent-runtime PATH entries. No root dependencies,
host/global configuration, TLS policy, or edition/site files were changed.

## Per-example disposition

| Example ID / path | Status | CLI stamp / evidence | New vs reused |
| --- | --- | --- | --- |
| `Chapter#ch1-unmanaged-context` | **PASS — historical preservation only** | Original 0.23.1 illustration; current CLI exit/runtime **not applicable** | Read-only comparison; not executed |
| `Chapter#ch1-conceptual-manifest` | **PASS — historical preservation only** | Original 0.23.1 conceptual manifest; current CLI exit/runtime **not applicable** | Read-only comparison; not executed |
| One-context/many-harnesses prose; `Core/local-instruction` | **PASS**, native projection scope | 0.31.0; exact local instruction/manifest and genuine lock | Reused independent Ch5 execution |
| Legacy versus native-plugin prose | **PASS**, registration distinction only | 0.31.0; native registration succeeds, its known audit **FAIL** remains distinct | Reused independent local controls; no runtime loading |
| Authorized deploy-set scanning prose | **PASS**, scoped positive/negative assertions | 0.31.0; source-only and unselected material excluded, selected Critical-class marker blocked | New shared controls |
| `includes: auto` / install-filter explanation | **PASS** | 0.31.0; canonical local fixture plus explicit-list control | Reused fixture + new control |
| Host-specific policy-location preview | **PASS — frozen-source contract check** | Source commit `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`; not live org enforcement | Source review, not a CLI execution stamp |

## Exact supporting commands and outcomes

All CLI entries below used **0.31.0**. Reused execution dates remain those
in the original Ch5 records.

| Origin / record ID | Input scope / CWD | Command | Exit | Native seconds |
| --- | --- | --- | ---: | ---: |
| R `local-local-instruction-install` | Source-only `Core/local-instruction`, prior `p/li` | `install` | 0 | 4.584 |
| R `local-local-instruction-restore` | Same resulting project | `install` | 0 | 2.007 |
| R `local-local-instruction-frozen` | Same resulting project | `install --frozen` | 0 | 2.429 |
| R `local-local-instruction-audit` | Same resulting project | `audit --ci` | 0 | 3.031 |
| R `native-metadata-install` | Exact `core-probes/projects/portable-metadata` input | `install` | 0 | 5.313 |
| R `native-metadata-restore` | Same installed native plugin | `install` | 0 | 3.372 |
| R `native-metadata-audit` | Same installed native plugin | `audit --ci` | **1** | 2.067 |
| N `decl-includes-install` | `Scratch/p/il`: one listed and one unlisted instruction | `install` | 0 | 4.073 |
| N `decl-includes-audit` | Same six native rule outputs | `audit --ci` | 0 | 2.837 |
| N `scan-source-only-install` | `Scratch/p/sr`: Operations repro sources + inert README marker | `install` | 0 | 3.946 |
| N `scan-source-only-audit` | Same installed project | `audit --ci` | 0 | 1.861 |
| N `scan-selected-skill-install` | `Scratch/p/ss`: `skills: [clean]`, inert marked skill unselected | `install` | 0 | 2.507 |
| N `scan-selected-skill-audit` | Same selected clean skill | `audit --ci` | 0 | 2.168 |
| N `scan-flagged-selected-blocked` | Same source, selection changed to `[flagged]` | `install` | **1, expected** | 2.260 |

The local instruction projected to `.github/instructions/`,
`.claude/rules/`, and `.cursor/rules/` with different native bytes, not
universal byte parity. Its unchanged complete lock SHA256 is
`0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa`.

The source-only README remained in the installed package cache while the
clean primitive deployed. Selecting the harmless character-class test skill
instead produced these exact diagnostic lines:

```text
[x]   Blocked: ./package contains critical hidden character(s)
  |-- skills/flagged/SKILL.md
  |-- Fix the reported file(s) in the package source, then reinstall
[x] Installation failed in 0.3s. No install transaction changes were committed.
```

No flagged skill became agent-readable. This is a successful **expected
negative assertion**, not a scan bypass or a malicious instruction fixture.

## Limits retained, not converted into guarantees

Native-plugin CI audit still returns **FAIL**, with:

```text
Native Agent Plugin canonical IR is missing, so deployment was blocked.
Use 'apm pack --claude-plugin' or ask the publisher for a legacy-compatible
package.
[x] 1 of 10 check(s) failed
```

Full unchanged output is in `Prior/logs/native-metadata-audit.*`.
Diagnosis/owner: local native-plugin replay lacks canonical IR —
`apm-cli-explorer` / upstream. Chapter 1 asserts whole-unit registration,
not an audit-clean plugin or successful Copilot loading, and points to
Chapter 3's visible limitation.

Policy source review confirms `.github-private` before GitHub fallbacks
and separate GitLab/ADO discovery rules. See `Wave/source-contracts.json`,
including `src/apm_cli/policy/discovery.py:53–72`. No org remote or private
policy authority was supplied to these fixtures. Audit exits do **not**
establish org-policy enforcement; the operations report's bypass and
fail-closed limitations remain applicable. Likewise, neither a hash, a
clean Unicode scan, nor registration authenticates a publisher or confines
agent runtime behavior.

**Skips:** no changed executable example required a network skip. Public
Git and the shared loopback registry were actually reachable where used.
Historical illustrations and unclaimed live harness/private-policy behavior
are out of this execution scope, not falsely labeled network failures or
freshly certified examples.

## Artifacts and handoff

`Wave` contains `sources/ch01.html`, `blocks/ch01.json`,
`source-inputs.json`, `reuse-evidence.json`, `source-contracts.json`,
`logs/*.{json,txt,stdout.bin,stderr.bin}`, `inputs/`, `snapshots/`,
`mutations/`, `assertions/`, `command-index.json`, `summary.json`,
and `final-source-checks.json`. Full absolute argv/CWDs are in raw records;
published reports use the aliases above. Final source/fixture hashes match
the initial capture.

**Concurrent-edit note:** the complete protected-file check at
`2026-09-16T01:57:51Z` passed. A later handoff check observed an unrelated
change to `content/toc.yml`; this verifier did not write or revert it.
All four chapter sources, selected executable fixtures, root `apm.yml` /
`apm.lock.yaml`, and edition version remain unchanged. The TOC is not an
execution input for these tests and receives no approval from this gate.
Current receipts are in `Wave/handoff-source-checks.json`.

**Minimal fixes applied: none. Mandatory Chapter 1 corrections: none.**
PASS is limited to this source hash and these scopes. The separate
[Chapter 3](ch03-verification.md) and [Chapter 4](ch04-verification.md)
reports retain their own mandatory corrections.
