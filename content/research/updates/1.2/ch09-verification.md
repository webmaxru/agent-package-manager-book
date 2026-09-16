# Chapter 9 — independent verification, book 1.2 / APM 0.31.0

**Verdict: PASS as documented; ready for chapter review. No Ch9 source fix
required.** Deliberate negative controls and documented upstream limitations
were asserted explicitly. The policy-disable, default hash fail-open,
plural-target audit, and stale-cache behaviors remain limitations, not fixes
or network skips.

## Frozen target, source identity, and isolation

| Item | Verified value |
| --- | --- |
| Chapter | `content/chapters/governance-and-policy.html` |
| Final HTML SHA-256 | `11391907af254a6c13866d431d40100043d1b43f6857dd4dc3e3e70091dbd01a` |
| Incoming/final bytes | Identical; this verifier did not edit Ch9 |
| Edition / target | **book 1.2 / exactly APM 0.31.0** |
| Executable | Supplied absolute `RunRoot/apm-native/unpacked/apm-windows-x86_64/apm.exe` |
| Executable SHA-256 | `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2` |
| Frozen source commit | `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` |
| Environment | Windows x64, Python 3.12.10, PyYAML 6.0.3 |
| New execution window, both chapters | 2026-09-16, 02:01–02:23 UTC |
| Final evidence assembly | 2026-09-16, 02:26 UTC |

Every new batch used the supplied absolute executable, verified its SHA-256,
and required exit **0** with exactly:

```text
Agent Package Manager (APM) CLI version 0.31.0
```

`RunRoot` means the supplied session's `files/book-v1.2` directory. No local
username or credential is published here. Define **V** =
`RunRoot/verify-ch08-ch09`, **F** =
`backend/examples/updates/1.2/operations`.
Command prefixes below are abbreviated: `audit ...`, `policy ...`, etc. mean
**`& $Apm` followed by those exact arguments**, with `$Apm` that absolute
executable, not a PATH lookup.

All APM work occurred in new short owned scratch roots, with isolated
HOME/profile/config/cache/temp and Git credential configuration. Inherited
credentials and the desktop `gh` helper were excluded. No real organization
policy repository, machine admin policy, global bin installation, MCP runtime,
push, publish, or agent session was instantiated.

HTTPS tests used an ephemeral loopback listener and a certificate trusted
only through the child process's `REQUESTS_CA_BUNDLE`. TLS verification stayed
enabled; the ephemeral key was deleted. All requests were anonymous. Synthetic
503s, absent parents, and harmless policy-comment edits are controlled negative
tests, **not unavailable-network skips**.

## Evidence and reuse

* **NEW** records: `V/batches/<batch>/logs/<sequence>-<id>.{json,txt}`.
  `V/command-index.json` resolves each `batch/id` below and retains exact
  commands, CWD, exits, output hashes, runtimes, and raw-file hashes.
* **REUSED** records: completed independent Ch6/Ch7/core executions that
  actually arrived, copied under `V/reused/`; original paths, version guards,
  snapshot hashes, and original runtime are in `V/reuse-index.json`.
* `V/example-statuses.json` provides per-figure statuses and record IDs.
  `V/batches/final-source/embedded-final-blocks.json` and
  `final-source-sha256.json` bind the verdict to the final chapter bytes.
* Every relevant generated lock and policy-cache artifact is retained in raw
  snapshots. Committed fixtures and their locks were not hand-edited.

Across the two requested chapters there were **146 new APM invocations**:
**15** exact-version guards, **10** help commands, **121** focused
example/control commands; summed recorded duration **775.921 s**.
**45** selected independent commands were reused, retaining **392.750 s** of
original command runtime and eight original version guards. These totals
describe the combined run, not an additional Ch9 run or elapsed wall time.
No full 306-probe rerun, `--suite all`, or 0.23.1 rerun occurred.

The supplied `verify.py` `policy` suite ran unchanged through its entrypoint,
with external timing/log capture and an explicit fresh `--work` directory.
Focused probes then executed the exact changed chapter commands, including
the `--no-fail-fast` variants not used by that suite.

### Direct-pin evidence did arrive

The direct pin controls were independently run by the Ch6/Ch7 verifier.
This verifier checked their exact manifest/policy bytes, real depth-two lock,
transitive manifest, output digests, expected findings, and original version
guard before reusing them. **No listener was bound to port 18431 here.**
Fresh case-matching controls used the supplied registry helper on an allocated
ephemeral port instead. Only that scratch endpoint changed; a new genuine lock
was generated rather than editing URLs in a committed lock.

