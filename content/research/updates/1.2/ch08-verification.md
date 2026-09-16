# Chapter 8 — independent verification, book 1.2 / APM 0.31.0

**Verdict: PASS after one minimal evidence correction; ready for chapter review.**
This verifies the chapter's stated outcomes, including deliberately failing
controls. It does **not** certify the defective APM trust/integrity guarantees
listed below, or claim an upstream bug was fixed.

## Frozen inputs and execution boundary

| Item | Verified value |
| --- | --- |
| Chapter | `content/chapters/security-by-default.html` |
| Final HTML SHA-256 | `21efe99d2991b10b85e8ce00c0d569bccbe66ff71422756172eeb902d04af450` |
| Incoming HTML SHA-256 | `c2d8c7d6b39473ea7499646d2a1ba22469abab056644be1dbda83589557c11ba` |
| Book / CLI target | **1.2 / exactly 0.31.0**, not latest |
| Executable | Supplied absolute `RunRoot/apm-native/unpacked/apm-windows-x86_64/apm.exe` |
| Executable SHA-256 | `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2` |
| Upstream source commit | `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` |
| Environment | Windows x64; Python 3.12.10; PyYAML 6.0.3 |
| New execution window, both chapters | 2026-09-16, 02:01–02:23 UTC |
| Final evidence assembly | 2026-09-16, 02:26 UTC |

`RunRoot` is the supplied session's `files/book-v1.2` artifact directory.
Absolute executable and working-directory paths are retained in local raw
records, not published with local usernames here. Every new batch checked the
executable hash and this exact successful banner before its examples:

```text
Agent Package Manager (APM) CLI version 0.31.0
```

Each APM invocation used the absolute executable, never PATH-selected `apm`.
Below, commands beginning with `install`, `audit`, etc. mean **`& $Apm` followed
by exactly those arguments**. `$Apm` denotes that supplied executable.

Fresh short owned scratch roots were created outside the repository. Child
HOME, user profile, app-data/config/cache, temporary directories, Git
configuration, and credential-helper access were isolated. Inherited credential
variables and the desktop `gh` launcher were excluded. MCP conflict lookup was
bounded to the unavailable loopback endpoint `https://127.0.0.1:9`; no MCP server
or harness was started. Only benign Unicode markers and ordinary text edits
were used. No machine policy, global bin installation, real service, push,
publish, dependency update in the book root, or agent session was performed.

### Evidence locations and provenance labels

Let **V** = `RunRoot/verify-ch08-ch09` and **F** =
`backend/examples/updates/1.2/operations`.

* **NEW**: independent execution in this verification. `batch/id` resolves via
  `V/command-index.json` to
  `V/batches/<batch>/logs/<sequence>-<id>.json` and `.txt`.
* **REUSED**: a completed **independent verifier** record that actually arrived.
  Selected Ch6/Ch7 and core records, version guards, and snapshots were copied to
  `V/reused/`; their originals and hashes are in `V/reuse-index.json`.
  This is not assumed future verification or a relabelled explorer transcript.
* `V/example-statuses.json` maps every current figure ID to exact records,
  arguments, exits, origin, and runtime. `V/embedded-blocks.json` retains the
  incoming HTML mappings; `V/batches/final-source/embedded-final-blocks.json`
  records the final code.
* Raw records retain stdout/stderr, CWD, arguments, exits, durations, and
  before/after inventories. Snapshots preserve actual manifests, lockfiles,
  and native outputs. `V/initial-failure-dispositions.json` retains initial
  unsuccessful assertions and their resolutions.

The combined Ch8/Ch9 run made **146 new APM invocations: 15 version guards,
10 help commands, and 121 targeted example/control commands**. Their summed
recorded duration was **775.921 s**; parallel execution means this is not elapsed
wall time or a benchmark. **45** selected independent commands were reused
with **392.750 s** of original command runtime and eight original batch guards.
The full 306-probe explorer run, `--suite all`, and historical 0.23.1 examples
were **not** rerun.

The supplied `verify.py` entrypoint and `security`, `hooks`, `policy`, and
`trust-limit` suite bodies were executed unchanged, with external timing/log
instrumentation and an explicit fresh `--work` path. The shared `repro` suite
was reused from the completed Ch6/Ch7 run instead of duplicated. A separate
read-only pass made 316 evidence/state assertions over the selected reused
records, including fixture hashes, output digests, snapshots, and version guards.

## Every current code example

