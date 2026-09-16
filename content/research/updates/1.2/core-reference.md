# Edition 1.2 core reference: APM 0.31.0

**Audience:** chapter-author and code-verifier. **Scope:** Chapters 1-5, with
Chapter 5 investigated first. This is empirical reference research, not chapter
content or a publication verdict.

**Frozen baseline:** book 1.1 / APM 0.23.1. **Inspected executable:** exactly
stable **0.31.0**. All ten intervening releases were read. The existing chapters,
historical research, edition metadata, TOC, changelog, site, and root APM
manifest/lockfile were not changed by this task.

The three new reusable fixtures each completed real `install`, bare restore,
`install --frozen`, and `audit --ci` commands with exit **0**. Their lockfiles
are unedited CLI output. These are **explorer observations**, not PASS/ACCEPT
verdicts on behalf of another agent. Native Agent Plugin installation also
worked, but its local-path CI audit has a reproducible failure described below;
that case is deliberately not exported as a green book fixture.

## Shared executable and provenance

Use this absolute executable across the update; do not resolve `apm` from PATH:

```powershell
$Apm = '<absolute RunRoot>\apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
# exit 0
```

| Item | Recorded value |
| --- | --- |
| Platform | Microsoft Windows 10.0.26200; OS/process architecture X64 |
| Release | [microsoft/apm v0.31.0][RELEASE], published 2026-09-15T17:48:53Z; neither draft nor prerelease |
| Official asset | `apm-windows-x86_64.zip`, 19,744,125 bytes |
| Archive SHA-256 | `a5b2b46378f560b3a2c4ff0c8a5e027cb851c5220ca8a31f9a44f9667ddb0f01` |
| Executable SHA-256 | `0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2` |
| Source checkout | Official tag, commit `8fd10ac5eafee7ca77d41cc34ba139d812fdacd5` |
| Book checkout inspected | `556f581abfb68a4ed4b9d6070e848d37330e3297` |

The expected executable was absent. The matching publisher `.sha256` sidecar
was downloaded afresh and checked against the ZIP **before extraction or
execution**. GitHub's release-asset digest independently matched it. An
authenticated `gh` metadata request returned SAML HTTP 403; the public
anonymous GitHub API supplied the stable-release metadata. No credentials,
package-index settings, TLS policy, PATH, or global CLI installation were
changed. The unsuccessful pip approach from the preceding task was not retried.

### Evidence locations

The session artifact root, called **RunRoot** below, is:

```text
<session artifacts directory>\book-v1.2
```

| Artifact relative to RunRoot | Purpose |
| --- | --- |
| `apm-native\provenance.json`, `version.txt`, `help.txt` | Binary provenance, exact banner, top-level help |
| `source\release.json`, `source\commit.txt`, `source\apm-0.31.0` | Stable-release metadata and frozen official source/docs |
| `upstream.json`, `upstream-notes.txt` | Original ten-release discovery result and readable release bodies |
| `core-probes\help` | Initial per-command help and exit codes |
| `core-probes\logs\<id>.json` and `<id>.txt` | Exact absolute command, argv, actual CWD, exit code, stdout/stderr, timing, and file-hash inventories |
| `core-probes\command-index.csv`, `summary.json` | Index and aggregate of the raw invocations |
| `core-probes\projects` | Preserved synthetic source fixtures and exact exported-example inputs |
| `core-probes\materialized` | Preserved short-path output trees, including real generated locks/configs |
| `core-probes\historical-core-blocks.json`, `old-core-claims.json` | Exact old code blocks, source hashes, and claim line anchors |
| `core-probes\fixtures.json`, `source-provenance.json` | Reusable-fixture commands/hashes and pinned-source hashes |
| `core-probes\probe-tools.ps1`, `assertions.jsonl`, `runtime-layout.json` | Probe harness, explicit assertions, and Windows-path adaptation |

For compactness, commands in tables use `apm` as a label. **Every actual APM
invocation used the absolute executable above.** Consult the corresponding
JSON for full arguments and working directory, including `--root` where used.
Raw failed attempts are retained, not rewritten into successful transcripts.

### Isolation and Windows limitations

The long requested artifact path produced native resolution-staging failures:
`WinError 3` at a 269-character staging directory, then `WinError 206` in a
shorter variant. Existing 8.3 aliases and extended-length spelling did not
solve APM's subsequent canonicalization. No Windows setting was changed.

Sources/logs stayed under `core-probes`. Ordinary materialization first used
the documented `--root` option with the uniquely owned temporary root
`%TEMP%\apmc-2d4facdd`. Some APM 0.31.0 paths do not
honor source redirection consistently: positional relative-package validation,
direct `--mcp` manifest lookup, and nested local dependencies failed under that
arrangement. Exact copies in short **normal working-directory mirrors**
succeeded. The final three exported fixtures were all checked using that
normal-CWD arrangement, not a modified CLI.

`USERPROFILE`, `HOME`, application-data/config directories, APM cache/home,
and temporary paths were redirected in child processes to owned scratch
locations. No global installs or persistent user configuration commands were
run. Native commands sharing this isolated APM home serialize on APM's
lifecycle lock; do not infer performance from their wall-clock durations.
Short temporary trees are preserved under `materialized` before targeted
cleanup; the shared executable and durable source/log artifacts remain.

## Concept anchors

Use the [edition 1.2 theory brief](theory.md), especially declaration authority,
materialization/reconciliation, reproducibility without timestamp churn,
scoped trust, and distribution-format boundaries. Historical concept briefs
remain useful with their original evidence:

| Chapter | Concept implemented by the features below |
| --- | --- |
| [1](../../01-the-context-problem-theory.md) | Shared context as a dependency; portability, reproducibility, provenance/security, governance |
| [2](../../02-lessons-from-package-managers-theory.md) | Declared intent versus resolved state; source identity and pinning |
| [3](../../03-primitives-and-harnesses-theory.md) | Primitive versus package versus harness; standards and bounded projection |
| [4](../../04-the-manifest-apm-yml-theory.md) | Reviewable manifest authority; local versus external sources |
| [5](../../05-install-and-restore-theory.md) | Materialization; add versus restore; explicit target selection |

## 1. Init and consented onboarding

**Commands:** `init`, `init --discover`, `init --discover --apply`.
**Implements:** Ch4 declared intent; Ch5 materialization and consent.
**Inspected version:** 0.31.0.

Plain `apm init --yes` in an empty directory still creates only `apm.yml`.
The scaffold has name, version `1.0.0`, description, author, commented target
examples, empty `dependencies.apm`/`dependencies.mcp`, `includes: auto`, and
`scripts: {}`. The isolated environment produced `author: Developer`; normal
Git author discovery remains documented. It creates no `.apm`, lockfile,
policy, or harness deployment. `init --yes --target copilot,claude,cursor`
writes an explicit target list. [INIT]

**New in this gap:** discovery inventories admissible existing skill/package
directories in recognized native layouts. It is not a rules-to-skills converter
and is not an install. A source at
`.claude\skills\checkout-review\SKILL.md` was supported; the loose native rule
`.claude\rules\manual-rule.md` was reported as unsupported and preserved.

| Probe ID | Command | Exit | Exact boundary observed |
| --- | --- | --- | --- |
| `ch5-discover` | `init --discover --format json` | 0 | No project writes; supported package plus unsupported loose rule |
| `ch5-discover-no-consent` | `init --discover --apply` in noninteractive mode | 1 | No writes; consent required |
| `ch5-discover-apply` | `init --discover --apply --yes --format json` | 0 | Only `apm.yml` added; no source move, translation, `.apm` copy, lock, or deploy |
| `ch5-discover-idempotent` | Same apply again | 0 | Byte-stable; no duplicate reference |
| `ch5-discover-target-conflict` | `init --discover --target copilot` | 2 | Invalid combination; target selection belongs to later install |
| `ch5-discover-self-dependency` | Apply to a root skill that contains the consumer | 1 | `unsafe`; no self-dependency or manifest write |
| `ch5-discover-managed` | Discovery after a pinned-target install | 0 | Source `already-declared`; output `managed`; loose rule still `unsupported` |

The JSON contract observed is:
`scope`, `root`, `manifest`, `findings`, `additions`, `applied`.
Each finding has `path`, `kind`, `status`, `reason`, and `dependency`.
All five documented statuses were encountered: `supported`,
`already-declared`, `managed`, `unsupported`, `unsafe`.

The newly created consumer manifest was genuinely minimal:

```yaml
name: onboarded-project
version: 1.0.0
dependencies:
  apm:
    - path: ./.claude/skills/checkout-review
```

It does **not** automatically pin targets or add the full plain-init scaffold.
For a shared project, deliberately pin targets before treating this as a
reproducible onboarding recipe. An initial one-off `--target copilot` install
followed by audit with no pinned target produced Claude drift in this source
layout. Pinning `targets: [copilot]` made normal install and CI audit succeed.

**Use:** bring an existing package under manifest management without moving
it. **Do not use:** automatic conversion of arbitrary instructions, hooks,
MCP configs, or all loose files. Plain `init --yes` can overwrite an existing
manifest; discovery/apply is the merge workflow. `--write` is the documented
alias of `--apply`; that alias was inspected in help, not separately executed.

**Reusable minimal example:** `backend\examples\updates\1.2\core\onboard-skill`.
For the pre-apply state and consent failures, use `core-probes\projects\onboard`
and the discovery logs; the exported fixture represents the pinned,
already-declared end state.

## 2. Add, restore, frozen install, and the real lockfile

**Commands:** `install <package>`, `install`, `install --frozen`, `audit --ci`.
**Implements:** Ch2 intent/result separation; Ch5 materialization and replay.
**Inspected version:** 0.31.0.

The ordinary add/restore distinction survives. A positional local add really
grew `dependencies.apm`; a later bare install read the declaration.
`ch5-add-normal-cwd` also demonstrated the v0.24 comment-preserving APM
dependency writer: the leading comment, blank line, and authored target-list
style survived. Do not retain Ch5's blanket claim that every add reserializes
and loses that formatting. However, a **direct MCP add still reserialized**
the separate `mcp` probe manifest and removed its comment; do not extrapolate
APM dependency-write preservation to every mutation path. [INSTALL] [WRITER]

`--target` on an existing manifest was not persisted. With an existing
`[copilot, claude]` declaration, an add targeting only Copilot was followed by
a bare restore that also deployed to Claude. The next bare restore was
byte-stable. Conversely, `ch5-install-bootstrap-targets` started with **no
manifest**: `install .\pkg --target copilot` created `apm.yml` and explicitly
reported `Targets set: copilot (persisted to apm.yml)`.

### Minimal public dependency, pinned before installation

`ch2-public-versions` successfully ran the old Ch2 command:

```text
apm view microsoft/apm-sample-package versions
v1.0.0  tag  fb285168
```

The new public fixture selects only that package's `style-checker` skill at
the immutable full commit. It avoids the full sample package's floating
transitive dependency and has no additional dependencies:

```yaml
# One public skill, immutable source identity.
dependencies:
  apm:
    - git: microsoft/apm-sample-package
      ref: fb2851683be0e0e7711421d518bd8dba23b0b1f6
      path: .apm/skills/style-checker
```

