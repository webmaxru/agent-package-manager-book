# Chapter 7 independent verification — book 1.2 / exact APM 0.31.0

**Verdict: PASS for the corrected source below, including the narrow
package-selector claim-gate closure.**
All six current code blocks and the coupled lifecycle, freshness, audit,
cleanup, and marketplace claims were covered. **The selected-registry cache
defect remains an underlying FAIL:** successful update, immediate audit 1,
frozen repair 0, then audit 0 were all recorded in that order. This verdict
does not mean APM is bug-free or that every native/policy/runtime guarantee
passed. Reviewer acceptance and publication remain separate.

| Verified source | Final SHA-256 |
| --- | --- |
| `content/chapters/lifecycle.html` | `e45b3d6410caf0b030fe90da58660008c8ce088d6b1f2656f5af94620fe75c72` |

The originally executed source, retained in `VerifyRoot/lifecycle.html`, has
SHA-256 `51fcf6ee4a7cd5c9da7737cde9e4dd7568b80588d404de5cc8ccf47d2a4c6259`.
The parent changed only the package-selector evidence comment and associated
prose under `ch7-verify`. All six current code blocks, the historical code
block, and the recorded fixture/runner input bytes remain unchanged.

## Narrow scope-evidence closure — 2026-09-16 UTC

**PASS for reviewer `a88f70d2-1fd7-40eb-8189-095a4afff48a`'s claim gate.**
This supersedes only the earlier interpretation of the `_local/package`
control as successful scoped scanning. No full suite or APM command was rerun:
**new native invocations 0; new native runtime 0.000 s**.

The original `final-edges-package-selector-narrower` record is retained
unchanged: `audit _local/package -f json`, exit **0**, **3.007836 s**, empty
stdout, and exact stderr:

```text
[!] Package '_local/package' not found in apm.lock.yaml or has no deployed files
```

**Original interpretation: FAIL as scope evidence.** That early return selected
no files; exit 0 does not prove a successful scan. The original raw log SHA-256
is `20bcde6fc30831aac7d025458e7207cb53d05e481ca08adf91ff66105d04ce70`.
Neither its argv/output nor the original whole-project audit results were
rewritten.

The corrected claim uses the completed **independent Ch8** final-source
record, not the explorer's superseded `scan-package-selector-narrower`:

| Evidence | Validated value |
| --- | --- |
| Report / source anchor | [Ch8 verification](ch08-verification.md#minimal-correction-original-error-and-final-rerun), `ch08-package-audit-scope` |
| Native record | `Ch89Evidence/batches/final-source/logs/002-final-source-canonical-scope.json` |
| Exact arguments after the supplied absolute executable | `audit ./package -f json` |
| CLI / native exit / original runtime | **0.31.0 / 0 / 3.113746 s** |
| Original native start | `2026-09-16T02:22:54.093923+00:00` |
| Actual coverage | **`files_scanned: 3`**, zero findings; empty stderr |
| Native-record SHA-256 | `8ded209aef8fa297b9a2309daae58bfc5327cbea5c6a01d8af7003ffb7e3fe36` |
| Before and after snapshot ZIP SHA-256, both identical | `8562acf01736a6fedec65842905e26f676d1920c01f4464b4ab16dc2c34e6339` |

Read-only equivalence checks completed at `2026-09-16T02:51:35.964637+00:00`
in **1.603586 s**, with these assertions:

- The Ch7 source diff consists of exactly two replacements: the evidence
  comment and its scope paragraph. All **seven complete `<pre><code>` blocks**
  are byte-identical, including attributes and line endings. The decoded
  ID-to-code map also matches the original capture; its sorted-key compact
  UTF-8 JSON SHA-256 is
  `ded5b0413cd61a4232d241abbe0e9b8c42ac7de4abdf4bd651f6062cf5e4bf47`.
- All **47** original fixture/runner input hashes still match. No fixture,
  generated lock, or code block was changed for this closure.
- Ch8's final HTML still hashes to
  `21efe99d2991b10b85e8ce00c0d569bccbe66ff71422756172eeb902d04af450`.
  Its `final-source` batch metadata, preceding successful exact-version guard,
  executable digest, argv, native JSON record, and both snapshot inventories
  were checked. The current executable digest still equals the frozen digest
  below; no fresh `--version` invocation is claimed.
- All **15 common project files** match the original Ch7 control byte-for-byte,
  including manifest
  `d30b320e9ace5f31e87888215b648a7485d0586b48d1ac1d2b19bfde9f4bf2a3`,
  complete lock
  `79fe2a70ae0c8b9987ddd0105d013c6593a6c3fd8135ae94601d4df58fd22772`,
  and unrelated governed marker
  `fe5f3c7cfcd248303085019d3e1a4bbf95700fc244470e8e0a957559d3ab2ec4`.
  Ch8 additionally has `package/README.md` and its cached copy, both hash
  `00cb08b149b8db44e8fe06dc0d7a2ff86453b69f696a12276e806dd512416d45`;
  neither belongs to the three recorded package deployments. Full-project
  byte identity is **not** claimed across those two extra files.
- The three recorded package files are `.claude/rules/library.md`,
  `.cursor/rules/library.mdc`, and
  `.github/instructions/library.instructions.md`; their normalized hashes
  match the lock. The unrelated Critical-class marker remains present and is
  not among them. The original whole-project bare/CI audits still fail 1/1
  on the matching governed inputs.

**Closure:** the corrected paragraph now distinguishes a no-files early return
from a real three-file canonical-selector scan and links to that validated
evidence. No further prose correction is requested for the final Ch7 SHA above.
Original raw logs, source captures, invocation totals, and historical status
artifacts remain unchanged; this dated delta supplies the current claim gate.

## Execution and evidence identity

**Actually executed:** APM **0.31.0**, always via the supplied absolute
executable. SHA-256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
Matching source/docs commit:
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`.
Platform: Windows x64; orchestration: Python 3.12.10 / PyYAML 6.0.3.

The original joint Ch6/Ch7 run contains **168 native invocations: 17 exact-version
guards, 12 help calls, and 139 example/control calls**. Summed native runtime
was **1,586.631 seconds**, not elapsed time or a performance claim. First
native start: `2026-09-16T02:01:58.593244Z`; last completion:
`2026-09-16T02:28:22.814093Z`. These are the same shared totals reported for
Ch6, not a second set of executions. No native timeout or unexpected native
exit occurred. One verifier-only assertion failure is preserved below.

| Alias | Meaning |
| --- | --- |
| `RunRoot` | Orchestrator session artifacts, `files/book-v1.2` |
| `VerifyRoot` | `RunRoot/verify-ch06-ch07` |
| `Scratch` | New short exclusively owned root recorded in `VerifyRoot/runtime-layout.json` |
| `Ops` | `backend/examples/updates/1.2/operations` |
| `Core` | `backend/examples/updates/1.2/core` |
| `Producer` | `backend/examples/updates/1.2/producer` |
| `Ch5Evidence` | `RunRoot/verify-ch05` |
| `Ch89Evidence` | `RunRoot/verify-ch08-ch09` |

Command tables give exact arguments following this executable:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

The unchanged `Ops/verify.py` test bodies and `main()` ran through an independent
subprocess recorder, with `--apm` and a new explicit `--work` for every batch:

```powershell
python -B "$VerifyRoot\driver.py" --apm $Apm --work "$Scratch\g" --suite registry
```

The original runner SHA-256 remained
`e4c349784005c6fc21d773f1365f66973f6d7c0c8cffbe838b9ea78738237ce5`.
Selected suites were `repro`, `registry`, `pack`, `lifecycle`, `mcp`, and the
separate `cleanup-limit`; **not `all` or all explorer probes**. Supplemental
batches executed only the displayed sequences or missing coupled controls.
The complete batch/work/exit matrix is in
[Ch6's execution record](ch06-verification.md#execution-identity-isolation-and-evidence).
All 17 batch guards checked the exact banner and binary digest before examples.

Each batch had its own HOME, USERPROFILE, APM cache/config, app-data paths,
temp, and Git configuration. Inherited credentials/APM overrides were removed,
the desktop `gh` launcher was hidden, and Git credential helpers/prompts were
disabled. Lifecycle commands used only the inert event recorder. No agent
runtime or MCP server was launched. No user/global install/config, root book
dependency, other verifier's temp, or live publication was changed.

### Registry socket ownership

Only this group used `127.0.0.1:18431`. Each registry context first bound a
socket with Windows `SO_EXCLUSIVEADDRUSE`, then transferred that **same open
handle** to the server, avoiding a check-close-bind race. The `registry`,
`registry-more`, and `registry-formats` contexts ran sequentially. All requests
were anonymous; no token value was used or recorded. Exclusive rebind after
the suites confirmed release. No unrelated listener/process was killed.

### Raw record and status tags

All raw evidence is under **`RunRoot/verify-ch06-ch07`**:

- `logs/<record-id>.json`, `.txt`, `.stdout.bin`, `.stderr.bin`: exact absolute
  executable/CWD/argv, native exit, UTC start/end, duration, original output,
  pre/post hashes and mtimes.
- `snapshots/<record-id>-before.zip` / `-after.zip`, `mutations/`, `assertions/`:
  original manifest/lock/native/cache bytes, deliberate scratch edits, and
  independently checked outcomes.
- `source-inputs.json`, `canonical-inputs.zip`, captured chapter files:
  input identity, code-block IDs/hashes, and unchanged canonical fixture bytes.
- `command-index.json`, `summary.json`, `batches/`, `verification-status.json`:
  complete command ledger, guards, wrapper outcomes, and per-example tags.
- `reuse-proof.json`, `reused/`: qualified independent Ch5/Ch8–9 evidence;
  no explorer execution was treated as an independent verdict.

Report excerpts omit positive JSON checks where stated. Diagnostic wording is
retained; terminal line endings/padding and local scratch prefixes are
normalized for publication. Full original output bytes remain in the raw logs.

## Per-code-block verification

Runtime sums the supporting example/control calls, excluding version/help
guards. Rows can share records; their runtimes are not additive.

| Block ID / input path | Status | CLI | Runtime (s) | Result |
| --- | --- | --- | ---: | --- |
| `ch7-audit-modes` — `Ops/repro` with one benign Copilot edit | **PASS**, expected exits | 0.31.0 | 11.838 | Bare JSON audit 0; CI JSON audit 1; neither repairs the edit |
| `ch7-pack-check` — `Ops/pack-check` | **PASS**, expected dirty result | 0.31.0 | 33.761 | Manifest materialized/audited; generation 0, clean check 0, edited catalog check 4 without writes |
| `ch7-registry-manifest` — `Ops/registry/apm.yml` | **PASS** | 0.31.0 | 16.431 | Full displayed manifest matches canonical text; genuine all-1.0.0 lock resolves/audits against the live owned loopback fixture |
| `ch7-registry-triad` | **PASS as documented defect reproduction** | 0.31.0 | 19.217 | Exact displayed sequence exits 0/0/0/**1**; cache-integrity failure retained |
| `ch7-registry-plan` | **PASS** | 0.31.0 | 4.268 | Every condensed line appears in actual preview; `1 updated, 2 unchanged`; project file hashes unchanged |
| `ch7-registry-repair` | **PASS**, bounded repair | 0.31.0 | 8.222 | Same failed state, frozen repair 0 then full audit 0; unchanged manifest/lock/native bytes |

`ch7-history-lock-diff` is **retained APM 0.23.1 historical evidence**, not
0.31.0 verification. Its LF-normalized HTML code body equals the original
`HEAD` block. Neither its manually seeded historical setup nor its timestamp
diff was reexecuted or relabeled.

### Coupled-claim coverage

| Chapter ID / area | Disposition | Evidence |
| --- | --- | --- |
| `ch7-triad-roles`, `ch7-report`, `ch7-registry-freshness` | **PASS**, bounded operational roles | Registry availability, exact/ranged constraints, Git-only unknown, mixed Wanted dash, no project writes |
| `ch7-change`, changed-selector and empty-cache prose | **PASS** | Consent refusal, exact no-op, constraint-respecting all-update, explicit selector reconciliation, no-consent same-ref cache repair |
| `ch7-audit-exits`, ownership/prune prose | **PASS**, expected negatives | All three target edits, invalid owners, unrecorded identical bytes, critical unrecorded file, qualified warning-only reuse, prune then install |
| `ch7-verify`, package-selector scope paragraph | **PASS after narrow correction / qualified independent reuse** | Ch8 `final-source-canonical-scope`: canonical `./package`, three files scanned, exit 0; the original `_local/package` no-files record is not successful scope evidence |
| `ch7-cold-audit` | **PASS for stated limits** | New cold public/local checks; cold failure 1; bare cache-only skip; independent Ch5 marker-present defect and Ch8/9 policy caveats |
| `ch7-preview-boundary` | **PASS** | Actual inert pre-events, no-script child environment, subtree-bound trust, nonfatal recorder exit 7 |
| `ch7-cleanup-outcomes` | **PASS as an accurate limitation table** | Edited-file refusal, real exclusive Windows file-lock leftover, retained stale edit, required MCP write failures |
| `ch7-selected-state`, `ch7-state-comparisons` | **PASS** | Lock/deployed/cache layer comparisons, failure before repair, complete lock hashes, actual public-semver no-op |
| `ch7-marketplace-check` | **PASS for marketplace-only scope** | Bytes/mtime comparisons, missing override, missing mixed-output ZIP, offline metadata exits 4/5 |

## Registry triad: failure preserved before repair

`Scratch/g/p1` copied the exact committed fixture and lock. Experimental
registries were enabled only in that batch's isolated HOME. The deterministic
server initially exposed only 1.0.0, then `advance()` exposed 1.1.0 and
2.0.0-beta.1. Nothing was pushed or published to a real registry.

| Record ID | CWD | Arguments after `& $Apm` | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `registry-registry-frozen` | `Scratch/g/p1` | `install --frozen` | 0 | 12.328 |
| `registry-registry-ci` | `Scratch/g/p1` | `audit --ci --no-fail-fast -f json` | 0 | 4.103 |
| `registry-registry-current-wanted-latest` | `Scratch/g/p1` | `outdated` | 0 | 4.653 |
| `registry-registry-selected-preview` | `Scratch/g/p1` | `update operations/range --dry-run --verbose` | 0 | 4.268 |
| `registry-registry-consent-required` | `Scratch/g/p1` | `update operations/range` | 1 | 10.397 |
| `registry-registry-selected-update` | `Scratch/g/p1` | `update operations/range --yes` | 0 | 5.365 |
| `registry-registry-selected-cache-drift` | `Scratch/g/p1` | `audit --ci --no-fail-fast -f json` | **1** | 4.932 |
| `registry-registry-selected-frozen-repair` | `Scratch/g/p1` | `install --frozen` | 0 | 4.266 |
| `registry-registry-updated-ci-after-repair` | `Scratch/g/p1` | `audit --ci --no-fail-fast -f json` | 0 | 3.956 |

The actual availability rows matched the chapter:

| Package | Current | Wanted | Latest | Status |
| --- | --- | --- | --- | --- |
| `operations/exact` | 1.0.0 | 1.0.0 | 2.0.0-beta.1 | outdated |
| `operations/other` | 1.0.0 | 1.1.0 | 2.0.0-beta.1 | outdated |
| `operations/range` | 1.0.0 | 1.1.0 | 2.0.0-beta.1 | outdated |

All three sources displayed `registry: fixture (outside constraint)`.
`outdated` and the preview left project file hashes unchanged. The
noninteractive refusal also left the complete project inventory unchanged:

```text
Cannot prompt for confirmation in non-interactive shell. Re-run with --yes to apply, or --dry-run to preview.
```

After selected apply, direct byte inspection—not just the plan—found:

| Dependency | Locked | Deployed text | Materialized cache metadata/text |
| --- | --- | --- | --- |
| `operations/range` | 1.1.0 | 1.1.0 | 1.1.0 |
| `operations/other` | 1.0.0 | 1.0.0 | **1.1.0** |
| `operations/exact` | 1.0.0 | 1.0.0 | 1.0.0 |

**Underlying CLI outcome: FAIL — selected update contaminated the unselected
dependency's cache. Suggested owner: `apm-cli-explorer` / upstream update
implementation.** The example passes because it explicitly teaches and asserts
this failure, not because the cache transition is correct.

The immediate audit's exact failing check was:

```json
{
  "name": "drift",
  "passed": false,
  "message": "drift detected: 1 file(s): .github/instructions/other.instructions.md",
  "details": [
    "modified: .github/instructions/other.instructions.md"
  ]
}
```

`content-integrity` passed; the JSON summary was total 10, passed 9, failed 1.
The audit did not repair or alter the project. Its stderr was:

```text
[!] Could not determine org from git remote; enforcement skipped (set policy.fetch_failure_default=block in apm.yml to fail closed)
[>] Replaying install (cache-only)...
[+] Replayed 3 package(s)
[>] Diffing scratch vs working tree...
[!] Drift detected: 1 file(s)
```

Frozen repair changed **exactly two file contents**:

```text
apm_modules/operations/other/.apm/instructions/other.instructions.md
apm_modules/operations/other/apm.yml
```

The manifest, complete lock, and deployed files did not move. The following
full CI audit returned 0. No `--no-drift`, hand-edited lock, or update of the
unselected dependency was substituted for that repair.

| State | Complete lock SHA-256 |
| --- | --- |
| Initial and selected preview | `57f3ad18af79da266ad2b83c72ff84b5bb3f6d990b58d9cd6db6e7b09b16904a` |
| Selected apply, failed audit, frozen repair, repaired audit | `49e87f953c1544a855c2ebbf94962afe20769200d9cbfad3868702142097cea6` |

### Remaining update/availability controls

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `registry-more-registry-frozen` | `Scratch/g2/p1` | `install --frozen` | 0 | 20.730 |
| `registry-more-registry-ci` | `Scratch/g2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 12.356 |
| `registry-more-exact-noop-plan` | `Scratch/g2/p1` | `update operations/exact --dry-run --verbose` | 0 | 9.392 |
| `registry-more-all-update-within-constraints` | `Scratch/g2/p1` | `update --yes` | 0 | 12.064 |
| `registry-more-all-update-ci` | `Scratch/g2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 11.404 |
| `registry-more-install-edited-exact-selector` | `Scratch/g2/p1` | `install` | 0 | 13.361 |
| `registry-more-edited-selector-ci` | `Scratch/g2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 15.041 |
| `registry-more-empty-modules-no-consent-update` | `Scratch/g2/p2` | `update` | 0 | 13.536 |
| `registry-more-noop-cache-repair-ci` | `Scratch/g2/p2` | `audit --ci --no-fail-fast -f json` | 0 | 7.952 |
| `registry-formats-git-unavailable-outdated` | `Scratch/gf/p1` | `outdated` | 0 | 6.182 |
| `registry-formats-registry-frozen` | `Scratch/gf/p2` | `install --frozen` | 0 | 5.707 |
| `registry-formats-registry-ci` | `Scratch/gf/p2` | `audit --ci --no-fail-fast -f json` | 0 | 1.869 |
| `registry-formats-mixed-source-install` | `Scratch/gf/p2` | `install` | 0 | 6.391 |
| `registry-formats-mixed-source-ci` | `Scratch/gf/p2` | `audit --ci --no-fail-fast -f json` | 0 | 2.145 |
| `registry-formats-mixed-source-outdated` | `Scratch/gf/p2` | `outdated` | 0 | 2.848 |

The exact pin stayed 1.0.0 while both ranges advanced to 1.1.0 under all-update.
Changing only the exact selector to 1.1.0, preserving its registry declaration,
then installing made all three versions 1.1.0. Deleting modules before an
otherwise no-op update restored the same cache refs without consent or
manifest/lock changes.

The Git-only control deliberately made public acquisition unavailable in the
child environment: `outdated` still exited 0, showed Current/Latest/Status/Source
without Wanted, and reported `unknown` with
`[i] Some dependencies could not be checked`. This is **not proof of freshness**
or a skipped verification. In a real mixed-source install, the public skill's
Wanted cell was `-`, with Latest `v1.0.0 (fb285168)` and status `up-to-date`;
the three registry rows retained the values above. Both reports were read-only.

The supplied registry suite also performs these graph controls; they are
retained rather than omitted from the command record, but do not constitute
a separate Chapter 9 verdict:

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `registry-registry-graph-frozen` | `Scratch/g/p2` | `install --frozen` | 0 | 4.075 |
| `registry-registry-graph-ci` | `Scratch/g/p2` | `audit --ci --no-fail-fast -f json` | 0 | 4.492 |
| `registry-bounded-direct-unbounded-transitive` | `Scratch/g/p2` | `audit --ci --policy ./apm-policy.yml -f json` | 0 | 3.537 |
| `registry-new-direct-intent` | `Scratch/g/p2` | `install` | 0 | 2.949 |
| `registry-unbounded-direct-fails-policy` | `Scratch/g/p2` | `audit --ci --policy ./apm-policy.yml -f json` | 1 | 2.013 |

## Audit modes, ownership, and cold-cache coverage

Each ordinary drift case appended only a harmless line to the named deployed
file, leaving source and lock untouched. Invalid owners and absent ownership
were deliberately corrupted only in scratch; those locks were not exported as
canonical examples.

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `repro-more-clean-bare` | `Scratch/r2/p1` | `audit -f json` | 0 | 10.449 |
| `repro-repro-ci` | `Scratch/r/p1` | `audit --ci --no-fail-fast -f json` | 0 | 4.345 |
| `repro-copilot-bare-drift` | `Scratch/r/p2` | `audit -f json` | 0 | 5.131 |
| `repro-copilot-ci-drift` | `Scratch/r/p2` | `audit --ci --no-fail-fast -f json` | 1 | 6.707 |
| `repro-claude-bare-drift` | `Scratch/r/p3` | `audit -f json` | 0 | 7.660 |
| `repro-claude-ci-drift` | `Scratch/r/p3` | `audit --ci --no-fail-fast -f json` | 1 | 5.093 |
| `repro-cursor-bare-drift` | `Scratch/r/p4` | `audit -f json` | 0 | 4.765 |
| `repro-cursor-ci-drift` | `Scratch/r/p4` | `audit --ci --no-fail-fast -f json` | 1 | 4.018 |
| `repro-invalid-owner-bare` | `Scratch/r/p5` | `audit -f json` | 1 | 3.914 |
| `repro-invalid-owner-ci` | `Scratch/r/p5` | `audit --ci --no-fail-fast -f json` | 1 | 3.747 |
| `repro-more-unrecorded-same-bytes-ci` | `Scratch/r2/p11` | `audit --ci --no-fail-fast -f json` | 1 | 2.772 |
| `repro-more-invalid-owner-prune` | `Scratch/r2/p10` | `prune` | 0 | 4.548 |
| `repro-more-after-prune-ci` | `Scratch/r2/p10` | `audit --ci --no-fail-fast -f json` | 1 | 5.094 |
| `repro-more-after-prune-install` | `Scratch/r2/p10` | `install` | 0 | 10.743 |
| `repro-more-after-prune-repaired-ci` | `Scratch/r2/p10` | `audit --ci --no-fail-fast -f json` | 0 | 3.275 |
| `final-edges-unrecorded-critical-bare` | `Scratch/e/p1` | `audit -f json` | 1 | 7.492 |
| `final-edges-unrecorded-critical-ci` | `Scratch/e/p1` | `audit --ci --no-fail-fast -f json` | 1 | 4.806 |
| `final-edges-package-selector-narrower` | `Scratch/e/p1` | `audit _local/package -f json` | 0 | 3.008 |
| `final-edges-bare-cold-cache-only` | `Scratch/e/p4` | `audit -f json` | 0 | 4.240 |
| `public-more-cold-public-ci` | `Scratch/u/p3` | `audit --ci --no-fail-fast -f json` | 0 | 25.391 |
| `public-more-cold-offline-ci` | `Scratch/u/p4` | `audit --ci --no-fail-fast -f json` | 1 | 28.990 |

The clean CI fixture had ten named checks, including
`deployment-ledger-owners`, `content-integrity`, and `drift`. Bare audit's
ordinary-drift JSON really said `"passed": true` while stderr described the
drift. Invalid ownership instead failed both modes. The exact failing CI
ownership check was:

```json
{
  "name": "deployment-ledger-owners",
  "passed": false,
  "message": "1 invalid deployment ownership record(s) -- Run 'apm prune', then rerun 'apm audit'.",
  "details": [
    "claude||project|.claude/rules/library.md: invalid owner(s) not-a-declared-owner; invalid active owner not-a-declared-owner"
  ]
}
```

After prune, the next audit still exited 1:

```text
unrecorded: .claude/rules/library.md
```

Install restored complete ownership; the final audit exited 0. Separately,
removing only a Copilot ownership row/file-hash entry while retaining identical
file bytes yielded `unrecorded` CI drift. The unrecorded Critical control
contained only an inert U+202E character-class marker in a governed instruction.
Whole-project bare/CI audit caught it; the package selector omitted that
unrelated file only in the **corrected canonical-selector evidence** described
above. The originally listed `final-edges-package-selector-narrower` call used
`_local/package`, selected **no files**, and returned 0 with the not-found/no-files
warning; it does **not** demonstrate a successful scoped scan. Ch8's validated
`final-source-canonical-scope` instead ran `audit ./package -f json`, actually
scanned **three** recorded package files, and returned 0. The original command
table row and raw warning remain unchanged.

Cold CI checks used independent empty homes/caches and absent modules. Public
success and local-source success left checkout bytes/mtimes unchanged. The
intentionally unavailable public source produced **exit 1**, with both
`config-consistency` and `drift` replay failures—not a harmless green skip.
Exact Git error:

```text
fatal: unable to access 'https://github.com/microsoft/apm-sample-package.git/': Failed to connect to github.com port 443 via 127.0.0.1 after 2016 ms: Could not connect to server
```

The independently executed bare cold-cache control instead exited 0 and
preserved the empty cache/project:

```text
[>] Replaying install (cache-only)...
[!] drift skipped: install cache not populated (run 'apm install' first or pass --no-drift)
```

This records the coverage difference; **the verifier did not follow the
suggestion to disable drift**.

### Independent evidence reused only after equivalence checks

The warning/policy cross-references were already being independently executed
by the Ch8/9 verifier. Rather than share its temp or rerun its suites, this
verifier checked individual command records, preceding version guards,
executable/runner digests, exact argv, both input/output snapshot inventories,
and the specific fixture mutations. Only the named results are reused; an
explorer result or another batch's blanket PASS is not substituted.

| Origin / record | Exact arguments after the same absolute executable | Exit | Original seconds |
| --- | --- | ---: | ---: |
| Ch8/9 `security/warning-install` | `install` | 0 | 4.917 |
| Ch8/9 `security/warning-installed-bare` | `audit -f json` | 2 | 4.357 |
| Ch8/9 `security/warning-installed-ci` | `audit --ci --no-fail-fast -f json` | 0 | 10.690 |
| Ch8/9 `final-source/final-source-canonical-scope` — scope-closure reuse | `audit ./package -f json` | 0 | 3.114 |
| Ch8/9 `policy/policy-blocking` | `audit --ci --policy ./apm-policy.block.yml -f json` | 1 | 4.191 |
| Ch8/9 `policy/env-disables-explicit-policy` | `audit --ci --policy ./apm-policy.block.yml -f json` | 0 | 10.176 |
| Ch8/9 `policy-web/policy-pin-nonempty-mismatch-audit` | `audit --ci --policy https://127.0.0.1:58269/pin.yml --no-cache -f json` | 0 | 6.309 |
| Ch8/9 `policy-final/policy-cold-fetch-default-warn` | `audit --ci --policy https://127.0.0.1:53426/unavailable.yml -f json` | 0 | 8.854 |
| Ch5 `auditrepro-install` | `install` | 0 | 2.906 |
| Ch5 `auditrepro-audit-json` | `audit --ci --no-fail-fast --format json` | 1 | 1.871 |
| Ch5 `frozenlocal-new-local-frozen` | `install --frozen` | 0 | 1.696 |

The Ch5 starting installs/audits, original `frozenlocal`, `local`, and
`auditrepro` version guards, and relevant Ch8/9 guards are retained with the
proof. Original Ch5 output `.bin` files were checked against its JSON;
no old scratch session was resumed. These runtimes and results are **not
additional new native invocations**.

Concrete equivalence checks:

- **Warning-only:** canonical `Ops/repro` manifest and package input, with
  exactly the suite's inert U+200B source-line addition before install.
  Source hash:
  `a9115f7b90916d833da8255e785555831d81f0f3ae95b40e9f3df919be500c02`;
  generated lock:
  `7ea0e332620bb22829ef0a7f6553ad76b95b4c9758d59a16a336e0225c75cff8`.
  Bare and CI saw identical project bytes; all canonical deployed hashes were
  independently recomputed and matched. Bare 2 / CI 0 therefore is not a
  tampered-hash case mislabeled as warning-only.
- **Explicit-policy bypass:** complete project bytes and argv matched between
  blocking and bypass controls. The only added environment setting was
  `APM_POLICY_DISABLE=1`; the exact block-policy hash was
  `ad63f118a4ea443bfaaac271dc107256995011d60783898d1dc5cb55921f41b3`.
  Control JSON failed; bypass JSON passed. This is not policy-compliance PASS.
- **Policy fetch/hash failures:** the actual preceding records returned
  baseline `"passed": true`, exit 0, with unchanged checkout bytes and
  explicit `enforcement skipped` diagnostics. The hash-failure record's
  parent batch later hit a verifier assertion that searched the wrong stream;
  its blanket batch status is **not inherited** here. The complete preceding
  native record and both snapshots were checked independently.
- **Marker-present Ch5 replay:** original authored inputs still match the
  preserved `core-probes/projects/apm-over-plugin` input, including
  `pkg/plugin.json` hash
  `633a0a9f5f80e31649d2e2636bce364afe7523866e3335b9c36acb97c1473d8b`.
  The audit still has exit **1** and changed only these installed cache files:
  `.apm/.plugin-skill-sources.json`, `.apm/prompts/legacy-command.prompt.md`,
  and `apm.yml`, all below `apm_modules/_local/pkg/`. Root manifest, lock,
  authored sources, and native outputs were unchanged. The defect remains
  **FAIL**, not a clean no-write guarantee.
- **Frozen local exception:** all eight canonical `Core` files still match
  the independent Ch5 input inventory/ZIP. Its retained old lock plus only
  the new `./other` skill/declaration produced the independently recorded
  one-to-two dependency change with exit 0. The exact before/after lock hashes
  and mutation equivalence are in the [Ch6 report](ch06-verification.md).
  The original erroneous expected exit `[1]` was not rewritten.

Exact policy warning excerpts:

```text
[!] Policy fetch failed: Policy hash mismatch from url:https://127.0.0.1:58269/pin.yml: expected sha256:a5b879c6f477a62f4cb74561672cab7a5fab6b6262138184bbb203e695e09c7d, got sha256:bebfc7d7892ec4cdb9754054a145ec9d7aa48285ee60d2c6151ef1335a3d0667; enforcement skipped (set policy.fetch_failure_default=block in apm.yml to fail closed)
[!] Policy fetch failed: HTTP 503 fetching https://127.0.0.1:53426/unavailable.yml; enforcement skipped (set policy.fetch_failure_default=block in apm.yml to fail closed)
```

**Diagnosis/owner:** these are the documented baseline-policy and package-form
limitations, not unavailable-network skips. Upstream behavior belongs with
`apm-cli-explorer`; the current author wording correctly limits the signal.
No broader Ch8/Ch9 acceptance is assigned by this report.

## Public no-op and clock-free evidence

The public fixture used `Core/pinned-skill`, with only the selector changed to
`^1.0.0` in scratch. It queried the real anonymous public source; it was not
replaced with a local mock or the Chapter 5 immutable-ref input left unchanged.

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `public-more-semver-install` | `Scratch/u/p5` | `install` | 0 | 17.600 |
| `public-more-semver-noop-preview` | `Scratch/u/p5` | `update --dry-run --verbose` | 0 | 21.561 |
| `public-more-semver-noop-apply` | `Scratch/u/p5` | `update --yes` | 0 | 19.690 |
| `public-more-git-only-outdated` | `Scratch/u/p5` | `outdated` | 0 | 8.684 |
| `final-edges-git-up-to-date-outdated` | `Scratch/e/p2` | `outdated` | 0 | 4.291 |
| `final-edges-git-outdated-verbose-shape` | `Scratch/e/p2` | `outdated --verbose` | 0 | 4.221 |
| `final-edges-semver-ci` | `Scratch/e/p2` | `audit --ci --no-fail-fast -f json` | 0 | 2.297 |
| `repro-more-outdated-local-only` | `Scratch/r2/p1` | `outdated` | 0 | 3.129 |
| `repro-more-outdated-json-unavailable` | `Scratch/r2/p1` | `outdated --json` | 2 | 2.741 |

Both no-op calls reported matching refs and retained complete project hashes.
The real format-2 lock recorded `resolved_tag: v1.0.0`,
`resolved_at: 2026-09-16T02:10:57+00:00`, and complete SHA-256
`2c33fb7959404c4f3d19c7a7da6d143f2fb5d58ce26cb9886e91df214c7eb523`.
It had no `generated_at`. The chapter's older explorer hash remains attached
to that separate historical-within-0.31.0 observation, not reused as this run's
hash. Fresh clock generation and legacy timestamp retention were independently
executed in the shared Ch6 controls.

**Verifier-only failure, transparently retained:** the first checker assumed
every Git-only `outdated` call must print column headers. With all dependencies
current, actual stdout was:

```text
[*] All dependencies are up-to-date
```

The native exit was 0 and project bytes were unchanged. The wrapper assertion
was too strict, not the chapter or CLI. Its original failed assertion and
batch result remain. The corrected expectation was rerun with identical argv
on byte-equivalent input in `final-edges`; the pending semver audit also ran.
The subsequent `registry-formats` controls really rendered and checked both
Git-only and mixed-source table shapes. No chapter change or behavioral
regression was hidden as a network skip.

Live special full-SHA/annotated-tag publication and the interactive default-No
prompt remain explicitly source-inspected contracts, not executed publication
or terminal-interaction experiments. Outdated's lack of a package filter was
checked in actual help; the nonexistent JSON flag was an asserted usage exit 2.

## Trusted preview side effects and cleanup

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `lifecycle-lifecycle-frozen` | `Scratch/l/p1` | `install --frozen` | 0 | 9.172 |
| `lifecycle-lifecycle-ci` | `Scratch/l/p1` | `audit --ci --no-fail-fast -f json` | 0 | 4.147 |
| `lifecycle-lifecycle-validate` | `Scratch/l/p1` | `lifecycle validate` | 0 | 3.799 |
| `lifecycle-lifecycle-trust` | `Scratch/l/p1` | `lifecycle trust` | 0 | 4.261 |
| `lifecycle-install-preview-no-events` | `Scratch/l/p1` | `install --dry-run` | 0 | 7.051 |
| `lifecycle-update-preview-has-pre-events` | `Scratch/l/p1` | `update --dry-run` | 0 | 8.593 |
| `lifecycle-update-preview-kill-switch` | `Scratch/l/p1` | `update --dry-run` | 0 | 4.540 |
| `lifecycle-uninstall-preview-pre-event` | `Scratch/l/p1` | `uninstall ./package --dry-run` | 0 | 4.662 |
| `lifecycle-lifecycle-untrust` | `Scratch/l/p1` | `lifecycle untrust` | 0 | 3.489 |
| `lifecycle-uninstall-retains-edited-file` | `Scratch/l/p1` | `uninstall _local/package` | 1 | 3.583 |
| `lifecycle-more-trust` | `Scratch/l2/p1` | `lifecycle trust` | 0 | 11.003 |
| `lifecycle-more-unrelated-edit-install` | `Scratch/l2/p1` | `install` | 0 | 22.290 |
| `lifecycle-more-subtree-edit-install` | `Scratch/l2/p1` | `install` | 0 | 10.594 |
| `lifecycle-more-retrust-failing-recorder` | `Scratch/l2/p1` | `lifecycle trust` | 0 | 9.959 |
| `lifecycle-more-nonfatal-seven` | `Scratch/l2/p1` | `install --verbose` | 0 | 14.346 |
| `lifecycle-more-stale-edited-install` | `Scratch/l2/p2` | `install` | 0 | 12.913 |
| `cleanup-limit-lifecycle-frozen` | `Scratch/w/p1` | `install --frozen` | 0 | 9.814 |
| `cleanup-limit-lifecycle-ci` | `Scratch/w/p1` | `audit --ci --no-fail-fast -f json` | 0 | 4.440 |
| `cleanup-limit-windows-locked-cleanup-reports-success` | `Scratch/w/p1` | `uninstall ./package` | **0** | 4.147 |

Assertions checked the event file, not just console messages:

- Untrusted materialization and trusted `install --dry-run`: no events.
- Trusted update preview: exactly `["pre-update", "pre-install"]`.
- Same preview with **child-only** `APM_NO_SCRIPTS=1`: unchanged recorder.
- Uninstall preview appended `pre-uninstall`.
- Unrelated description edit preserved trust and emitted pre/post-install.
  Changing the lifecycle subtree revoked trust and left the recorder unchanged.
- After retrusting `python record.py --fail`, APM returned 0 while the isolated
  `scripts.log` recorded **`exit_code=7`**. The script records only synthetic
  event names, never environment values or payload paths.

### Edited target refusal — PASS negative test

The edited target, declaration, and lock remained; modules were already
removed in part. Exact refusal output, following the module-removal message:

```text
Retained user-edited file .github/instructions/notice.instructions.md from ./package; resolve it and retry.
[x] Uninstall could not remove tracked target files; manifest and lockfile ownership were preserved. Package directories may already have been removed.
[x]   - .github/instructions/notice.instructions.md
[x] Resolve or remove the listed files, then retry uninstall.
```

Stderr was empty. **Diagnosis:** expected preservation of a user edit, not
blanket transactional rollback. No author correction is required.

### Windows locked-file cleanup — underlying FAIL retained

A real `CreateFileW` handle with share mode zero held
`apm_modules/_local/package/apm.yml`. Both before/after inventories recorded
`PermissionError` while the handle was held; after closing only this verifier's
handle, the file remained and matched its original source bytes.

Nevertheless uninstall exited **0**, removed the declaration/ownership and
dependency-only lock, and printed:

```text
[i] Removed _local/package from apm_modules/
[*] Uninstall complete: Removed 1 package(s) from apm.yml, Removed 1 package(s) from apm_modules/
```

There was **no error output; stderr was empty**. This is the reproduced
success-reporting defect, not a successful deletion. Suggested owner:
`apm-cli-explorer` / upstream Windows cleanup implementation. The chapter
already states the exact limitation and does not prescribe killing processes,
deleting broad target directories, or blindly retrying a removed identifier.

The separate stale-edit install retained the old edited target with this warning:

```text
[!]   Kept user-edited file .github/instructions/notice.instructions.md (from ./package); delete manually if no longer needed
```

### Native MCP controls — limited coverage, not runtime certification

The original MCP fixture's baseline installation/audit and frozen manifest
mismatch controls are listed in the shared Ch6 report. These coupled Ch7
controls used the same fixture or a byte-equivalent copy of this verifier's
own clean snapshot:

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `mcp-mcp-native-missing-not-audit-gated` | `Scratch/m/p1` | `audit --ci --no-fail-fast -f json` | 0 | 5.876 |
| `mcp-more-edited-native-ci` | `Scratch/m2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 22.025 |
| `mcp-more-edited-native-frozen` | `Scratch/m2/p1` | `install --frozen` | 0 | 12.272 |
| `mcp-more-missing-native-update-preview` | `Scratch/m2/p1` | `update --dry-run` | 0 | 8.700 |
| `mcp-more-missing-native-update-yes` | `Scratch/m2/p1` | `update --yes` | 0 | 22.114 |
| `mcp-more-repaired-native-ci` | `Scratch/m2/p1` | `audit --ci --no-fail-fast -f json` | 0 | 12.650 |
| `mcp-mcp-native-write-error` | `Scratch/m/p1` | `install` | 1 | 15.517 |
| `mcp-force-does-not-hide-write-error` | `Scratch/m/p1` | `install --force` | 1 | 13.869 |

Missing/edited native config was not detected by CI audit. Frozen left the
edited arguments intact. After removing the file, update preview did not
recreate it; accepted update did. The deliberately nonexistent MCP executable
was never launched.

For a directory occupying the required JSON path, both install variants
reported this error (only the path prefix is symbolized):

```text
Error configuring MCP server: [Errno 13] Permission denied: 'Scratch/m/p1/.github/mcp.json'
```

Both then reported:

```text
MCP configuration failed for selected runtime(s): operations-fixture (copilot). Fix the failed runtime MCP config and rerun apm install.
```

**Diagnosis:** intended I/O-failure controls, not a network skip and not evidence
that `--force` repairs arbitrary filesystem problems. Missing/edited native
audit results remain a separate confirmed coverage limitation.

## Marketplace-only release gate

The literal block used `Ops/pack-check`. The missing-override test started
from this verifier's clean generated snapshot. The mixed-output test combined
canonical `Producer/local-bundle` sources with the contained local
`Producer/marketplace` package/configuration, then installed/audited and
generated its own real ZIP/catalog before deleting only the ZIP.
`Producer/metadata-offline` provided the pinned public metadata-negative input.
No canonical fixture or genuine input lock was hand-edited.

| Record ID | CWD | Arguments | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `pack-pack-check-frozen` | `Scratch/p/p1` | `install --frozen` | 0 | 11.338 |
| `pack-pack-check-ci` | `Scratch/p/p1` | `audit --ci --no-fail-fast -f json` | 0 | 3.821 |
| `pack-pack-generate-local-output` | `Scratch/p/p1` | `pack --offline --json` | 0 | 4.416 |
| `pack-check-clean-readonly` | `Scratch/p/p1` | `pack --check-clean --offline --json` | 0 | 4.656 |
| `pack-check-clean-drift-four` | `Scratch/p/p1` | `pack --check-clean --offline --json` | 4 | 9.529 |
| `pack-more-missing-output-override` | `Scratch/p2/p1` | `pack --check-clean --offline --json --marketplace-path claude=alternate/marketplace.json` | 4 | 17.193 |
| `pack-more-mixed-install` | `Scratch/p2/p2` | `install` | 0 | 13.451 |
| `pack-more-mixed-ci` | `Scratch/p2/p2` | `audit --ci --no-fail-fast -f json` | 0 | 10.347 |
| `pack-more-mixed-generate` | `Scratch/p2/p2` | `pack --offline --force --archive --json` | 0 | 12.549 |
| `pack-more-mixed-missing-zip-clean` | `Scratch/p2/p2` | `pack --check-clean --offline --force --archive --json` | 0 | 8.087 |
| `pack-more-offline-uncertifiable` | `Scratch/p2/p3` | `pack --offline --check-clean --json` | 4 | 10.707 |
| `pack-more-strict-offline` | `Scratch/p2/p3` | `pack --offline --strict-metadata --json` | 5 | 11.285 |
| `pack-more-strict-before-clean` | `Scratch/p2/p3` | `pack --offline --strict-metadata --check-clean --json` | 5 | 11.926 |

The clean and dirty checks retained project bytes; the recorded inventories
also include mtimes. Missing override and mixed-output checks explicitly
asserted unchanged bytes **and mtimes**. The override was not created.
The deleted bundle ZIP stayed absent even though clean marketplace comparison
returned 0. Thus the chapter's **catalog cleanliness, not bundle certification**
qualification is essential and verified.

Offline negative JSON diagnostics were exactly:

| Condition | Exit | Error code |
| --- | ---: | --- |
| Edited generated catalog | 4 | `marketplace_drift` |
| Uncertifiable offline metadata with clean check | 4 | `marketplace_metadata_uncertifiable` |
| Strict offline metadata | 5 | `metadata_incomplete` |
| Strict metadata plus clean check | 5 | `metadata_incomplete` |

These are **PASS expected-negative tests**, not network skips or repaired
metadata. The CLI's actual error envelopes and unchanged state are retained
in the named logs/snapshots.

## Final limits, fixes, and handoff

- **Updated runnable examples marked `SKIPPED-needs-network`: none.**
  Public sources and the owned loopback registry were exercised. Deliberately
  unavailable acquisition, offline metadata, drift, and ownership cases asserted
  their expected outcomes instead of being skipped.
- No historical 0.23.1 command, private repository, live push/publish, real
  organization authority, paid runtime, agent callback, or MCP process was
  executed or newly stamped. Source-inspected tag and interactive-prompt
  contracts remain visibly bounded in the chapter.
- A passing test of a documented failure is **not** a passing implementation
  guarantee. Selected-registry cache contamination, Windows cleanup leftovers,
  marker-present replay mutation, native MCP coverage, and policy bypass/fetch
  limits remain visible. No drift suppression or hidden repair erased them.
- All sixteen current Ch6/Ch7 code blocks matched their recorded inputs;
  complete manifests were actually materialized and audited, not merely
  YAML-parsed. Protected canonical inputs remain unchanged. Ch7's source hash
  changed only for the parent's narrow scope comment/prose correction, verified
  in the dated delta above. Raw logs preserve clocks, identities, normalized
  hashes, and before/after files rather than trusting success messages.
- **Content/fixture edits by this verifier: none. Further prose correction
  requested: none for the corrected final source SHA.** The parent's
  package-selector correction is closed using validated independent Ch8
  evidence, with no new CLI run and the original no-files record retained.
  The separate original no-table verifier assertion and its earlier rerun
  remain recorded without alteration.
- Verifier-owned repository changes are only `ch06-verification.md` and this
  report. No other chapter/fixture/research metadata, TOC, site, root
  dependencies, commits, or publication were changed.

**Handoff: Chapter 7 code-verification PASS with documented underlying CLI
failures retained; reviewer decision remains separate.**
