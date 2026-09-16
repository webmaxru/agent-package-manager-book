# Chapter 5 independent verification — book 1.2 / APM 0.31.0

**Current code-gate verdict: PASS — opening-comment privacy-only delta,
2026-09-16 UTC.** Only the two workstation-specific path references were
replaced. Every byte outside the opening HTML comment is unchanged.
This closes the source-identity update without reopening the chapter or
assigning reviewer acceptance.

## Final privacy-only delta — current source identity

| Revision | SHA256 |
| --- | --- |
| Supplied accepted snapshot and preceding independent code-gate PASS | `c06627ac2367a41f9d8a427a6021b695c4c4d28237ca4c3cda951a56effe1e25` |
| **Current independently checked source** | **`286f2d6a873b7152a09033a0e5c2330bbef8004a42818e103e6b7e594e9c3d1a`** |

**Chapter:** `content/chapters/install-and-restore.html`.
The comparison input is
`RunRoot/integration-inputs/accepted/install-and-restore.html`; its
measured hash matches the supplied `c066…` identity and the previously
captured `VerifyRoot/provenance-delta/chapter-source.html`.

**Exact change scope — PASS:** the final file reconstructs byte-for-byte
from that accepted snapshot by replacing only opening-comment lines
**16** and **20**:

- The `RunRoot` definition now names the orchestrator's symbolic session
  artifact directory under `files/book-v1.2`.
- The executable reference is now
  `RunRoot/apm-native/unpacked/apm-windows-x86_64/apm.exe`.

There are no changes after the opening comment's closing delimiter.
Rendered prose, captions, all **16 raw `<pre><code>` blocks**, their
attributes/entities/whitespace/line endings, and all operative claims are
therefore unchanged. All **eight Core fixture files**, including the three
genuine locks, still match the prior input hashes and `canonical-core.zip`
bytes. No path cleanup, code normalization, or lock regeneration was
applied to an executable fixture.

**CLI evidence:** retained exact **APM 0.31.0** execution.
**New APM invocations: 0**, including no new `--version` invocation.
**New native runtime: 0.000 s.** No scratch project was created or resumed.
The original command exits/runtimes, expected-negative results, native and
legacy-marker audit **FAIL** records, historical **0.23.1** stamps, and
private/live skip dispositions remain unchanged.

The read-only comparison
`python <VerifyRoot>/privacy-delta/check.py <Repo>` exited **0** in
**0.056 s**, completed `2026-09-16T03:11:30.944698Z`.
`VerifyRoot` means `RunRoot/verify-ch05`; `Repo` is the book checkout.
Receipts are `VerifyRoot/privacy-delta/check.json`, `chapter-source.html`,
`report-before.md`, and `check.py`. Prior evidence was not overwritten.

The separate [checkout verification](checkout-verification.md) establishes
canonical **Git/LF on Windows**, not Linux execution. The existing
fixture attributes pin generated locks/catalog JSON to LF; ordinary
source files remain platform text. This privacy delta changes neither
that attribute policy nor any source/lock line endings.

**Verifier change: this report only**, plus owned raw receipts. The
author supplied the two comment edits. No new behavior or general
cross-platform guarantee is asserted. Final integration review remains
responsible for the new provenance identity; no reviewer acceptance is
claimed here.

---

## Previous provenance/status delta — retained for source `c066…`

The following verdict and source identity describe the preceding revision.
Its full execution evidence and underlying failures remain intact.

**Current code-gate verdict: PASS — final provenance/status-only delta,
2026-09-16 UTC.** The previous independent PASS carries forward to the
source below. This continuation covers the author's removal of obsolete
waiting-status wording and confirms the clarified APM-package versus
legacy-marker provenance; it does not establish new CLI behavior or issue
a reviewer decision.

## Final provenance/status delta — current source identity

**Chapter:** `content/chapters/install-and-restore.html`

| Revision | SHA256 |
| --- | --- |
| Previous independent code-gate PASS | `b0e4d83bb09ec4c04c5de269e1d75f14d81107b631ddbaa262fd8ab6046e7393` |
| **Current independently checked source** | **`c06627ac2367a41f9d8a427a6021b695c4c4d28237ca4c3cda951a56effe1e25`** |

**Scope:** author cleanup of obsolete “await delta verification/review”
clauses/comments, plus clarification that the tested marker-present
input was an **eligible APM package with a co-located legacy
`plugin.json` marker**, followed by the separately identified marker-free
control. No manifest, command, fixture, lock, target, or expected outcome
changed. The frozen local-path exception and both audit limitations remain
visible. Unrelated historical blocks were not reopened.

**CLI evidence:** retained exact **APM 0.31.0** execution.
**New APM invocations: 0**, including **no new `--version` invocation**.
**New native runtime: 0.000 s.** No scratch project was resumed or created.
The original **143 invocations / 562.791 s** and their dates, raw logs,
failed assertions, and per-example outcomes remain unchanged.

### Independent comparison — PASS

- All **16 complete `<pre><code>` blocks**, including attributes, entities,
  whitespace, and line endings, are byte-identical to the preserved
  executed source. The previous PASS already attested that same equality
  for source `b0e4…`; this is the executable identity chain, not a
  manufactured copy of the earlier full prose revision.
- The decoded ID-to-code map still equals `VerifyRoot/chapter-blocks.json`.
  Its sorted-key compact UTF-8 JSON SHA256 remains
  `dab23b0ed340c32eb4e354783c74348b4a417188974fa2ec891f7a7c052dd96c`.
- All **eight Core fixture files** — three manifests, three complete
  generated locks, and two source files — match `source-inputs.json` and
  `canonical-core.zip` byte-for-byte. The two complete chapter manifests
  still equal their canonical inputs; the displayed four-command argv
  sequence is unchanged.
- The named current status/provenance anchors agree with the prior
  verdict: the obsolete waiting clauses are absent; the input is correctly
  described as an eligible APM package, not a native Agent Plugin; only
  `pkg/plugin.json` is omitted for the clean control. The original
  marker-present audit failure is still explicit.
- The directly relevant retained before-inventories and lock snapshots
  confirm that distinction: marker-present and marker-free inputs both
  classify as `apm_package`; the latter differs by **only**
  `pkg/plugin.json` before first install. No fixture was silently repaired.