All rows use **APM 0.31.0**. Times sum the cited command records; shared records
appearing in several rows are not additional executions.

| Example ID / input path | Status / origin | Exact command coverage and native exits | Seconds |
| --- | --- | --- | ---: |
| `ch08-scan-file-controls` / generated benign `critical.md`, `warning.md` | **PASS / NEW** | `audit --file critical.md` → **1**; `audit --file warning.md` → **2**; `audit --file critical.md --strip --dry-run` → **0**; `audit --file critical.md --strip` → **0**; clean rescan `audit --file critical.md` → **0** | 21.034 |
| `ch08-installed-warning` / scratch variant of `F/repro` | **PASS / NEW** | `install` → **0**; `audit -f json` → **2**; `audit --ci --no-fail-fast -f json` → **0** | 19.964 |
| `ch08-deployed-drift` / `F/repro` | **PASS / REUSED** | After a benign edit, `audit -f json` → **0** and `audit --ci --no-fail-fast -f json` → **1**, separately for Copilot, Claude, and Cursor | 33.375 |
| `ch08-trust-consumer` / `F/trust/apm.yml` | **PASS as a documented failure control / NEW** | Exact YAML matches the fixture; `install` → **0**, `approve --list` → **0**, parked-state `audit --ci --no-fail-fast -f json` → **1** | 23.464 |
| `ch08-trust-package` / `F/trust/package/apm.yml` | **PASS as a documented failure control / NEW** | Exact dependency YAML was loaded by the same actual installation and audit. Intentionally nonexistent MCP command was configured, not executed | 23.464 |
| `ch08-trust-initial` / complete `F/trust` | **PASS as documented; underlying gates FAIL / NEW** | `install` → **0**; `approve --list` → **0**; `policy explain ./package` → **0**; `audit --ci --no-fail-fast -f json` → **1** | 36.127 |
| `ch08-trust-approved` / reviewed inert fixture | **PASS / NEW** | `approve ./package` → **0**; `install` → **0**; `audit --ci --no-fail-fast -f json` → **0** | 21.031 |
| `ch08-canonical-grant` / generated consumer `apm.yml` excerpt | **PASS / NEW** | Compared with actual output of `approve ./package` → **0** and `approve friendly-display-name` → **0**; both persist `./package#1.0.0`, with boolean hooks/MCP grants | 12.158 |
| `ch08-trust-reproduction` / `F/verify.py --suite trust-limit` | **PASS / NEW** | Supplied entrypoint completed successfully with absolute `--apm` and safety-only `--work`; native sequence including version guard: **0, 0, 0, 1, 0, 0, 0**. The expected audit failure is not hidden | 46.674 |
| `ch08-package-audit-scope` / corrected inline control, `F/repro` variant | **PASS after minimal correction / NEW** | `audit ./package -f json` → **0**, **three files actually scanned**; repeated after the chapter edit with the same result | 6.043 |

Record mappings:

* Standalone controls: `security/{critical-scan,warning-scan,strip-preview,strip,clean-after-strip}`.
* Warning installation: `security/{warning-install,warning-installed-bare,warning-installed-ci}`.
* Drift: reused `verify-ch06-ch07/logs/repro-{copilot,claude,cursor}-{bare,ci}-drift.json`.
* Initial/approved trust: `trust-limit/{parked-hook-install,parked-decision,parked-hook-audit-replay,canonical-approval,approved-install,approved-audit}`;
  explanation: `trust-extra/trust-explain-canonical`.
* Canonical alias: `trust-extra/trust-display-name-not-authority` actually exits
  **0**, despite the older probe's misleading name.
* Corrected scope: `security-final/scan-package-selector-canonical` and
  `final-source/final-source-canonical-scope`.

The reproduction entrypoint's complete wall time was **47.459 s**. It is a
reproduction of a known failure, not a green MCP-withholding certification.

## Minimal correction, original error, and final rerun

The incoming prose treated `scan-package-selector-narrower` as evidence that a
package-selected audit had scanned the dependency but excluded an unrelated file.
The original explorer log and the independent rerun instead returned **0**,
with empty stdout and this exact stderr:

```text
[!] Package '_local/package' not found in apm.lock.yaml or has no deployed files
```

**Original evidence status: FAIL.** Diagnosis: wrong local selector; a
zero-files early return is not evidence of a successful scoped scan.
Suggested owner if this returns: **chapter-author / apm-cli-explorer**.