## Every current code example

Every row targets **APM 0.31.0**. Repeated record references are shared evidence,
not repeated executions. Times sum the cited APM command records.

| Example ID / path | Status / origin | Exact executed coverage | Exit(s) | Seconds |
| --- | --- | --- | --- | ---: |
| `ch9-schema-031` / `F/policy/apm-policy.schema.yml` excerpt | **PASS / NEW** | Exact displayed fields match the full fixture; `policy status --policy-source ./apm-policy.schema.yml --json --check` | **0** | 2.701 |
| `ch9-schema-status-031` / same full policy | **PASS / NEW** | Same command; found, warn, no warnings, three registered compilation targets | **0** | 2.701 |
| `ch9-local-parent-031` / `F/policy/apm-policy.parent.yml` | **PASS / NEW** | Full YAML matches; effective child status and required-package audit below | **0/1** | 4.524 |
| `ch9-local-child-031` / `F/policy/apm-policy.child.yml` | **PASS, intended relaxation rejected / NEW** | Full YAML matches; parent block/deny/require retained | **0/1** | 4.524 |
| `ch9-local-merge-031` / complete local policy fixture | **PASS / NEW** | `policy status --policy-source ./apm-policy.child.yml --check --json`; `audit --ci --policy ./apm-policy.child.yml --no-fail-fast -f json` | **0/1** | 4.524 |
| `ch9-direct-pin-negative-031` / controlled `F/registry-graph/apm.yml` excerpt | **PASS, intended negative / REUSED** | Bounded direct audit; `install` after direct-only constraint edit; unbounded direct audit. Audits: `audit --ci --policy ./apm-policy.yml -f json` | **0/0/1** | 8.500 |
| `ch9-consumer-failclosed-031` / consumer `apm.yml` fragment | **PASS / NEW** | Exact `policy.fetch_failure_default: block` fragment; `audit --ci --policy https://127.0.0.1:53426/unavailable.yml -f json`, before/after consumer setting | **0/1** | 15.183 |
| `ch9-pilot-manifest-031` / `F/policy/apm.yml` | **PASS / NEW** | Full YAML matches; actual locked materialization and clean baseline | **0/0** | 12.367 |
| `ch9-pilot-baseline-031` / complete fixture, including `.apm/` and genuine lock | **PASS, baseline only / NEW** | `install --frozen`; `audit --ci --no-fail-fast -f json` | **0/0** | 12.367 |
| `ch9-pilot-warn-031` / `F/policy/apm-policy.warn.yml` | **PASS, finding retained / NEW** | `policy status --policy-source ./apm-policy.warn.yml --json --check`; `audit --ci --policy ./apm-policy.warn.yml --no-fail-fast -f json` | **0/0** | 3.882 |
| `ch9-pilot-block-031` / `F/policy/apm-policy.block.yml` | **PASS, intended negative / NEW** | Same status/audit arguments with `./apm-policy.block.yml` | **0/1** | 4.504 |
| `ch9-pilot-audits-031` / warn then block controls | **PASS / NEW** | Both exact status/audit pairs above, same missing requirement and clean baseline | **0/0/0/1** | 8.385 |

Primary current-record mappings:

* Schema/status: `policy-local/policy-status-schema`.
* Local parent/child: `policy-local/{policy-local-inheritance-status,policy-local-inheritance-audit}`.
* Baseline: `policy/{policy-frozen,policy-ci}`.
* Warn/block: `policy-local/{policy-status-warn,policy-audit-warn,policy-status-block,policy-audit-block}`.
* Direct constraint: reused
  `registry-{bounded-direct-unbounded-transitive,new-direct-intent,unbounded-direct-fails-policy}`.
* Consumer fetch default: `policy-final/{policy-cold-fetch-default-warn,policy-cold-fetch-consumer-block}`.

The minimal consumer has no org remote. Its clean baseline is **not**
organization compliance. The deliberately missing
`example-org/required-review-package#v1.0.0` was never fetched.

Verbatim selected findings from the warn and block audits:

```json
{
  "name": "required-packages",
  "passed": true,
  "message": "1 required package(s) missing from manifest (enforcement: warn)",
  "details": ["example-org/required-review-package"]
}
```

```json
{
  "name": "required-packages",
  "passed": false,
  "message": "1 required package(s) missing from manifest",
  "details": ["example-org/required-review-package"]
}
```