- The executable file digest still equals
  `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
  This is a file-identity check, **not** a fresh version execution.

The comparison command was
`python <VerifyRoot>/provenance-delta/check.py <Repo>`: exit **0**,
**0.647 s** read-only check runtime, completed
`2026-09-16T02:20:39.321981Z`. Only evidence receipts were written outside
the repository. `VerifyRoot` retains its alias below:
`RunRoot/verify-ch05`; `Repo` means the book checkout. Published artifacts
do not embed workstation-specific paths.

### Retained outcomes and status scope

Commands are exact arguments after the original absolute `& $Apm`.
These rows are **reused independent execution, not new invocations**:

| Record ID | Command | Exit | Original runtime (s) | Status retained |
| --- | --- | ---: | ---: | --- |
| `control-no-marker-install` | `install` | 0 | 5.954 | PASS, selected marker-free input |
| `control-no-marker-audit` | `audit --ci` | 0 | 5.485 | PASS, selected marker-free input |
| `control-no-marker-contraction` | `install` | 0 | 4.608 | PASS, manifest target contraction |
| `control-no-marker-contracted-audit` | `audit --ci` | 0 | 3.695 | PASS, contracted marker-free input |
| `ownership2-four-target-audit` | `audit --ci` | **1** | 7.583 | **FAIL**, documented marker-present replay defect |

`ch5-current-restore` and the selected `ch5-target-ownership-control`
retain their independent PASS scopes. The twelve unchanged canonical
fixture commands remain covered by the preceding independent gate, not a
new execution claim. The marker-present legacy-command mismatch and
installed-module mutation remain **FAIL**, with the exact diagnostics in
the retained F2 record below. Native-plugin canonical-IR audit failure,
historical **0.23.1** stamps, and private/live
`SKIPPED-needs-network` dispositions are unchanged.

**Verifier-applied change for this continuation:** this report only.
The author supplied the chapter cleanup; the verifier changed no chapter,
fixture, root dependency, metadata, site, or unrelated state.
No reviewer acceptance is claimed by this continuation.

Receipts: `VerifyRoot/provenance-delta/check.json`, `chapter-source.html`,
`report-before.md`, and `check.py`. The prior report and original failed
execution records are preserved rather than rewritten.

---

## Previous verifier delta — retained record for source `b0e4…`

The following verdict and line anchors describe the preceding source
revision, not a second new execution or a current reviewer decision.

**Verdict: PASS — narrow delta verification completed 2026-09-16 UTC.**
F1's revised frozen-install claims and F2's explicitly selected marker-free
control agree with the persisted independent evidence. The code-verifier
blockers are resolved for the finalized source below; **reviewer acceptance
has not been assigned**. The marker-present audit defect remains an actual
**FAIL**, now visibly documented, not a network skip or a repaired CLI.

## Delta verification — revised claims and source identity

**Chapter:** `content/chapters/install-and-restore.html`
**Target/evidence CLI:** APM **0.31.0**, retained original execution.
**New APM invocations:** **0**; delta native runtime **0.000 s**.

| Source revision | SHA256 |
| --- | --- |
| Originally executed, preserved as `VerifyRoot/chapter-source.html` | `eb84cb1c4e8d78a23bc77aec2771ce795bfadb89b5555292a0287f83d55579fc` |
| Author correction received for this delta, before caption finalization | `c704b1035656f32860593f7f3ad807afbf0ac960a27df76b0f3340a1615a777e` |
| **Final verified chapter, after removing only the requested caption fragment** | **`b0e4d83bb09ec4c04c5de269e1d75f14d81107b631ddbaa262fd8ab6046e7393`** |

This was a read-only evidence comparison followed by the single authorized
caption edit, **not a resumed verifier session or a new execution batch**.
The author's selected control already ran in the original 143 invocations;
no new executable input or previously untested behavior requires a rerun.
No old scratch project was resumed and no new scratch project was needed.
The original invocation count, dates, **562.791 s** summed native runtime,
raw outputs, failed assertions, and historical-version boundaries remain
unchanged.

### Identity and executable equivalence — PASS

- All **16 `<pre><code>` blocks** are byte-identical to the captured chapter,
  including code attributes, HTML entities, whitespace, and line endings.
  Their decoded ID-to-code map also equals `VerifyRoot/chapter-blocks.json`.
  SHA256 of that map, serialized as sorted-key compact UTF-8 JSON
  (`ensure_ascii=False`, separators `(',', ':')`):
  `dab23b0ed340c32eb4e354783c74348b4a417188974fa2ec891f7a7c052dd96c`.
- All **eight canonical fixture paths and byte hashes** match
  `source-inputs.json`, `final-source-checks.json`, and `canonical-core.zip`:
  three manifests, three complete locks, and two authored source files in
  `backend/examples/updates/1.2/core/`. The two complete chapter manifests
  still match their canonical inputs. No fixture was edited or regenerated.
- The twelve literal fixture records still show the exact displayed
  `install`, `install`, `install --frozen`, `audit --ci` sequences, all exit
  **0**, with the complete lock hashes recorded below. Their native output
  bytes and post-command snapshot hashes were cross-checked, not reexecuted.
- The prepared executable's current file SHA256 still equals
  `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
  All **18 persisted `--version` guards** were re-read and assert exit 0 and
  exactly `Agent Package Manager (APM) CLI version 0.31.0`. Supporting
  records identify the same absolute executable/digest and a preceding
  guard in their isolated batch. **No fresh `--version` invocation is
  claimed.**
- The chapter diff contains claim/provenance/status prose only. Historical
  0.23.1 blocks, current expected-negative commands, native-target outcome
  commands, and private/live skips were neither changed nor restamped.

Read-only Python checks (`python -`, inline assertions; no file writes)
exited **0**: source/code/fixture/binary checks **0.994 s**; scoped raw
JSON/output-byte/ZIP/ledger checks **0.630 s**; post-caption checks
**0.022 s**. The evidence check compared **43 retained records**, including
the 18 version guards, and finished at `2026-09-16T01:16:29.850117Z`.
Final-source checks finished at `2026-09-16T01:18:01.224526Z`. These are
read-only check runtimes, not additional APM execution or elapsed review time.

### Delta per-example disposition

These dispositions supersede only the original **chapter-claim** blockers.
Other per-example statuses and CLI stamps in the original record below are
retained; none represents a new run.

| Example ID / path | Current status | CLI evidence | Resolution |
| --- | --- | --- | --- |
| `ch5-current-restore`, `Chapter#ch5-frozen-boundary`, exercise and closing prose | **PASS** | 0.31.0, retained | **F1 resolved:** existing-lock requirement, limited structural checks, and the new-local-declaration exception are explicit; the twelve unchanged fixture commands remain PASS |
| `ch5-target-ownership-control`, `ProbeInputs/apm-over-plugin` minus only `pkg/plugin.json`, then `ProbeInputs/manifest-contraction/apm.yml` | **PASS**, selected marker-free control | 0.31.0, retained | **F2 resolved for the chapter:** the deliberately selected, already verified control installs and audits before/after contraction; original native runtime **19.742 s** |
| Original marker-present `ch5-target-ownership-control` audit reproductions | **FAIL**, documented CLI limitation retained | 0.31.0, retained | Legacy-command replay mismatch and installed-module mutation are not repaired or relabeled; diagnosis/upstream owner remains `apm-cli-explorer` |

### F1 resolution — PASS

At finalized chapter lines **397–410**, **915–918**, and **1044–1046**, the
author now says frozen install performs **limited structural checks**,
requires an existing lock, and can deploy a newly declared local dependency
and rewrite that lock with exit **0**. The exercise and closing paragraph
both link to the exception. Cold acquisition and the separate content-audit
boundary remain correctly scoped.

The raw `frozenlocal-new-local-frozen` before-state retained the exact
one-dependency lock. Only the manifest declaration and new `other/SKILL.md`
had been added by setup. Its successful command added
`.agents/skills/other/SKILL.md` and `apm_modules/_local/other/SKILL.md`,
changing the lock from one dependency to two with the old/new hashes in F1
below. Stderr was empty. This is now the **asserted exception**, not a
refusal claim. The original `expected_exit_codes: [1]` / failed assertion
is preserved as evidence of the old wording error.