The minimal fix was to teach the working canonical selector, `./package`,
explicitly state that it scanned three files, and retain the earlier no-files
limitation. The new paragraph has ID `ch08-package-audit-scope` and a current
probe mapping. Two metadata-only clarifications define the independent evidence
alias and include `core-probes/projects/transitive` in the depth table's fixture
list. No example fixture or lockfile was edited.

The corrected command produced:

```json
"summary": {
  "files_scanned": 3,
  "files_affected": 0,
  "critical": 0,
  "warning": 0,
  "info": 0
}
```

The unrelated governed file still contained the benign Critical-class marker.
Whole-project audits of that state failed **1/1**; the corrected package audit
returned **0**. It was rerun against the final edited source, not merely
substituted into the report.

## Supplementary changed claims and probe mappings

### Scan timing, selection, stripping, and ownership

All commands in this table are **NEW**, with expected behavior asserted.

| Chapter surface / record ID | Exact command(s) | Exit(s) / observed state |
| --- | --- | --- |
| `ch08-scan-severity` / `security-extra/scan-info` | `audit --file info.md --verbose` | **0**; legitimate emoji is non-blocking |
| `ch08-authorized-scan` / `scan-source-only-install`, `scan-source-only-ci` in `security-extra` | `install`; `audit --ci --no-fail-fast -f json` | **0/0**; README marker exists in materialized source; clean primitive deploys |
| Same table / `scan-admissible-selected-skill`, `scan-admissible-selected-ci` | `install`; same CI audit | **0/0**; valid metadata manifest and `skills: [clean]`; flagged skill is absent from deployment |
| Same table / `scan-mixed-package-install` | `install` | **1**; clean package deployed, Critical-bearing primitive withheld |
| Break-glass boundary / `scan-mixed-force-benign-only` | `install --force` | **0**; only this harmless marker control was forced |
| Project strip / `scan-warning-short-strip`, `scan-warning-short-frozen-restore` | `audit --strip`; `install --frozen` | **0/0**; source unchanged, marker returns in deployed content |
| `ch08-audit-boundaries` / `scan-unrecorded-whole-bare`, `scan-unrecorded-whole-ci` | `audit -f json`; `audit --ci --no-fail-fast -f json` | **1/1**; Critical marker in an unrecorded governed file is detected |
| Hook ownership / `hooks/user-hook-is-not-drift` | `audit --ci --no-fail-fast -f json` | **0**; unrelated user-owned Claude hook is not APM drift |
| Hook ownership / `hooks/user-hook-survives-uninstall` | `uninstall ./package` | **0**; user hook preserved |
| Hook ownership / `hooks/owned-hook-sidecar-is-drift` | `audit --ci --no-fail-fast -f json` | **1**; edited APM-owned sidecar detected |
| Hook ownership / `security-final/hooks-owned-sidecar-missing-ci` | same CI audit | **1**; missing `.claude/apm-hooks.json` detected |

The hook fixture was independently materialized twice with `install --frozen`
and audited clean before mutations; both native event/configuration families
and the generated genuine lock were retained. No callback ran.

For ordinary drift/owner/CRLF claims, **REUSED** `repro` records assert:

* Clean `install --frozen` / CI audit: **0/0**, **12.234 / 4.345 s**.
* Invalid canonical owners: bare / CI audit **1/1**, **3.914 / 3.747 s**.
* CRLF-only deployed-text changes: CI audit **0**, **4.668 s**; unchanged lock.
  Independent SHA-256 calculations over LF-normalized text match all six
  deployment rows. This does not establish raw-tree byte normalization.

### Canonical consent and known local trust failures

`trust-extra` adds these actual controls; all native exits below are expected:

| IDs | Exact command sequence | Exit sequence |
| --- | --- | --- |
| `trust-display-name-not-authority`, `trust-alias-approved-install`, `trust-approved-list` | `approve friendly-display-name`; `install`; `approve --list` | **0/0/0** |
| `trust-version-change-install`, `trust-version-change-list` | `install`; `approve --list`, after source version becomes 1.1.0 | **0/0**; original grant bytes unchanged |
| `trust-deny-canonical`, `trust-denied-list`, `trust-denied-install`, `trust-denied-audit-ci` | `deny ./package`; `approve --list`; `install`; `audit --ci --no-fail-fast -f json` | **0/0/0/1** |
| `trust-mcp-only-parked-install`, `trust-mcp-only-list`, `trust-mcp-only-audit-ci` | `install`; `approve --list`; same CI audit | **0/0/0**, despite actual MCP configuration under default-deny |
| `trust-two-identities-install`, `trust-two-identities-approve-one`, `trust-two-identities-list`, `trust-two-identities-install-one` | `install`; `approve ./one`; `approve --list`; `install` | **0/0/0/0**; one's hook deployed, two's withheld despite identical display metadata |

