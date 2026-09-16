# Chapter 6 independent verification — book 1.2 / exact APM 0.31.0

**Verdict: PASS for the updated chapter and its bounded claims.**
All ten current code blocks were covered by real CLI execution and input/output
comparisons. The historical 0.23.1 block was not rerun or restamped.
This is a code-verification verdict, not reviewer acceptance or certification
that frozen install, audit, or APM generally is defect-free.

| Verified source | Final SHA-256 |
| --- | --- |
| `content/chapters/the-lockfile-and-reproducibility.html` | `45aa09e83b7d2b64353921c8b7f13b37d6b68dffa71181ad1659432aaf6662e2` |

The source is byte-identical to the captured input. No chapter or canonical
fixture fix was necessary. The newly qualified frozen-install language agrees
with the independently verified Chapter 5 local-path exception.

## Execution identity, isolation, and evidence

- **Executed CLI:** exactly **0.31.0**. Every invocation used the orchestrator's
  absolute executable, not a PATH-selected `apm`.
- **Executable SHA-256:**
  `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
- **Matching source/docs commit:**
  `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`.
- Windows x64; Python 3.12.10 and PyYAML 6.0.3 for orchestration and independent
  byte assertions. APM itself parsed, resolved, installed, exported, and audited.
- Joint Ch6/Ch7 run: **168 native invocations**, comprising **17 version guards,
  12 help calls, and 139 example/control calls**. Summed native runtime:
  **1,586.631 seconds**. Parallel runtimes are not elapsed time or a benchmark.
  First native start: `2026-09-16T02:01:58.593244Z`; last native completion:
  `2026-09-16T02:28:22.814093Z`. These totals are shared with the Ch7 report,
  not additional per-chapter runs.
- Every batch first asserted the exact version banner and executable digest.
  No native command timed out or returned an unexpected exit.

Published paths below are symbolic:

| Alias | Meaning |
| --- | --- |
| `RunRoot` | Orchestrator session artifacts, `files/book-v1.2` |
| `VerifyRoot` | `RunRoot/verify-ch06-ch07` |
| `Scratch` | Newly created, exclusively owned short root in `VerifyRoot/runtime-layout.json` |
| `Ops` | `backend/examples/updates/1.2/operations` |
| `Core` | `backend/examples/updates/1.2/core` |
| `Producer` | `backend/examples/updates/1.2/producer` |
| `Ch5Evidence` | `RunRoot/verify-ch05` |

Every command-table entry is the exact argument vector following `& $Apm`:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

Each batch used a distinct HOME, USERPROFILE, APM home/cache, app-data/config
paths, and temp directory. The existing runner's credential-variable filtering,
hidden `gh` launcher, disabled Git credential helper, and isolated Git config
were retained. No real user/global configuration, installed CLI, root book
dependencies, or another verifier's scratch project was changed.

The **unmodified** `Ops/verify.py` suites `repro`, `registry`, `pack`, `lifecycle`,
`mcp`, and `cleanup-limit` ran through an independent recorder. It calls the
original `main()` with explicit `--apm`, `--work`, and `--suite`; the test bodies
and fixtures were not patched. Only subprocess recording was augmented with
original stdout/stderr bytes, timestamps, durations, and pre/post snapshots.
Runner SHA-256:
`e4c349784005c6fc21d773f1365f66973f6d7c0c8cffbe838b9ea78738237ce5`.
The displayed Ch6 suite omits `--work`; this verification supplied the required
new short owned location instead of relying on shared/default temp.

Actual wrapper form, from the book checkout:

```powershell
python -B "$VerifyRoot\driver.py" --apm $Apm --work "$Scratch\r" --suite repro
```

The same form selected these distinct work roots; no `--suite all` run occurred:

| Suite/batch | Work suffix | Wrapper result |
| --- | --- | --- |
| `repro`, `registry`, `pack`, `lifecycle`, `mcp`, `cleanup-limit` | `r`, `g`, `p`, `l`, `m`, `w`, respectively | all 0 |
| `help-only`, `repro-more`, `registry-more`, `lifecycle-more` | `h`, `r2`, `g2`, `l2` | all 0 |
| `mcp-more`, `pack-more`, `sbom`, `public-graph` | `m2`, `p2`, `s`, `f` | all 0 |
| `public-more` | `u` | 1: verifier-only output-shape assertion; disposition below |
| `final-edges`, `registry-formats` | `e`, `gf` | both 0; remaining coverage completed |

Each corresponding `<batch>-version` record exited 0. The relevant root,
install, audit, outdated, update, lock, lock-export, find, pack, lifecycle,
uninstall, and prune help calls all exited 0.

### Durable raw record

| Under `VerifyRoot` | Contents |
| --- | --- |
| `the-lockfile-and-reproducibility.html`, `lifecycle.html`, `source-inputs.json` | Exact chapter inputs, block IDs/hashes, canonical input hashes |
| `canonical-inputs.zip` | Unmodified manifests, locks, and authored fixture sources |
| `logs/<record-id>.json`, `.txt`, `.stdout.bin`, `.stderr.bin` | Absolute executable/CWD, argv, exit, timing, exact process output, before/after hashes and mtimes |
| `snapshots/<record-id>-before.zip`, `-after.zip` | Original per-command project bytes |
| `mutations/`, `assertions/` | Explicit scratch-only setup changes and independent state assertions |
| `batches/`, `command-index.json`, `summary.json` | Version guards, wrapper outcomes, complete native command ledger |
| `verification-status.json` | Source-specific per-example PASS tags and supporting record IDs |
| `reuse-proof.json`, `reused/` | Qualified independent Ch5/Ch8–9 reuse; original failures retained |
| `pinned-source-checks.json`, `registry-release-check.json` | Source commit/hashes, Git checkout setting, released exclusive registry socket |

Raw records retain original output. Report excerpts normalize terminal line
endings/padding and symbolize scratch prefixes; they do not replace the raw
failure output.

## Per-example disposition

Paths are chapter anchors unless a fixture is named. Runtime sums the listed
supporting native calls, including fixture preparation where relevant, but
excludes version/help guards. Shared records appear under more than one block;
**do not add this column to derive total runtime**.

| Block ID / input path | Status | CLI | Runtime (s) | Verified result |
| --- | --- | --- | ---: | --- |
| `ch6-repro-manifest` — `Ops/repro/apm.yml` | **PASS** | 0.31.0 | 55.678 | Complete displayed manifest matches canonical text; real install, replay, frozen, and CI audit succeed |
| `ch6-library-manifest` — `Ops/repro/package/apm.yml` | **PASS** | 0.31.0 | 55.678 | Exact displayed dependency manifest accepted and materialized, with its authored instruction retained |
| `ch6-current-restore` | **PASS** | 0.31.0 | 55.678 | Exact four-command sequence; six native files and complete lock hash verified after each call |
| `ch6-current-lock` — `Ops/repro/apm.lock.yaml` excerpt | **PASS** | 0.31.0 | 55.678 | All selected scalars and both complete ownership rows match newly generated output; excerpt was never used as a restore input |
| `ch6-current-find` | **PASS**, including expected miss | 0.31.0 | 32.172 | Dependency/workspace provenance exits 0/0; untracked query exits 1; no writes |
| `ch6-lock-only` | **PASS** | 0.31.0 | 11.376 | Retained-lock canary and separate source-only resolution both tested |
| `ch6-sbom-export` — `Producer/pinned-bundle` | **PASS** | 0.31.0 | 76.475 | Genuine locked public input restored/audited; identical fixed-clock exports; SPDX control; cold offline export without hydration |
| `ch6-missing-git-manifest` | **PASS**, negative setup | 0.31.0 | 10.087 | Exact dependency mapping applied to a separate installed `repro` copy, retaining its old lock |
| `ch6-missing-git-frozen` | **PASS**, expected exit 1 | 0.31.0 | 10.087 | Missing Git dependency named; complete project hashes and mtimes unchanged |
| `ch6-repro-suite` | **PASS**, expected negatives asserted | 0.31.0 | 65.573 | Unmodified suite completed; drift, invalid-owner, CRLF, and canary checks confirmed independently |

`ch6-find-historical` is **retained historical evidence only, APM 0.23.1**.
Its LF-normalized HTML code body equals the original `HEAD` block. It received
no 0.31.0 execution status. The old Meridian transitive hashes are not presented
as fresh resolutions or replay results.

## Exact current commands and results

`Scratch/r2/p1` began with only the two manifests and two authored instructions:
no lock, modules, or native outputs. The canonical lock was preserved separately
for comparison.

| Record ID | CWD | Arguments after `& $Apm` | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `repro-more-install` | `Scratch/r2/p1` | `install` | 0 | 19.957 |
| `repro-more-restore` | `Scratch/r2/p1` | `install` | 0 | 13.503 |
| `repro-more-frozen` | `Scratch/r2/p1` | `install --frozen` | 0 | 10.547 |
| `repro-more-audit-ci` | `Scratch/r2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 11.671 |
| `repro-more-find-package` | `Scratch/r2/p1` | `find .github/instructions/library.instructions.md --source` | 0 | 10.581 |
| `repro-more-find-workspace` | `Scratch/r2/p1` | `find .github/instructions/workspace.instructions.md --source` | 0 | 11.069 |
| `repro-more-find-untracked` | `Scratch/r2/p1` | `find .github/not-owned.md` | 1 | 10.523 |
| `repro-more-missing-git-frozen` | `Scratch/r2/p2` | `install --frozen` | 1 | 10.087 |
| `repro-lock-retains-ownership` | `Scratch/r/p7` | `lock` | 0 | 3.290 |
| `repro-more-fresh-lock-only` | `Scratch/r2/p7` | `lock` | 0 | 8.085 |

