# Chapter 3 independent delta verification — book 1.2 / APM 0.31.0

**Verdict: PASS — chapter claim gate closed by the prose/comment-only delta,
2026-09-16 UTC.** F3.1 and F3.2 are resolved in the source identified below.
The withheld-MCP audit is still an actual CLI **FAIL**; the chapter now
discloses it accurately rather than promising an audit-clean result.
No APM command was rerun and no reviewer acceptance is claimed.

## Final prose/comment delta — source-specific PASS

| Revision | SHA256 |
| --- | --- |
| Original independently checked source; claim gate blocked | `75539973972750ea2179029cbf1e1c9c555aad46298714c117767ee847d268a9` |
| **Final source; chapter claim gate PASS** | **`cd9c17d28a240a3cf82f34239d6eec05faa11215825c8a400fca7231e7362741`** |

**Chapter:** `content/chapters/primitives-and-harnesses.html`.
**CLI evidence:** retained exact **APM 0.31.0** execution.
**New APM invocations: 0**, including no new `--version` call.
**New native runtime: 0.000 s.** No scratch project was created or resumed.

The final source was reconstructed **byte-for-byte** from the captured
original by applying only these two author corrections:

1. The MCP evidence comment now says **“Explorer path confirmation”** and
   points to this independent verification report.
2. A visible paragraph in `#ch3-mcp-boundary` gives the withheld depth-two
   control's `audit --ci` exit **1** and exact
   `nested-checkout-probe: in manifest but not in lockfile` diagnostic.
   It explicitly distinguishes correct withholding from an audit-clean
   project and rules out a network skip or suppressed audit.

There are no other source changes. All **four `<pre><code>` blocks** —
attributes, HTML entities, whitespace, line endings, decoded content, and
example IDs — remain identical to the original capture. The historical
0.23.1 illustrations were not restamped or reexecuted.

The shared Ch3/Ch4 read-only comparison also confirms all **38 captured
fixture files across eight fixture groups** equal their original hashes
and canonical ZIP bytes. This includes the complete Core fixtures and
relevant Operations/Producer inputs. The noncanonical nested-MCP and local
skill-selection inputs, registry helper, and competing-root-skill source
also match the exact recorded inputs. No executable fixture changed.

### Resolved chapter claims; underlying execution statuses retained

| Chapter ID / finding | Current chapter-claim status | CLI result retained |
| --- | --- | --- |
| `ch3-mcp-boundary`, F3.1 | **PASS — visible failure disclosure** | **FAIL**, `mcp-nested-audit`: `audit --ci`, exit **1**, original **2.200 s** |
| MCP evidence comment, F3.2 | **PASS — provenance corrected** | No new command; explorer observation is no longer called independent verification |
| `ch3-existing-skill-manifest`, `ch3-existing-skill-install` | **PASS**, unchanged literal fixture scope | `decl-onboard-locked-install`: `install`, **0**, **4.930 s**; `decl-onboard-locked-audit`: `audit --ci`, **0**, **1.870 s** |

The relevant raw failure output and original version guard were reread,
not reexecuted. The retained exact diagnostic remains:

```text
  config-consistency details:
    - nested-checkout-probe: in manifest but not in lockfile

[x] 1 of 8 check(s) failed
```

This PASS closes the **chapter disclosure/provenance findings**, not the
upstream consistency defect. The direct/root/re-declared MCP results,
native-plugin canonical-IR failure, marker-present legacy-command replay
failure, and historical/runtime boundaries remain as recorded below.
No actual failure was relabeled PASS or `SKIPPED-needs-network`.

### Check receipt and handoff

`python <Wave>/prose-delta/check.py <Repo>` completed with exit **0** in
**0.256 s**, at `2026-09-16T02:32:57.436453Z`; this is read-only comparison
time, not additional native runtime. `Wave` is `RunRoot/verify-core-wave`,
and `Repo` is the book checkout. The original **78-invocation /
241.350 s** wave and all prior reused execution counts remain unchanged.

Receipts are `Wave/prose-delta/check.json`, `ch03-source.html`,
`ch03-source.diff`, and `ch03-report-before.md`. The original
`Wave/verification-status.json` and original failed assertions still
describe the initial source; this dated delta supplies the final
source-specific chapter claim gate.

**Remaining mandatory Chapter 3 corrections: none within this gate.**
The author supplied the prose/comment edits. Verifier changes for this
closure are limited to the two requested verification reports and raw
receipts; no chapter, fixture, dependency, metadata, or Chapter 5 file was
edited. No broader research or reviewer disposition was added.