The real 0.31.0 lock records `package_type: claude_skill`,
`virtual_path: .apm/skills/style-checker`, the exact commit/ref above, and:

```text
content_hash: sha256:867912713bf45048211440b81ea0ced396ad0a0993447dd540fe5c219722d318
deployed SKILL.md: sha256:1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829
```

The skill's version is legitimately `unknown`; that does not erase its
immutable Git commit. Copilot/Cursor share `.agents\skills\style-checker`;
Claude uses `.claude\skills\style-checker`.

| Probe IDs | Outcome |
| --- | --- |
| `ch5-public-declared-git` | Declared Git install, exit 0 |
| `ch5-public-git-restore`, `ch5-public-git-frozen` | Warm replay, both exit 0; unchanged lock bytes |
| `ch5-public-git-audit` | CI audit, exit 0 |
| `ch5-public-git-cold-frozen` | Only manifest/lock copied, separate initially empty APM cache; exit 0, unchanged lock bytes, real package hydration |
| `git-cache-line-endings.json` | The resulting Git checkout's local `core.autocrlf` is `false` |

The positional tag/subdirectory add was bounded and stopped after 300 seconds
in package validation. It is **not** a successful transcript. The declared
Git/full-SHA path above subsequently succeeded against the real public
repository, without TLS/index changes or a mocked downloader.

### Replace the old timestamp proof

New locks omit `generated_at`. They also contain canonical `deployments`
ownership records in addition to compatible per-dependency/local deployed-file
fields. The local-only instruction lock did not carry `apm_version`, whereas
the package and MCP locks did; do not invent a uniform top-level field set.
Compare actual bytes/hashes, not a timestamp. Warm public/local restores and
the cold public frozen restore were byte-stable. [LOCK]

The old Ch5 assertion that restore never prints a no-op message is obsolete:
the public and local-only probes printed
`No changes -- install state already up to date`. Local-path package probes
can still print `Installed 1 APM dependency` on an unchanged replay; neither
wording nor the dependency counter is a universal oracle.

**Use:** ordinary install to reconcile declared state; frozen install for a
structural lock/manifest gate; audit for on-disk integrity. **Do not use:**
bare install as an unconditional promise that edited manifests, local sources,
or a missing lock cannot cause new resolution. Unchanged Git dependencies
reuse the locked graph, including transitive manifests; deliberate graph
refresh belongs to update/lock-update. That full-graph contract is
source-grounded here, not a newly executed moving-upstream experiment. [LOCK]

**Reusable examples:** `core\local-instruction` and `core\pinned-skill` under
the backend update-example directory. A local path is not a Git version pin:
its source must travel with the repository and remain available.

## 3. Target selection: distinguish error, skip, and successful work

**Surface:** `targets`, `targets:`, `--target`, legacy `--runtime`.
**Implements:** Ch3 bounded portability; Ch4/5 explicit deployment authority.
**Inspected version:** 0.31.0.

Help/source define precedence as CLI target/runtime selection, manifest
targets, saved configuration, then filesystem detection. The CLI-over-manifest
and manifest/auto-detection cases were run; saved user-default mutation was
intentionally not tested. [INSTALL] [TARGET-CATALOG]

| Actual scenario | Exit | Evidence |
| --- | --- | --- |
| No target, local instruction present | 2 | `ch5-no-target`: no files written, no AGENTS.md fallback |
| No target, direct self-defined MCP add | 2 | `ch5-mcp-no-target`: no manifest/config mutation; replaces the old Ch1 skip-with-success caveat |
| Empty scaffold, dry-run, no work | 0 | `ch1-empty-dry-run` |
| Ambiguous Claude and Cursor markers | 2 | `ch5-ambiguous-targets` |
| Unknown CLI target / empty manifest target list | 2 | `ch5-unknown-target`, `ch4-empty-targets` |
| Missing lock under frozen install | 1 | `ch5-frozen-missing-lock`, no project changes |
| Manifest `targets: [all, claude]`, no markers | 2 | `ch4-legacy-manifest-all`: warning; whole field treated as omitted, including the sibling |
| Disabled `grok-cloud`, local instruction-only input | 0 | `ch3-experimental-target-disabled`: enable-feature hint, no deploy/lock, `.gitignore` added |
| Only an Agent Plugins v1 package, target Codex | 1 | `ch5-plugin-excluded`, no committed install state |
| Same native plugin plus an ordinary skill, target Codex | 0 | `ch5-plugin-mixed-skip`: ordinary skill deployed, plugin skipped with recovery guidance |
| Target-excluded native plugin, dry-run | 0 | `ch5-plugin-excluded-dry-run`; not proof a real install can succeed |
| Legacy plugin explicitly declaring `skills: []` | 0 | `ch3-plugin-empty-declaration`: no skills, named diagnostic |
| Missing declared plugin component / invalid CLI skill name | 1 | `ch3-plugin-missing-declaration`, `ch4-invalid-cli-skill-selection`; no new lock activation |

The native-plugin all-skipped failure is **specific**, not a blanket
"every zero-deploy is exit 1" rule. A successful exit can contain explicit
skips; a preview can succeed while the real operation fails.

### Catalog corrections

`init --yes --target all` persisted **nine** default stable targets:
`claude`, `codex`, `copilot`, `cursor`, `gemini`, `grok-build`, `kiro`,
`opencode`, `windsurf`. Retire the fixed "eight" count in Ch3 and old notes.
`agent-skills`, `antigravity`, and `hermes` are explicit-only additions;
IntelliJ-specific integration is MCP-only, with file primitives using Copilot's
profile. Experimental targets are excluded from `all`. IntelliJ and the
unexecuted target profiles are help/source evidence, not live integration
claims. [TARGET-CATALOG] [TARGET-MATRIX]