Observed complete lock SHA-256 after **each** generation/replay/audit command:

```text
79fe2a70ae0c8b9987ddd0105d013c6593a6c3fd8135ae94601d4df58fd22772
```

`generated_at` was absent. All authored input hashes remained unchanged.
The six output paths were exactly the two Copilot instructions, two Claude
rules, and two Cursor rules listed in the chapter. Their canonical hashes,
ownership keys, and active owners were checked against actual bytes, not
inferred from an installed-package counter. The clean CI report contained ten
passing checks; ten was not treated as an invariant for other fixtures.

The find results were:

```text
_local/package  ./package
.  (workspace)
[x] '.github/not-owned.md' is not tracked by any installed package in apm.lock.yaml.
```

The deliberate missing-Git test returned this exact stdout, with empty stderr:

```text
[>] Installing dependencies from apm.yml...
[x] --frozen: apm.lock.yaml is out of sync with apm.yml.
  - microsoft/apm-sample-package is declared in apm.yml but missing from apm.lock.yaml
[i] Tip: run 'apm outdated' to see what changed, then 'apm update'.
[x] Install failed after 0.2s.
```

**Diagnosis:** intended structural refusal, not a broken example or network
skip. No public graph was acquired by this refusal test. No author correction
is required.

## Hashes, clocks, and source identity — PASS