The missing-Git and missing-lock controls both retain exit **1**, the
specific refusal diagnostics below, and identical before/after file hashes
**and mtimes**. `cold-frozen` still demonstrates successful locked-source
hydration without a lock change. The cited frozen source at commit
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`,
`src/apm_cli/install/plan.py:453–487`, explicitly skips local dependencies
in its presence check, consistent with—not a substitute for—the execution.

### F2 resolution — PASS for the selected control; original audit FAIL retained

Finalized chapter lines **425–437** identify the precise marker-free
provenance; lines **439–451** disclose both its successful sequence and the
marker-present defect. Independent byte/state comparisons establish:

1. `inputs/om.zip`, `inputs/oc.zip`, and `inputs/tc2.zip` contain the same ten
   authored files and match the preserved `ProbeInputs/apm-over-plugin`
   input. The `control-no-marker-install` before-state equals that input
   **minus only `pkg/plugin.json`**. `pkg/legacy-command.md` and every other
   authored file remain; there was no initial lock or generated deployment.
   `mutations/control-remove-marker.json` records the omitted marker's
   original hash:
   `633a0a9f5f80e31649d2e2636bce364afe7523866e3335b9c36acb97c1473d8b`.
2. `mutations/control-no-marker-contract.json` replaces only the manifest
   target list `[copilot, claude, cursor, kiro]` with `[copilot]`. Its bytes
   match `ProbeInputs/manifest-contraction/apm.yml`: manifest SHA256
   `f6d2b95240f3947e7b0118ab07b6d75899c84c7a0760f15c4644f4385e47b6dc`
   becomes
   `c539ce0a45a263a2145224e10eb110b8e890a71292bf2f890ea1e783ae19cd8c`.
   No lock or installed material was edited to make audit pass.
3. The generated ledgers select `package_type: apm_package`, first across
   four targets and then Copilot only. Snapshot comparison confirms removal
   of the ten stale native file paths, retention of the four surviving
   Copilot/shared files and all eight marker-free package source files,
   and matching canonical deployed-text hashes. Both audits report
   `[*] All 10 check(s) passed` and leave project byte inventories unchanged.
4. The separate `ownership2` control remains the evidence for preservation
   of added human-authored Claude/Cursor/Kiro files. Those files were **not**
   retroactively attributed to the marker-free input; the chapter comment
   correctly points to `assertions/ownership2.json`.
5. `ownership2-four-target-audit`, `ownership2-contracted-audit`, and
   `auditrepro-audit-json` still exit **1** for unintegrated legacy commands.
   Their recorded mutations add only the two installed `.apm` files and
   change `apm_modules/_local/pkg/apm.yml`, exactly as listed in original F2.
   Authored source, root manifest, lock, and deployed files remain unchanged
   by those audits. The original exact diagnostics below remain applicable;
   **no network skip, drift suppression, or audit-clean relabeling** occurred.

### Exact retained commands supporting the revised claims

Aliases retain their original definitions below. Commands are exact
arguments following `& $Apm`; CWD is under `Scratch/p`. All executions in
this table are from the **original 2026-09-16 batch, not this delta**.

| Record ID | CWD | Command | Revised expected / recorded exit | Original runtime (s) |
| --- | --- | --- | --- | ---: |
| `frozenlocal-new-local-frozen` | `fl` | `install --frozen` | 0 / 0, documented local exception | 1.696 |
| `frozenlocal-missing-git-frozen` | `fg` | `install --frozen` | 1 / 1, expected structural refusal | 1.780 |
| `boundaries-missing-lock` | `fm` | `install --frozen` | 1 / 1, expected missing-lock refusal | 6.193 |
| `control-no-marker-install` | `om` | `install` | 0 / 0 | 5.954 |
| `control-no-marker-audit` | `om` | `audit --ci` | 0 / 0 | 5.485 |
| `control-no-marker-contraction` | `om` | `install` | 0 / 0 | 4.608 |
| `control-no-marker-contracted-audit` | `om` | `audit --ci` | 0 / 0 | 3.695 |

### Minimal fix and reviewer gate

**Only verifier-applied chapter diff:** remove
`; claim correction pending` from the `ch5-current-restore` caption
(finalized line **940**). Restoring exactly that fragment reconstructs the
author-input SHA256 above, proving there was no other editorial change.
The final chapter hash was computed **after** this finalization. No
executable block, manifest, fixture, root dependency, metadata, TOC, site,
or unrelated user/global state was changed. No new sample files, agents,
commits, publishing, or historical/live executions were introduced.

**Reviewer gate handoff: code verification PASS; reviewer decision pending.**
F1/F2 author corrections are sufficient and require no CLI rerun. The
separate native-plugin audit limitation, marker-present audit FAIL,
private/live skips, and historical 0.23.1 boundaries remain visible.
Other author/reviewer status wording was intentionally left untouched.

The original report and raw evidence are retained below. In particular,
`summary.json`, `verification-status.json`, and original failed assertion
records still describe the originally executed source SHA; they were not
rewritten to erase failures. This dated delta supplies the current
source-specific disposition.

---

## Original verification record — retained, claim gate superseded above

**Original verdict: FAIL — not ready for reviewer acceptance.** The twelve literal
install/replay/frozen/audit commands in the three current fixtures all passed.
However, independent coupled tests found an overbroad frozen-install claim
(F1) and an undisclosed audit failure in the target-contraction control (F2).
Neither is a network skip.

**Originally verified source:** `content/chapters/install-and-restore.html`

```text
SHA256: eb84cb1c4e8d78a23bc77aec2771ce795bfadb89b5555292a0287f83d55579fc
```

The chapter and all eight files in `backend/examples/updates/1.2/core/` had
identical hashes before and after verification. This verdict applies to that
chapter revision, not a subsequent author edit. No chapter prose, verification
caption, canonical fixture, root dependency, site, or edition metadata was
changed by this verifier. No commit or publication was made.

## Execution and evidence

- **CLI actually executed:** exactly **0.31.0**, using the orchestrator's
  prepared executable, never PATH-resolved `apm`.
- **Executable SHA256:**
  `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
- **Execution date:** 2026-09-16 UTC. First invocation started at
  `00:42:30.409634Z`; the last started at `00:54:19.627604Z`.
- **143 native CLI invocations:** 18 exact-version guards, 8 help commands,
  and 117 example/control invocations, including retained initial attempts
  and independent reproductions. Summed native runtime: **562.791 seconds**.
  Batches overlapped; that sum is not elapsed time or a performance benchmark.
  No command timed out.
- Windows x64; Python 3.12.10 / PyYAML 6.0.3 for orchestration and independent
  file assertions. APM itself, not a Python reimplementation, parsed and
  installed the manifests and ran the audits.

Aliases used below deliberately avoid publishing workstation-specific paths:

| Alias | Meaning |
| --- | --- |
| `RunRoot` | Orchestrator's session artifact directory `files/book-v1.2` |
| `VerifyRoot` | `RunRoot/verify-ch05` |
| `Scratch` | Fresh, uniquely owned short temporary root recorded in `VerifyRoot/runtime-layout.json` |
| `Core` | `backend/examples/updates/1.2/core` in the book checkout |
| `ProbeInputs` | `RunRoot/core-probes/projects` |
| `Chapter` | `content/chapters/install-and-restore.html` |

Every command table gives the **exact arguments following `& $Apm`**:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

All 18 batches independently checked that exact banner and executable digest
before example execution. The top-level help and `init`, `install`, `audit`,
`preview`, `run`, `compile`, and `list` help all exited 0.

Projects ran in **normal short working directories**, not the book checkout,
long artifact paths, or `--root` redirection. Each batch had a separate
isolated home, APM cache, application-data/config paths, and temp directory.
Child environments were allowlisted: no inherited host credentials, APM
policy bypasses, `gh` launcher, or AI-runtime PATH entries; Git user/system
configuration and credential helpers were isolated. There were no real
global installs. The one global dry-run used only the isolated home and
changed neither it nor its project.

Local suites also passed with HTTP/HTTPS proxies directed to unavailable
loopback, demonstrating that their local operations did not require those
network transports. Public tests used actual anonymous Git access to the
pinned sample. Failure reproductions were repeated **without** that offline
proxy to eliminate it as a cause.

### Durable artifacts

| Under `VerifyRoot` | Contents |
| --- | --- |
| `chapter-source.html`, `chapter-blocks.json`, `source-inputs.json` | Exact tested chapter, extracted executable blocks, and initial hashes |
| `runtime-layout.json` | Actual executable, short scratch paths, platform, isolation |
| `logs/<record-id>.json` | Exact absolute command/argv/CWD, native exit, stdout/stderr, duration, before/after file hashes and mtimes |
| `logs/<record-id>.stdout.bin`, `.stderr.bin` | Original process output bytes |
| `logs/<record-id>.txt` | Readable command, exit, timing, stdout/stderr |
| `inputs/*.zip`, `snapshots/*.zip`, `canonical-core.zip`, `final-projects.zip` | Selected input bytes, per-command resulting projects, canonical comparison locks, final source/output trees |
| `mutations/*.json` | Explicit scratch-only setup edits, before/after bytes and hashes |
| `assertions/*.json`, `batches/*.json` | Independent state assertions and completed batch results |
| `command-index.json`, `summary.json`, `verification-status.json` | Full invocation index, findings, and per-example verification tags |
| `static-checks.json`, `final-source-checks.json` | Historical-code preservation and unchanged chapter/canonical-fixture checks |
| `verify.py`, `summarize.py` | This verifier's reproduction/indexing machinery |

The report excerpts retain diagnostic wording; terminal line endings and
trailing padding are normalized for Markdown. Complete output, including display tables,
is preserved in the named raw logs. Native return codes came directly from
the child process, before any formatting or file analysis. Nonzero batch
wrappers also failed explicitly: no pipeline-last-exit ambiguity.

## Per-example status

All paths below refer to `Chapter#<example-id>` unless a fixture is named.
Runtime is the sum of supporting example/control invocations, excluding
version/help guards. Shared evidence is counted for each covered ID; do not
sum this column as total run time.

| Example ID / fixture path | Status | CLI | Runtime (s) | Result |
| --- | --- | --- | ---: | --- |
| `ch5-discover-apply` | **PASS** | 0.31.0 | 39.654 | Original pre-apply input; inventory, consent, idempotence, invalid target combination, and subsequent materialization asserted |
| `ch5-onboard-manifest` — `Core/onboard-skill/apm.yml` | **PASS** | 0.31.0 | 13.794 | Exact chapter manifest installs, restores, freezes unchanged, and audits; F1 limits changed-local-intent claims |
| `ch5-pinned-manifest` — `Core/pinned-skill/apm.yml` | **PASS** | 0.31.0 | 17.587 | Real immutable public skill resolved; exactly one dependency; expected files and lock reproduced |
| `ch5-current-restore` — all three `Core` fixtures | **FAIL: coupled claim** | 0.31.0 | 149.241 | All twelve displayed commands passed, but the surrounding blanket frozen/matching-lock guarantee is false for newly declared local dependencies; F1 |
| `ch5-current-lock` — `Core/pinned-skill/apm.lock.yaml` excerpt | **PASS** | 0.31.0 | 35.040 | Every excerpt field matched newly generated CLI output; complete lock, native hashes, cold replay, and CRLF boundary checked |
| `ch5-preview` | **PASS** | 0.31.0 | 11.572 | Local prompt compiled with frontmatter removed; no discoverable Copilot runtime required |
| `ch5-targetless` | **PASS**, expected negative | 0.31.0 | 28.619 | Exit 2, no file writes, no `AGENTS.md`; both suggested target repairs independently worked |
| `ch5-missing-runtime` | **PASS**, expected negative | 0.31.0 | 10.172 | Prompt compilation preceded missing-executable exit 1; harmless shell control exited 0 |
| `ch5-native-target-outcomes` | **PASS**, scoped outcomes | 0.31.0 | 33.438 | Real native-only/mixed/preview exits 1/0/0 reproduced; documented native CI audit remains an underlying **FAIL**, not an audit-clean fixture |
| `ch5-meridian-clone` | **SKIPPED-needs-network** | Not executed; target 0.31.0 only | — | Fictional private GitHub SSH repository; no accessible repository or authorized SSH permission |

Additional coupled verification IDs, **not new chapter anchors**:

| Verifier ID / chapter area | Status | CLI | Runtime (s) |
| --- | --- | --- | ---: |
| `ch5-target-ownership-control` — targeting/ownership prose, `ProbeInputs/apm-over-plugin` then `manifest-contraction` | **FAIL**; install cleanup passes but CI replay does not, F2 | 0.31.0 | 98.473 |
| `ch5-add-target-bootstrap-controls` — add writer, target precedence, bootstrap and preview caveats | **PASS** | 0.31.0 | 27.119 |
| `ch5-mcp-writer-control` — separate direct-MCP writer caveat | **PASS**, config-only | 0.31.0 | 16.216 |

## F1 — frozen install does not reject new local declarations

**Status: FAIL, reproducible chapter-claim mismatch.**
**Owner:** `chapter-author` for wording; `apm-cli-explorer` for shared Ch6/CI
reference propagation.

The statement at **Chapter lines 390–394** says:

> The stricter CI cousin, `apm install --frozen`, requires a matching lock
> and refuses new resolution.

That is too broad. Starting from the exact, audit-clean `onboard-skill`
fixture, I retained its generated one-dependency lock, copied a second
ordinary local skill to `other/SKILL.md`, and appended only this declaration:

```yaml
    - path: ./other
```

This was a real dependency-list change, not a lock edit or a missing source.
The resulting manifest was accepted by the real CLI.