`apm targets --json` is useful **filesystem inventory**, not proof that the
manifest's target set was selected: before deployment, the pilot's three
manifest targets appeared inactive in that inventory. The install itself
reported the authoritative `Targets: ... (source: apm.yml)`.

### Target contraction and ownership

The unconfounded APM-package case `ch5-manifest-target-contraction` changed the
manifest from four targets to Copilot and ran ordinary install. Non-Copilot
managed outputs were removed and the surviving Copilot outputs retained;
the new lock is also saved as `snapshots\manifest-contraction.lock.yaml`.
Do not substitute the earlier `ch5-target-contraction` flag-only probe for
this proof: it used a skill-collection shape and retained non-Copilot files.
Pin and review the manifest for durable target changes. [INSTALL]

**Use:** explicit manifest targets for shared/CI workflows; a flag for a
one-invocation selection; inventory to diagnose signals. **Do not use:** `all`
in a new manifest, an exit code alone to claim universal capability deployment,
or a selected file-profile alias to infer MCP configuration identity.

**Minimal examples:** the three exported fixtures all pin targets. Negative
cases remain in `projects\target-*`, `portable`, `mixed`, and their named logs.

## 4. Manifest authority, source layouts, and component declarations

**Surface:** eligible `apm.yml`, `plugin.json`, `dependencies.apm` object entries,
`includes`, `license`.
**Implements:** Ch3 package/primitive distinction; Ch4 reviewable declaration
authority. **Inspected version:** 0.31.0.

An eligible APM manifest plus `.apm` wins over a co-located plugin marker.
`ch4-apm-over-plugin` locked the dependency as `apm_package`, deployed its
`.apm` skill/rule/prompt/agent, and did not deploy the plugin-only command.
`ch4-apm-source-control` repeated the APM layout without a plugin marker.
Metadata-only `apm.yml` alongside a plugin, with neither `.apm` nor APM/MCP
dependencies, does not force the APM route; `ch3-legacy-metadata-install`
and its audit both exited 0. [TYPES] [MANIFEST]

**Important experimental control:** the earlier `classify` fixture also
contained `skills\<name>\SKILL.md` at package root. It selected
`skill_bundle`, not `apm_package`. Its primitive projection/classification
warnings are useful, but its name `ch3-apm-declaration-first` must not be
mistaken for isolated APM-versus-plugin precedence evidence. Root skill and
skill-collection signals are real package forms, not disposable extra files.

For legacy plugins, explicit component declarations replace directory
discovery for that component:

| Declaration / request | Observed behavior |
| --- | --- |
| `"skills": ["./skills/kept", "./extra/custom"]` | Only `kept` and off-convention `custom` deployed; `skills\unlisted` did not |
| `"skills": []` | Nothing under the conventional skill directory deployed; diagnostic named the shadowed skills |
| A declared missing skill directory | Install exit 1 before activation |
| Unknown string `$schema` | Warning, then structural legacy-plugin classification; not automatic rejection |
| `--skill not-declared` | Exit 1; available names were `custom, kept`, not the undeclared directory |
| Local `path:` entry with `alias`, `targets: [claude]`, `skills: [kept]` | Alias appeared during resolution; only Claude's `kept` skill deployed |

Evidence: `ch3-plugin-legacy-declarations`, `ch3-plugin-empty-declaration`,
`ch3-plugin-missing-declaration`, `ch4-invalid-cli-skill-selection`,
`ch4-path-options`. An omitted plugin component key permits conventional
discovery; the empty and explicit-list forms are not equivalent to omission.
The omitted-key rule is also explicit in the pinned package-type reference.

`includes: [one instruction]` still did **not** filter `install`: an unlisted
second `.apm` instruction deployed too, producing six native rules across the
three pilot targets (`ch4-includes-not-install-filter`). Preserve that old
install caveat, but qualify it by operation: `includes` records deployment
consent and is an exhaustive allowlist for **plugin packing**, a Ch10
source-grounded distinction not exercised with pack in this core task.
It does not choose between `.apm` and plugin-native source layouts. [MANIFEST]

`license` is valid optional metadata, although plain init does not generate
it. The local package with `license: MIT` installed and audited successfully.
Replace Ch4's "there is no license key" heading, rather than turning scaffold
minimality into a schema prohibition.

**Use:** explicit plugin components and dependency skill/target subsets when
you mean a restriction; keep the introductory `.apm` manifest simple.
**Do not use:** `includes` as an install filter, a filename as the sole type
oracle, or `apm.yml` absence to reject every installable package.

**Minimal reference inputs:** `projects\legacy-metadata`,
`projects\path-options`, `projects\apm-over-plugin`; reusable local-source
manifest: `core\local-instruction`.

## 5. Portable Agent Plugins are not flattened legacy plugins