The independent calculations and captured locks confirm:

- Local `repro`: `_local/package`, `source: local`, `local_path: ./package`;
  no fabricated Git ref/commit or package-tree hash in this emitted entry.
- Git skill: immutable ref/commit
  `fb2851683be0e0e7711421d518bd8dba23b0b1f6`, `version: unknown`,
  `.apm/skills/style-checker`, and package-tree hash
  `sha256:867912713bf45048211440b81ea0ced396ad0a0993447dd540fe5c219722d318`.
  Both deployed skill files hash to
  `sha256:1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829`.
- Registry `operations/exact` at 1.0.0: actual downloaded deterministic archive
  hash `sha256:8e1dec8b5d49dea68be67302bd96ec4bad440e78f2a91c623251a0a47bc5857b`;
  separate tree hash
  `sha256:44130bee98159567e75a7daa3e66204356b2c4adfe6b9e755e1383539f5a5efe`.
  Its recorded URL is
  `http://127.0.0.1:18431/v1/packages/operations/exact/versions/1.0.0/download`;
  there is no Git commit field. The registry materialization/audit commands are
  recorded in the [Ch7 report](ch07-verification.md), not borrowed explorer PASSes.
- MCP-only locks and URI ownership were materialized using `Ops/mcp`;
  native configuration coverage remains limited, as tested below.
- The GitCache checkout's **local** config actually contained
  `autocrlf = false`. Sorted path/raw-byte package hashes were recomputed
  independently without importing APM's hashing implementation.
- All **six** `repro` native files were changed to CRLF. Their raw hashes
  differed from their recorded hashes, while CRLF-to-LF hashes matched every
  corresponding deployment row. Audit exited 0 and preserved all project
  bytes, including the complete lock. This is not a cross-harness byte-equality
  claim or a test of every `.gitattributes`/binary-content case.