| Record ID | CWD under `Scratch/p` | Command | Expected / actual exit | Seconds |
| --- | --- | --- | --- | ---: |
| `frozenlocal-baseline-install` | `fl` | `install` | 0 / 0 | 2.690 |
| `frozenlocal-baseline-audit` | `fl` | `audit --ci` | 0 / 0 | 1.544 |
| `frozenlocal-new-local-frozen` | `fl` | `install --frozen` | **1 / 0** | 1.696 |
| `frozenlocal-new-local-audit` | `fl` | `audit --ci` | 0 / 0 | 1.562 |
| `boundaries-mismatched-lock` — first independent reproduction | `mm` | `install --frozen` | **1 / 0** | 3.181 |

There was **no error output** from the failing-claim command: it succeeded
and changed recorded state. Exact stdout of `frozenlocal-new-local-frozen`
(stderr empty):

```text
[>] Installing dependencies from apm.yml...
[>] Resolving ./other...
[i] Targets: copilot  (source: apm.yml)
  [+] ./.claude/skills/checkout-review (local)
  [+] ./other (local)
  |-- (files unchanged)
  |-- Skill integrated -> .agents/skills/
  [i] Skipped inactive experimental resolver for target 'copilot-cowork' during
lockfile reconciliation.
  [i] Skipped inactive experimental resolver for target 'copilot-app' during
lockfile reconciliation.
[*] Installed 2 APM dependencies in 0.3s.
[i] Lockfile presence verified. Run 'apm audit' for on-disk content integrity.
```

Asserted state effects:

- Added `.agents/skills/other/SKILL.md` and
  `apm_modules/_local/other/SKILL.md`.
- Changed the lock from one dependency to two.
- Old lock SHA256:
  `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28`.
- New lock SHA256:
  `daadeb90f18c0c5958b0c73557b233a94a6fa168c12ad7b9c984a0cb5b9303a7`.

The contrast control added a **pinned Git dependency absent from the lock**,
not a local path. `frozenlocal-missing-git-frozen`, CWD `fg`,
`install --frozen`, exited **1** in **1.780 s**, with no project writes.
Its preceding baseline `install` exited 0 in 1.574 s. The failure explicitly
reported the manifest/lock being out of sync and named
`microsoft/apm-sample-package` as missing. No full-package Git graph was
installed by this refusal test.