**Surface:** root `plugin.json` declaring
`https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.
**Implements:** Ch3 distribution format versus primitive; bounded portability.
**Inspected version:** 0.31.0.

For the Copilot target, the native fixture stayed whole under
`apm_modules\_local\pkg`. APM wrote:

```text
apm_modules\.github\plugin\marketplace.json
apm_modules\.github\plugin\apm-registration.json
.github\copilot\settings.local.json
```

The settings projection referenced the repository-relative `apm_modules`
directory and enabled `checkout-plugin@apm`. No loose
`.agents\skills\retry\SKILL.md` duplicate was created. Restore succeeded too.
Evidence: `ch3-plugin-native`, `ch3-plugin-native-restore`.

This differs from the legacy plugin's per-primitive projection. The pinned
docs require stable **Copilot CLI >=1.0.81 to load** the native registration;
APM does not locate or execute Copilot to materialize/register it. Runtime
loading was **not executed** in this task. The docs' merge-only behavior for
unrelated pre-existing settings is source-grounded, not a collision test
performed here. [NATIVE]

For non-Copilot targets, use the explicit fail/skip distinctions in section 3.
The actual recovery hint offered a plain skill subpath, for example
`apm install ./pkg/skills/retry --target codex`, rather than silently
decomposing the recognized Agent Plugin.

### CI-audit limitation: retain the failure

The local-path native plugin installed successfully, but `audit --ci` failed:

```text
Native Agent Plugin canonical IR is missing, so deployment was blocked.
```

The original plugin-only fixture also hit `config-consistency` because
`pkg\apm.yml` was absent. Adding a legitimate metadata-only `apm.yml` removed
that consistency complaint **without changing native classification**, but
the drift-replay failure remained in a normal short CWD:
`ch3-portable-metadata-install` exit 0,
`ch3-portable-metadata-audit` exit 1.

This is an observed 0.31.0 local-path limitation, **not a network skip**.
Do not add `--no-drift`/`--no-policy`, hand-edit the lock, claim a verifier
PASS, or extrapolate it to every Git-sourced plugin. The legacy metadata-only
control audited successfully. Keep the native case as research evidence until
the verifier/author explicitly handles this limitation.

**Use:** whole-unit registration for supported Agent-Plugin-aware runtimes.
**Do not use:** as proof all harnesses can load every plugin or as an
audit-clean sample based only on install exit 0.

**Minimal input:** `projects\portable` (root plugin manifest, one skill,
empty valid `mcp.json`); mitigation/control input: `projects\portable-metadata`.
Both have preserved real materialization/lockfiles in the artifact mirrors,
but neither is exported as a green chapter example.

## 6. MCP integration is target-specific and depth-aware

**Surface:** `dependencies.mcp`, `install --mcp`, explicit runtime targets.
**Implements:** Ch3 connection versus execution; Ch4 typed declaration;
Ch1/5 bounded trust and materialization. **Inspected version:** 0.31.0.

Self-defined MCP still uses a list of objects, not a name-to-object mapping.
Registry references are another supported entry form; "all MCP entries must
be objects" is broader than the schema. All live configuration probes used an
intentionally nonexistent command and public dummy values. APM configured
files without starting that command or an agent runtime. [MANIFEST]

`ch3-mcp-separate-targets` explicitly selected
`copilot,vscode,claude,kiro,codex`. One identical manifest entry produced:

| Target | Actual project output | Dummy environment value in native config |
| --- | --- | --- |
| Copilot CLI | `.github\mcp.json`, `mcpServers` | `${CORE_MCP_VALUE}` |
| VS Code | `.vscode\mcp.json`, `servers` | `${env:CORE_MCP_VALUE}` |
| Claude Code | `.mcp.json`, `mcpServers` | Resolved literal `book-fixture-public-value` |
| Kiro | `.kiro\settings\mcp.json`, `mcpServers` | `${CORE_MCP_VALUE}` |
| Codex | `.codex\config.toml`, `mcp_servers` | Resolved literal `book-fixture-public-value` |

Thus the old `vscode -> copilot, no separate .vscode output` statement must
be restricted to **file primitives**, not MCP. The manifest placeholder
remained unchanged in this file-authored case, the lock recorded all five
runtime ownership entries, and repeating the identical target selection left
the lock/config bytes unchanged (`ch3-mcp-target-map-stable`).

The MCP-only case wrote a genuine lock with `dependencies: []`,
`mcp_servers`, `mcp_configs`, `mcp_target_servers`, and URI deployment records.
Its bare restore, frozen install, and CI audit all exited 0
(`ch3-mcp-restore`, `ch3-mcp-frozen`, `ch3-mcp-only-audit`).

**Secret-handling caution, proven using a non-secret:** direct
`--env 'VALUE=${CORE_MCP_VALUE}'` resolved the supplied variable into the
consumer manifest and lock. Copilot's native config then referenced
`${VALUE}` and warned it was unset. Do not infer "no plaintext anywhere"
from a placeholder in one generated runtime file. The file-authored
same-name placeholder experiment above is the cleaner reference input.

### Direct versus transitive self-defined MCP

| Probe | Exit | Observed trust boundary |
| --- | --- | --- |
| `ch3-direct-package-mcp-trusted` | 0 | A direct dependency's self-defined MCP was trusted and configured; diagnostic explicitly named direct-dependency trust |
| `ch3-nested-mcp-normal-cwd` | 0 | Depth-two self-defined MCP withheld with re-declaration guidance; ordinary skills still installed |
| `ch3-transitive-mcp-redeclared` | 0 | Consumer re-declaration configured the named server; the transitive-candidate warning still appeared |

The child's `devDependencies.mcp` server was not deployed. Root/direct and
depth-two sources must not be collapsed into "every dependency-provided MCP
server is blocked." Neither a warning nor successful package installation
alone proves the connection's final state; inspect the config and lock.
[MCP-VIEW]

Self-defined MCP configuration was **not intrinsically network-free** in this
binary: conflict detection attempts a registry identity lookup even with
synthetic server metadata. The initial public-registry attempt was stopped
at 180 seconds. Local config probes therefore explicitly used the process-only
`MCP_REGISTRY_URL=https://127.0.0.1:9` with two-second connect/read bounds.
Connection failure falls through the CLI's own canonical-name comparison;
no server was served, TLS verification was not disabled, and the override
warning is in the logs. This is a configuration probe, not proof the public
MCP registry or a real MCP server is available. [MCP-CONFLICT]

