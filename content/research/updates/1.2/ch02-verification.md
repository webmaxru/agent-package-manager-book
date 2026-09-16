# Chapter 2 independent delta verification — book 1.2 / APM 0.31.0

**Verdict: PASS.** The current replay uses byte/argv/input-equivalent
independent Ch5 evidence; the public version query and the remaining
registry/identity controls were independently executed. The historical
full-package tag snippet remains **0.23.1-only**, not a new install proof.
No chapter or fixture was edited.

## Source, executable, and evidence

| Item | Value |
| --- | --- |
| Chapter | `content/chapters/lessons-from-package-managers.html` |
| Source SHA256 | `a4e626f634b7a930483e233023e79bf61f092bbd95e316c33f91f253f8260ff7` |
| Exact current CLI | **0.31.0** |
| Execution date | 2026-09-16 UTC |
| Code blocks | 3: historical tag illustration, version query, current two-command replay |

`RunRoot` is the orchestrator's `files/book-v1.2` artifact directory.
`Wave`/`N` = `RunRoot/verify-core-wave`; `Prior`/`R` =
`RunRoot/verify-ch05`; record IDs resolve to `logs/<id>.json` and matching
raw output files. `Scratch` is the new short owned root in
`Wave/runtime-layout.json`. `Core` and `Operations` refer respectively to
`backend/examples/updates/1.2/core` and `.../operations`.

All table commands are exact arguments after the absolute executable:

```powershell
$Apm = Join-Path $RunRoot 'apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

Executable SHA256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
Each new batch checked the exact banner first. Commands used normal short
CWDs with isolated HOME/cache/config/temp/credentials, not `--root`, the
book checkout, a PATH-selected APM, or host/global configuration.

The [wave accounting](ch01-verification.md#execution-and-bounded-reuse)
is **78 new invocations / 241.350 s**, including 9 version guards and 7
help commands, for all four chapters together. **53 independent Ch5
command records and 13 original guards** were checked read-only, not
rerun. Explorer observations were not promoted to independent verification.

## Per-example disposition

| Example ID / path | Status | CLI / runtime | Origin and input scope |
| --- | --- | --- | --- |
| `Chapter#ch2-pin-history` | **PASS — historical-boundary check only** | Original **0.23.1** stamp; no new command/exit/runtime | Code unchanged except Git checkout EOL representation; full-package tag install deliberately not executed |
| `Chapter#ch2-view-versions` | **PASS** | **0.31.0**, exit 0, **3.018 s** | **New** anonymous Git query, empty `Scratch/p/pv`, no default registry |
| `Chapter#ch2-current-replay` | **PASS** | **0.31.0**, exits 0/0, original **11.722 s** | **Reused independent** first `install` and unchanged `install` for exactly the named pinned-skill fixture |
| `ch2-source-identities` | **PASS**, source-specific scope | **0.31.0** | Genuine Git/local/registry locks; new legacy-timestamp and explicit-Git/default-registry controls |
| `ch2-registry-report` | **PASS** | **0.31.0** | New controlled registry listing/report/no-op preview, not a live publication |
| `ch2-replay-boundary` | **PASS**, unchanged versus edited intent | **0.31.0** | Reused Git replay/ref-edit controls; new registry-selector edit + install/audit |
| `ch2-audit-boundary` | **PASS**, integrity/Unicode scope | **0.31.0** | Independently retained clean audit plus shared new scan controls; no CVE-feed or universal coverage claim |
| `ch2-registry-boundary` | **PASS**, experimental implementation versus service/spec distinction | **0.31.0** plus frozen source | New gate/consumption evidence; source-only publication/API/spec contract review |

The historical reference explicitly lacked a completed old live-tag probe.
The revised caption no longer calls that historical snippet a current
verified full-package installation. Neither the single-skill result nor
another chapter's full graph is substituted for it.

## Replay equivalence — PASS

First input was **only** `Core/pinned-skill/apm.yml`, without the committed
fixture lock or generated files:

```text
manifest SHA256:
345bd03e5b24af37425cffe624cf8d3ebafff7e60b061b7af1288de7ce65162b

complete generated/replayed lock SHA256:
6b9ebb9ddcba38e6eddae38ca0c3658c2fabeee90e279857c9159f149ba09507
```

`Wave/reuse-evidence.json` checks the canonical bytes against
`Prior/canonical-core.zip`, the first command's complete before-inventory,
both exact `["install"]` argv arrays, the first after-state versus second
before-state, complete lock bytes, raw stdout/stderr, resulting snapshots,
and the preceding exact-version guard. This is bounded delta reuse of
**independent execution**, not merely the explorer's equal-looking manifest.

| Origin / record ID | Exact command | Exit | Native seconds |
| --- | --- | ---: | ---: |
| R `public-pinned-skill-install` | `install` | 0 | 8.574 |
| R `public-pinned-skill-restore` | `install` | 0 | 3.148 |
| R `public-pinned-skill-frozen` | `install --frozen` | 0 | 2.969 |
| R `public-pinned-skill-audit` | `audit --ci` | 0 | 2.896 |
| R `cold-frozen` | `install --frozen` | 0 | 10.335 |
| R `cold-audit` | `audit --ci` | 0 | 2.544 |
| R `ref-initial-frozen` | `install --frozen` | 0 | 15.084 |
| R `ref-changed-ref-install` | `install` | 0 | 10.193 |
| R `ref-changed-ref-audit` | `audit --ci` | 0 | 4.743 |

The cold control started with only the canonical manifest/lock and an
independent empty cache. The ref-edit control deliberately changed the
declared full SHA to the sample's `v1.0.0` ref; it is reconciliation
evidence, not a simulated moving-upstream experiment.

The lock has exactly one skill dependency, full commit/ref
`fb2851683be0e0e7711421d518bd8dba23b0b1f6`, and no `generated_at`.
Inventory `version: unknown` is compatible with that immutable Git identity.
Both `.agents/skills/style-checker/SKILL.md` and
`.claude/skills/style-checker/SKILL.md` exist and have SHA256
`1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829`.
No full sample/transitive graph or live harness behavior is newly certified.

## New commands — precise current claims

| Record ID under N | CWD under `Scratch/p` | Exact command | Exit | Native seconds |
| --- | --- | --- | ---: | ---: |
| `public-versions` | `pv` | `view microsoft/apm-sample-package versions` | 0 | 3.018 |
| `reg-feature-disabled` | `rg` | `install` | **1, expected** | 2.130 |
| `reg-enable` | `rg` | `experimental enable registries` | 0 | 1.746 |
| `reg-install` | `rg` | `install` | 0 | 2.821 |
| `reg-audit` | `rg` | `audit --ci` | 0 | 2.104 |
| `reg-view-routed` | `rg` | `view operations/exact versions` | 0 | 2.567 |
| `reg-outdated` | `rg` | `outdated` | 0 | 1.740 |
| `reg-exact-pin-plan` | `rg` | `update operations/exact --dry-run --verbose` | 0 | 3.019 |
| `reg-edited-selector-install` | `rg` | `install` | 0 | 2.535 |
| `reg-edited-selector-audit` | `rg` | `audit --ci` | 0 | 2.398 |
| `reg-disable` | `rg` | `experimental disable registries` | 0 | 2.179 |
| `final-legacy-timestamp-restore` | `ts` | `install` | 0 | 8.581 |
| `final-enable-registries` | `gr` | `experimental enable registries` | 0 | 3.944 |
| `final-explicit-git-install` | `gr` | `install` | 0 | 11.315 |
| `final-explicit-git-audit` | `gr` | `audit --ci` | 0 | 5.122 |
| `final-disable-registries` | `gr` | `experimental disable registries` | 0 | 3.342 |

The public query included `v1.0.0` / `fb285168` and wrote no project files.
`view --help`, `outdated --help`, `update --help`, and
`experimental --help` were also executed, exit 0; their raw records and
individual guards are indexed in `Wave/command-index.json`.