Verbatim relevant output from `trust-explain-canonical`:

```text
./package#1.0.0: 1 hook(s), 1 MCP server(s)
  verdict: blocked
  hooks   [x] blocked  (layer: default-deny)
  mcp     [x] blocked  (layer: default-deny)
```

Yet `.github/mcp.json` contained `operations-trust-fixture`, and the lock's
dependency `exec_status` was `gated_pending_approval`. **The local executable
MCP gate guarantee is FAIL**, not a network skip.

Parked-hook CI audit exited **1**, with these exact finding strings:

```text
unintegrated: .claude/apm-hooks.json
unintegrated: .claude/settings.json
unintegrated: .github/hooks/package-notice.json
```

**Parked-hook replay is FAIL**, not a network skip. Approval of this inspected
inert fixture makes its approved-state audit pass; that is **not a fix** for
either pre-approval defect. Suggested upstream diagnosis owner:
**apm-cli-explorer / APM maintainers**.

### Depth, native paths, lifecycle, and public replay — validated reuse

| Current chapter surface | Completed independent records reused | Actual result |
| --- | --- | --- |
| `ch08-mcp-depth-controls` | Core `mcp-transitive-install`, `mcp-nested-install`, `mcp-nested-redeclared-install` | **0/0/0**, **7.050/3.043/6.213 s**; direct MCP configured, depth-two candidate withheld while skills deploy, root re-declaration configured the named server |
| `ch08-mcp-paths` | Core `mcp-root-config-install`, `mcp-root-config-audit` | `install` / `audit --ci`: **0/0**, **15.883/2.355 s**; Copilot `.github/mcp.json`, VS Code `.vscode/mcp.json`, Claude `.mcp.json`, with the documented native containers |
| `ch08-mcp-audit-limit` | Ch6/Ch7 `mcp-mcp-native-missing-not-audit-gated`, `mcp-more-edited-native-ci` | CI audit **0/0**, **5.876/22.025 s**; missing/edited native bytes not repaired or rejected |
| Same limit | `mcp-mcp-frozen-repairs-native-file`, `mcp-more-edited-native-frozen`, `mcp-mcp-frozen-catches-manifest-lock-mismatch` | `install --frozen`: **0/0/1**, **16.508/12.272/3.171 s**; repairs absence, preserves native edit, rejects manifest-to-lock argument mismatch |
| `ch08-lifecycle-boundary` | `lifecycle-lifecycle-trust`, `lifecycle-install-preview-no-events`, `lifecycle-update-preview-has-pre-events`, `lifecycle-update-preview-kill-switch`, `lifecycle-uninstall-preview-pre-event` | `lifecycle trust`; `install --dry-run`; `update --dry-run`; same update with child `APM_NO_SCRIPTS=1`; `uninstall ./package --dry-run`: all **0**. Only the documented pre-event cases ran the benign recorder |
| Same trust scope | `lifecycle-more-trust`, `lifecycle-more-unrelated-edit-install`, `lifecycle-more-subtree-edit-install` | `lifecycle trust`; two `install` controls: **0/0/0**; unrelated metadata retains trust, lifecycle-subtree edit revokes it |
| `ch08-audit-pitfall` | `public-more-pinned-frozen`, `public-more-cold-public-ci`, `public-more-cold-offline-ci` | `install --frozen` → **0**, **33.522 s**; cold CI audit → **0**, **25.391 s**; intentionally unavailable hydration → **1**, **28.990 s**, not a green skip |

Public replay uses the real
`microsoft/apm-sample-package/.apm/skills/style-checker` at immutable commit
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`. Empty-cache and unchanged-checkout
assertions were checked, not inferred from exit codes.

The prior independent nested fixture also had a separate `audit --ci` failure
(**1**, **2.200 s**), retained verbatim:

```text
config-consistency details:
    - nested-checkout-probe: in manifest but not in lockfile