The reusable repro suite's exact additional native calls:

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `repro-repro-frozen` | `Scratch/r/p1` | `install --frozen` | 0 | 12.234 |
| `repro-repro-ci` | `Scratch/r/p1` | `audit --ci --no-fail-fast -f json` | 0 | 4.345 |
| `repro-copilot-bare-drift` | `Scratch/r/p2` | `audit -f json` | 0 | 5.131 |
| `repro-copilot-ci-drift` | `Scratch/r/p2` | `audit --ci --no-fail-fast -f json` | 1 | 6.707 |
| `repro-claude-bare-drift` | `Scratch/r/p3` | `audit -f json` | 0 | 7.660 |
| `repro-claude-ci-drift` | `Scratch/r/p3` | `audit --ci --no-fail-fast -f json` | 1 | 5.093 |
| `repro-cursor-bare-drift` | `Scratch/r/p4` | `audit -f json` | 0 | 4.765 |
| `repro-cursor-ci-drift` | `Scratch/r/p4` | `audit --ci --no-fail-fast -f json` | 1 | 4.018 |
| `repro-invalid-owner-bare` | `Scratch/r/p5` | `audit -f json` | 1 | 3.914 |
| `repro-invalid-owner-ci` | `Scratch/r/p5` | `audit --ci --no-fail-fast -f json` | 1 | 3.747 |
| `repro-canonical-crlf-hashes` | `Scratch/r/p6` | `audit --ci --no-fail-fast -f json` | 0 | 4.668 |

The twelfth suite call is the retained-lock canary already listed above.
Ordinary benign drift failed CI but not bare audit. Invalid ownership failed
both modes. Exact failing checks and the subsequent prune/install control are
retained in the Ch7 report and raw logs.

### Lock-only canary and target contraction

Deleting **only** `.github/instructions/library.instructions.md` while keeping
the prior lock produced the intended canary: `lock` exited 0, did not recreate
the file, and retained complete lock bytes, hashes, and ownership. In the
separate source-only project, `lock` created modules and a resolution-only lock,
but no deployment rows or harness directories.

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `repro-more-contraction-lock-only` | `Scratch/r2/p8` | `lock` | 0 | 6.818 |
| `repro-more-contraction-install` | `Scratch/r2/p8` | `install` | 0 | 6.638 |
| `repro-more-contraction-ci` | `Scratch/r2/p8` | `audit --ci --no-fail-fast -f json` | 0 | 5.152 |
| `repro-more-legacy-timestamp-restore` | `Scratch/r2/p9` | `install` | 0 | 5.651 |
| `public-more-semver-install` | `Scratch/u/p5` | `install` | 0 | 17.600 |

Contraction changed only manifest targets to `[copilot]`. Lock-only retained
all six files and the old complete lock; install removed the four dropped
Claude/Cursor outputs and retained authored sources. Audit then passed.

The compatibility test explicitly seeded `generated_at: 2026-01-01T00:00:00Z`
in a **disposable** copy, not a canonical lock. Unchanged install retained that
complete legacy-bearing file. The independently resolved Git-semver lock used
format `'2'`, constraint `^1.0.0`, tag `v1.0.0`, and actual
`resolved_at: 2026-09-16T02:10:57+00:00`. Its complete hash was
`2c33fb7959404c4f3d19c7a7da6d143f2fb5d58ce26cb9886e91df214c7eb523`.
The subsequent no-op preview/apply retained it; see Ch7. No old explorer
resolution timestamp/hash was relabeled as this execution.