**Use:** explicit declarations and target lists to configure known connections.
**Do not use:** install success as a runtime health check, an MCP file-profile
alias as a promise of identical config locations, or a direct-dependency trust
result as proof of transitive approval.

**Minimal inputs:** `projects\mcp-file`, `projects\nested`,
`projects\nested-redeclared`. They remain artifacts, not real server examples
recommended for end users.

## 7. Instructions, agents, and explicit compilation

**Surface:** `.apm` primitives, instruction frontmatter, `compile`.
**Implements:** Ch3 same intent/different native bytes; Ch4 single authored
source; Ch5 complete materialization. **Inspected version:** 0.31.0.

The exact Ch4 instruction body was rerun against the target CLI. It still
projects to Copilot `.instructions.md`, Claude `.md` rules with `paths`,
and Cursor `.mdc` rules with `globs`. Claude drops the description; Cursor
keeps it, now quoted in the observed serializer. The old local Cursor hash
must not be carried forward as a 0.31.0 constant.

An `applyTo` list remained a list in Claude `paths` and Cursor `globs`.
Prompts still project to Claude/Cursor commands, dropping unsupported `mode`
with warnings. Kiro now received `.kiro\agents\reviewer.md` in the live
four-target probe. Markdown with document-only frontmatter and non-Markdown
assets under the agent source directory were explicitly diagnosed and not
deployed as agents. A valid agent in the same directory still deployed.
Malformed instruction YAML caused install exit 1 with no activated output
(`ch4-malformed-instruction`). [CLASSIFY] [TARGET-MATRIX]

Do not call this "all `.md` files in a recognized directory are agents":
declaration/classification matters as well as location.

`install` is still not a substitute for root-context compilation:

| Probe | Result |
| --- | --- |
| `ch5-compile-only-install` | A root local instruction targeting Codex: exit 0, only `.gitignore` added; no AGENTS.md and no lockfile |
| `ch3-explicit-compile` | Subsequent explicit compile: exit 0, AGENTS.md generated; unmatched glob fell back to project-root placement |
| `ch5-dependency-compile-hint` | Dependency instructions targeting Codex: install emitted `Run 'apm compile' to update AGENTS.md` |
| `ch3-handwritten-root-preserved` | Compile retained an existing hand-authored, unmarked root AGENTS.md byte-for-byte and warned |

Consequently, both "every successful install writes a lock" and "install alone
loads instructions for every target" need qualification. The pinned matrix
also names Gemini, OpenCode, and Hermes as post-install compilation targets;
those additional profiles were not materialized here. [TARGET-MATRIX]

**Use:** install for the pilot's native per-file rules; compile when the target
needs aggregate/root context. **Do not use:** default compile as permission to
overwrite a human-owned root file, or cross-harness byte equality as the
definition of portability.

**Reusable minimal example:** `core\local-instruction`; negative/advanced
inputs: `projects\compile-only`, `root-preserve`, `malformed-instruction`.

## 8. Script execution remains optional and experimental

**Commands:** `list`, `preview`, `run`.
**Implements:** Ch5 named workflow versus materialization/runtime boundary.
**Inspected version:** 0.31.0.

`ch5-scripts-list` showed the declared script map. `preview review` compiled
the prompt to `.apm\compiled\review.txt`, stripped frontmatter, and displayed
the compiled command as `copilot`, without invoking Copilot. A deliberately
missing command under `run broken` exited 1. `run echo` printed
`CORE_SCRIPT_OK` and exited 0.

The CLI still marks `run` experimental. It executes the command a script
names; a script that names a harness needs that harness, but an ordinary shell
script does not require an AI runtime. The old real Copilot execution,
latency, and billing transcript remain **0.23.1-only** evidence and were not
re-executed or relabeled.

**Use:** preview to inspect prompt compilation without runtime cost; run for
an intentionally supplied command. **Do not use:** a successful preview to
certify agent execution or assume every script is a harness invocation.
**Minimal input:** `projects\scripts`; all four commands have named raw logs.

## 9. Ch1/2 corrections that should not become a feature tour

The context-as-dependency problem, six package-manager fundamentals, and
book's four-properties/three-promises mapping remain the right conceptual
frame. The identity is still Microsoft's `apm-cli` / `microsoft/apm`, but
Python/pip is not the sole installation route. The inspected release's docs
cover Homebrew core, Windows package managers, and checksum-verified native
assets. Only the isolated native path was executed here. [INSTALLATION]

"The registry HTTP API is still only future plumbing" is no longer adequate
CLI guidance. REST-based package registries and their HTTP API are shipped
**behind the experimental registries flag**. `ch2-registry-flag-required`
proved that an unenabled `registries:` block fails with exit 1, not silent Git
fallback. Registry install/publish against a real backend was not run; this
does not establish an official hosted central public registry. Prefer
"Git is the default and needs no central registry; REST registries are an
explicit experimental option." [REGISTRIES]

`view`, `outdated`, `update`, and `audit` help were captured; only view and the
relevant audits were executed. Preserve the distinction between built-in
Unicode/integrity checks and a CVE feed. Private-registry Latest/Wanted
semantics and actual update planning belong to the later lifecycle wave.

For Ch1's policy-location preview, 0.31.0 help now names GitHub's
`.github-private` before `.github`, `.apm`, `_apm`, and ADO's `apm/apm-policy`
before its legacy fallback. Those are inspected help/source contracts, not
live organization-policy discovery. Defer detailed governance to Ch9.