```

This is an additional **FAIL / replay limitation**, not a network skip.
The chapter's depth table promises configuration/withholding results, not a
clean nested replay. Its direct and re-declared audit controls exited **0**.

The broader invocation alternative was **NEW**:
`scoped-controls/depth-two-trust-transitive-flag`,
`install --trust-transitive-mcp` → **0**, **7.849 s**. It configured only the
named candidate, excluded dependency dev-MCP, and did not add a root declaration.

### Bin consent, destination binding, and executable provenance

**NEW**, project scope only:

| Record in `scoped-controls` | Exact command | Exit / seconds | Asserted boundary |
| --- | --- | --- | --- |
| `bin-project-default` | `install` | **0 / 3.200** | Bin skipped as not trusted |
| `bin-project-trust-explicit` | `install --trust-bin` | **0 / 2.332** | Diagnostic requires global scope; no global install performed |
| `bin-project-no-trust-explicit` | `install --no-trust-bin` | **0 / 2.176** | Bin withheld |
| `bin-project-frozen` | `install --frozen` | **0 / 2.199** | Bin withheld |
| `http-never-sends-credential` | `install`, public non-credential marker supplied to the isolated child | **1 / 2.174** | HTTP authentication refused before any request |
| `different-binding-anonymous-only` | `install`, mismatched destination binding | **0 / 1.900** | Actual anonymous fixture install; no Authorization header |
| `credential-anonymous-installed-audit` | `audit --ci --no-fail-fast -f json` | **0 / 1.626** | Resulting anonymous install audited clean |

The registry helper used an allocated ephemeral loopback port, **not 18431**.
It had no publication endpoint and only served inert fixtures. No real token
was read, sent, recorded, or embedded.

The exact executable was independently inspected with
`Get-AuthenticodeSignature -FilePath $Apm` in a read-only PowerShell command
(exit **0**, **2.151 s**):

```json
{
  "Status": "NotSigned",
  "SignerPresent": false
}
```

`V/batches/scoped-controls/authenticode.json` retains the exact command/output.
The ZIP was rehashed and still matches the retained publisher sidecar:
`a5b2b46378f560b3a2c4ff0c8a5e027cb851c5220ca8a31f9a44f9667ddb0f01`.
Neither result establishes agent-package publisher authentication.

## Skips and source-only limits

| Case | Status / specific unavailable dependency or boundary | Visible chapter treatment |
| --- | --- | --- |
| Private `meridian-finance/checkout-review-pack` and its tools package | **SKIPPED-needs-network** — no private repository read authorization supplied | Explicit marker in Meridian beat and worked example |
| Meridian's real `local-fetch` connection from private `checkout-review-tools` | **SKIPPED-needs-network** — no actual MCP endpoint/executable or runtime authorization supplied for this private service; local configuration-only controls above still executed | Private Meridian fetch is explicitly skipped; the chapter says no real server was launched |
| Native harness callback execution | **NOT RUN by scope**, not a network skip — no harness or agent session was started | Callback definitions are explicitly labelled unexecuted |
| Windows admin lifecycle discovery | **SOURCE-ONLY / NOT RUN**, not a network skip — machine policy creation prohibited by scope | `%ProgramData%\APM\policy.d\*.json` is labelled source-inspected |
| Actual global/user bin deployment | **NOT RUN by scope**, not a network skip or PASS | Chapter explicitly says deployment/permissions were not exercised |
| Local-bundle digest-bound approvals | **SOURCE-ONLY**, not relabelled as a local-path execution | Chapter distinguishes the source contract from the tested ordinary grant |
| Historical 0.23.1 examples | **NOT RERUN / NOT RELABELLED** | Historical evidence remains historical |

Source-only contracts were inspected at the frozen commit, with file hashes
and exact line anchors in `V/batches/final-source/pinned-source-guards.json`.
The source checkout's inspected `src` and `docs` were unmodified.

## Final disposition

All nine current code blocks, the corrected inline command, and their coupled
changed claims are covered by fresh execution, validated independent reuse,
or explicitly bounded source/service limitations above. The final-source check
matched every displayed command's exact arguments and every YAML
manifest/excerpt to the executed input or genuine generated output.

Only the narrow Ch8 selector-evidence correction and metadata clarifications
were applied. This verifier did not edit Ch9, fixtures, historical samples,
edition metadata, TOC, site, or root dependencies, and made no commit or publish
operation. Concurrent unrelated worktree changes were left alone.

**Ready for review.** Keep the local MCP gate, parked-hook replay, native-MCP
audit, and policy failures visible. An accurately reproduced documented
failure is not an upstream repair or blanket security certification.