All other checks in these two no-fail-fast controls passed. No fixed check
count is asserted as an API.

## Known schema and command-mode coverage

`policy-local` used the chapter-mapped synthetic `case-*.yml` inputs:

| Input / probe suffix | Exact status arguments after `policy status` | Exit(s) / assertion |
| --- | --- | --- |
| Top-level policy `targets` / `policy-status-unknown-top` | `--policy-source ./case-unknown-top.yml --json` | **0**; `outcome: empty`, warning, no target rule |
| String `dependencies.allow` / `policy-status-wrong-list` and `-check` | `--policy-source ./case-wrong-list.yml --json`, then add `--check` | **0/1**; malformed, not accepted |
| Quoted boolean / `policy-status-wrong-bool` and `-check` | `--policy-source ./case-wrong-bool.yml --json`, then add `--check` | **0/1**; malformed |
| Boolean TTL / `policy-status-wrong-integer` and `-check` | `--policy-source ./case-wrong-integer.yml --json`, then add `--check` | **0/1**; malformed |
| `policy-mode-off` | `audit --ci --policy ./case-off.yml --no-fail-fast -f json` | **0**, 2.515 s; required-package policy checks omitted, baseline still runs |
| `policy-source-without-ci` | `audit --policy ./apm-policy.block.yml -f json` | **0**, 3.761 s; policy option is not enforced |
| `policy-install-no-override-flag` | `install --policy ./apm-policy.block.yml` | **2**, 1.929 s; option rejected |

Verbatim relevant diagnostics:

```text
Unknown top-level policy key: 'targets'
```

```text
Invalid policy file case-wrong-list.yml: Policy validation failed: dependencies.allow must be a YAML list of package patterns
Invalid policy file case-wrong-bool.yml: Policy validation failed: dependencies.require_pinned_constraint must be a boolean, got 'true'
Invalid policy file case-wrong-integer.yml: Policy validation failed: cache.ttl must be a positive integer, got 'True'
```

```text
[!] --policy requires --ci mode. Use 'apm audit --ci --policy <source>' to run policy checks.
```

```text
Usage: apm.exe install [OPTIONS] [PACKAGES]...
Try 'apm.exe install --help' for help.

Error: No such option: --policy (Possible options: --no-policy, --only)
```

These are successful **negative example assertions**, not broken policies
recommended to readers. Plain diagnostic status exit 0 does not mean parsing
succeeded.

### Mandatory hashes do not become advisory under warn

`policy-hash/public-required-hash-baseline-ci` used the real public sample
skill at immutable commit
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`, materialized from the independently
verified snapshot. Its baseline
`audit --ci --no-fail-fast -f json` passed **0**, **5.996 s**.
Only dependency `content_hash` fields were then removed in scratch.

`policy-hash/policy-require-hash-even-warn` ran:

```text
audit --ci --policy ./hash-policy.yml --no-fail-fast -f json
```

Exit **1**, **4.199 s**, under
`enforcement: warn` and `security.integrity.require_hashes: true`.
The other baseline checks remained clean. Exact failing check message:

```text
Locked dependencies are missing required content hashes -- run 'apm install' to regenerate them
```

The CLI itself rendered `<redacted-invalid-registry-url>` in that check's
details; this report did not replace a real package with a fabricated success.
Full output and the deliberately altered scratch lock are retained.

## Inheritance, matching, and direct scope

### Tighten-only: local, null-child, cold HTTPS, and warm HTTPS

The actual local child resolved in block mode with deny/require counts **1/1**
and `extends_chain: []`. Its audit failed the inherited required-package rule.
Thus the empty chain array is not evidence that no local merge occurred.

The additional null-child variant also resolved **0** and audited **1**:
`policy-hash/null-child-inheritance-status` /
`null-child-inheritance-audit`, **2.893 / 2.852 s**. Exact commands:

```text
policy status --policy-source ./apm-policy.nullchild.yml --json --check
audit --ci --policy ./apm-policy.nullchild.yml --no-fail-fast -f json
```

`policy-web` used the retained parent/child bytes from the mapped operations
control, with an allocated loopback HTTPS origin:

| Probe | Exact command | Exit / seconds |
| --- | --- | --- |
| `policy-https-cold-chain` | `policy status --policy-source https://127.0.0.1:58269/child.yml --json --check` | **0 / 4.888** |
| `policy-https-warm-chain` | Same command | **0 / 4.632** |
| `policy-https-inheritance-audit` | `audit --ci --policy https://127.0.0.1:58269/child.yml --no-fail-fast -f json` | **1 / 4.415** |
| `policy-cross-host-chain` | `policy status --policy-source https://127.0.0.1:58269/cross.yml --json --check` | **1 / 5.762** |
| `policy-incomplete-chain` | Same status arguments with `https://127.0.0.1:58269/incomplete.yml` | **1 / 3.887** |