Replace "scanning before anything touches disk" with "before agent-readable
deployment": acquisition/staging and cache writes are distinct from activation.
Keep APM's install/integrity plane separate from inference-time behavior;
do not inflate that into "APM never executes commands" when scripts and
separate lifecycle features exist.

## Release-by-release core impact

This table accounts for the complete frozen gap at core-chapter scope.
The original release bodies remain in `upstream.json`; the edition-wide
theory/impact work is separate. Source and help claims below are not mislabeled
as live tests of private infrastructure or later-chapter examples. [CHANGELOG]

| Release | Core disposition |
| --- | --- |
| 0.24.0 | Recheck APM manifest comments, local path `targets`/`skills`/`alias`, stdio environment handling, and locked replay. All received focused probes above. Hook event/combined-manifest routing, Antigravity trigger details, and pack attestation are later-wave source impacts, not new core worked examples. |
| 0.24.1 | Local transitive identity, virtual recursion, casing, and MCP/dev state inform graph and connection boundaries. Nested local/direct-MCP cases were run. Private host, marketplace transport, global Claude config, and update-specific LSP/MCP repairs stay out of this core execution scope. |
| 0.25.0 | Correct policy-candidate preview and target/ownership discussion. `.apm` versus plugin layout receives controlled target-version probes. Dashboard, prune internals, marketplace transport, and policy enforcement are not core chapter operations. |
| 0.26.0 | Retire fixed no-op/output assumptions; inspect explicit compilation hints, target contraction, local skill filters, synthetic metadata/lock normalization, and OS-trust-store installation guidance. Public Git restore/cache behavior was run; no TLS settings were changed. Deep hook cleanup, private auth, policy-cache, and mutation/CI work are deferred or internal. |
| 0.27.0 | MCP-only locks, exact MCP target ownership, preserved mappings, and exclusion of dependency dev-MCP directly affect core promises and were probed. Registry/container launch details, global targets, marketplace semver, and advanced auditing remain later-wave material. |
| 0.28.0 | Kiro agents and list-valued instruction globs were materialized; disabled Grok Cloud selection was observed. Registry object forms and alias-refresh semantics are source handoffs, not independently exercised registry/update scenarios. |
| 0.29.0 | Major Ch3/5 change: native Agent Plugins, exhaustive legacy skill declarations, and Copilot/VS Code MCP separation. These have real positive/negative probes. Native binary provenance and noninteractive bin-consent help were inspected; executable deployment, pack output, and signed-installer behavior were not separately tested. |
| 0.29.1 | Update manifest/layout authority, declaration-first agent filtering, truthful outcomes, preserved root context, omitted new-lock timestamps, and MCP configuration boundaries. Relevant cases were rerun; plugin CI-audit limitations were retained rather than hidden. Global lifecycle, publishing/pack, private hosts, and LSP-specific fixes stay with later chapters. |
| 0.30.0 | Setup/provenance guidance changes: package-manager ownership and checksum-verifying installers. No new daily consumer verb is required. Cache maintenance and uninstall error reporting are Ch7+, not core examples. |
| 0.31.0 | Pilot priority: init discovery/apply and Agent Plugin all-skipped failure versus mixed/preview success. Cold Git restore and `core.autocrlf=false` were checked. Manifestless Git collection subset support is source-grounded, not proven by the smaller single-skill fixture. Registry reporting/build metadata and the gh-aw target break belong to later waves. |

Release housekeeping, CI fixtures, dashboards, performance-only refactors, and
contributor-governance changes without a changed core behavioral claim do not
justify additional Ch1-5 commands or a chapter restructure.

## Old claims: author replacement checklist

| Historical anchor | Action for 1.2 |
| --- | --- |
| Ch1/reference: missing-target MCP can skip and return success | Replace with the observed direct-add exit 2/no-mutation case; retain the separate empty-work no-op |
| Ch1/2/5: identical bytes across any harness | Separate locked source identity from target-native projection; qualify by supported primitives and selected targets |
| Ch1/5: before any disk write; every install writes a lock | Distinguish staging from activation; include empty/compile-only exceptions |
| Ch1 policy candidate list | Add the current help-grounded candidates without claiming live organization verification |
| Ch2: registry API only future plumbing | Describe shipped experimental registries; do not invent a hosted central service |
| Ch2: no ref means tomorrow's unchanged locked install must move | Clarify no-lock/fresh-resolution risk versus replay of an unchanged locked graph |
| Ch3: exactly eight default harness targets | Nine in this inspected catalog; prefer named examples and the versioned matrix over a timeless count |
| Ch3/reference: no separate VS Code output | Restrict the alias statement to file primitives; MCP paths are distinct |
| Ch3: every plugin unpacks into the same primitives | Split legacy plugin projection from whole native Agent Plugin registration |
| Ch3: all recognized-directory files deploy | Account for document/asset classification, required declarations, and supported package layouts |
| Ch4: no `license` key | Optional schema field, absent only from the plain-init scaffold |
| Ch4: includes never an allowlist | True for install discovery, false as a blanket statement about packing |
| Ch4: `.apm` is the only authorable/installable source | Keep it as the introductory convention; existing skills/plugins can retain native layouts |
| Ch5: init only creates a new scaffold | Preserve plain init and add the separate discover/apply merge boundary |
| Ch5: `--target` never persists | Existing-manifest override versus install bootstrap and explicit init persistence |
| Ch5: restore timestamp unchanged proves equality | New locks omit it; use genuine lock/deployment hashes and expected output paths |
| Ch5: add always reflows/drops comments | APM dependency writer preserves the tested formatting; direct MCP writer still differs |
| Ch5: exit 0 means all requested context arrived | Explicit skip/unsupported/mixed/preview cases disprove that shortcut |
| Ch5: install alone finishes every target's instruction setup | Native per-file projection versus explicit root-context compilation |
| Ch5: runtime required for every script | Required for a script naming that runtime; safe shell scripts are also supported |