---

## Original independent record — retained; chapter-claim blockers superseded above

The following verdict, source hash, line anchors, and pending corrections
describe the originally tested revision. Its CLI failures and exact
execution evidence remain valid and are not erased by the prose closure.

**Verdict: FAIL pending two small author corrections, not a rewrite.**
The two current worked-example blocks pass. The new depth-two MCP control
installs as described but fails CI audit, without that failure being visible
beside the chapter's claim. One evidence comment also incorrectly calls
explorer evidence independent. Exact corrections are at the end.

No chapter or fixture was changed. Known native-plugin failures remain
**FAIL**, not network skips or PASS guarantees.

## Source and execution identity

| Item | Value |
| --- | --- |
| Chapter | `content/chapters/primitives-and-harnesses.html` |
| Source SHA256 | `75539973972750ea2179029cbf1e1c9c555aad46298714c117767ee847d268a9` |
| Current CLI | Exactly **0.31.0** |
| Execution date | 2026-09-16 UTC |
| Code blocks | 4: two historical illustrations, complete onboard manifest, install command |

Aliases: `RunRoot` = orchestrator's session `files/book-v1.2`;
`Wave`/`N` = `RunRoot/verify-core-wave`; `Prior`/`R` =
`RunRoot/verify-ch05`; `ProbeInputs` = `RunRoot/core-probes/projects`;
`Core` and `Operations` = `backend/examples/updates/1.2/core` and
`.../operations`. `Scratch` is the new owned short root recorded in
`Wave/runtime-layout.json`. Record IDs below mean `logs/<id>.json` and
the matching `.txt`, `.stdout.bin`, and `.stderr.bin` files.

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

Executable SHA256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
All command tables give exact arguments after `& $Apm`. Actual invocations
used the absolute executable, short normal CWDs, isolated HOME/cache/config/
temp/credentials, no inherited host tokens or credential helpers, and no
book-root dependencies or user/global configuration.