Warm status made **zero additional requests**. The CLI-written effective
cache, not a manufactured cache fixture, retained block enforcement,
block fetch posture, TTL **120**, max depth **3**, required pins, deny/require
entries, narrowed allow list, `scripts: deny`, and `executables.deny_all: true`.
The inherited required-package audit still failed. Cross-host/incomplete
resolution failures were asserted, not skipped.

Source guards independently confirm intersection, additive union, stricter
severity, minimum TTL/depth, OR pin requirement, and the five-level chain cap.
The conflicting companion schema table was not used to weaken these results.

### Path/case coverage

**NEW** `scoped-controls` installed the inert registry graph at an allocated
ephemeral endpoint, then ran these exact audits:

| Probe / policy | Command | Exit / seconds | Meaning |
| --- | --- | --- | --- |
| `policy-registry-mixedcase-allow` / `allow.yml` | `audit --ci --policy ./allow.yml --no-fail-fast -f json` | **0 / 2.186** | `OPERATIONS/**` matches `operations/parent` |
| `policy-registry-mixedcase-deny` / `deny.yml` | Same arguments with `./deny.yml` | **1 / 2.311** | Same canonical-case match denies it |
| `policy-allow-null` / `null.yml` | Same with `./null.yml` | **0 / 2.155** | Null allow has no opinion |
| `policy-allow-empty` / `empty.yml` | Same with `./empty.yml` | **1 / 2.311** | Empty allow denies all |
| `policy-deny-wins` / `deny-wins.yml` | Same with `./deny-wins.yml` | **1 / 2.580** | An allow match does not cancel deny |
| `mcp-policy-same-case` / `same-case.yml` | Same with `./same-case.yml`, against exact root-MCP fixture | **0 / 2.656** | Actual MCP name allowed |
| `mcp-policy-changed-case` / `changed-case.yml` | Same with `./changed-case.yml` | **1 / 1.966** | Uppercase MCP name is not the same identity |

Verbatim relevant failure strings:

```text
operations/parent: denied by pattern: OPERATIONS/**
operations-fixture: not in allowed sources
```

GitHub repository-prefix normalization, local-path sensitivity, preserved
`#ref`/virtual-path suffix casing, and `*` versus `**` segment matching were
independently source-inspected. They are **SOURCE-ONLY boundaries**, not
fresh executions against every host, filesystem, ref, or subpath. The report
does not generalize canonical owner/repository case folding to MCP identities.

### Direct-only pin requirement: exact shared negative

The validated reused `registry-graph` snapshot has a real depth-two dependency.
The parent package declares an unbounded transitive constraint. Under the same
blocking pin policy:

| Reused record | Root direct constraint | Exact command | Exit / seconds |
| --- | --- | --- | --- |
| `registry-bounded-direct-unbounded-transitive` | `^1.0.0` | `audit --ci --policy ./apm-policy.yml -f json` | **0 / 3.537** |
| `registry-new-direct-intent` | Changed to `>=1.0.0` | `install` | **0 / 2.949** |
| `registry-unbounded-direct-fails-policy` | `>=1.0.0` | Same explicit-policy audit | **1 / 2.013** |

Exact failing check detail:

```text
operations/parent: unbounded upper; pair with '<X.Y' or use a caret range
```

The direct-negative YAML in the chapter equals that executed variant.
The verifier also checked the transitive manifest and source implementation's
direct-dependency restriction. This was not replaced with a transitive `#main`
example or an invented registry wildcard.

## Bypass matrix: preserve the authority failure

All controls use the same missing-required-package block policy, with clean
baselines. The first four records are in `policy-finish`; the last is in
`policy-final`. Define the exact base command:

```text
audit --ci --policy ./apm-policy.block.yml --no-fail-fast -f json
```

