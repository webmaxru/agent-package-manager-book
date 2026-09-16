# Edition 1.2 operations reference — Chapters 6–9

**Frozen baseline:** APM 0.23.1 / book 1.1. **Inspected target: exactly APM
0.31.0**, book edition 1.2. This is empirical research and an author/verifier
handoff, **not chapter prose, an independent code-verifier verdict, or release
acceptance**.

The prepared executable reported:

```text
Agent Package Manager (APM) CLI version 0.31.0
```

Every APM invocation used that executable's **absolute path**, never `apm`
resolved from PATH. Its SHA-256 was
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
The matching source/docs checkout is official tag `v0.31.0`, commit
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`. No CLI upgrade, global install,
root authoring-dependency change, live push, policy publication, or agent
runtime execution was performed.

## Read this first: corrections beyond the theory handoff

The [theory brief](theory.md) is the concept map, not a fresh execution
verdict. Exact-version probes resolved several old caveats and exposed
important exceptions to target-tag documentation:

1. **Local policy inheritance now works.** `extends: ./parent.yml` merged
   parent restrictions. Delete Ch9's old “local parents are not merged”
   caveat. Empty child deny/require lists did **not** erase restrictions.
2. **Explicit policy does not beat every bypass.** `--policy FILE` overrides
   `--no-policy`, but **`APM_POLICY_DISABLE=1` still suppresses the explicit
   policy**, even with consumer fail-closed configuration.
3. **Do not promise hash-pin failure always fails CI.** A policy-byte hash
   mismatch was reported, but `audit --ci --policy URL` exited **0** under
   default consumer fetch-failure posture. Adding
   `policy.fetch_failure_default: block` made it exit **1**.
4. **Executable decisions and actual local MCP output disagreed.** A direct
   local dependency's MCP was configured while approval inspection reported
   `mcp[x:default-deny]`. Its hooks were withheld, but CI replay then expected
   the parked hooks and failed. Approval followed by install made that
   fixture audit-clean. Do not relabel the old two-gate demo as a proven
   0.31.0 MCP-withholding guarantee.
5. **Selected registry update has a cache-state failure.** The plan, lock,
   and deployed bytes preserved an unselected dependency at 1.0.0, but its
   materialized cache advanced to 1.1.0. Immediate CI audit failed.
   `install --frozen` repaired the cache without changing the lock, followed
   by a clean audit.
6. **Warning-only is not a CI failure by itself.** Installed benign U+200B
   content produced bare-audit exit **2**, but CI audit exit **0**. A Critical
   finding or a hash mismatch is different.
7. **Frozen MCP checks are manifest-to-lock checks.** A missing native MCP
   file was restored; an edited native MCP file was left unchanged. The
   tested MCP-only project's CI audit did not detect either native-file
   absence or edited arguments.
8. **Windows deletion failure can be misreported as success.** An exclusive
   OS lock prevented deleting a materialized file, yet uninstall returned
   **0**, printed `Uninstall complete`, and removed its declaration and
   dependency ownership. The distinct edited-target-file refusal correctly
   returned **1** and retained the contract.
9. **The inspected PE is not Authenticode-signed.**
   `Get-AuthenticodeSignature` reported `NotSigned`, no signer, on the
   checksum-verified executable above. Release notes mention signing work,
   but that is not evidence this particular ZIP-contained executable is
   signed. Do not transfer either installer checksums or binary signing
   claims to agent-package publisher authentication.

These are not `SKIPPED-needs-network` cases. They are observed behavior,
coverage limits, or reproducible failures of the claimed contract.

## Evidence, isolation, and status vocabulary

**RunRoot** means the orchestrator's session `files/book-v1.2` directory.
**OpsRoot** is `RunRoot/operations-probes`. Absolute executable/CWD paths are
recorded in the raw artifacts rather than embedding local usernames in
reusable examples.

| Artifact under OpsRoot | Contents |
| --- | --- |
| `runtime-layout.json`, `short-public-layout.json` | Exact executable, hash, source commit, and owned temporary paths |
| `logs/<probe-id>.json` and `.txt` | Exact argv, absolute command/CWD, exit, stdout/stderr, duration, and before/after file hashes |
| `command-index.json`, `summary.json`, `evidence-counts.json` | Invocation index and counts; historical unmet expectations remain visible |
| `diagnostic-disposition.json` | Distinguishes corrected assumptions, invalid initial fixtures, Windows path limits, and actual failures |
| `assertions/*.json` | Explicit state assertions, including retained failed assumptions |
| `snapshots/*.zip` | Original manifests, genuine lockfiles, and materialized project snapshots |
| `fixture-verification/all-first.json` | First reusable run, stopped at the newly discovered selected-update cache failure |
| `fixture-verification/all-final.json` | Final reusable suites, asserting both intended outcomes and labelled limitations |
| `fixture-verification/trust-limit.json`, `cleanup-limit.json` | Separate reproductions of genuine CLI failures |
| `policy-inputs/`, `policy-cache-generated/`, `policy-*-http-requests.json` | Input policies, CLI-generated effective cache/TTL metadata, anonymous loopback request evidence |
| `registry-*-requests.json`, `registry-http-requests.json` | Loopback-only publication-state changes and requests; no live publish operation |
| `credential-loopback-requests.json`, `authenticode.json` | Boolean header-presence observations, and the inspected PE signature result |
| `old-claim-anchors.json`, `old-code-blocks.json`, `research-inputs.json` | Ch6–9 legacy claim/code anchors and input hashes |
| `pinned-sources.json`, `fixture-lock-provenance.json` | Target-tag source citations/hashes and unedited exported-lock hashes |
| `probe.py`, `*_probes.py`, `*_followup.py`, `record_evidence.py` | Reproduction machinery; no APM internals were patched or imported as the tool under test |

**Statuses used below:** **OBSERVED** = real command and state inspection;
**NEGATIVE** = deliberately invalid/edited safe fixture produced its intended
error; **FAILURE/LIMIT** = a genuine behavior discrepancy or coverage boundary;
**SOURCE-ONLY** = target-tag contract not exercised here;
**SKIPPED-needs-network** = explicitly unavailable private/live infrastructure.
An expected nonzero in a negative test is not a broken example. Conversely,
making a regression reproduction's test assertion pass does not certify the
underlying APM guarantee.

Child HOME, APM home/cache, app-data directories, temp, and Git configuration
were redirected. No machine admin policy files were created. A desktop `gh`
helper still supplied its own auth fallback during an early incorrectly
routed synthetic transitive dependency; no token value was collected or
committed. Subsequent child environments also hid all PATH entries containing
a `gh` launcher and set an empty Git credential helper. The final reusable
runner includes those stronger controls.

The ordinary profile-temp root was `apmo-2d4facdd`. Some longer fixture names,
and the full public Git package's `.git/objects/pack` staging paths, still
exceeded Windows limits. The full public graph succeeded under the shorter
owned `C:\Windows\Temp\apmo-2d4facdd` root; the final reusable runs also used
short subdirectories there. No OS long-path setting or global Git
configuration was changed. The first full-package diagnostic said “network
error” but its underlying error was **`Filename too long`**: this was not a
network skip. Failed attempts were preserved, not overwritten.

The public packages were real. Policy inheritance used a loopback HTTPS
server with an ephemeral certificate trusted **only by the child process's
`REQUESTS_CA_BUNDLE`**; TLS verification was not disabled and the ephemeral
private key was deleted after the test. Registry examples used the shipped
anonymous HTTP-loopback exception. No real credentials, webhook endpoints,
MCP servers, paid runtimes, or harness callbacks were exercised.

## Reusable examples and concept links

All fixtures are under
[`backend/examples/updates/1.2/operations`](../../../../backend/examples/updates/1.2/operations/README.md).
The nine `apm.lock.yaml` files are genuine, unedited CLI results. **Do not
hand-author replacements.** The `trust` lock preserves a legitimately
installed-but-parked state whose audit failure is explicitly documented.

```powershell
$Apm = '<absolute prepared APM 0.31.0 executable>'
python .\backend\examples\updates\1.2\operations\verify.py --apm $Apm --suite all
# Separate, deliberate reproductions of known failures:
python .\backend\examples\updates\1.2\operations\verify.py --apm $Apm --suite trust-limit
python .\backend\examples\updates\1.2\operations\verify.py --apm $Apm --suite cleanup-limit
```

Python 3.12.10 / PyYAML 6.0.3 were used. The runner requires Python 3.10+ and
PyYAML 6, copies examples to a new short directory, and records full results
there. It uses the supplied absolute executable and rejects a non-0.31.0
banner. `--suite all` reproduces labelled limitations as well as successful
behavior; it is not an all-green security certification.

| Chapter | Implements concept |
| --- | --- |
| 6 | [Recorded identity, content addressing, and provenance](../../06-the-lockfile-and-reproducibility-theory.md); [clock-free reproducibility](theory.md#3-reproducibility-is-recorded-identity-and-content-not-a-clock) |
| 7 | [Report/change/verify and reviewed lifecycle](../../07-lifecycle-theory.md); [freshness versus permission versus integrity](theory.md#4-freshness-permission-to-change-and-integrity-are-separate-questions) |
| 8 | [Install-time supply-chain checks versus runtime controls](../../08-security-by-default-theory.md); [scoped trust](theory.md#5-trust-is-scoped-consent-not-proof-of-benign-behavior) |
| 9 | [Reviewed authority and tighten-only governance](../../09-governance-and-policy-theory.md); [protected enforcement point](theory.md#6-governance-needs-a-reachable-authority-and-a-protected-enforcement-point) |

Command tables below use `install`, `audit`, etc. as shorthand for
`& $Apm <command>`. Exact shell commands/absolute paths are in each named log.

---

## OP06.1 — Timestamp-free lockfiles and recorded identity

**Surface:** `apm.lock.yaml`, `lockfile_version`, `resolved_commit`,
`resolved_ref`, `content_hash`, `resolved_hash`, `deployments`,
`deployed_file_hashes`, `local_deployed_file_hashes`.
**Implements:** Ch6 recorded identity/content/provenance; theory §3.
**Inspected CLI:** 0.31.0. [LOCKFILE]

Fresh locks omit `generated_at`. Unchanged local/package/MCP restores were
byte-stable; the independently hydrated public frozen lock was byte-stable
too. This is evidence about **complete recorded state**, not a clock.
An existing legacy timestamp was tolerated and retained on an unchanged
restore. Git-semver locks still recorded `constraint`, `resolved_tag`, and
`resolved_at`, with `lockfile_version: '2'`; omission of a volatile write
timestamp does not mean every timestamp disappeared.

The source/identity fields are type-dependent:

| Kind actually observed | Recorded identity/integrity |
| --- | --- |
| Public Git skill slice | Repository, host, virtual path, full commit/ref, package-tree `content_hash`, deployed hashes |
| Local path package | `_local/package`, `source: local`, `local_path: ./package`, deployed hashes; no invented Git commit/ref |
| Experimental registry package | `source: registry`, exact version/ref, archive `resolved_url` / `resolved_hash`, package-tree and deployed hashes; no Git commit |
| Root `.apm/` content | `local_deployed_*` and canonical rows owned by `.` |
| MCP-only project | Empty APM dependency list plus `mcp_servers`, `mcp_configs`, `mcp_target_servers`, and URI ownership rows |

Canonical deployment rows contain `kind`, `target`, `value`, `runtime`,
`scope`, `owners`, `active_owner`, and optional `content_hash`. The compatible
per-dependency/local file lists remain; do not omit the new ownership view
from Ch6's field explanation. Root-local or directory/native rows need not
have the same fields/hashes as a Git file dependency.

`name` and ordinary Git/local `version` are self-asserted inventory metadata,
not publisher identity. A skill's `version: unknown` did **not** mean it was
unpinned: the immutable commit was present. The Git-semver form resolved a
real semantic version separately. [LOCKFILE]

| Probe ID | Command / result | Status |
| --- | --- | --- |
| `repro-install`, `repro-restore`, `repro-frozen` | `install`, `install`, `install --frozen`: all 0; no fresh timestamp, unchanged restore lock |
| `mcp-install`, `mcp-restore` | Both 0; MCP-only lock exists and restore bytes agree |
| `lock-legacy-timestamp-restore` | `install`: 0; explicitly seeded legacy timestamp retained |
| `git-semver-install`, `git-semver-noop-plan`, `git-semver-noop-apply` | Install, preview, apply: all 0; real `resolved_at`, no-op plan correctly unchanged |
| `public-independent-lock` | `lock`: 0; fresh resolution-only result, not relabelled as a restore |

**Use:** commit and review the actual manifest/lock pair; compare complete
bytes or hashes for restore evidence. **Do not use:** `generated_at` as a
change oracle, `unknown` as an unpinned test, or one lock shape as a universal
Git/registry/local schema.

**Minimal examples:** [repro manifest](../../../../backend/examples/updates/1.2/operations/repro/apm.yml)
and its [real lock](../../../../backend/examples/updates/1.2/operations/repro/apm.lock.yaml);
[registry real lock](../../../../backend/examples/updates/1.2/operations/registry/apm.lock.yaml).

**Author — Ch6:** replace the annotated timestamp row and timestamp-based
no-op transcript; remove “every dependency has ref + SHA + content hash.”
Do not simply restamp the old environment-dependent local hash.

### Hash normalization is not source-byte rewriting

Deployed UTF-8 text hashes normalize CRLF to LF. Rewriting all six deployed
instruction projections to CRLF still passed `audit --ci` with unchanged lock
bytes (`hash-crlf-ci`, exit 0). An independent SHA-256 calculation over
normalized bytes matched the lock, while raw file bytes differed.

Package-tree `content_hash` has a different contract: sorted relative paths
and actual materialized bytes. The target's GitCache-backed subpath checkout
pins `core.autocrlf=false`, but that does not override every `.gitattributes`
or `core.eol` rule, nor rewrite CRLF committed in the source. This raw-tree
definition is target-source-grounded, not a universal cross-platform
whole-package equality claim. [LOCKFILE]

**Author — Ch6/8:** say “canonical deployed-text hash,” not “every output is
byte-identical across platforms/harnesses.” Copilot/Claude/Cursor instruction
representations legitimately had different hashes.

### `lock export --timestamp` is an SBOM control

`help-lock-export-help` confirmed:

```text
lock export -f [cyclonedx|spdx]
--timestamp TEXT  Pin the SBOM timestamp (ISO 8601 with timezone required...)
```

Help specifies timestamp fallback: `SOURCE_DATE_EPOCH`, legacy lock
`generated_at`, then Unix epoch. It is not a flag for restoring `generated_at`
to fresh lockfiles. Export execution was not needed for this bounded update;
do not turn this help confirmation into an executed SBOM example.

## OP06.2 — Frozen semantics and cold-cache replay

**Command:** `install --frozen`.
**Implements:** Ch6 reproducible restore; theory §§2–3.
**Inspected CLI:** 0.31.0. [INSTALL] [BASELINE]

Frozen is a structural lock/manifest gate, including declared MCP lock
configuration. It is **not** a universal native-file content audit, a ban on
materialization writes, or a promise that every metadata edit leaves the
lock byte-identical. Retain Priya's missing regenerated lock story.

| Exact probe ID | Safe setup and command | Exit / observed output |
| --- | --- | --- |
| `frozen-missing-lock` | Delete scratch lock; `install --frozen` | **1**; `--frozen requires apm.lock.yaml to exist` |
| `frozen-missing-direct` | Declare public package absent from existing lock; same command | **1**; names missing direct package; no project writes |
| `frozen-missing-local-path` | Remove declared local source directory | **1**; missing local source is not hydrated from nowhere |
| `public-frozen-ref-edit-same-commit` | Change public skill's full-SHA selector to `v1.0.0` at the same commit | **0**, lock metadata changed; not a literal-ref-string gate |
| `public-frozen-promote-transitive-shortpath` | Add the already locked public transitive skill directly at its locked SHA | **0**, lock changed to represent direct declaration |
| `frozen-edited-deployment` | Edit a deployed instruction before frozen restore | **0**; managed file restored; the preflight did not reject content drift |
| `frozen-mcp-manifest-changed` | Change root MCP args, keep old lock | **1**; `MCP server 'operations-fixture' config differs from apm.lock.yaml` |
| `frozen-mcp-missing-lock-state` | Remove synthetic MCP lock-state keys | **1**; server missing from lock; no repair writes |
| `frozen-mcp-missing-native-file` | Delete `.github/mcp.json`, leave manifest/lock consistent | **0**, native file recreated |
| `frozen-mcp-native-changed` | Edit native MCP arguments only | **0**, file left unchanged |
| `frozen-positional-conflict`, `frozen-mcp-add-conflict` | Add-style invocation combined with frozen | **1**, explicit conflict error |
| `frozen-update-conflict` | `install --frozen --update` | **2**, usage conflict |

The first versions of the MCP native-file probes wrongly expected failure;
the preserved exit 0 results are **the finding**, not a failed manifest.
Likewise, do not copy exit 2 to every forbidden frozen combination.

Cold-cache proof used more than a warmed directory:

| Probe ID | Initial state | Actual result |
| --- | --- | --- |
| `public-cold-ci` | Deployed tree + manifest/lock, no modules, independent empty cache | `audit --ci --no-fail-fast -f json`: **0**; no checkout writes |
| `public-cold-offline-ci` | Same, but process proxy deliberately points at unavailable loopback | **1**; replay/hydration failure, not a harmless green skip; no checkout writes |
| `public-cold-frozen` | No modules and another empty cache | `install --frozen`: **0**; genuine public hydration, complete lock bytes unchanged |
| `public-full-git-apm-cold-shortpath` | Full Git `apm_package` graph, no modules, empty cache | **0**; Git package + transitive skill restored from pins |
| `cold-local-audit-ci`, `cold-local-frozen` | Valid local source, no modules | Both **0**; audit kept modules absent in checkout, frozen materialized them |
| `registry-graph-cold-frozen` | Locked parent/leaf 1.0.0; loopback source subsequently offers 1.1.0 | **0**, parent/leaf remain locked; identical lock bytes |

The immutable public sample commit was
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`.
The full sample's unbounded transitive resolved in this run to
`fb4eb04fcbd30de50052b1155d81167393dfb5aa` for
`github/awesome-copilot/skills/review-and-refactor`. The sample's direct pin
does not freeze a **fresh** future resolution of that transitive; committing
the genuine graph does. The local registry graph supplies a controlled,
no-live-push demonstration of replay versus subsequent newer resolution.

**Use:** frozen materialization in reproducible builds; audit separately;
permit necessary network access for missing locked content. **Do not use:**
“cold” as a synonym for “offline,” or install's successful exit as proof that
arbitrary native config bytes were checked.

**Minimal examples:** `repro/`, `mcp/`,
[registry graph](../../../../backend/examples/updates/1.2/operations/registry-graph/apm.yml);
the existing core
[pinned public skill](../../../../backend/examples/updates/1.2/core/pinned-skill/apm.yml)
is reused rather than modified by this task.

**Author — Ch6:** replace the old six-row table with these bounded cases.
For a moving upstream branch, explain unchanged-manifest locked replay;
do not infer that changing any manifest selector to any other commit must
pass. Private host-qualified frozen matching remains SOURCE-ONLY here.

## OP06.3 — Lock-only generation and provenance lookup

**Commands:** `lock`, `find PATH --source`, `find PATH --path`.
**Implements:** Ch6 separation of contract generation/materialization and
traceability. **Inspected CLI:** 0.31.0. [LOCK] [LOCKFILE]

`lock` runs resolution/materialization as needed for dependency metadata but
does not deploy or delete harness files. It **retains existing deployment
ownership** until ordinary reconciliation can safely clean it. A brand-new
resolution-only lock has no prior deployment rows to retain. Both statements
are true; the old “always omits deployed_files” generalization is not.

| Probe ID | Operation | Exit / state |
| --- | --- | --- |
| `lock-retains-ownership` | Delete a deployed canary but retain the old lock, then `lock` | **0**; canary absent; old file hashes/ownership and lock bytes retained |
| `lock-new-resolution-only` | Fresh local project, `lock` before install | **0**; resolution recorded, no deployment rows or harness files |
| `target-contraction-lock-only` | Narrow manifest to Copilot, then `lock` | **0**; Claude/Cursor files and ownership retained |
| `target-contraction-install`, `target-contraction-ci` | Then ordinary install and CI audit | **0**, **0**; dropped target files removed, remaining state clean |
| `find-package-source` | `find .github/instructions/library.instructions.md --source` | **0**, dependency provenance |
| `find-local-source` | Same query for workspace instruction | **0**, workspace provenance |
| `find-untracked` | Query `.github/not-owned.md` | **1**, not tracked |

`--path` remains in the inspected help. The full public graph snapshot also
records `depth`/`resolved_by`; do not reproduce old transitive commit prefixes
as current evidence. `find` is a provenance lookup, not publisher
authentication or a second integrity check.

**Use:** headless lock generation or provenance lookup. **Do not use:** lock
alone to repair missing harness files, or assume deletion is safe before
hash-aware install/prune.

**Minimal example:** `verify.py --suite repro`; `repro/apm.lock.yaml`.
**Author — Ch6:** keep the canary experiment, but show both “existing lock”
and “no previous lock” cases rather than deleting the evidence needed to
demonstrate retention.

---

## OP07.1 — Report, deliberately update, then verify

**Commands/keys:** `outdated`, `update [PACKAGES] --dry-run|--yes`,
`dependencies.apm[].{git,ref}` and experimental
`dependencies.apm[].{registry,id,version}`.
**Implements:** Ch7 deliberate lifecycle; theory §4.
**Inspected CLI:** 0.31.0. [OUTDATED] [UPDATE] [REGISTRIES]

`outdated` queries source freshness without changing project state.
`update` offers a constraint-respecting plan and requires consent for
changes. `audit` checks the resulting state. This is still the right
maintenance triad, but update is **not the only verb capable of changing
resolution**: explicit manifest edits followed by install, install refresh
modes, and lock refresh modes also do so.

Git-only output retains Current/Latest/Status/Source. Registry rows introduce
**Wanted**: Current = locked version; Wanted = highest version allowed by the
manifest; Latest = highest published parseable version, including eligible
prereleases under this implementation's ordering. Newer Latest does not
authorize crossing a constraint.

The controlled loopback source initially served 1.0.0 and then exposed 1.1.0
and `2.0.0-beta.1`. No real repository tag or registry release was pushed.

| Probe ID | Command | Exit / concrete result |
| --- | --- | --- |
| `registry-outdated-current-wanted-latest` | `outdated --verbose` | **0**; exact: Current/Wanted 1.0.0; range: Wanted 1.1.0; Latest 2.0.0-beta.1; no writes |
| `registry-outdated-wide` | `outdated` after updates | **0**; full Source text `registry: fixture (outside constraint)`; Latest prerelease visible |
| `registry-selected-plan` | `update operations/range --dry-run --verbose` | **0**; **`1 updated, 2 unchanged`**, no project writes |
| `registry-selected-without-consent` | `update operations/range` with closed stdin | **1**; `Cannot prompt for confirmation in non-interactive shell` |
| `registry-selected-apply` | `update operations/range --yes` | **0**; selected lock version 1.1.0; exact/other locked at 1.0.0 |
| `registry-exact-noop-plan` | `update operations/exact --dry-run --verbose` | **0**; `All dependencies already at their latest matching refs.` |
| `registry-apply-within-constraints` | `update --yes` | **0**; allowed ranges advance; exact pin stays |
| `registry-install-edited-constraint` | Edit exact selector to 1.1.0, then `install` | **0**; proves install can reconcile changed declared intent |
| `git-semver-noop-plan`, `git-semver-noop-apply` | Public Git `^1.0.0` preview/apply | **0**, **0**; accurate no-op; no manufactured update count |
| `registry-update-empty-cache-no-consent` | `update` with unchanged refs and empty modules | **0**; restores same cache refs without consent or lock mutation |
| `mcp-repair-preview-control`, `mcp-repair-apply-control` | MCP-only `update --dry-run`, then `update --yes` | **0**, **0**; preview did not repair; apply recreated missing config |
| `registry-outdated-no-json-flag` | `outdated --json` | **2**; no such output flag |

The target help offers no outdated package filter. Local dependencies are
skipped by freshness reporting. Outdated findings are not process errors.
Network/query failures can report `unknown`; do not certify a source's
freshness from cached refs alone. Full-SHA Git refresh has special
annotated-semver-tag rules; preserve this as a bounded note, not a new tag
tutorial. [OUTDATED] [UPDATE]

### Reproducible selected-update cache failure

The first probes checked the plan/lock and later audited after updating
everything. The reusable runner inserted the missing **immediate** audit
and found a real failure:

```text
                     lock       deployed text       apm_modules metadata
operations/range     1.1.0      1.1.0               1.1.0
operations/other     1.0.0      1.0.0               1.1.0   <-- unselected
operations/exact     1.0.0      1.0.0               1.0.0
```

`selected-registry-update-audit-reproduced` returned **1** with:

```text
modified: .github/instructions/other.instructions.md
```

`content-integrity` passed because deployed bytes still matched the lock;
cache-based drift replay failed. `selected-registry-update-frozen-repair`
returned **0**, changed the two cached `other` files, and left the lock
byte-identical. `selected-registry-update-after-repair-ci` then returned **0**.
The final reusable registry suite asserts the failure **before** repair.
This is not a justification for `--no-drift`.

**Use:** owner-reviewed periodic refresh with diff + immediate audit.
**Do not use:** the repaired plan counter as proof that all cache/state
transitions are correct, nor assume noninteractive decline exits 0.

**Minimal examples:** [registry manifest](../../../../backend/examples/updates/1.2/operations/registry/apm.yml),
[deterministic server](../../../../backend/examples/updates/1.2/operations/registry_fixture.py),
`verify.py --suite registry`.

**Author — Ch7:** remove “only version-moving verb,” “pinned packages never
show outdated,” and “plan always overstates movement.” Replace the old
`-> -` transcript with the observed accurate plan. Keep an explicit
experimental-registry boundary and the selected-cache caveat; do not
recommend bypassing audit to make the refresh look successful.

## OP07.2 — Drift, ownership, and audit exit codes

**Commands:** `audit`, `audit --ci --no-fail-fast -f json`, `prune`.
**Implements:** Ch7 integrity verification; Ch6 provenance ownership.
**Inspected CLI:** 0.31.0. [AUDIT] [BASELINE]

Bare audit reports ordinary replay drift advisory-only. Invalid canonical
deployment ownership is different: it fails **both** modes. CI audit can
hydrate locked content in scratch when the checkout has no modules; “audit
is always offline” and “setup-only CI must skip drift” are obsolete.

| Situation actually isolated | Bare audit | CI audit | Evidence |
| --- | --- | --- | --- |
| Clean recorded local project | 0 | 0 | Baselines / reusable runner |
| Benign modified Copilot rule | 0 | 1 | `drift-copilot-bare`, `drift-copilot-ci` |
| Benign modified Claude rule | 0 | 1 | `drift-claude-bare`, `drift-claude-ci` |
| Benign modified Cursor rule | 0 | 1 | `drift-cursor-bare`, `drift-cursor-ci` |
| Invalid deployment owner/active owner | 1 | 1 | `ownership-invalid-bare`, `ownership-invalid-ci` |
| Replayed file has no ownership claim, even though bytes agree | Not rerun for this case | 1 | `ownership-unrecorded-ci` reports `unrecorded` |
| Critical character in an unrecorded governed file | 1 | 1 | `scan-unrecorded-whole-bare`, `scan-unrecorded-whole-ci` |
| Warning-only content installed and correctly hashed | 2 | **0** | `scan-warning-short-bare`, `scan-warning-short-ci` |
| Cold replay cannot hydrate locked source | Do not extrapolate | 1 | `public-cold-offline-ci` |

Ten checks happened to run in the clean local dependency fixture:
`lockfile-exists`, `ref-consistency`, **`deployment-ledger-owners`**,
`deployed-files-present`, `no-orphaned-packages`,
`skill-subset-consistency`, `config-consistency`, `content-integrity`,
`includes-consent`, `drift`. This is an observed list, **not a universal
fixed total**. Empty projects, early failures, policy, and configuration
change the count. `--no-fail-fast` is used here for diagnostic coverage.

`prune` removed the invalid owner rows (`ownership-prune`, 0), but the next
audit found an **unrecorded** file (`ownership-after-prune`, 1). Ordinary
install then restored complete ownership and audit passed
(`ownership-reinstall-after-prune`, `ownership-repaired-after-install`,
both 0). “Prune repairs invalid ownership” does not mean every remaining
deployment discrepancy is automatically resolved.

**Use:** CI integrity gating, read-only diagnosis, then explicit repair.
**Do not use:** bare audit as a drift gate, fixed totals as an API, or
`--no-drift` as a repair.

**Minimal example:** `repro/`, `verify.py --suite repro`.
**Author — Ch7/8:** replace the stale exit-code table, remove Ch8's
cross-chapter “Chapter 7 got this wrong” correction after aligning the
chapters, and keep built-in audit distinct from a CVE database.

## OP07.3 — Cleanup and trusted lifecycle scripts

**Commands/keys:** `uninstall`, `update`, `install`,
`lifecycle.{pre-install,post-install,pre-update,post-update,pre-uninstall,post-uninstall}`,
`lifecycle trust|untrust|validate|test`, `APM_NO_SCRIPTS=1`.
**Implements:** deliberate change and scoped consent; theory §§4–5.
**Inspected CLI:** 0.31.0. [UNINSTALL] [LIFECYCLE] [LIFECYCLE-CLI]

APM **can execute** lifecycle commands. Project commands are skipped until
the canonical lifecycle subtree is trusted. Editing unrelated metadata
keeps trust; changing the subtree revokes it. Trust is stored in the
redirected APM home's `scripts-trust.json`, not committed into the lock.
Commands are synchronous with timeouts; HTTP callbacks are a distinct
documented background mechanism, not exercised against a live endpoint.

The safe command in `lifecycle/record.py` reads stdin JSON and records only
event names. It neither logs environment values nor the payload's absolute
working directory.

| Probe ID | Command / controlled state | Exit / observation |
| --- | --- | --- |
| `lifecycle-validate` | Validate fixture | **0** |
| `lifecycle-test-preview` | `lifecycle test post-install` | **0**; no execution |
| `lifecycle-test-explicit-execute` | Same with `--execute`, before trust | **0**; explicit inspection ran the event despite untrusted project state |
| `lifecycle-trust`, `lifecycle-install-trusted` | Trust, then install | **0**, **0**; pre-install + post-install recorded |
| `lifecycle-other-edit-keeps-trust` | Change description, install | **0**; scripts still execute |
| `lifecycle-subtree-edit-revokes` | Change lifecycle command, install | **0**; project scripts skipped |
| `lifecycle-command-failure-nonfatal` | Retrust harmless recorder that exits 7 after recording | APM **0**; `scripts.log` contains `exit_code=7` |
| `lifecycle-kill-switch`, `lifecycle-untrust` | Disable for one run / revoke | **0**, **0** |
| `lifecycle-invalid-http-plain` | Validate an `http://` webhook definition only | **1**; HTTPS required; no request made |
| `lifecycle-invalid-unknown-event` | Unknown event name | **1** |
| `lifecycle-invalid-run-key`, `lifecycle-run-alias-execute` | `run: echo harmless` | **0**, **0**; actual binary accepts the `run` alias despite narrower field tables |

### Dry-run is not a blanket no-code-execution promise

With trusted project lifecycle scripts:

| Command | Observed event changes |
| --- | --- |
| `install --dry-run` | No events |
| `update --dry-run` | **pre-update and pre-install** ran; fixture file changed |
| No-op `update --yes` | **pre-update and pre-install** ran; no post-update in this local no-op case |
| `uninstall ./package --dry-run` | **pre-uninstall** ran |
| `update --dry-run` with `APM_NO_SCRIPTS=1` | No event/file change in the reusable control |

Evidence: `lifecycle-install-dry-run`, `lifecycle-update-dry-run`,
`lifecycle-update-no-op`, `lifecycle-uninstall-dry-run`,
`event-results/*.json`, and the reusable lifecycle suite.
Do not convert the documented post-event schedule into a guarantee for
every no-op path.

### Cleanup errors: preserve the tested distinctions

| Probe ID | Safe failure setup | Actual result |
| --- | --- | --- |
| `uninstall-selection-atomic` | One valid and one unknown identifier | **1**, no project or lifecycle writes; valid selection not removed |
| `uninstall-edited-file` | Edit owned target file before uninstall | **1**, file + manifest/lock retained; modules already partly removed |
| `uninstall-retry-after-repair` | Restore benign original file, retry same portable key | **0**; final dependency removed, lock deleted in that dependency-only fixture |
| `install-stale-edited-file` | Still-present source stops producing an edited old target file | **0**, edited stale file retained with warning |
| `mcp-required-native-write-failure`, `mcp-required-native-write-force` | A directory occupies required MCP JSON file path | Both **1**; `--force` does not turn general write failure into success |
| `uninstall-directory-delete-failure` | Windows `CreateFileW` share-mode zero on module manifest | **0**, falsely reports complete; locked file remains, declaration/lock removed |
| `uninstall-locked-file-reproduced` | Independent fixture and verified OS-level lock | **0**, same flaw; root-local lock rows may remain, but removed dependency ownership is gone |

The first directory-delete retry then failed selection because the preceding
“successful” uninstall had already removed its declaration. Do not describe
that as a missing network permission or a broken fabricated identifier.
The final `cleanup-limit` suite reproduced the dependency-only variant.

**Use:** explicit lifecycle trust for reviewed repository automation; honor
cleanup warnings and preserve ownership until corrected. **Do not use:**
update/uninstall preview in an untrusted automation context as a guarantee
of no side effects, or nonfatal lifecycle command errors as deployment
transaction guarantees.

**Minimal example:** [lifecycle manifest](../../../../backend/examples/updates/1.2/operations/lifecycle/apm.yml),
`record.py`, `verify.py --suite lifecycle`; separate `--suite cleanup-limit`.
**Author — Ch7/8:** add a short boundary callout, not a webhook tutorial.
Keep the monthly review owner and the reviewed diff; do not teach silent
best-effort cleanup as reliable completion.

---

## OP08.1 — Authorized deploy-set scan and its limits

**Commands:** automatic install scan; `audit --file`, `--strip`,
`--strip --dry-run`.
**Implements:** early supply-chain checkpoint, not semantic intent analysis.
**Inspected CLI:** 0.31.0. [SECURITY] [AUDIT]

The scanner checks the **authorized deployable source set** before
agent-readable deployment, not every downloaded file before any disk write.
A plain package README containing a harmless Critical-class marker did not
block a clean primitive. A declared skill subset excluded an unselected
marker-bearing skill. A mixed install deployed the clean package, withheld
the Critical-bearing primitive, and exited 1: the whole batch was not an
all-or-nothing transaction.

| Probe ID | Exact command / setup | Result |
| --- | --- | --- |
| `scan-critical` | `audit --file critical.md`, benign U+202E + U+200B | **1** |
| `scan-warning` | `audit --file warning.md`, benign U+200B only | **2** |
| `scan-info` | `audit --file info.md --verbose`, legitimate emoji sequence | **0** |
| `scan-strip-preview`, `scan-strip`, `scan-after-strip` | Preview, strip, rescan same file | **0/0/0**; preview unchanged, strip removed markers |
| `scan-source-only-install`, `scan-source-only-ci` | README marker outside authorized primitives | **0/0** |
| `scan-admissible-selected-skill`, `scan-admissible-selected-ci` | Local collection with metadata manifest and `skills: [clean]` | **0/0**; unselected marker not deployed |
| `scan-mixed-package-install` | Clean + Critical-class fixture packages | **1**, clean package deployed |
| `scan-mixed-force-benign-only` | Explicit force on that harmless test only | **0**; break-glass bypass is real |
| `scan-unrecorded-whole-bare`, `scan-unrecorded-whole-ci` | Add unrecorded governed Critical-class file to locked project | **1/1** |
| `scan-package-selector-narrower` | `audit _local/package -f json` on that same project | **0, but zero files scanned**; superseded as scan evidence by the independent Ch8 correction below |
| `scan-warning-short-strip`, `scan-warning-short-frozen-restore` | Strip deployed warning copies, then frozen restore | **0/0**; source unchanged, marker reappears on restore |

**Independent correction:** [ch08-verification.md](ch08-verification.md) proves
`audit ./package -f json` scanned three files and exited 0, including a rerun
against the final chapter. The older `_local/package` success is retained as a
zero-coverage observation, not successful package-scan evidence.

The initial skill-collection attempt omitted any local intake manifest or
root skill/plugin marker and was rejected. Adding a valid metadata manifest
fixed the fixture. The original rejection is not evidence that skill
selection or deploy-set scanning failed.

**Use:** built-in pre-deploy checks plus explicit review/audit; `--file` for
arbitrary standalone content. **Do not use:** a clean Unicode report as a
benign-intent certificate, whole-project claims for a package-scoped audit,
or stripping a deployed copy as a durable upstream fix.

**Minimal example:** `verify.py --suite security`; it generates only inert
character-class test text, not an injection payload. No invisible markers
are hidden in the committed authored fixture files.
**Author — Ch8:** replace “before any disk write,” “all downloaded files,”
and universal batch-transaction wording. Keep force as a loud exception,
not normal remediation.

## OP08.2 — Hook ownership and native paths

**Surface:** `.apm/hooks/*.json`, package/per-dependency `targets`,
merged native settings and APM sidecars.
**Implements:** runtime callback versus package lifecycle; bounded
portability and ownership. **Inspected CLI:** 0.31.0. [HOOKS]

The hook fixture uses a harmless Node `.mjs` callback with a sibling helper.
APM deployed it but did not start a harness or run it. Source `SessionStart`
became Copilot `sessionStart` and Claude `SessionStart`.

Observed outputs included:

```text
.github/hooks/package-notice.json
.github/hooks/scripts/package/.apm/hooks/notice.mjs
.github/hooks/scripts/package/.apm/hooks/helper.mjs
.claude/hooks/package/.apm/hooks/{notice.mjs,helper.mjs,package.json}
.claude/settings.json
.claude/apm-hooks.json
.cursor/hooks/package/.apm/hooks/{notice.mjs,helper.mjs,package.json}
.cursor/hooks.json
.cursor/apm-hooks.json
```

Copilot **did not receive** the Node `package.json` sidecar; Claude/Cursor
did. `.mjs` keeps the Copilot ESM example independent of that sidecar.
Do not promise a universal hook JSON/event shape or duplicate sidecar layout.

| Probe ID | Observation |
| --- | --- |
| `hooks-install`, `hooks-restore`, `hooks-frozen`, `hooks-audit-ci` | All **0**; stable genuine hook ownership lock |
| `hooks-user-entry-audit-ci` | Add unrelated user-owned Claude hook; audit **0** |
| `hooks-user-entry-restore`, `hooks-user-entry-uninstall` | Both **0**, user hook preserved |
| `hooks-owned-sidecar-drift-ci`, `hooks-owned-sidecar-missing-ci` | Both **1**; owned sidecar edits/absence are not ignored |
| `hooks-target-contraction-install`, `hooks-target-contraction-update` | Both **0**; remove dropped Claude/Cursor contributions and owners |
| Corresponding `*-ci` probes | **0** after contraction |
| `hooks-dependency-target-filter` | Per-dependency `[claude]` narrowed three authorized targets; only Claude deployed |
| `target-override-preserves-others` | One-run `--target copilot` did not contract the explicit manifest's other targets |

**Use:** target-specific callbacks only where justified; preserve user-owned
merged entries and review APM-owned sidecars. **Do not use:** hook files as
portable skills, a package's target declaration to expand consumer authority,
or `--target` alone as a declaration that every other target was removed.

**Minimal example:** [hooks fixture](../../../../backend/examples/updates/1.2/operations/hooks/apm.yml),
`verify.py --suite hooks`. **Author — Ch7/8:** retain the source/runtime
distinction and qualify drift by ownership; a user hook is not an APM tamper.

## OP08.3 — Executable approvals, MCP, and credential destinations

**Commands/keys:** `executables: {}`, `approve`, `deny`, `policy explain`,
`install --trust-bin|--no-trust-bin`, `dependencies.mcp`,
registry credential URL bindings.
**Implements:** scoped consent and destination authority, not benignness.
**Inspected CLI:** 0.31.0. [APPROVE] [INSTALL] [MCP] [REGISTRIES]

### Canonical identity, aliases, and version-looking grants

Without the broad gate opt-in, backward-compatible executable deployment
rules still exist; plugin-bin invocation consent is an additional boundary.
With `executables: {}`, hooks in the local fixture were parked.
`approve --list` and `policy explain ./package` reported deciding layers.

`approve friendly-display-name` **was accepted as an alias**, contrary to an
initial overstrict expectation, and wrote the **canonical** key:

```yaml
executables:
  allow:
    ./package#1.0.0:
      hooks: true
      mcp: true
```

`approve ./package` was also accepted. The old “keys on name, not path”
pitfall must be replaced by “accepted selectors may include aliases; the
persisted grant is bound to canonical dependency identity.”

Changing the local dependency's declared version to 1.1.0 left the original
grant unchanged, and `approve --list` reported
`./package#1.1.0: hooks[+:project-allow] mcp[+:project-allow]`.
These version-looking ordinary keys are **not per-release approvals**.
Two packages with identical self-asserted name/version metadata proved the
identity boundary: approving `./one` deployed only one's hook, not two's.

Evidence: `trust-display-name-not-authority`, `trust-approve-canonical`,
`trust-approved-list`, `trust-version-change-install`,
`trust-version-change-list`, `trust-two-identities-*`, all exit **0**.
`trust-invalid-string`, `trust-invalid-grant-string`, and
`trust-invalid-grant-bool-string` each exited **1** on malformed native YAML
types. Local-bundle digest-bound grant keys are **SOURCE-ONLY here**, delegated
to the separate producer/distribution research rather than guessed from an
ordinary local-path grant.

### Do not conceal the two observed local gate failures

The local direct dependency had `registry: false` MCP and an empty consumer
`executables` block. Its initial output included:

```text
hooks skipped (not approved ...)
Trusting direct dependency MCP 'operations-trust-fixture' ...
Configured 1 server
```

Yet `trust-explain-canonical` reported:

```text
verdict: blocked
hooks [x] blocked (layer: default-deny)
mcp   [x] blocked (layer: default-deny)
```

An MCP-only control (no hooks) reproduced actual native configuration while
`trust-mcp-only-list` reported `mcp[x:default-deny]`.
That control audited **0**, so a successful audit is not proof this
executable decision was enforced. The hook-bearing parked fixture audited
**1** (`trust-audit-ci`):

```text
unintegrated: .claude/apm-hooks.json
unintegrated: .claude/settings.json
unintegrated: .github/hooks/package-notice.json
```

After canonical approval + reinstall, `trust-approved-audit-ci` exited **0**.
After denial, inspection reported `project-deny` and the hook replay failure
returned. This is a live local-path limitation, not evidence that every
remote MCP path behaves identically. Do not turn the intended trust ladder
into an unqualified empirical guarantee.

The [core reference](core-reference.md#6-mcp-integration-is-target-specific-and-depth-aware)
already proved direct self-defined MCP trust, depth-two withholding,
consumer re-declaration, and separation of dev-only entries. Reuse that
evidence; “every dependency-provided MCP is transitive and blocked” is false.
`--trust-transitive-mcp` remains distinct from the broad executable gate.

### Native MCP paths and audit boundary

The `mcp/` fixture generated:

| Target | Path | Native container |
| --- | --- | --- |
| Copilot CLI | `.github/mcp.json` | `mcpServers` |
| VS Code | `.vscode/mcp.json` | `servers` |
| Claude Code | `.mcp.json` | `mcpServers` |

Its lock recorded per-runtime MCP ownership URIs with null content hashes.
`mcp-edited-native-ci` and `mcp-missing-native-audit-ci` both exited **0**:
native argument edits/file absence are not covered as deployed-text hash
drift in this MCP-only example. Pair the frozen manifest/lock checks with
direct runtime-config inspection; never advertise audit as a comprehensive
MCP configuration byte comparator or a server health test.

Core research also demonstrated environment placeholder differences and
that direct `--env` input can materialize a non-secret value in manifest/lock.
Keep secret guidance precise: a placeholder in one output does not prove
there is no plaintext elsewhere.

### Plugin bin consent: do not force global scope to manufacture a PASS

| Probe ID | Command | Observed project-scope result |
| --- | --- | --- |
| `bin-project-default` | `install` in noninteractive mode | **0**; `bin/ executables skipped (not trusted)` |
| `bin-project-trust-explicit` | `install --trust-bin` | **0**; `re-run with -g (global) to deploy them to Claude Code` |
| `bin-project-no-trust-explicit`, `bin-project-frozen` | Explicit deny / frozen | Both **0**, no bin deployment |

The flags are shipped and the default-withholding diagnostic is verified.
Actual user-scope bin deployment and its permissions were **not run**:
global installs were expressly out of scope. The target contract says
invocation consent cannot override policy denial. Do not confuse this
additional default with the older broad gate's opt-in status.

### Credential URL binding: withhold credentials, not necessarily the request

The tests used only the literal public marker
`PUBLIC-NON-CREDENTIAL-FIXTURE`; no actual secret was read or sent.

| Probe ID | Safe local test | Result |
| --- | --- | --- |
| `credential-registry-path-binding` | User-owned binding `/bound-path`, project URL `/different-path`, same TLS origin | **1** only because fixture package was absent (404); request was **anonymous** |
| `credential-bound-tls-request` | Matching binding | **1** (intentional 404); header present, value never logged |
| `credential-registry-no-http-auth` | Matching HTTP-loopback binding with marker | **1**, **no request**: credentials are not sent over HTTP |
| Reusable `different-binding-anonymous-only` | Mismatched binding, public anonymous package exists | **0**, actual install, no auth header |
| `registry-reject-token-key-in-manifest` | Forbidden `token:` key with public marker | **1**, no token-bearing project schema accepted |
| `credential-policy-url-redaction` | Policy URL with public query/fragment marker | **0**, diagnostic source omitted query/fragment |
| `policy-reject-plain-http` | Policy source is `http://` loopback | `status --check`: **1**; different policy-transport rule from anonymous registries |

The first credential assertion wrongly expected zero requests on binding
mismatch. The actual safe behavior is **anonymous access**, not mandatory
request refusal. Do not label that as credential leakage.

**Use:** canonical reviewable grants, per-destination credentials, explicit
MCP declarations/config review. **Do not use:** self-asserted names, ordinary
version suffixes, a clean scan, checksums, or a successful install as proof
of publisher trust or runtime confinement.

**Minimal examples:** `trust/` (labelled failure reproduction), `mcp/`,
`verify.py --suite credential`, `--suite trust-limit`.
**Author — Ch8:** preserve withhold-versus-build-break for the proven
depth-two case, but replace the old direct executable-MCP green claim with
the observed limitation or a narrowly verified hooks-only demonstration.
Do not add `--no-drift` to make the parked fixture green.

### Installer and runtime boundary

Lifecycle admin JSON discovery is Windows
`%ProgramData%\APM\policy.d\*.json`, not an organization YAML-policy location.
The POSIX counterpart is `/etc/apm/policy.d/*.json`. User lifecycle scripts
are under the APM user manifest; project trust is subtree-bound. No machine
policy file was written. These are SOURCE-ONLY admin/fleet paths, supported
by the pinned lifecycle reference. [LIFECYCLE]

The prepared ZIP checksum was verified by setup; this role rechecked the
executable identity and observed **NotSigned** through Windows Authenticode.
Do not describe this as a signing verification success. Regardless of
installer channel, none of these observations establishes agent-package
signatures, SLSA provenance, semantic benignness, or runtime sandboxing.

---

## OP09.1 — Policy schema, diagnostics, and authoritative enforcement

**Commands/keys:** `policy status --policy-source ... --json [--check]`,
`audit --ci --policy ...`, `enforcement`,
`compilation.target.allow`, `policy.fetch_failure_default`.
**Implements:** reachable authority and protected enforcement; theory §6.
**Inspected CLI:** 0.31.0; **policy remains early preview**. [POLICY] [POLICY-REF] [POLICY-SCHEMA]

Use the valid [schema fixture](../../../../backend/examples/updates/1.2/operations/policy/apm-policy.schema.yml)
for the chapter's trimmed YAML, not an invented exhaustive schema.
It validates dependency allow/deny/require, depth/pin constraints, MCP
transport/self-defined settings, compilation target rules, manifest fields,
unmanaged-file settings, cache, and executable posture. Additional
security/registry fields have separate feature/coverage boundaries.

Unknown top-level keys **warn**. They do not become rules:

```text
warnings: ["Unknown top-level policy key: 'targets'"]
rule_counts.compilation_targets_allowed: -1
```

`policy-status-unknown-top` exited **0** and reported `outcome: empty` because
there was no real rule. Correct nesting produced the expected target-rule
count. Known wrong native types produced `outcome: malformed`, e.g.:

```text
dependencies.allow must be a YAML list of package patterns
```

`policy-status-wrong-list`, `-wrong-bool`, and `-wrong-integer` returned **0**
in diagnostic mode; their `*-check` variants returned **1**. Parser rejection
is not the same as “every command must now exit 1”: a malformed explicit
policy audit followed consumer fetch-failure posture (`policy-explicit-malformed-default`
0; `policy-explicit-malformed-failclosed` 1).

`policy status --check` gates **resolution outcome**, not rule compliance.
The local warning and blocking policies both resolved with status exit 0,
but their audits differed:

| Probe ID | Command | Exit |
| --- | --- | --- |
| `policy-audit-warn` | `audit --ci --policy ./apm-policy.warn.yml --no-fail-fast -f json` | **0**; missing required package visible as `(enforcement: warn)` |
| `policy-audit-block` | Same with block policy | **1**; missing required package fails |
| `policy-no-remote-status`, `policy-no-remote-check` | `policy status --json`, then `--check` with no remote | **0**, **1** |
| `policy-source-without-ci` | Bare audit with `--policy` | **0** plus ignored-option warning; not the policy gate |
| `policy-install-no-override-flag` | `install --policy FILE` | **2**; install has no such override flag |

Baseline audit failures remain independent of the policy warn/block dial.
Additionally, `security.integrity.require_hashes: true` is explicitly
fail-closed even in warn mode: `policy-require-hash-even-warn` returned **1**
for a deliberately hash-stripped public Git lock, check
`dependency-content-hashes`. Do not describe every policy-related condition
as uniformly downgradable to exit 0.

`compilation.target.allow` is still correct, but the plural-only audit
limitation remains: `[copilot, claude, cursor]` against allow `[claude]`
audited **0** (`policy-target-plural-audit`); the singular `target: copilot`
control failed **1** (`policy-target-singular-audit`). Plural `targets` are
real authorized targets, **not merely candidate hints**. This audit check's
limited input handling is why target restrictions are a weak audit-gate demo.

**Use:** local rehearsal via explicit source, machine-readable diagnostics,
and protected CI for actual authority. **Do not use:** correct parse alone
as evidence of enforcement, or a local filename as proof install will
auto-discover it.

**Minimal examples:** `policy/apm-policy.warn.yml`, `.block.yml`, `.schema.yml`;
`verify.py --suite policy`.
**Author — Ch9:** replace “silent drop/no warning” with the real warning and
native-type diagnostic; keep `compilation.target.allow`; use a robust
dependency violation rather than plural targets as the rollout example.

## OP09.2 — Tighten-only inheritance and direct pin scope

**Surface:** policy `extends`, allow/deny/require lists, escalation fields,
cache TTL, `dependencies.require_pinned_constraint`.
**Implements:** authoritative inheritance and bounded consumer control.
**Inspected CLI:** 0.31.0. [INHERITANCE] [POLICY-CHECKS]

The target policy-schema page contradicts the actual implementation:
its inheritance section says child `[]` can clear inherited deny/require
lists and `fetch_failure` is child-overridden. **Do not copy that table.**

A parent with block enforcement, block fetch posture, TTL 120, max depth 3,
required/denied packages, pinned-constraint requirement, MCP denial,
required manifest field, `scripts: deny`, and `executables.deny_all: true`
was combined with a child attempting to relax all of them.

`policy-https-cold-chain` and `policy-https-warm-chain` both resolved **0**:
effective enforcement block, one deny, one require, one MCP deny, one
required manifest field. The **CLI-written cached YAML**, not a handcrafted
fixture, retained:

```yaml
enforcement: block
fetch_failure: block
cache: {ttl: 120}
dependencies:
  max_depth: 3
  require_pinned_constraint: true
# Parent deny/require entries also remained.
manifest:
  scripts: deny
executables:
  deny_all: true
```

The warm invocation made **zero additional server requests**; it did not
silently weaken the policy. `policy-https-inheritance-audit` failed **1** on
the retained required-package rule. `policy-cross-host-chain` and
`policy-incomplete-chain` both produced `status --check` exit **1**; no
cross-host credentials were sent.

The local counterpart is now empirical too:
`policy-local-inheritance-status` returned **0**,
`policy-local-inheritance-audit` **1**, using
`extends: ./apm-policy.parent.yml`. Parent block/required/denied rules survived
empty child lists. Local status returned an empty `extends_chain` array even
though effective values proved the merge; do not use that array alone to
conclude “no inheritance.”

| Rule family | Safe teaching contract supported by target source/probes |
| --- | --- |
| Allow lists | Narrow by intersection; null has no opinion, empty allow denies everything |
| Deny/require lists | Additive union; null/empty child does not erase parent's entries |
| Enforcement and fetch-failure posture | Escalate to stricter value |
| Max depth / TTL | Minimum |
| Require pinned constraint, required safety booleans | Cannot weaken inherited true requirements |
| `mcp.trust_transitive` | Remains parsed-but-not-enforced per target docs/source; do not substitute it for CLI/declaration trust |

### The pin requirement is direct-scoped

The loopback registry parent had a bounded root constraint `^1.0.0`, but its
own manifest declared child `>=1.0.0` without an upper bound. Real install
produced a depth-two lock, and
`policy-pin-direct-only-control` audited **0** under a blocking pin policy.
Changing the root's direct constraint to `>=1.0.0`, installing, and auditing
produced **1** (`policy-pin-direct-unbounded-control`).

The initial transitive fixture incorrectly omitted its own registry routing
and used `*` as though it were a supported registry semver range; it was
rejected/routed as a Git source. The corrected explicit-registry,
`>=1.0.0` fixture is the usable evidence. Do not call that setup mistake an
APM transitive-pin-policy failure.

Mixed-case registry owner/repository policy patterns were also verified:
`OPERATIONS/**` allow passed **0**, deny failed **1**
(`policy-registry-mixedcase-allow`, `policy-registry-mixedcase-deny`).
GitHub casing normalization is target-source-grounded; refs, subpaths, and
MCP identities must not be described as generally case-insensitive.

**Use:** local rehearsal of parent/child tightening, explicit direct bounded
constraints, warm-cache parity checks. **Do not use:** local inheritance as
automatic organization discovery or a transitive-only unbounded dependency
as Ch9's failing pin example.

**Minimal examples:** [parent](../../../../backend/examples/updates/1.2/operations/policy/apm-policy.parent.yml),
[child](../../../../backend/examples/updates/1.2/operations/policy/apm-policy.child.yml),
[registry graph + policy](../../../../backend/examples/updates/1.2/operations/registry-graph/apm-policy.yml).
**Author — Ch9:** preserve warn → measure → remediate → block; replace the
old local-inheritance pitfall and correct the pin-rule setup to a direct
violation, consistent with Ch11.

## OP09.3 — Discovery, cache paths, bypasses, and fetch-failure authority

**Surface:** host-specific discovery, `--no-policy`, `APM_POLICY_DISABLE`,
consumer `policy.fetch_failure_default` / `policy.hash`.
**Implements:** reachable authority plus protected inputs.
**Inspected CLI:** 0.31.0. [DISCOVERY] [POLICY-REF]

Host-specific paths are SOURCE-ONLY for live private organizations in this
task; do not invent a universal repository cascade:

| Host | Target-tag discovery contract |
| --- | --- |
| GitHub/GitHub-class | `.github-private` preferred, then `.github`, `.apm`, `_apm` |
| GitLab | Top-level group's `apm-policy` project; self-managed-host controls documented separately |
| Azure DevOps | Project `apm`, repository `apm-policy`; legacy `_apm/_apm` only after a 404 |

Meridian may keep `.github`; preferred `.github-private` does not require a
fictional migration. Private-host publication/authorization remains
**SKIPPED-needs-network**: no organization repository or permissions were
supplied and no live policy was published.

Policy cache moved out of `apm_modules/.policy-cache/`. The live cache was
under the isolated **APM cache root**
`policy_v1/<project-key>/<source-key>.{yml,meta.json}`. TTL and complete strict
fields survived warm reads; project inventories remained unchanged.

### Explicit source and bypass matrix — use actual outcomes

All cases below used the same real missing-required-package block policy.

| Probe ID | Invocation/environment | Exit |
| --- | --- | --- |
| `policy-explicit-control-no-bypass` | `audit --ci --policy ./apm-policy.block.yml ...` | **1** |
| `policy-explicit-flag-only` | Add `--no-policy` | **1**; explicit source wins over flag |
| `policy-explicit-env-only` | Set `APM_POLICY_DISABLE=1`, no bypass flag | **0**, only baseline checks |
| `policy-explicit-overrides-disable` | Both env disable and `--no-policy` | **0** |
| `policy-disable-even-failclosed` | Env disable plus explicit source plus consumer fail-closed | **0** |
| `policy-implicit-disabled-baseline` | Auto-discovery suppressed with `--no-policy` | **0**, baseline still runs |

The misleadingly named early probe `policy-explicit-overrides-disable`
**did not** prove override: its unexpected exit 0 triggered the isolated
controls. Preserve its actual result. The target audit help/docs describe
explicit-source precedence too broadly for the environment variable.

**Author — Ch9:** remove “explicit --policy always beats both bypasses.”
Explain why a required job must protect its command, selected policy,
environment, and workflow inputs. `--ci` is not itself an unbypassable
organization authority.

### Fetch and policy-byte hash failure

| Probe ID | Case | Exit / behavior |
| --- | --- | --- |
| `policy-no-remote-failclosed-install`, `policy-no-remote-failclosed-audit` | Consumer `fetch_failure_default: block`, no remote | **1/1** |
| `policy-cold-fetch-default-warn` | First explicit HTTPS fetch receives synthetic 503; no cache | **0**, warning, enforcement skipped |
| `policy-cold-fetch-consumer-block` | Same, consumer fail-closed | **1** |
| `policy-pin-nonempty-valid` | Real nonempty policy matches consumer SHA-256 pin | `status --check`: **0** |
| `policy-pin-nonempty-mismatch-status` | Only a harmless comment changes fetched raw bytes | `status --check`: **1**, mismatch diagnostic |
| `policy-pin-nonempty-mismatch-audit` | Same mismatch, default consumer posture | **0**, warning, policy skipped |
| `policy-pin-nonempty-mismatch-failclosed` | Same mismatch, consumer fail-closed | **1** |
| `policy-stale-fetch-block-status` | Expired TTL=1 cached policy with `fetch_failure: block`; refresh 503 | `status --check`: **1**, `outcome: cached_stale` |
| `policy-stale-fetch-block-audit` | Same stale policy, explicit audit | **0**, cached rules still evaluated; not a freshness failure |

Do not claim that an unread remote `fetch_failure: block` secures a first
fetch. Also do not promote the doc's “hash mismatch always fail-closed”
wording over the actual audit result. `status --check` is useful for an
explicit freshness/resolution preflight, but it is not a substitute for
rule compliance, and its stale rejection differs from audit's cached-rule
evaluation. No cache timestamp was hand-edited to make this result: the
loopback policy really expired after its one-second TTL.

**Use:** consumer fail-closed defaults and protected policy/preflight inputs
when policy must be reachable; inspect both discovery status and rule audit.
**Do not use:** remote intent alone as cold-fetch authority, or checksum
pinning as a way around protected enforcement.

**Minimal examples:** `policy/` plus the reusable policy suite; raw loopback
TLS/hash/fetch fixtures are retained in `policy_probes.py`,
`policy_followup.py`, and `final_edge_probes.py`.

---

## OP07.4 — `pack --check-clean` is a separate, read-only release check

**Command:** `pack --check-clean [--offline] [--marketplace-path ...]`.
**Implements:** report-before-change over generated distribution output,
not deployed integrity. **Inspected CLI:** 0.31.0. [PACK]

This is a bounded Ch7/Ch9 distinction, not a new Ch10 tutorial.
The local fixture has both an explicit empty dependency mapping and a
local marketplace entry. `pack --offline --json` generated its ordinary
outputs. `pack --check-clean --offline --json` then exited **0** and changed
**no** project file. Editing the marketplace JSON produced **4**, still
without repairing/writing anything; a missing overridden marketplace path
also produced **4**.

Evidence: `pack-check-generate`, `pack-check-clean-readonly`,
`pack-check-dirty-readonly`, `pack-check-path-override-missing`.
The final reusable pack suite repeats clean and dirty byte inventories.

**Use:** check generated marketplace output against declared inputs.
**Do not use:** as an alias for `audit --ci`, an automatic repair, or a
bundle-round-trip test. Remote metadata certification (`--strict-metadata`,
exits 4/5 interplay) remains SOURCE-ONLY here and belongs to the other
researcher's producer scope.

**Minimal example:** [pack-check manifest](../../../../backend/examples/updates/1.2/operations/pack-check/apm.yml),
`verify.py --suite pack`.

## Chapter-by-chapter author instructions

### Chapter 6 — retain the forgotten-lock story, replace the evidence

- Keep Priya adding a dependency without committing the regenerated lock.
  Missing lock/direct dependency still fails 1 before project mutation.
- Replace `generated_at` fields/transcripts with real no-timestamp locks.
  Explain legacy timestamps and semver `resolved_at` separately.
- Add canonical ownership and type-specific identity/hash fields; remove
  “unknown means unpinned” and the old unconditional local deployed-hash
  environment caveat.
- Retain same-commit ref-change and already-locked transitive-promotion
  nuance; do not broaden it into “frozen allows arbitrary new resolution.”
- Add cold-cache hydration and MCP **manifest-to-lock** cases. Do not call
  frozen restore read-only or all native state content-verified.
- Rewrite the lock-only omission claim into fresh versus pre-existing
  ownership cases. Keep `find` as provenance, not trust.

### Chapter 7 — preserve the maintenance cadence; update outcomes

- Keep the report → reviewed change → verify workflow and monthly owner.
  Update is the recommended consented path, not the only version-moving verb.
- Replace overstated no-op plans with accurate `unchanged` behavior.
  Explain registry Current/Wanted/Latest without promising a public hosted
  registry or expanding the chapter into registry administration.
- Noninteractive change without `--yes` exited 1. Preview has lifecycle
  exceptions; use `APM_NO_SCRIPTS=1` when demonstrating strict no-execution.
- Replace fixed audit totals and “always offline”; add ownership failure
  in both modes and warning-only CI nuance.
- Do not hide selected-update cache drift: immediate audit exposed it;
  frozen repair then passed without moving the lock.
- Bound cleanup completion/error claims, especially the actual Windows
  exclusive-file-lock failure. `check-clean` is separate marketplace drift.

### Chapter 8 — keep the gate-versus-runtime boundary honest

- Scan authorized deployable files, not all downloaded bytes; partial
  multi-package success is possible before an overall exit 1.
- Make Critical/Warning/Info and bare/CI outcomes agree with Ch7; remove the
  old corrective aside after the table is fixed.
- Separate ordinary drift, invalid ownership, unrecorded governed content,
  and user-owned hook additions.
- Reuse core depth-two MCP/redeclaration evidence. Fix Copilot versus
  VS Code MCP paths and avoid a blanket no-plaintext claim.
- Replace name-only approval teaching with canonical keys and accepted
  selectors. Ordinary version suffixes are not per-release consent.
- Explicitly handle the observed local MCP decision/output mismatch and
  parked-hook replay failure; no silent green restamp.
- Mention noninteractive/frozen bin withholding without performing or
  promising project-scope global-only deployment.
- Add lifecycle consent as the exception to “APM never runs code.”
  Windows admin JSON paths are not org-policy YAML paths.
- Do not assert the inspected executable is signed: it was NotSigned.
  No package signing, publisher authentication, semantic safety certificate,
  or runtime sandbox was established.

### Chapter 9 — preserve rollout, fix authority and inheritance

- Keep warn → measure → remediate → block and `.github` as a valid fictional
  location; describe host-specific preferred discovery without relocating
  Meridian unnecessarily.
- Unknown keys now warn; known wrong types are rejected by parsing, while
  command exit depends on diagnostic/fetch posture.
- Keep `compilation.target.allow`, but do not use plural-only target audit
  as the blocking example.
- Replace the local-extends non-merge pitfall with a real local rehearsal.
  Empty deny/require arrays do not relax the parent; cached strict fields
  and TTL survive.
- Use an unbounded **direct** dependency for the pin violation; the
  controlled pinned-direct/unbounded-transitive graph passed.
- Correct policy cache location and first-fetch consumer authority.
- Explicit policy beats the flag, **not the observed env bypass**.
  Protect the required workflow's inputs/environment. Hash mismatches and
  stale-cache posture have actual outcomes that differ from broad docs.
- Keep the preview label and parsed-but-not-enforced transitive-policy
  caveat; do not invent live private-host governance verification.

## Verifier handoff and limits

The final reusable run returned 0 after reproducing its expected cases,
including labelled CLI limitations; the first run's real selected-update
failure is preserved. `trust-limit` and `cleanup-limit` also reproduced
their documented failures. None is an agent-reviewer ACCEPT verdict.

The retained evidence contains **306 primary APM invocations**, including
**25 help probes**, plus **87 invocations in the final reusable suite**,
the preserved 80-invocation first run, and 11 separate trust/cleanup
reproduction invocations. No primary invocation timed out. Nine genuine
lockfiles were exported. Python/YAML syntax, local file links, and the
fixture scan for local usernames/private paths/token-shaped values passed.

1. Re-run the exact-version fixture commands above in a new short directory.
   Check every observed nonzero, known-limit label, and actual native config.
2. Use the **genuine** committed locks and retained snapshot locks for
   excerpts. Do not regenerate historical 0.23.1 output and call it 0.31.0.
3. No private org policy, GHES/GitLab/ADO permission chain, private registry,
   real MCP runtime, global bin deployment, or machine admin policy was
   executed. Live private/publication steps are **SKIPPED-needs-network**
   where applicable; global/admin/runtime exclusions are **scope limits**,
   not network excuses.
4. The existing local-native Agent Plugin canonical-IR audit failure from
   core research remains an independent known limitation. This task did not
   rerun it or “fix” it by disabling drift.
5. Public Git network runs succeeded after shortening Windows paths; early
   path errors and the invalid synthetic registry routing/collection
   attempts are setup limitations with corrected controls, not shipping
   feature failures.
6. Ch5 and Ch10–12 were concurrently owned by other researchers/authors.
   This task changed only this note and the operations fixture subdirectory;
   it did not author chapters, version metadata, TOC/site files, or commits.

## Pinned sources and release-impact trace

The supplied `upstream.json` was inspected across all ten intervening releases,
following the scoped release-note entries and relevant `impact.md` rows.
The main shipped-change groups
used here include graph replay/host matching (#1973/#2010/#2011), target
ownership and hook cleanup (#2114/#2249/#2275), accurate update planning
(#2053/#2165/#2305), cold audit/frozen fixes (#2329/#2502/#2446),
unrecorded-content coverage (#2380/#2381), lock-only cleanup and timestamp
changes (#2312/#2616), bin consent and malformed trust (#2508/#2719),
user hook drift (#2682), policy cache/discovery/casing
(#2193/#2235/#2058/#2450/#2662/#2706), and registry reporting (#2874).
PR grouping identifies release impact, not a claim that every theoretical
guarantee in those changes passed these probes.

- [Install][INSTALL], [lock][LOCK], [lockfile schema][LOCKFILE],
  [audit][AUDIT], [baseline checks][BASELINE].
- [Update][UPDATE], [outdated][OUTDATED], [uninstall][UNINSTALL],
  [pack][PACK].
- [Security][SECURITY], [hooks][HOOKS], [approvals][APPROVE],
  [MCP][MCP], [lifecycle guide][LIFECYCLE], [lifecycle CLI][LIFECYCLE-CLI].
- [Policy guide][POLICY], [policy reference][POLICY-REF],
  [policy schema with the conflicting inheritance table][POLICY-SCHEMA],
  [parser][PARSER], [inheritance implementation][INHERITANCE],
  [direct-pin checks][POLICY-CHECKS], [discovery][DISCOVERY].
- [Experimental registries][REGISTRIES], [HTTP API][REGISTRY-API],
  [target changelog][CHANGELOG], [frozen release][RELEASE].

[RELEASE]: https://github.com/microsoft/apm/releases/tag/v0.31.0
[CHANGELOG]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/CHANGELOG.md
[INSTALL]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/install.md
[LOCK]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/lock.md
[LOCKFILE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/lockfile-spec.md
[AUDIT]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/audit.md
[BASELINE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/baseline-checks.md
[UPDATE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/update.md
[OUTDATED]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/outdated.md
[UNINSTALL]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/uninstall.md
[PACK]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/pack.md
[SECURITY]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/security.md
[HOOKS]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/producer/author-primitives/hooks-and-commands.md
[APPROVE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/approve.md
[MCP]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/consumer/install-mcp-servers.md
[LIFECYCLE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/lifecycle-scripts.md
[LIFECYCLE-CLI]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/lifecycle.md
[POLICY]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/apm-policy.md
[POLICY-REF]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/policy-reference.md
[POLICY-SCHEMA]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/policy-schema.md
[PARSER]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/parser.py
[INHERITANCE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/inheritance.py
[POLICY-CHECKS]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/policy_checks.py
[DISCOVERY]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/discovery.py
[REGISTRIES]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/guides/registries.md
[REGISTRY-API]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/registry-http-api.md