## Frozen and cold-audit boundary — PASS for the qualifications

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `repro-more-missing-lock-frozen` | `Scratch/r2/p3` | `install --frozen` | 1 | 7.513 |
| `repro-more-missing-local-source-frozen` | `Scratch/r2/p4` | `install --frozen` | 1 | 9.121 |
| `repro-more-edited-native-frozen` | `Scratch/r2/p5` | `install --frozen` | 0 | 9.941 |
| `repro-more-edited-native-after-repair-ci` | `Scratch/r2/p5` | `audit --ci --no-fail-fast -f json` | 0 | 9.398 |
| `repro-more-cold-local-ci` | `Scratch/r2/p6` | `audit --ci --no-fail-fast -f json` | 0 | 12.281 |
| `repro-more-cold-local-frozen` | `Scratch/r2/p6` | `install --frozen` | 0 | 8.741 |
| `public-more-pinned-frozen` | `Scratch/u/p1` | `install --frozen` | 0 | 33.522 |
| `public-more-same-commit-tag-frozen` | `Scratch/u/p2` | `install --frozen` | 0 | 16.811 |
| `public-more-same-commit-tag-ci` | `Scratch/u/p2` | `audit --ci --no-fail-fast -f json` | 0 | 11.195 |
| `public-more-cold-public-ci` | `Scratch/u/p3` | `audit --ci --no-fail-fast -f json` | 0 | 25.391 |
| `public-more-cold-offline-ci` | `Scratch/u/p4` | `audit --ci --no-fail-fast -f json` | 1 | 28.990 |
| `public-graph-full-graph-cold-frozen` | `Scratch/f/p1` | `install --frozen` | 0 | 44.251 |
| `public-graph-full-graph-ci` | `Scratch/f/p1` | `audit --ci --no-fail-fast -f json` | 0 | 12.129 |
| `public-graph-promote-transitive-frozen` | `Scratch/f/p1` | `install --frozen` | 0 | 15.673 |
| `public-graph-promote-transitive-ci` | `Scratch/f/p1` | `audit --ci --no-fail-fast -f json` | 0 | 14.178 |
| `mcp-mcp-frozen` | `Scratch/m/p1` | `install --frozen` | 0 | 23.232 |
| `mcp-mcp-ci` | `Scratch/m/p1` | `audit --ci --no-fail-fast -f json` | 0 | 9.847 |
| `mcp-mcp-native-missing-not-audit-gated` | `Scratch/m/p1` | `audit --ci --no-fail-fast -f json` | 0 | 5.876 |
| `mcp-mcp-frozen-repairs-native-file` | `Scratch/m/p1` | `install --frozen` | 0 | 16.508 |
| `mcp-mcp-frozen-catches-manifest-lock-mismatch` | `Scratch/m/p1` | `install --frozen` | 1 | 3.171 |
| `mcp-mcp-reconcile-new-intent` | `Scratch/m/p1` | `install` | 0 | 4.283 |
| `mcp-more-edited-native-ci` | `Scratch/m2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 22.025 |
| `mcp-more-edited-native-frozen` | `Scratch/m2/p1` | `install --frozen` | 0 | 12.272 |

All corresponding chapter-table qualifications held:

1. Missing lock and missing direct Git declaration refused without writes.
   Missing local **source directory** also failed, but is not advertised as
   the same read-only structural refusal.
2. A benign instruction edit was repaired, not rejected, by frozen install.
3. Full-SHA to same-commit `v1.0.0` changed lock metadata with exit 0.
4. Declaring an already locked transitive directly at its recorded SHA changed
   the lock with exit 0.
5. Changed declared MCP arguments failed manifest-to-lock consistency.
   Missing native MCP config was not audit-gated, then frozen recreated it.
   Edited native MCP config was not audit-gated and frozen left its bytes intact.
   This is a **confirmed coverage limit**, not native-config certification.
6. Cold public CI audit used a genuinely separate empty home/cache and absent
   modules; it acquired locked content without checkout writes. Local cold CI
   audit likewise left modules absent; local frozen install materialized them.

The full graph's genuine manifest/lock came from
`RunRoot/operations-probes/snapshots/public-full-shortpath.zip` **as input bytes
only**. The archive and extracted manifest/lock hashes were recorded; its
explorer execution was not borrowed. This verifier independently restored and
audited the public graph, then promoted the transitive at
`fb4eb04fcbd30de50052b1155d81167393dfb5aa`. The committed graph, not a new
floating transitive resolution, determined that identity.

Missing-lock diagnostic:

```text
[x] --frozen requires apm.lock.yaml to exist. Run 'apm install' (without --frozen) or 'apm update' first.
```

Missing-local diagnostic:

```text
[x] Local package path does not exist: ./package
```

For deliberately unavailable public acquisition, `config-consistency` and
`drift` both failed. Exact terminal Git error:

```text
fatal: unable to access 'https://github.com/microsoft/apm-sample-package.git/': Failed to connect to github.com port 443 via 127.0.0.1 after 2016 ms: Could not connect to server
```

That **asserted exit 1 is not `SKIPPED-needs-network`**. Only the child's
HTTP/HTTPS/ALL proxy was pointed at unavailable loopback; TLS verification,
protocol fallback, and host configuration were not weakened. The successful
public control used real anonymous Git access.

### Qualified reuse of independent Chapter 5 evidence

`reuse-proof.json` validates the prior executable digest, exact argv/version
guards, original stdout/stderr bytes, after-snapshot hashes, canonical input
bytes, and the precise source/declaration mutation. It did not resume the old
scratch projects or treat explorer observations as independent results.

| Ch5 record | Exact arguments | Recorded exit | Original seconds | Reused fact |
| --- | --- | ---: | ---: | --- |
| `frozenlocal-baseline-install` | `install` | 0 | 2.690 | Genuine one-local-dependency starting lock |
| `frozenlocal-baseline-audit` | `audit --ci` | 0 | 1.544 | Clean starting state |
| `frozenlocal-new-local-frozen` | `install --frozen` | 0 | 1.696 | Added `./other` installs and rewrites the old lock |
| `frozenlocal-new-local-audit` | `audit --ci` | 0 | 1.562 | Resulting two-dependency state audits |
| `local-local-instruction-install` | `install` | 0 | 4.584 | Root-local-only lock omits `apm_version` and `generated_at` |

All eight canonical `Core` file hashes still match `Ch5Evidence/source-inputs.json`
and `canonical-core.zip`. The new-local case retains the original manifest
sources plus only the recorded new skill and declaration. The lock changes
from `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28`
to `daadeb90f18c0c5958b0c73557b233a94a6fa168c12ad7b9c984a0cb5b9303a7`;
the new source equals both its deployed and cached skill bytes.
The prior failed expectation `[1]` is preserved: current Ch6 correctly asserts
the **actual 0/local-path exception**, not the superseded blanket refusal.
These are retained original runtimes, not new native invocations.

## SBOM example — PASS

| Record ID | CWD | Exact arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `sbom-pinned-bundle-frozen` | `Scratch/s/p1` | `install --frozen` | 0 | 33.584 |
| `sbom-pinned-bundle-ci` | `Scratch/s/p1` | `audit --ci --no-fail-fast -f json` | 0 | 9.087 |
| `sbom-cyclonedx` | `Scratch/s/p1` | `lock export --format cyclonedx --timestamp '2026-09-16T00:00:00+00:00' -o sbom.cdx.json` | 0 | 8.883 |
| `sbom-cyclonedx-repeat` | `Scratch/s/p1` | `lock export --format cyclonedx --timestamp '2026-09-16T00:00:00+00:00' -o sbom.cdx.json` | 0 | 9.375 |
| `sbom-spdx` | `Scratch/s/p1` | `lock export --format spdx --timestamp '2026-09-16T00:00:00Z' -o sbom.spdx.json` | 0 | 11.444 |
| `final-edges-cold-offline-sbom` | `Scratch/e/p3` | `lock export --format cyclonedx --timestamp '2026-09-16T00:00:00+00:00' -o sbom.cdx.json` | 0 | 4.101 |

Both fixed-clock CycloneDX files were byte-identical, with SHA-256
`259d68d9530d886d701405415547cd28500bb9caa930b85fcdef872867c3fb8b`.
JSON advertised CycloneDX 1.5 and SPDX-2.3. A third CycloneDX export from
manifest/lock-only input, empty cache, and deliberately unavailable outbound
proxy produced the same bytes without modules or cache hydration. Root lock
bytes remained unchanged and did not acquire `generated_at`.

The help/source fallback order—explicit timestamp, `SOURCE_DATE_EPOCH`, legacy
lock timestamp, Unix epoch—was checked at the frozen commit. This is not
presented as execution of every fallback branch or signed publisher attestation.

## Limits, skips, fixes, and handoff

- **Runnable updated examples marked `SKIPPED-needs-network`: none.** Public
  acquisition succeeded; controlled acquisition failure was asserted as exit 1.
  Loopback registry requests were anonymous. A bound socket with Windows
  exclusive-address use was transferred to each registry server without a
  check-close-bind race; subsequent exclusive rebind confirmed release.
  No unrelated listener/process was stopped.
- Binary-byte rules, special live Git tag publication, publisher authenticity,
  private host behavior, live agent/MCP execution, and universal cross-platform
  equivalence are not newly executed guarantees. The chapter keeps those
  boundaries or source-inspected contracts separate.
- The companion Ch7 report retains the selected-registry cache failure before
  its repair. Ch5's marker-present audit mutation remains an underlying
  **FAIL**, not an audit-clean package-form guarantee. Neither finding is
  erased by the clean instruction fixture here.
- One **verifier-only** assertion required `outdated` to print a table even
  when all dependencies were current. Actual output was
  `[*] All dependencies are up-to-date`, exit 0. The original wrapper failure
  remains recorded. The corrected assertion and previously unexecuted audit
  were completed on byte-equivalent input in `final-edges`; real Git-only
  unknown and mixed-source tables were subsequently executed successfully.
  No chapter/code correction was needed.
- **Minimal content/fixture fix applied: none. Prose correction requested:
  none for this source SHA.** Verifier-owned repository changes are only this
  report and the companion Ch7 report. No other chapter, fixture, research
  metadata, TOC, site, root dependency, commit, or publication was changed.

**Handoff: Chapter 6 code-verification PASS; reviewer decision remains separate.**