| Probe | Environment / command difference | Actual exit / seconds | Assertion |
| --- | --- | --- | --- |
| `policy-explicit-control-no-bypass` | Base command, disable absent | **1 / 6.360** | `required-packages` fails |
| `policy-explicit-flag-only` | Insert `--no-policy` before `--no-fail-fast` | **1 / 4.358** | Explicit source beats flag |
| `policy-explicit-env-only` | Base command; child `APM_POLICY_DISABLE=1` | **0 / 6.443** | Policy checks absent |
| `policy-explicit-overrides-disable` | Environment disable plus inserted `--no-policy` | **0 / 6.474** | Still baseline-only |
| `policy-disable-even-failclosed` | Base command; environment disable; consumer `policy.fetch_failure_default: block` | **0 / 14.093** | Still baseline-only |

**Underlying authority guarantee: FAIL.** Diagnosis: in this release the
environment disable suppresses the explicit policy, even with consumer
fail-closed settings. Suggested owner: **apm-cli-explorer / APM maintainers**;
required-workflow owners must protect their environment and inputs.

There is no fabricated error message for the suppressing runs: they exit 0
with baseline JSON and no `required-packages` check. That **absence was
asserted**. The chapter correctly teaches it as failure to enforce, not
compliance or an unavailable-network skip.

## Fetch/hash/stale behavior: exact observed failures

### Malformed explicit policy

Both commands were exactly:

```text
audit --ci --policy ./case-wrong-list.yml --no-fail-fast -f json
```

`policy-finish/policy-explicit-malformed-default`: **0**, **6.732 s**, policy
skipped. Adding consumer `policy.fetch_failure_default: block` produced
`policy-explicit-malformed-failclosed`: **1**, **5.932 s**, with empty stdout
and exact stderr:

```text
[x] Policy fetch failed: Invalid policy file case-wrong-list.yml: Policy validation failed: dependencies.allow must be a YAML list of package patterns (policy.fetch_failure_default=block)
```

### Raw-byte hash pin

The served nonempty policy required the manifest `name` field. A harmless
comment changed its raw bytes after the valid pin control:

| `policy-web` probe | Exact command | Exit / seconds |
| --- | --- | --- |
| `policy-pin-nonempty-valid` | `policy status --policy-source https://127.0.0.1:58269/pin.yml --json --check` | **0 / 5.635** |
| `policy-pin-nonempty-mismatch-status` | Same with `--no-cache` before `--json` | **1 / 6.714** |
| `policy-pin-nonempty-mismatch-audit` | `audit --ci --policy https://127.0.0.1:58269/pin.yml --no-cache -f json` | **0 / 6.309** |
| `policy-pin-nonempty-mismatch-failclosed` | Same audit, consumer fail-closed added | **1 / 4.694** |

Verbatim fatal stderr for the fail-closed run:

```text
[x] Policy fetch failed: Policy hash mismatch from url:https://127.0.0.1:58269/pin.yml: expected sha256:a5b879c6f477a62f4cb74561672cab7a5fab6b6262138184bbb203e695e09c7d, got sha256:bebfc7d7892ec4cdb9754054a145ec9d7aa48285ee60d2c6151ef1335a3d0667 (policy.fetch_failure_default=block)
```

**The blanket “hash mismatch always fails audit” guarantee is FAIL.**
The default audit warned and skipped policy but returned 0; consumer block
changed the result. This behavior is accurately taught, not claimed fixed.
Suggested diagnosis owner: **apm-cli-explorer / APM maintainers**.

### First fetch and real TTL expiry

`policy-final` used only anonymous loopback HTTPS:

| Probe | Exact command | Exit / seconds |
| --- | --- | --- |
| `policy-cold-fetch-default-warn` | `audit --ci --policy https://127.0.0.1:53426/unavailable.yml -f json` | **0 / 8.854**, synthetic 503, policy skipped |
| `policy-cold-fetch-consumer-block` | Same command, consumer block added | **1 / 6.329**, fetch failure |
| `policy-stale-cache-seed` | `policy status --policy-source https://127.0.0.1:53426/stale.yml --json --check` | **0 / 7.308** |
| `policy-stale-fetch-block-status` | Same status after actual TTL expiry and refresh 503 | **1 / 6.899**, `outcome: cached_stale` |
| `policy-stale-fetch-block-audit` | `audit --ci --policy https://127.0.0.1:53426/stale.yml -f json` | **0 / 10.362**, cached rules evaluated |

TTL was genuinely **1 second**, followed by a wait; cache timestamps were
not hand-edited. The cached policy had `fetch_failure: block`. Status rejected
staleness, whereas its compliant cached-rule audit still passed. Freshness and
rule compliance are different checks, just as the chapter says.

## Target audit and MCP trust limits

`policy-finish/{policy-target-plural-audit,policy-target-singular-audit}`
both ran:

```text
audit --ci --policy ./case-target-claude.yml --no-fail-fast -f json
```

* Valid plural `targets: [copilot, claude, cursor]`: **0**, **9.689 s**;
  `compilation-target` reported exactly
  `No compilation target set in manifest`.
* Singular `target: copilot`: **1**, **4.453 s**; the target check failed with
  `Target(s) ['copilot'] not in allowed list ['claude']`.
  `deployed-files-present` and `content-integrity` also failed in that scratch
  variant. This is **not** represented as a clean one-rule rollout control.

**Plural-target audit coverage remains FAIL/limited**, not permission to
deploy disallowed targets. The correct policy key remains
`compilation.target.allow`; changing the intended plural manifest to hide the
gap would be the wrong fix.

`mcp.trust_transitive` was checked against the target parser/docs and remains
**parsed but not enforced**. The actual default depth, root re-declaration,
and explicit `--trust-transitive-mcp` boundary are covered in the
[Ch8 verification](ch08-verification.md), including its retained local MCP
gate and parked-hook failures. Nothing here certifies a live MCP server.

## Discovery, private services, and source-only claims

Frozen source guards confirm:

* GitHub-class candidate order: `.github-private`, `.github`, `.apm`, `_apm`.
* GitLab remote parsing takes the first namespace segment; its adapter selects
  that group's `apm-policy` project.
* ADO primary project/repository is `apm/apm-policy`; `_apm/_apm` is attempted
  only when the primary result is not-found, not on an arbitrary auth failure.
* Cache location is the APM cache root's
  `policy_v1/<project-key>/<source-key>.{yml,meta.json}`; default TTL is 3600 s.

These are **SOURCE-ONLY contracts**, not executed authorization claims.
Hashes/line anchors are retained in
`V/batches/final-source/pinned-source-guards.json` and
`V/additional-source-only-guards.json`.

| Case | Status / precise reason | Chapter visibility |
| --- | --- | --- |
| Live private GitHub/GHES org policy discovery | **SKIPPED-needs-network** — no protected organization repository or read authorization supplied | Explicit marker in discovery section |
| Live GitLab top-level-group policy discovery | **SKIPPED-needs-network** — no group/project service access or authorization supplied | Explicit marker in discovery section |
| Live Azure DevOps policy discovery | **SKIPPED-needs-network** — no org/project/repository authorization supplied | Explicit marker in discovery section |
| Publishing/protecting Meridian's real policy | **SKIPPED-needs-network** — no publication permission or protected policy repository supplied; no push attempted | Discovery and evidence-scope markers |
| Private `meridian-finance/meridian-standards` | **SKIPPED-needs-network** — private package read authorization unavailable | Explicit evidence-scope marker |
| Real `io.github.github/github-mcp-server` registry/runtime | **SKIPPED-needs-network** — live registry/service access and runtime authorization not supplied | Explicit evidence-scope marker; local controls are not substituted as a live PASS |
| Admin lifecycle policy or global executable deployment | **NOT RUN by scope**, not a network skip or policy-engine PASS | Kept separate in Ch8; no machine/global state instantiated |
| Four historical `backend/examples/ch09/` policies | **NOT RERUN / NOT RELABELLED** | Their 0.23.1 verification stamps remain explicit |

## Initial verifier assertions and final disposition

Raw failed verifier attempts were not overwritten:

* `policy-local` initially expected the literal word “ignored” in the bare-audit
  warning. The real warning is quoted above; its policy-not-enforced behavior
  was subsequently asserted from the retained result.
* `policy-finish` and `policy-web` initially searched **stdout** for fatal
  diagnostics. Actual expected errors are on **stderr**. `policy-final`
  validated the retained exact outputs and completed only the outstanding
  controls. These were verifier assertions, not CLI regressions or network
  skips.
* The separate Ch8 wrong-selector evidence issue was minimally corrected and
  rerun; it did not require a Ch9 or fixture change.

No new native command had an unexpected exit code. More importantly, the
expected failures assert actual rule presence/absence, exact findings,
cache behavior, and resulting files rather than accepting exits alone.

All twelve current Ch9 code blocks match their executed inputs/commands.
**No Ch9, fixture, lockfile, historical sample, edition metadata, TOC, site,
or root-dependency edits were made by this verifier. No commit or publish
operation was performed.**

**Ready for review**, with the documented upstream authority and coverage
failures retained. PASS here means the chapter accurately teaches the tested
0.31.0 behavior, not that those upstream guarantees now work.