## Reusable fixtures and verifier handoff

All paths below are under `backend\examples\updates\1.2\core`.

| Fixture | Minimal purpose | Observed 0.31.0 commands | Lock SHA-256 |
| --- | --- | --- | --- |
| `local-instruction` | Exact historical instruction body, explicit Copilot/Claude/Cursor targets | install / restore / frozen / CI audit: `0 / 0 / 0 / 0` | `0ae47bad542167d3ec125f13e7db970aafe523c2d14592be85fe209a4b9a1baa` |
| `onboard-skill` | Existing Claude-layout skill referenced locally, explicit Copilot target | install / restore / frozen / CI audit: `0 / 0 / 0 / 0` | `55a83f56b7355cee8b1293a153fb4e674b6e075c4c86caac1578a1da00a86e28` |
| `pinned-skill` | One public skill, exact Git commit, no floating transitive dependency | install / restore / frozen / CI audit: `0 / 0 / 0 / 0` | `6b9ebb9ddcba38e6eddae38ca0c3658c2fabeee90e279857c9159f149ba09507` |

The first two are local. The third needs the public Git source on a genuinely
cold cache; a cold frozen restore was also executed successfully.
`fixtures.json` identifies the exact `fixture-<name>-<operation>` records.
No hand-authored lock metadata or fabricated hashes were added.

Run the verifier in a **fresh, short-path copy** with a separate isolated home
and cache, using the shared absolute executable. Reuse the environment-setup
skill's isolation rules, not the book root or a user's global installation.
The core commands in that copied fixture are:

```powershell
& $Apm install
& $Apm install
& $Apm install --frozen
& $Apm audit --ci
```

Check exit codes, exact expected native paths, and complete lock bytes.
For discovery, start from the preserved pre-apply input, assert JSON shape and
no-write behavior, apply with consent, pin targets, then install. Do not run
plain `init --yes` over an authored fixture as a substitute.

### Verification-stamp inventory

| Historical material | What remains historical versus newly observed |
| --- | --- |
| Ch1 conceptual manifest/anti-pattern | Existing 0.23.1 captions untouched; current empty-init/no-work/target behavior separately observed |
| Ch2 full sample tag-install snippet | Not rerun as that full-package operation; retain historical evidence. `view ... versions` was successfully rerun at 0.31.0 |
| Ch3 unpinned full sample Copilot/Claude installs and plugin scaffold | Not relabeled; current mappings and package formats were tested with controlled local inputs and a pinned single skill |
| Ch4 full worked manifest/instruction | Corresponding instruction body and three-target outcome rerun at 0.31.0 in the new local fixture; old caption/old output hashes remain untouched pending author/verifier work |
| Ch5 full `microsoft/apm-sample-package#v1.0.0` plus old transitive graph | Remains 0.23.1 evidence, including `fb285168`/`a4aebcd4` full-package records and old content hash. The new single-skill lock is a different verified scope |
| Ch5 Copilot execution/time/credits | 0.23.1 only; no paid/live agent execution was performed |
| Ch5 preview/missing-runtime behavior | Newly observed at 0.31.0 with a minimal prompt and inert shell commands, not a reverified real Copilot session |
| New fixtures | Exact 0.31.0 explorer evidence and real locks; independent verifier/reviewer gates still required |

## Focused author recommendations

**Chapter 5 pilot:** keep the four-command consumer loop and Meridian story.
First replace the overloaded restore/exit-code claims, target persistence
absolute, timestamp proof, and comment-loss caveat. Add a compact
discovery -> consented declaration -> install sidebar, not a replacement
daily workflow. Use the local instruction and pinned single-skill fixtures
for controlled materialization/replay evidence. If retaining the original
full-package add transcript, have the verifier rerun that exact graph rather
than substituting the new skill-only result. Treat the native-plugin audit
failure as a named limitation, not a green install/audit example.

**Chapters 1-4:** Ch1 needs bounded portability/security wording and the small
policy-preview correction, not more flags. Ch2 needs the registry-capability
correction, current installation identity/provenance, and precise pin/replay
language. Ch3 needs the legacy/native plugin split, package-layout exceptions,
separate MCP targets, Kiro agents, and a version-aware target catalog.
Ch4's basic scaffold and three-target instruction remain sound; refine
license/includes semantics, demonstrate authoritative local options only
where needed, and connect existing-source onboarding to target pinning.

Unexecuted registry backends, real harness loading, plugin executables,
hooks, policy enforcement, LSP-specific lifecycles, pack/publish, and the
complete historical sample graph remain explicit handoffs, not invented
verification. Do not advance `content\version.yml` or publish from this research.

## Pinned official sources

[RELEASE]: https://github.com/microsoft/apm/releases/tag/v0.31.0
[CHANGELOG]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/CHANGELOG.md
[INIT]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/init.md
[INSTALL]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/install.md
[LOCK]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/lockfile-spec.md
[MANIFEST]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/manifest-schema.md
[TYPES]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/package-types.md
[TARGET-CATALOG]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/core/target_catalog.py
[TARGET-MATRIX]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/targets-matrix.md
[WRITER]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/commands/_apm_yml_writer.py
[CLASSIFY]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/install/primitive_classification.py
[NATIVE]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/consumer/copilot-agent-plugins.md
[MCP-VIEW]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/integration/mcp_config_view.py
[MCP-CONFLICT]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/core/conflict_detector.py
[REGISTRIES]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/guides/registries.md
[INSTALLATION]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/getting-started/installation.md