Registry input was the **complete unchanged Operations/registry manifest**,
not just Chapter 4's excerpt: three dependency entries, initial selectors
1.0.0 / ^1.0.0 / ^1.0.0, explicit Copilot target, default `fixture`, and
`includes: auto`. Manifest SHA256:
`d8d6ea2fb9dffc74da04466cf1d6a4901bbf5e9cb3034fb77abd22af934293a4`.
The existing deterministic server was served at its literal
`http://127.0.0.1:18431`, anonymously, with no publication endpoint.

The disabled-feature refusal included:

```text
Top-level 'registries:' blocks requires the experimental registries feature.
Enable with: apm experimental enable registries.
```

Its full native diagnostic is in `N/logs/reg-feature-disabled.*`;
manifest/project hashes and mtimes did not change. Enable/disable wrote
only the disposable batch HOME, not the user's configuration.

After exposing 1.1.0 and 2.0.0-beta.1, actual report rows were:

| Package | Current | Wanted | Latest |
| --- | --- | --- | --- |
| `operations/exact` | 1.0.0 | 1.0.0 | 2.0.0-beta.1 |
| `operations/other` | 1.0.0 | 1.1.0 | 2.0.0-beta.1 |
| `operations/range` | 1.0.0 | 1.1.0 | 2.0.0-beta.1 |

Each row said `registry: fixture (outside constraint)`. Row-level
assertions, not just substring presence elsewhere in the table, passed.
The exact-pin preview said:

```text
All dependencies already at their latest matching refs.
```

Outdated and preview preserved complete project hashes **and mtimes**.
Changing only the exact dependency selector to 1.1.0 then running ordinary
install advanced that locked result and passed CI audit. No selected-update
cache regression was suppressed or claimed fixed.

Two additional input distinctions were deliberately **not reused**:

- `ts`: the retained local-instruction output tree was copied and a legacy
  `generated_at: '2026-07-02T00:00:00Z'` field seeded only in its scratch
  lock. The new restore preserved its complete lock bytes. This is not
  hand-authored production lock metadata or a recommendation to add it.
- `gr`: the pinned-skill manifest received an explicit registry/default
  mapping in scratch. Real Git install/audit succeeded with **zero**
  registry requests and the same complete canonical Git lock. This proves
  explicit `git:` routing for that new input, rather than transferring a
  no-registry fixture PASS to a different configuration.

## Source-only boundaries, skips, and fixes

Frozen-source receipts in `Wave/source-contracts.json` identify commit
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`. They substantiate the full-graph
unchanged-Git contract, source-specific lock fields, experimental client/API,
and OpenAPM v0.1 Working Draft's deferral of a normative registry wire
contract. The single-skill run is not presented as a new moving-transitive
experiment. A compatible loopback server is not evidence of a
Microsoft-operated public searchable service. Publication/server-side
authorization and other-project fingerprints were not freshly tested;
the latter remain explicitly July 2026 research.

Audit results are baseline integrity/content results, **not proof of
org-policy enforcement, publisher authentication, or MCP/runtime safety**.
The native/MCP/policy limitations in the supplied references remain
limitations, not implicit guarantees under this PASS.

**SKIPPED-needs-network: none among the changed executable examples.**
Public Git and the isolated registry were actually executed. Historical
code and unclaimed live publication/runtime/private-policy operations are
out of scope, not relabeled as new-version tests or network skips.

All source, fixture, and protected-file hashes were unchanged at the
native-evidence finalization check (`2026-09-16T01:57:51Z`). A subsequent
TOC-only concurrent change does not alter these inputs; see the
[handoff note](ch01-verification.md#artifacts-and-handoff).
Raw commands, exits, complete output bytes, generated locks,
input/mutation inventories, and snapshots are under `Wave`; prior evidence
was read-only.

**Minimal fixes applied: none. Mandatory Chapter 2 corrections: none.**
Reviewer acceptance remains separate from this source-specific PASS.