The empirical local-path exception is also explicit in the frozen target's
[structural checker](https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/install/plan.py#L453-L487):
local dependencies are skipped by its direct-dependency presence check.
This is an intentional implementation boundary that the blanket book claim
fails to convey, not evidence of a network outage or proof of regression
from a separately tested older version.

**Precise author edit requested:**

1. Replace the blanket sentence at lines 390–394 with a scoped statement, for
   example: “`apm install --frozen` requires an existing lock and performs
   limited structural consistency checks. In 0.31.0, its direct-dependency
   presence check skips local paths: a newly declared local dependency can
   still install and change the lock. It is not an on-disk content audit.”
2. At **lines 893–895**, qualify “frozen install for manifest/lock consistency”
   with that local-path exception; the four commands themselves need no change.
3. At **lines 1024–1026**, call it a **limited** structural CI gate and point
   back to the exception. Keep the successful unchanged/cold replay evidence;
   do not turn this finding into “frozen is always ineffective.”

## F2 — contraction control's install and audit disagree

**Status: FAIL, reproducible APM 0.31.0 audit/replay defect.**
**Owner:** `apm-cli-explorer` for diagnosis/upstream handoff; `chapter-author`
for a visible limitation on the control cited at **Chapter lines 415–429**.

The chapter identifies `ProbeInputs/apm-over-plugin` followed by
`ProbeInputs/manifest-contraction` as its exact ownership control. These
contain an eligible APM package with `.apm` sources **and** a co-located
legacy `plugin.json` pointing to `legacy-command.md`.

Real install selected `package_type: apm_package`, deployed the four intended
targets, and omitted the plugin-only command. Reducing the manifest to
Copilot really did remove stale non-Copilot managed outputs and preserve
the surviving shared/Copilot files, package source, and added human-owned
Claude/Cursor/Kiro files. **That specific cleanup claim passed.**

However, CI audit replay incorrectly expected the legacy command as well:

| Record ID | CWD under `Scratch/p` | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `ownership2-four-target-install` | `tc2` | `install` | 0 | 8.905 |
| `ownership2-four-target-audit` | `tc2` | `audit --ci` | **1** | 7.583 |
| `ownership2-manifest-contraction` | `tc2` | `install` | 0 | 5.916 |
| `ownership2-contracted-audit` | `tc2` | `audit --ci` | **1** | 5.349 |
| `control-same-input-install` — no offline proxy | `oc` | `install` | 0 | 9.270 |
| `control-same-input-audit` | `oc` | `audit --ci` | **1** | 7.039 |
| `auditrepro-install` — another fresh copy | `ar` | `install` | 0 | 2.906 |
| `auditrepro-audit-json` | `ar` | `audit --ci --no-fail-fast --format json` | **1** | 1.871 |
| `auditrepro-reinstall` | `ar` | `install` | 0 | 1.842 |
| `auditrepro-audit-after-reinstall` | `ar` | `audit --ci` | **1** | 1.868 |

Exact failing check from `auditrepro-audit-json` stdout:

```json
{
  "name": "drift",
  "passed": false,
  "message": "drift detected: 3 file(s): .claude/commands/legacy-command.md, .cursor/commands/legacy-command.md, .github/prompts/legacy-command.prompt.md",
  "details": [
    "unintegrated: .claude/commands/legacy-command.md",
    "unintegrated: .cursor/commands/legacy-command.md",
    "unintegrated: .github/prompts/legacy-command.prompt.md"
  ]
}
```

The full JSON reported 10 checks, 9 passed, 1 failed. Exact stderr:

```text
[!] Could not determine org from git remote; enforcement skipped (set policy.fetch_failure_default=block in apm.yml to fail closed)
[>] Replaying install (cache-only)...
[+] Replayed 1 package(s)
[>] Diffing scratch vs working tree...
[!] Drift detected: 3 file(s)
```

After contraction, the exact failing detail was:

```text
  drift details:
    - unintegrated: .github/prompts/legacy-command.prompt.md

[x] 1 of 10 check(s) failed
```

Audit also **mutated installed package material in the real working tree**:

```text
added:   apm_modules/_local/pkg/.apm/.plugin-skill-sources.json
added:   apm_modules/_local/pkg/.apm/prompts/legacy-command.prompt.md
changed: apm_modules/_local/pkg/apm.yml
```

The authored `pkg` source, root manifest, lock, and deployed target files
were unchanged by audit; the mutation was confined to `apm_modules`.
This is not a claimed deletion of human source or a change to the book
checkout. Reinstallation did not cure the next audit.

A separate scratch control removed **only** `pkg/plugin.json` before first
installation; neither the canonical fixture nor an attested lock was edited.
It passed all of:

| Record ID | CWD | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `control-no-marker-install` | `om` | `install` | 0 | 5.954 |
| `control-no-marker-audit` | `om` | `audit --ci` | 0 | 5.485 |
| `control-no-marker-contraction` | `om` | `install` after the same target edit | 0 | 4.608 |
| `control-no-marker-contracted-audit` | `om` | `audit --ci` | 0 | 3.695 |

This isolates the co-located legacy-marker/replay disagreement. The absent
Git-remote policy warning was not the failed check and also occurred in
clean controls. **Do not classify this local defect as
`SKIPPED-needs-network`, suppress drift, or export this mixed-layout control
as an audit-clean example.**

**Precise author action requested:** the cleanup paragraph need not be
reversed, but its exact control needs a visible limitation, for example:
“This control verifies install cleanup only. Its co-located legacy plugin
marker causes a separate 0.31.0 CI audit replay mismatch and mutates the
installed package cache; it is not an audit-clean worked fixture.”
Alternatively, author/explorer may deliberately select the separately
verified marker-free control and update its provenance. Do not silently
substitute it for the original input or relabel the original audit PASS.

## Literal current fixture sequences — all PASS

First-materialization copies contained only these authored files, no lock,
modules, or previously deployed output:

| CWD under `Scratch/p` | Fixture | Inputs beside `apm.yml` |
| --- | --- | --- |
| `li` | `Core/local-instruction` | `.apm/instructions/meridian-checkout.instructions.md` |
| `os` | `Core/onboard-skill` | `.claude/skills/checkout-review/SKILL.md` |
| `ps` | `Core/pinned-skill` | None |

The exact chapter YAML blocks for `ch5-onboard-manifest` and
`ch5-pinned-manifest` matched their canonical manifests. Real CLI installation
established acceptance, not merely a generic YAML parse.

| Record ID | Command | Exit | Seconds |
| --- | --- | ---: | ---: |
| `local-local-instruction-install` | `install` | 0 | 4.584 |
| `local-local-instruction-restore` | `install` | 0 | 2.007 |
| `local-local-instruction-frozen` | `install --frozen` | 0 | 2.429 |
| `local-local-instruction-audit` | `audit --ci` | 0 | 3.031 |
| `local-onboard-skill-install` | `install` | 0 | 2.695 |
| `local-onboard-skill-restore` | `install` | 0 | 2.856 |
| `local-onboard-skill-frozen` | `install --frozen` | 0 | 3.936 |
| `local-onboard-skill-audit` | `audit --ci` | 0 | 4.307 |
| `public-pinned-skill-install` | `install` | 0 | 8.574 |
| `public-pinned-skill-restore` | `install` | 0 | 3.148 |
| `public-pinned-skill-frozen` | `install --frozen` | 0 | 2.969 |
| `public-pinned-skill-audit` | `audit --ci` | 0 | 2.896 |

Each independently generated **complete** lock matched the corresponding
canonical lock. Each replay, frozen install, and CI audit retained those
bytes and the authored source/manifest bytes:

| Fixture | Complete lock SHA256 |
| --- | --- |
| `local-instruction` | `0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa` |
| `onboard-skill` | `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28` |
| `pinned-skill` | `6b9ebb9ddcba38e6eddae38ca0c3658c2fabeee90e279857c9159f149ba09507` |

The expected native files were checked, not inferred from exit 0:

- Local instruction:
  `.github/instructions/meridian-checkout.instructions.md`,
  `.claude/rules/meridian-checkout.md`,
  `.cursor/rules/meridian-checkout.mdc`.
  Their three native representations have different byte hashes.
- Onboard skill: `.agents/skills/checkout-review/SKILL.md`.
  Original Claude-layout source retained; lock ownership authorizes only
  Copilot, not an additional Claude deployment.
- Public skill: `.agents/skills/style-checker/SKILL.md` and
  `.claude/skills/style-checker/SKILL.md`, with no transitive dependency.
  Full commit/ref:
  `fb2851683be0e0e7711421d518bd8dba23b0b1f6`.
  Both deployed canonical text hashes:
  `sha256:1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829`.
  Generated package-tree hash:
  `sha256:867912713bf45048211440b81ea0ced396ad0a0993447dd540fe5c219722d318`.
  The genuine lock says `version: unknown`, `package_type: claude_skill`,
  and `virtual_path: .apm/skills/style-checker`, as excerpted.

Every hashed project-relative ownership record was independently checked
against its actual file. None of the three new locks contains
`generated_at`; the local-instruction-only lock omits `apm_version`.
The exact ownership/native fields in the excerpt were not hand-generated.

### Cold public replay and changed intent

`pc` began with **only** `Core/pinned-skill/apm.yml` and its committed lock,
plus a separate initially empty cache:

| Record ID | CWD | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `cold-frozen` | `pc` | `install --frozen` | 0 | 10.335 |
| `cold-audit` | `pc` | `audit --ci` | 0 | 2.544 |
| `ref-initial-frozen` | `re`, another manifest/lock-only copy | `install --frozen` | 0 | 15.084 |
| `ref-changed-ref-install` | `re` | `install` after editing the selector to `v1.0.0` | 0 | 10.193 |
| `ref-changed-ref-audit` | `re` | `audit --ci` | 0 | 4.743 |

Cold restore genuinely fetched/materialized the public package and both
native destinations without changing the lock. Editing the ref to the
same-commit public tag changed `resolved_ref` and lock bytes under ordinary
install, without moving `resolved_commit`. This verifies reconciliation of
edited intent; it is **not** a new moving-upstream/transitive-graph experiment.

### Frozen versus content audit; CRLF and local sources

These scratch mutations were all inert and recorded, not applied to canonical
fixtures:

| Record ID | CWD | Command / setup | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `boundaries-missing-lock` | `fm` | `install --frozen`, source-only local fixture | 1, expected | 6.193 |
| `boundaries-initial-install` | `fm` | `install` | 0 | 5.833 |
| `boundaries-drift-ci` | `fm` | `audit --ci`, harmless line appended to deployed Copilot rule | 1, expected | 5.739 |
| `boundaries-frozen-repair` | `fm` | `install --frozen` | 0 | 4.998 |
| `boundaries-repaired-audit` | `fm` | `audit --ci` | 0 | 5.284 |
| `boundaries-crlf-ci` | `fm` | `audit --ci`, all three deployed text files changed to CRLF only | 0 | 4.574 |
| `boundaries-source-reconcile` | `fm` | `install`, safe authored instruction-body edit | 0 | 4.001 |
| `boundaries-source-audit` | `fm` | `audit --ci` | 0 | 3.274 |

Missing-lock refusal named `--frozen requires apm.lock.yaml to exist` and
wrote nothing. Drift audit identified the edited native file and was
read-only. Frozen did not reject that content drift: it restored the authored
rule and retained the lock. CRLF-only changes passed canonical text hashing
and CI audit without rewriting those files or the lock. A real local source
edit instead changed deployed content and lock hashes on ordinary install.

The first F1 setup also ran `boundaries-matching-install` (0, 3.515 s),
the unexpectedly successful `boundaries-mismatched-lock` (0, 3.181 s), then
`boundaries-mismatch-reconcile` (0, 3.031 s) and
`boundaries-mismatch-audit` (0, 2.441 s) in `mm`. Those later successes do not
erase its failed frozen-refusal expectation.

## Discovery and init — PASS

`di2` copied exactly the original
`ProbeInputs/onboard/.claude/skills/checkout-review/SKILL.md` and
`.claude/rules/manual-rule.md`, **not** its later manifest/output and **not**
the already-declared `Core/onboard-skill` fixture.

| Record ID | Command | Exit | Seconds |
| --- | --- | ---: | ---: |
| `discover2-inventory` | `init --discover --format json` | 0 | 3.959 |
| `discover2-no-consent` | `init --discover --apply` with closed stdin | 1, expected | 2.459 |
| `discover2-apply` | `init --discover --apply --yes --format json` | 0 | 5.067 |
| `discover2-idempotent` | `init --discover --apply --yes --format json` | 0 | 4.963 |
| `discover2-target-conflict` | `init --discover --target copilot` | 2, expected | 4.683 |
| `discover2-install-pinned` | `install`, after deliberately adding `targets: [copilot]` | 0 | 7.095 |
| `discover2-audit-pinned` | `audit --ci` | 0 | 3.801 |
| `discover2-managed` | `init --discover --format json` | 0 | 2.047 |

Inventory returned `scope`, `root`, `manifest`, `findings`, `additions`,
`applied`; supported skill and unsupported loose rule were asserted.
Inventory and denied apply preserved the complete file inventory and mtimes.
Consented apply added **only** `apm.yml`, declaring
`path: ./.claude/skills/checkout-review`, without targets, source movement,
translation, lock, or deployment. Repeated apply was byte-stable and did not
duplicate the reference. Later pinned install deployed the Copilot skill
while retaining both source files; discovery then distinguished
`already-declared`, `managed`, and `unsupported`.

Exact consent-prompt ending and error:

```text
Add the listed dependencies to consumer apm.yml? [y/N]:
```

```text
Aborted!
```

Exact invalid-combination diagnostic:

```text
Error: --discover cannot scaffold a name/plugin/marketplace or select targets.
```

The supplementary scaffold checks were also real:
`discover2-plain-init`, CWD `ie2`, `init --yes` → 0 (1.940 s), created only
`apm.yml`; `discover2-empty-preview`, same CWD, `install --dry-run` → 0
(1.649 s), no lock or aggregate context; `discover2-plain-overwrite`, a
separate sacrificial authored copy `io2`, `init --yes` → 0 (1.991 s),
overwrote its old declaration. No canonical authored manifest was overwritten.

## Targetless, add writer, and bootstrap — PASS

`tl2` copied only `ProbeInputs/targetless/apm.yml` and
`.apm/instructions/probe.instructions.md`, omitting later `.gitignore` and
all harness markers. `ad2` used the exact authored `add-local` inputs;
`bt2`/`bd2` started with only `ProbeInputs/bootstrap/pkg/SKILL.md`.

| Record ID | CWD | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `targets2-targetless` | `tl2` | `install` | 2, expected | 6.978 |
| `targets2-targetless-flag-fix` | `tl2` | `install --target copilot` | 0 | 5.157 |
| `targets2-targetless-flag-audit` | `tl2` | `audit --ci` | 0 | 6.459 |
| `targets2-targetless-manifest-fix` | `tp2`, separate source copy with `targets: [claude]` added | `install` | 0 | 5.306 |
| `targets2-targetless-manifest-audit` | `tp2` | `audit --ci` | 0 | 4.719 |
| `targets2-local-add` | `ad2` | `install .\pkg --target copilot` | 0 | 4.399 |
| `targets2-local-add-restore` | `ad2` | `install` | 0 | 3.950 |
| `targets2-local-add-stable` | `ad2` | `install` | 0 | 3.337 |
| `targets2-local-add-audit` | `ad2` | `audit --ci` | 0 | 3.729 |
| `targets2-bootstrap` | `bt2` | `install .\pkg --target copilot` | 0 | 3.154 |
| `targets2-bootstrap-audit` | `bt2` | `audit --ci` | 0 | 2.839 |
| `targets2-bootstrap-preview` | `bd2` | `install .\pkg --target copilot --dry-run` | 0 | 2.614 |
| `targets2-global-preview` | `bd2` | `install "$Scratch\p\bd2\pkg" --global --target copilot --dry-run` | 0 | 3.097 |

The targetless command's stderr contained the exact chapter excerpt:

```text
Error: [x] No harness detected
```

It preserved files and mtimes and produced no `AGENTS.md`. Both target fixes
materialized the expected native rule and audited successfully.

The positional local add declared `.\pkg`, retained the leading comment,
blank line, and authored block-list target style. **Its writer normalized
CRLF to LF**; the chapter promises formatting preservation, not byte equality
across a manifest edit. Existing `[copilot, claude]` intent survived the
Copilot-only flag. The first add deployed only to Copilot; the next bare
restore also deployed to Claude, and another replay preserved lock/manifest
bytes.

Manifestless real add created `apm.yml` and persisted Copilot targets.
Project bootstrap dry-run also created a manifest but no lock/deployment.
The global dry-run changed no project or isolated-home/cache file.

The separate MCP writer caveat was reproduced with an inert scratch
manifest in `mc`:

```powershell
& $Apm install --mcp checkout-probe --transport stdio --env 'VALUE=${CORE_MCP_VALUE}' -- apm-book-mcp-not-a-real-executable --probe
& $Apm audit --ci
```

Records `mcp-direct-add` and `mcp-audit`: **0 / 0**, **10.366 / 5.850 s**.
`CORE_MCP_VALUE` was the non-secret `book-fixture-public-value`.
Only child processes used `MCP_REGISTRY_URL=https://127.0.0.1:9` with
two-second connect/read bounds, allowing the CLI's own unavailable-registry
fallback. The direct MCP writer dropped the leading comment and materialized
`.github/mcp.json` without executing the nonexistent command. This verifies
configuration/writer behavior, not availability of a live MCP registry/server.

## Explicit compilation — PASS

These checks reused original authored inputs, not the preserved generated
`AGENTS.md` from the compile-only probe:

| Record ID | CWD | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `ownership2-compile-only-install` | `co2` | `install` | 0 | 3.773 |
| `ownership2-explicit-compile` | `co2` | `compile` | 0 | 3.650 |
| `ownership2-handwritten-root` | `hp2` | `compile` | 0 | 2.904 |

Codex local-instruction install added only `.gitignore`, with no lock or
`AGENTS.md`. Explicit compilation then created aggregate context containing
the instruction body. The separate unmarked hand-authored root file in
`ProbeInputs/root-preserve` was preserved byte-for-byte.

## Scripts and expected missing runtime — PASS

`sc` copied only `ProbeInputs/scripts/apm.yml` and
`.apm/prompts/review.prompt.md`, excluding earlier compiled output. Neither
Copilot nor `apm-book-nonexistent-runtime` was discoverable on child PATH.

| Record ID | Command | Exit | Seconds |
| --- | --- | ---: | ---: |
| `scripts-list` | `list` | 0 | 4.132 |
| `scripts-preview` | `preview review` | 0 | 1.696 |
| `scripts-missing` | `run broken` | 1, expected | 1.978 |
| `scripts-echo` | `run echo` | 0 | 2.450 |
| `scripts-install` | `install` | 0 | 3.055 |
| `scripts-audit` | `audit --ci` | 0 | 2.689 |

Preview wrote `.apm/compiled/review.txt`, containing exactly the prompt body
without YAML frontmatter. The original command, compiled command, Windows
output path, and completion message agree with the chapter's condensed
display. `run broken` first printed `Compiling prompt...`, then:

```text
[x] Script execution error: Script execution failed with exit code 1
```

Exact stderr:

```text
'apm-book-nonexistent-runtime' is not recognized as an internal or external command,
operable program or batch file.
```

The successful ordinary-shell control printed `CORE_SCRIPT_OK`.
No live `run review` was performed.

## Native target outcomes — PASS assertions, known audit FAIL retained

Inputs were fresh copies of `ProbeInputs/portable`, `mixed`, and
`portable-metadata`; their canonical/exported fixtures were not altered.

| Record ID | CWD | Command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `native-excluded` | `np` | `install --target codex` | 1, expected | 6.403 |
| `native-excluded-preview` | `np` | `install --target codex --dry-run` | 0 | 5.406 |
| `native-mixed` | `nm` | `install --target codex` | 0 | 6.086 |
| `native-mixed-audit` | `nm` | `audit --ci` | 1, limitation | 4.791 |
| `native-metadata-install` | `nc` | `install` | 0 | 5.313 |
| `native-metadata-restore` | `nc` | `install` | 0 | 3.372 |
| `native-metadata-audit` | `nc` | `audit --ci` | 1, documented defect | 2.067 |

All-excluded real install changed no project file and activated no lock;
its exact concluding diagnostic was:

```text
[x] Installation failed in 0.7s. No install transaction changes were committed.
```

Its guidance named native Copilot-only support, the explicitly selected
Codex target, and the plain-skill recovery command
`apm install ./pkg/skills/retry --target codex`. Preview completed without
deploying. Mixed install deployed `.agents/skills/ordinary/SKILL.md`, not the
native plugin's loose skill or Copilot registration; success did not hide
the recovery warning.

For the Copilot-selected metadata control, APM registered the whole plugin
through `apm_modules/.github/plugin/marketplace.json`,
`apm-registration.json`, and `.github/copilot/settings.local.json`, without
a loose skill duplicate or a discoverable Copilot executable.

The documented native CI replay defect was independently reproduced, not
copied from explorer verdicts. Exact failing diagnostic:

```text
Native Agent Plugin canonical IR is missing, so deployment was blocked.
```

`native-metadata-audit` failed only its drift check; metadata-only `apm.yml`
removed the separate missing-manifest complaint but did **not** repair replay.
It changed no project bytes. The extra mixed audit also failed, reporting
missing `pkg/apm.yml` plus native canonical-IR replay failure; that input
retains its Copilot manifest despite the earlier one-off Codex flag.

These are **underlying audit FAIL results**. The chapter's explicitly scoped
negative/limitation demonstration matches them, hence its table's PASS
status; neither case is promoted to an audit-clean worked fixture or
network skip. F2 is a different, legacy-marker/APM-layout defect.

## Skips, historical evidence, and remaining limits

| Example / activity | Status | Exact unavailable dependency or permission |
| --- | --- | --- |
| `ch5-meridian-clone`: `git clone git@github.com:meridian/meridian-checkout.git`; subsequent `cd meridian-checkout && apm install` | **SKIPPED-needs-network** | The story URL is fictional/private, not an accessible fixture; no authorized SSH repository access. The chapter visibly names this skip. No command was attempted. |
| Live Copilot `apm run review` follow-up | **SKIPPED-needs-network** | No Copilot CLI/authenticated service session is provisioned in the isolated verifier, and no paid inference is authorized. Preview and inert execution are the actual current tests. |
| Loading native registration in Copilot | **SKIPPED-needs-network** | Loading requires Copilot CLI >=1.0.81 and an authorized runtime session; neither was provisioned/executed here. Offline registration alone was verified. |

The following original code blocks were compared with Git HEAD and retained
unchanged, **not executed or restamped at 0.31.0**:
`ch5-add-historical`, `ch5-added-manifest-historical`,
`ch5-lock-historical`, `ch5-restore-historical`,
`ch5-meridian-manifest-historical`, `ch5-list-historical`,
`ch5-run-historical`. Their evidence remains **APM 0.23.1**. In particular,
the complete old public/transitive graph, hashes, timings, and paid Copilot
recording were not substituted with the current single-skill result.

Additional limits:

- Clean audits cover the default CLI checks for these projects, including
  integrity and drift. Scratch projects have no organization remote, so
  logs explicitly report that organization-policy discovery/enforcement was
  skipped. This is **not** proof of private organization-policy enforcement.
  No `--no-policy` or `--no-drift` bypass was used.
- Saved user-default target configuration was not mutated. Actual tests
  cover CLI versus manifest, no-target detection, durable targets, and
  bootstrap. The saved-default precedence and broader target catalog remain
  pinned-help/source evidence, not tests of unrelated user configuration.
- No live proprietary source, push, publication, AI runtime, registry server,
  or MCP server was executed. No credentials were supplied or recorded.
- Full moving-transitive-graph replay, package-replacement atomicity,
  multi-package batch rollback, and every target/package restriction remain
  cited contracts outside these bounded executions. The historical graph
  is not a new PASS.
- The source `.apm`/legacy-marker control is not among the three canonical
  core fixtures. Its newly found failure must not invalidate their actual
  green byte/command results, or conversely be hidden by those successes.

### Retained verifier-only corrections

Initial logs were not overwritten:

1. The first discovery harness expected the words `consent`/`--yes` and a
   literal `--target` in diagnostics. Actual output is the consent prompt
   plus `Aborted!`, and “select targets.” All stated chapter exits/effects
   already matched. Exact diagnostic assertions passed on fresh `discover2`
   inputs.
2. The first add-format assertion incorrectly required raw prefix bytes.
   The author promises comment/blank-line/list **style**, not CRLF retention.
   Independent `targets2` execution passed the corrected formatting check.
3. The first unexpected ownership audit was fully logged with native exit 1,
   then the verifier's console hit a Windows `cp1252` encoding exception
   while printing its Unicode table. UTF-8 console handling was corrected;
   fresh `ownership2` and further controls completed and retained the genuine
   audit failures.

These are reproduction-harness fixes, not book or CLI fixes. No broken
example was made green by discarding failed output.

## Original handoff and reviewer gate — superseded for the finalized source

**Minimal book/fixture fixes applied: none.** F1 needs a scoped behavioral
claim, not a typo correction. F2 needs explicit limitation/provenance handling
and an explorer diagnosis, not a silent fixture redesign.

The reviewer can rely on the named PASS results and exact expected-negative
assertions, but **cannot gate this chapter revision ACCEPT yet**:

1. Correct F1's frozen-install guarantee and coupled exercise/closing wording.
2. Visibly disclose F2 for the referenced contraction control, or deliberately
   adopt the separately verified marker-free control with updated provenance.
3. Preserve the already documented native audit defect, explicit live/private
   skips, and historical 0.23.1 boundaries.
4. Recheck the changed source hash and any newly changed executable inputs;
   do not stamp unaffected/unexecuted historical material with the new version.

Author/reviewer retain responsibility for final chapter status labels.