This is part of the shared **78-invocation / 241.350 s** delta wave
(9 version guards, 7 help commands, 62 example/control commands).
**53 Ch5 independent command records plus 13 original guards** were
cross-checked read-only; their original runtime is not new execution.
See `Wave/reuse-evidence.json` and the
[wave accounting](ch01-verification.md#execution-and-bounded-reuse).

## Every code block

| Example ID / path | Status | CLI / exits / runtime | Evidence and input scope |
| --- | --- | --- | --- |
| `Chapter#ch3-meridian-map` | **PASS — historical preservation only** | Original 0.23.1; no new CLI exit/runtime | Original code content preserved, with only Git checkout EOL representation differing |
| `Chapter#ch3-historical-manifest-shape` | **PASS — historical preservation only** | Original 0.23.1; no new CLI exit/runtime | Explicitly incomplete conceptual sketch; eight-target comment remains historical, not newly validated schema |
| `Chapter#ch3-existing-skill-manifest` | **PASS** | 0.31.0; install/audit 0/0 | Exact canonical manifest; retained Ch5 source-only evidence plus the new literal complete-fixture copy |
| `Chapter#ch3-existing-skill-install` | **PASS** | 0.31.0; install **0, 4.930 s**; audit **0, 1.870 s** | N `decl-onboard-locked-install`, `decl-onboard-locked-audit` |

### Why the literal install was new, not blindly reused

The caption tells the reader to copy **the fixture**, including hidden
`.claude` source. That committed fixture also contains a lock. The prior
Ch5 first install started with source files **without** a lock. Those
starting states are not byte/input-equivalent.

The new `Scratch/p/os` before-state contained exactly:

```text
apm.yml
apm.lock.yaml
.claude/skills/checkout-review/SKILL.md
```

| File | SHA256 |
| --- | --- |
| `apm.yml` | `a865eef2ce859f724178723a72152678a19012a6a8ad1b9bca949c76927d7210` |
| Authored `SKILL.md` | `838837e021cefe28b5624e508d2ec2a7871c7b59c7166f42e57e5c7d1502d8f6` |
| Complete lock | `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28` |

The code block plus its omitted terminal newline equals the canonical
manifest bytes. New `install` materialized
`.agents/skills/checkout-review/SKILL.md`, preserved the source and lock,
and `audit --ci` passed. The skill was not invoked. Its Claude-shaped
source directory did not authorize a Claude deployment.

The independently retained source-only Ch5 sequence is separately valid:

| R record ID | Exact command | Exit | Original seconds |
| --- | --- | ---: | ---: |
| `local-onboard-skill-install` | `install` | 0 | 2.695 |
| `local-onboard-skill-restore` | `install` | 0 | 2.856 |
| `local-onboard-skill-frozen` | `install --frozen` | 0 | 3.936 |
| `local-onboard-skill-audit` | `audit --ci` | 0 | 4.307 |

All eight Core files, full prior output bytes, exact argv, snapshots, and
preceding guards were compared before reuse. No explorer PASS stamp was
substituted for those independent records.

## Operative-claim disposition

| Chapter ID / claim | Status at 0.31.0 | Basis |
| --- | --- | --- |
| `ch3-layout-authority` | **PASS for classification/selection**; marker-present audit **FAIL** retained separately | Exact reused eligible-manifest control; new metadata-only, explicit/empty/omitted/missing skill controls |
| `ch3-plugin-formats` | **PASS for whole-unit registration**; native audit **FAIL**, already documented | Exact `portable-metadata` independent input/records; no Copilot runtime executed |
| `ch3-target-catalog` | **PASS**, catalog/output scope | New `init --yes --target all`; retained Kiro agent output; frozen matrix for unexecuted target profiles |
| `ch3-hooks-lifecycle` | **PASS**, configuration and inert local execution | New hook install/audit plus untrusted/trusted/subtree-changed lifecycle controls |
| `ch3-mcp-boundary` | **FAIL — missing visible audit limitation**, F3.1 | Root/direct/redeclared paths pass; correctly withheld depth-two input still fails CI audit |
| `ch3-mcp-boundary` evidence comment | **FAIL — provenance wording**, F3.2 | `Operations/mcp` explorer observation is not independent code verification |
| `ch3-deploy-scan` | **PASS**, bounded positive/negative controls | Source-only README/unselected skill not deployed; selecting inert Critical-class marker blocks install |
| `ch3-historical-projection` | **PASS — archival boundary only** | Explicit 0.23.1 full-package table; no 0.31.0 full-package/Copilot/Claude rerun claimed |

Definitions of model/human/harness triggers and the standards are conceptual
contracts, not claims that an agent or paid runtime was exercised here.

## Declaration and target controls

All N commands below are new, using the identified inputs in short normal
CWDs. The legacy controls retain the source plugin and skill bytes from
`ProbeInputs`; the omission control removes only its `skills` key from
the metadata-only fixture.

| Origin / record ID | Exact command | Exit | Native seconds |
| --- | --- | ---: | ---: |
| R `ownership2-four-target-install` | `install` | 0 | 8.905 |
| R `ownership2-four-target-audit` | `audit --ci` | **1** | 7.583 |
| R `control-no-marker-install` | `install` | 0 | 5.954 |
| R `control-no-marker-audit` | `audit --ci` | 0 | 5.485 |
| N `decl-metadata-legacy-install` | `install` | 0 | 2.348 |
| N `decl-metadata-legacy-audit` | `audit --ci` | 0 | 2.161 |
| N `decl-undeclared-skill` | `install --skill not-declared` | **1, expected** | 2.577 |
| N `decl-legacy-empty` | `install` | 0 | 2.633 |
| N `decl-legacy-missing` | `install` | **1, expected** | 2.422 |
| N `final-omitted-skills-install` | `install` | 0 | 5.185 |
| N `final-omitted-skills-audit` | `audit --ci` | 0 | 5.262 |
| N `decl-init-all` | `init --yes --target all` | 0 | 2.294 |
| R `ownership2-compile-only-install` | `install` | 0 | 3.773 |
| R `ownership2-explicit-compile` | `compile` | 0 | 3.650 |
| R `ownership2-handwritten-root` | `compile` | 0 | 2.904 |

Checks establish:

- Eligible APM input is byte-identical to `ProbeInputs/apm-over-plugin`.
  Its first-install lock says `apm_package`; `.apm` primitives deploy,
  including `.kiro/agents/reviewer.md`, without the plugin-only command.
  The marker-free control omits **only** `pkg/plugin.json`, not source
  material or failing audit checks.
- Metadata-only `pkg/apm.yml` does not force the APM route. Explicit
  `kept` and off-convention `custom` deploy; `unlisted` does not.
  Empty declaration deploys no skills. Omission discovers conventional
  `kept`/`unlisted`, not off-convention `custom`.
- Unknown skill selection exits 1 and names `Available: custom, kept`.
  No project bytes change; two installed-cache mtimes do change.
  Missing declared `./skills/missing` exits 1 with no activated lock.
  These are expected refusals, not network failures.
- The real `all` expansion is the nine chapter-named default stable targets.
  This is not a claim that bare install selects all nine.
- Codex local install does not create root context; subsequent `compile`
  does. The separate hand-authored root file control is preserved.

The exact marker-present audit diagnostic remains:

```text
  drift details:
    - unintegrated: .claude/commands/legacy-command.md
    - unintegrated: .cursor/commands/legacy-command.md
    - unintegrated: .github/prompts/legacy-command.prompt.md

[x] 1 of 10 check(s) failed
```

Diagnosis/owner: install classification and legacy-command audit replay
disagree — `apm-cli-explorer` / upstream. See the retained F2 record in
[Ch5 verification](ch05-verification.md). This is not an audit-clean
precedence fixture or a regression repaired by this wave.

## Native registration — documented failure retained

| R record ID | Exact command | Exit | Original seconds |
| --- | --- | ---: | ---: |
| `native-metadata-install` | `install` | 0 | 5.313 |
| `native-metadata-restore` | `install` | 0 | 3.372 |
| `native-metadata-audit` | `audit --ci` | **1** | 2.067 |
| `native-excluded` | `install --target codex` | **1, expected** | 6.403 |
| `native-mixed` | `install --target codex` | 0 | 6.086 |
| `native-excluded-preview` | `install --target codex --dry-run` | 0 | 5.406 |

Byte-equivalent input is `ProbeInputs/portable-metadata`, not an invented
Git-sourced plugin. The plugin stays under `apm_modules/_local/pkg`;
APM's marketplace/registration ledger and
`.github/copilot/settings.local.json` enable `checkout-plugin@apm`.
There is no loose `.agents/skills/retry/SKILL.md` duplicate.

The exact audit failure includes:

```text
Native Agent Plugin canonical IR is missing, so deployment was blocked.
Use 'apm pack --claude-plugin' or ask the publisher for a legacy-compatible
package.
[x] 1 of 10 check(s) failed
```

Full native output, including terminal wrapping, is preserved in the
named raw log. Diagnosis/owner: local native-plugin canonical-IR replay —
`apm-cli-explorer` / upstream. Chapter lines 338–342 already disclose it.
Copilot CLI >=1.0.81 loading is the frozen source contract, **not a live
runtime result or an audit guarantee**.

## MCP — correct install outcomes, real audit failure

Input `Operations/mcp/apm.yml` has only self-defined
`operations-fixture`, with the deliberately nonexistent command
`operations-fixture-not-a-real-server`. It configures `.github/mcp.json`
(`mcpServers`), `.vscode/mcp.json` (`servers`), and `.mcp.json`
(`mcpServers`). Actual names, executable, arguments, lock ownership, and
empty APM dependency list were inspected.

Identity lookup is explicitly bounded with process-only
`MCP_REGISTRY_URL=https://127.0.0.1:9` and two-second connect/read limits.
The CLI's own name-comparison fallback runs after connection refusal.
TLS verification is not disabled, no real MCP server starts, and this
does not establish public MCP-registry availability.

| N record ID | Input / CWD under `Scratch/p` | Exact command | Exit | Seconds |
| --- | --- | --- | ---: | ---: |
| `mcp-root-config-install` | `Operations/mcp` source manifest, `mc` | `install` | 0 | 15.883 |
| `mcp-root-config-audit` | Same project | `audit --ci` | 0 | 2.355 |
| `mcp-transitive-install` | `ProbeInputs/transitive`, actually **direct** dependency, `md` | `install` | 0 | 7.050 |
| `mcp-transitive-audit` | Same direct-dependency project | `audit --ci` | 0 | 3.798 |
| `mcp-nested-install` | `ProbeInputs/nested`, actual depth two, `mn` | `install` | 0 | 3.043 |
| `mcp-nested-audit` | Same withheld depth-two project | `audit --ci` | **1** | 2.200 |
| `mcp-nested-redeclared-install` | `ProbeInputs/nested-redeclared`, `mr` | `install` | 0 | 6.213 |
| `mcp-nested-redeclared-audit` | Same re-declared project | `audit --ci` | 0 | 1.912 |

Direct self-defined MCP is configured with its direct-trust diagnostic.
Depth-two MCP is withheld; ordinary skills still deploy. Consumer
re-declaration configures the named server; dependency dev-only MCP is
not configured. Those install assertions pass.

### F3.1 — withheld depth-two MCP is not audit-clean

**Status: FAIL**, APM **0.31.0**, `audit --ci` exit **1**, **2.200 s**.
Exact failure detail from `N/logs/mcp-nested-audit.*`:

```text
  config-consistency details:
    - nested-checkout-probe: in manifest but not in lockfile

[x] 1 of 8 check(s) failed
```

Stderr:

```text
[>] Replaying install (cache-only)...
[+] Replayed 2 package(s)
[>] Diffing scratch vs working tree...
[+] No drift detected
```

Diagnosis: the audit consistency check still expects the correctly
withheld nested server. Owner: `apm-cli-explorer` / upstream for the CLI;
`chapter-author` for visible scope. This is entirely local and reproducible
from the supplied fixture, **not SKIPPED-needs-network**.

## Hooks, lifecycle, and scanning

| N record ID | Exact command | Exit | Seconds |
| --- | --- | ---: | ---: |
| `events-hooks-install` | `install` | 0 | 3.916 |
| `events-hooks-audit` | `audit --ci` | 0 | 1.904 |
| `events-lifecycle-untrusted` | `install` | 0 | 2.583 |
| `events-lifecycle-trust` | `lifecycle trust` | 0 | 1.782 |
| `events-lifecycle-trusted` | `install` | 0 | 3.332 |
| `events-lifecycle-edit-revokes` | `install` | 0 | 2.379 |
| `events-lifecycle-audit` | `audit --ci` | 0 | 2.506 |
| `scan-source-only-install` | `install` | 0 | 3.946 |
| `scan-source-only-audit` | `audit --ci` | 0 | 1.861 |
| `scan-selected-skill-install` | `install` | 0 | 2.507 |
| `scan-selected-skill-audit` | `audit --ci` | 0 | 2.168 |
| `scan-flagged-selected-blocked` | `install` | **1, expected** | 2.260 |

Hooks use the unchanged Operations hook source; Copilot gets `sessionStart`
and Claude `SessionStart`. No harness or Node callback ran.
Lifecycle uses the inspected inert `python record.py`: no events before
trust; exactly `pre-install`, `post-install` after trust; changing only
one lifecycle timeout from 5 to 6 suppresses subsequent execution.
Only that batch added Python to its restricted PATH.

Scanner inputs contain harmless character-class text, not a prompt
injection payload. README/unselected content stays outside the authorized
deploy set. Selecting the marked skill produces:

```text
[x]   Blocked: ./package contains critical hidden character(s)
  |-- skills/flagged/SKILL.md
```

No flagged skill is activated. This is an asserted expected failure,
not proof of benign intent, package signatures, or runtime confinement.

## Mandatory corrections and completion boundary

1. **F3.1 — `#ch3-mcp-boundary`, lines 495–501:** add a visible sentence
   that the tested withheld depth-two fixture is **not audit-clean in
   0.31.0**, with the exact `config-consistency` error above; distinguish
   the re-declared control's successful audit. Keep the correct depth
   explanation. Do not hide this through `--no-drift`, `--no-policy`,
   lock edits, or a network skip.
2. **F3.2 — line 483 evidence comment:** replace “Independent path
   confirmation” for the Operations explorer's `mcp-install` with
   “explorer observation,” or point to this wave's
   `mcp-root-config-install` / `mcp-root-config-audit` independent records.
   It is a provenance correction, not a request for another MCP run.

Existing native-plugin disclosure is sufficient; the marker-present
precedence audit failure is retained above and in Ch5, never represented
as a clean guarantee. Unexecuted target profiles and runtime loading
remain explicitly document-only support boundaries. Source receipts use
frozen commit `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`.

No current command was skipped for missing network. Private services,
real MCP processes, paid/harness execution, and organization enforcement
are not asserted by this gate. Built-in audit success in an org-remote-free
scratch project is not a policy-enforcement result.

Verifier-only initial diagnostic-wording/mtime assertions were corrected
by read-only comparison in `Wave/assertion-delta/declarations.json`
(0 new native commands); original assertions remain. Actual CLI failures
were not relabeled.

**Minimal fixes applied to book content: none.** All four chapter sources,
selected fixtures, and root APM dependency hashes still match the initial
capture. A later unrelated TOC change is recorded in the
[shared handoff note](ch01-verification.md#artifacts-and-handoff), not
approved or reverted by this verifier. Raw output, generated locks,
mutations, source receipts, input ZIPs, and command snapshots are under
`Wave`; original Ch5 evidence remains untouched. A prose/comment-only
correction can receive bounded delta review against these same records;
do not rerun the full probe suites.
