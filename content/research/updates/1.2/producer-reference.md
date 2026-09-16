# Edition 1.2 producer, enterprise, and landscape reference

**Scope:** Chapters **10–12 only**. **Frozen range:** book 1.1 / APM **0.23.1**
to exactly stable **0.31.0**. Audience: chapter-author, code-verifier, and the
orchestrator. These are empirical explorer observations and source-grounded
integration contracts, **not** verifier PASS/ACCEPT or publication approval.

Read before authoring: [edition theory](theory.md), [core reference](core-reference.md),
the full supplied `impact.md` and `upstream.json`, the old Ch10–12 fragments,
old Ch10/11 reference caveats, and every existing `backend/examples/ch10` and
`ch11` file. All ten intervening release bodies were read. No historical
chapter, example, verification stamp, root skill manifest/lock, or site/edition
metadata was edited by this task.

## Author-critical conclusions

1. **Keep Meridian's instruction + prompt + skill together.** Its historical
   no-`dependencies` manifest still produces in-tree plugin manifests, not a
   ZIP. A **separate** new fixture with `dependencies: {}` proves local-only
   default-format packing and a real archive-to-consumer round-trip.
2. **Default remains Claude-compatible.** `plugin` is a compatibility alias,
   not Agent Plugins 1.0. Strict `agent-plugin` is opt-in and rejects Meridian's
   commands/instructions before writing. Native registration works; the known
   native CI canonical-IR error is a separate limitation.
3. **Local source and dependency authority differ.** Local packing follows the
   selected source layout and exhaustive `includes`; dependencies supply
   attested deployed files, not arbitrary cache content.
4. **`--check-clean` is genuinely read-only.** Clean, drifted, missing-output,
   override-path, and mixed bundle/marketplace cases preserved project file
   hashes and modification times. Unavailable metadata cannot certify a clean
   catalog; combined strict/clean checks returned **5**, not 4.
5. **Registry implementation exists; a public hosted hub is not established.**
   The experimental client and implementable `/v1` API are shipped. They are
   neither a proxy nor evidence of a Microsoft-operated searchable registry.
6. **CI now supports cold scratch replay.** Clean cold audit passed without
   rewriting the checkout; unreachable source hydration failed closed. Remove
   the old mandatory `--no-drift` setup-only advice.
7. **Do not claim blanket gh-aw/APM 0.31.0 compatibility.** The re-vendored
   shared file requires a concrete target and still defaults to CLI 0.28.0.
   Both pack and restore need the explicit 0.31.0 override. A nonempty public
   instruction passed the Action-shaped CLI pair, but the legacy Copilot
   pack **silently omitted the public shared-path skill**, returning an empty
   archive with exit 0. This is a real compatibility finding, not a network skip.

## Executable, provenance, and evidence

Every APM invocation used this absolute executable; `apm` in tables is only
an abbreviation:

```powershell
$Apm = '<absolute RunRoot>\apm-native\unpacked\apm-windows-x86_64\apm.exe'
& $Apm --version
# Agent Package Manager (APM) CLI version 0.31.0
```

The environment-setup skill's **reuse** path was used, not an installer.
The ZIP SHA-256 was checked again against its publisher sidecar:
`a5b2b46378f560b3a2c4ff0c8a5e027cb851c5220ca8a31f9a44f9667ddb0f01`.
Executable SHA-256:
`0712ec0bab35fbc5ed995641097878641e8ebfa6c6576c64cde0aedba5c095c2`.
Target source HEAD:
`8fd10ac5eafee7ca77d41cc34ba139d812fdacd5`.
Stable release metadata and original checksum acquisition remain in
`apm-native` / `source` and are described in the core reference. [RELEASE]

**RunRoot** is
the session's `<artifacts directory>\book-v1.2`.
This wave's durable evidence is under **`RunRoot\producer-probes`**:

| Artifact | What it records |
| --- | --- |
| `logs/<id>.json`, `.txt` | Absolute command, argv, CWD, exit, stdout/stderr, timing, before/after file hashes and modification times |
| `command-index.csv`, `summary.json` | Complete **131-invocation** CLI index; no timeouts; initial expectation disagreements retained |
| `evidence-assertions.json`, `assertions.jsonl` | Byte/path/read-only assertions; not another role's verdict |
| `fixtures.json`, `bundle-inventories.json` | Exact authored inputs, genuine lock hashes, recomputed bundle payload digests |
| `snapshots`, `archive-repeat.json`, `mutations.json` | Unedited original lock/skill; deliberate ASCII-only negative controls; archive comparison |
| `source-provenance.json` | Frozen release metadata, inspected source receipts, and historical-input hashes |
| `action/` | Exact v1.10.0 Action metadata, README, and selected implementation; blobs checked against its commit tree |
| `gh-aw/.github/workflows/`, `gh-aw-contract.json` | Byte-matched canonical shared import and example; static binding checks, **no compilation** |
| `materialized/` | Preserved short-path probe projects and generated outputs |
| `probe-tools.ps1`, control/analyzer scripts | Reproduction machinery outside the book checkout |

Native resolution staging failed with `WinError 3` on the first, longer
Meridian consumer paths. Those failed logs remain. Moving materialization to
the unique short root
`%TEMP%\pp-2d4f` with short project names succeeded;
no Windows setting or CLI source was changed. The initial scaffold/Meridian
pack trees used sibling temporary root `apmp-2d4facdd`.

Child processes used isolated home, application-data, config/cache, and
temporary directories; inherited private token/password credentials were not
offered to public probes. The registry feature was enabled only in an owned
scratch home and then disabled. No global CLI/skill upgrade, private access,
live publish, paid agent execution, commit, or agent dispatch occurred.

## Concept map

| Chapter | Concept brief and implementation focus |
| --- | --- |
| [10](../../10-becoming-a-producer-theory.md) | Producer/consumer symmetry; extraction versus copying; declared package intent and distribution formats |
| [11](../../11-enterprise-at-fleet-scale-theory.md) | Reachable authority, protected enforcement, operational ownership, inventory and integrity |
| [12](../../12-the-landscape-and-whats-next-theory.md) | Standards versus tools; management versus discovery; implemented capability versus roadmap |

Use [edition theory §§1, 3, 5–8](theory.md) for the updated boundaries. None of
these features adds a fifth property or requires changing Meridian's three
harnesses or the final adopt/watch/build-around decision.

## 1. Scaffolding and the two plugin format families

**Surface:** `plugin init`, `plugin init --format agent-plugin`,
`pack --format ...`. **Implements:** [distribution-format boundaries](theory.md#7-a-distribution-format-must-preserve-the-package-you-intend-to-share).
**Inspected CLI:** 0.31.0.

Live help lists `plugin`, `agent-plugin`, `claude`, `claude-plugin` for plugin
init; pack additionally accepts legacy `apm`. No-flag init created only
`apm.yml` and root `plugin.json`. Explicit Agent Plugin init added `mcp.json`
and pinned schema URLs. Both scaffolds have version `0.1.0`, empty
`dependencies.apm` / `dependencies.mcp`, `devDependencies.apm: []`,
`includes: auto`, and `scripts: {}`. Neither creates a skill or lockfile.
Plain consumer init produced version `1.0.0`. [PLUGIN] [FORMATS]

```powershell
& $Apm plugin init --yes --target copilot
& $Apm plugin init --yes --target copilot --format agent-plugin
# Run in DIFFERENT empty scratch directories.
```

| Probe | Observation |
| --- | --- |
| `init-legacy-plugin` | Exit 0; Claude-compatible root manifest, no pinned Agent Plugins `$schema` |
| `init-portable-plugin` | Exit 0; root plugin and MCP schema `https://agent-plugins.org/schemas/1.0.0/...`; empty MCP server map |
| `portable-default-alias` | `pack --format plugin -o legacy`: exit 0; Claude-compatible output, not native Agent Plugin |
| `conflicting-format-selectors` | `pack --claude-plugin --format agent-plugin`: usage exit 2, no writes |

**Use:** start a producer or deliberately select its distribution contract.
**Do not use:** the CLI's “Pack as Agent Plugins v1” next-step suggestion as
evidence that the default changed. `--format plugin` retains its old meaning.
`unpack` and pack `--target` remain deprecated; legacy `apm` is a tooling
format, not the recommended consumer bundle.

**Minimal examples:** `backend/examples/updates/1.2/producer/portable-plugin`
and its README; exact generated scaffolds are in the named probe trees/logs.
The root `plugin.json` identity is generated, not hand-invented.

## 2. Declaration authority, HYBRID, includes, and author-only tooling

**Surface:** eligible `apm.yml`, `.apm/`, plugin `skills`, `type`,
`includes`, `devDependencies`. **Implements:** [declaration authority](theory.md#1-declaration-is-authority-not-a-directory-heuristic)
and producer/consumer symmetry. **Inspected CLI:** 0.31.0.

An eligible APM manifest wins over co-located plugin signals: eligibility
requires `.apm/` or APM/MCP dependencies. Metadata-only `apm.yml` does not by
itself override a plugin. Root skill/collection layouts are separate signals;
do not turn this into an unconditional “any apm.yml wins” rule. Explicit
plugin `skills` declarations are exhaustive, empty means none, and omission
permits conventional discovery. The controlled installs and negative skill
selection cases are already proven in [core §§4–5](core-reference.md);
this wave did not relabel them as new producer invocations. [TYPES]

**Two different meanings of hybrid:** a root `SKILL.md` plus `apm.yml` is a
supported HYBRID **layout**, with separate human-facing and runtime
descriptions. That is not activation of **`type: hybrid`**. The target manifest
reference still calls `type` reserved. In `reserved-type-install` /
`reserved-type-pack`, changing Meridian's type to `prompts` did not suppress
its instruction or skill: both commands exited 0 and retained all three
primitive types. Keep the reserved-field caveat. [MANIFEST]

| Producer selection | Actual 0.31.0 result |
| --- | --- |
| `.apm/` and root `skills/`, `includes: auto` | `.apm/` won; root skill omitted with an actionable warning (`local-source-authority`) |
| `includes: [skills/unlisted]` | Only that explicitly named root skill shipped; unlisted `.apm` prompt/instruction/skill did not (`pack-includes-exhaustive`) |
| Missing listed path | Pack exit 1 before writes (`pack-includes-missing`) |
| Local prompt edited after install | New source marker shipped; older deployed prompt was unchanged. “Pack only reads the last deployment” is false for first-party source |
| Local dev dependency | Installed for the author but absent from default bundle; no runtime local-dependency rejection for this dev-only entry (`fixture-dev-*`) |

`includes` is **not** an install-discovery allowlist; the core wave proved that
unlisted instructions still install. Its exhaustive pack behavior must be
qualified by operation. Dependency dev-MCP exclusion is likewise a different
surface from approving a consumer's executable connections. [PACK-GUIDE]

**Use:** keep Meridian's `.apm` source layout; restrict publication with an
explicit includes list; put author tooling in `devDependencies`.
**Do not use:** `type` to force classification, includes to filter install,
or extra undeclared plugin directories to expand a package's declared skills.

**Minimal examples:** `producer/local-bundle`, `producer/dev-only`, and
`producer/marketplace/plugins/review/plugin.json`; exact includes controls
are preserved as `l`, `il`, and `ix` in the scratch evidence.

## 3. Existing Meridian routing versus a genuine local-only bundle

**Surface:** `dependencies: {}`, `pack`, `--archive`, `-o`.
**Implements:** [producer/consumer symmetry](../../10-becoming-a-producer-theory.md)
and [recorded reproducibility](theory.md#3-reproducibility-is-recorded-identity-and-content-not-a-clock).
**Inspected CLI:** 0.31.0.

| Manifest content | Result in this release |
| --- | --- |
| `dependencies` **mapping**, including `{}` | Bundle; default Claude-compatible |
| Omitted or null `dependencies` | Not a bundle trigger |
| `marketplace` | Configured catalog artifacts; can coexist with a bundle |
| Claude/Copilot targets | Ecosystem plugin manifests, alongside applicable outputs |
| None of those | Nothing-to-pack error, as described by help/source |

The **unchanged historical** Meridian sample still took the manifest-only
route. `meridian-install`, `meridian-preview`, and `meridian-pack-routing`
returned 0. `pack --archive -o dist --verbose` wrote only
`.github/plugin/plugin.json` and `.claude-plugin/plugin.json`; no ZIP.
Fresh plugin metadata was JSON-equivalent to historical
`plugin.json.generated`, including repository/keywords and string-author
mapping; `type` remained absent. Do not copy a stale “those enrichment fields
are only planned” note over this observed result.

The **new** `producer/local-bundle/apm.yml` deliberately changes the routing:

```yaml
name: meridian-standards
version: 1.0.0
description: Shared Meridian engineering instructions, prompts, and review skills.
author: Meridian Platform Engineering
license: MIT
type: hybrid
targets: [copilot, claude, cursor]
dependencies: {}
includes: auto
```

```powershell
& $Apm install
& $Apm pack --dry-run --verbose
& $Apm pack
& $Apm pack --archive -o dist
```

All returned 0. Actual directory: **`build/meridian-standards-1.0.0/`**, not an
unversioned `<name>/` promise. The ZIP was
`dist/meridian-standards-1.0.0.zip`. It contained generated `plugin.json`,
`commands/checkout-review.md`,
`instructions/meridian-engineering.instructions.md`,
`skills/secure-payment-review/SKILL.md`, and the enriched lock. Root producer
lock bytes did not need fabricated bundle metadata. [PACK]

### Source install is not archive verification

The old-source local consumer succeeded at the short path using
`install ./pkg`, then `audit --ci`, both exit 0 (`meridian-source-short`,
`meridian-source-audit`). The manifest retained the portable `./pkg` spelling;
do not perpetuate “all local adds become absolute paths.”

Separately, a real generated ZIP installed successfully into a fresh
consumer. For the three-target example use:

```powershell
& $Apm install '<absolute path to meridian-standards-1.0.0.zip>' --target copilot,claude,cursor
& $Apm audit --ci
```

`archive-explicit-multitarget` and its audit returned 0. Eight distinct native
files existed across `.github`, `.claude`, `.cursor`, and shared `.agents`
(the CLI reported nine copy operations). Copilot's packed prompt correctly
landed in **`.github/prompts`**, not a commands directory.

**Important imperative-route limits:** without that explicit flag, the ZIP
probe selected only Copilot despite three targets in the consumer manifest.
The route did not add the ZIP to `dependencies.apm`; its real lock recorded
`local_deployed_files` / hashes and local-bundle ownership, not a replayable
archive dependency row. Retain the artifact and distinguish this one-shot
deployment from normal declared-source restore.

Runtime **local-path dependencies** are still rejected at pack time
(`pack-local-dependency-rejected`, exit 1). Empty dependencies plus owned
local primitives are not that case. `devDependencies` are excluded instead.

**Use:** Git refs for normal versioned sharing; default bundles for handoff;
local-only bundle when no remote dependency is needed.
**Do not use:** an old no-dependencies manifest's successful `--archive`
invocation as evidence a ZIP exists, or a source install as archive proof.
**Minimal example:** `producer/local-bundle`, with an unedited real lock.

## 4. Strict Agent Plugins 1.0: format support is not an audit verdict

**Surface:** `pack --format agent-plugin`, root schema, declarative plugin
dependency. **Implements:** [bounded portable distribution](theory.md#7-a-distribution-format-must-preserve-the-package-you-intend-to-share).
**Inspected CLI:** 0.31.0.

The skill-only fixture produced root `plugin.json` with
`$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`,
`mcp.json` even with no servers, `skills/review/SKILL.md`, and an embedded
lock whose **`pack.format` is `agent-plugin`**. No format feature toggle was
needed. Its source-project install/audit have an empty dependency graph;
their exit 0 is **not** a native consumer test. [PACK] [NATIVE]

Meridian's `pack --format agent-plugin -o rejected` returned **1**, with no
file or timestamp changes:

```text
Cannot pack Agent Plugin: non-portable primitives would be discarded
(commands, instructions).
```

The supported portable components are skills and MCP, not Meridian's whole
package. Agents, commands, instructions, hooks, extensions, and LSP are
outside this output contract; see the pinned docs for their distinct
limitations rather than silently dropping them.

The generated strict bundle was copied unchanged to a consumer's `pkg`:

```yaml
name: native-consumer
version: 1.0.0
targets: [copilot]
dependencies:
  apm:
    - path: ./pkg
```

`native-bundle-declared-install` returned **0** and registered the whole
plugin via APM's Copilot marketplace. It wrote registration/settings paths,
not a loose skill duplicate. APM did not launch or require finding Copilot.
Actual loading requires **Copilot CLI >=1.0.81** and remains
**SKIPPED-needs-network** here: no configured harness/runtime session was run.

`native-bundle-imperative-rejected` returned **1** without writes:
`install <bundle>` owns no native dependency row and directs the user to the
declarative route.

**Retain the known failure:** `native-bundle-audit` returned **1**. It reported
the missing source `apm.yml` consistency issue and
**`Native Agent Plugin canonical IR is missing`** during drift replay.
Core research already proved that legitimate metadata-only `apm.yml` removes
the first complaint but not the latter. Do not modify the packed lock, add
unattested files, disable drift, call this a network skip, or infer lack of
format support from this replay defect.

**Use:** portable skills/MCP for a supported native host.
**Do not use:** a universal Meridian migration or an audit-clean consumer
fixture. **Minimal input:** `producer/portable-plugin`; native consumer and
real generated lock are preserved in scratch project `n`.

## 5. Attested inputs, bundle integrity, and SBOM inventory

**Surface:** dependency `deployed_files` / `deployed_file_hashes`,
`pack.bundle_files`, `lock export`. **Implements:** [identity/content, not a clock](theory.md#3-reproducibility-is-recorded-identity-and-content-not-a-clock)
and [scoped trust](theory.md#5-trust-is-scoped-consent-not-proof-of-benign-behavior).
**Inspected CLI:** 0.31.0.

`producer/pinned-bundle` resolves only the public style-checker skill:

```yaml
dependencies:
  apm:
    - git: microsoft/apm-sample-package
      ref: fb2851683be0e0e7711421d518bd8dba23b0b1f6
      path: .apm/skills/style-checker
```

The genuine lock records that full commit, `package_type: claude_skill`,
`is_virtual: true`, and `version: unknown`. Exact source identity is still
present; do not invent a semantic version for the skill:

```text
content_hash:
  sha256:867912713bf45048211440b81ea0ced396ad0a0993447dd540fe5c219722d318
deployed SKILL.md:
  sha256:1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829
```

| Control | Actual outcome |
| --- | --- |
| Altered attested deployed skill | Both `claude-plugin` and `agent-plugin` pack exit 1 before writes |
| Deleted attested skill | Default pack exit 1, restore guidance |
| Altered cache skill, clean deployed skill | Default pack exit 0; exported skill exactly matched the original deployed bytes |
| Altered eligible `.github` instruction | Legacy `apm` pack exit 1, same hash-mismatch diagnostic |
| Copilot shared `.agents` skill in legacy format | **Omitted before verification**, empty successful bundle; see §9 |
| Changed payload / extra file / missing file in a genuine local bundle | Consumer install exit 1 in all three controls; no project writes |

The shared verifier checks files that enter a bundle. It deliberately tolerates
**missing** recorded hashes in older locks; a mismatched recorded hash fails.
Thus “every old lock attests every file” remains false. Directory cache presence
cannot add publishing authority. Source and code both document this boundary.
[ATTEST] [PACK-GUIDE]

The embedded **`pack.bundle_files`** maps payload-relative paths to raw SHA-256
hex digests; the lock cannot hash itself. Digests for three produced bundles
were independently recomputed. This is integrity relative to trusted metadata,
not signed publisher attestation. An untrusted party able to replace both
payload and its hash manifest is not authenticated by that manifest.

### SBOM is an inventory export, not a signature

```powershell
& $Apm lock export --format cyclonedx --timestamp '2026-09-16T00:00:00+00:00' -o sbom.cdx.json
& $Apm lock export --format spdx --timestamp '2026-09-16T00:00:00Z' -o sbom.spdx.json
```

Both returned 0. Output advertised **CycloneDX 1.5** and **SPDX-2.3**. The
virtual skill's inventory used the package identity and commit-bearing generic
PURL; SPDX declared/concluded license was `NOASSERTION`, not the producer's
own MIT license assigned to every dependency. A repeated identical CycloneDX
export was byte-identical. A date lacking timezone (`2026-09-16`) returned
usage **2** without creating the requested output. [LOCK-EXPORT] [SECURITY]

New locks omit `generated_at`. SBOM default timestamp in this probe was the
Unix epoch; documented precedence is explicit timestamp, `SOURCE_DATE_EPOCH`,
legacy lock timestamp, epoch. **`pack.packed_at` and archive metadata are
separate:** repeated default ZIP packing changed `pack.packed_at` and ZIP
member timestamps. Payload bytes were unchanged; the embedded locks were
semantically identical except for `packed_at`. Do not promise identical ZIP
bytes from lock equality alone. The root lock remained unchanged by pack/export.

**Use:** inventory/license review and changed-byte detection.
**Do not use:** clean scans, hashes, or unsigned SBOM JSON as benign-content,
publisher identity, SLSA, or runtime-sandbox certification.
**Minimal example:** `producer/pinned-bundle`; SBOMs, bundle maps, and negative
controls remain in session artifacts rather than the book checkout.

## 6. Read-only release gates and strict marketplace metadata

**Surface:** `marketplace init`, `marketplace.outputs`,
`pack --check-clean`, `--strict-metadata`, `--marketplace-path`, `--json`.
**Implements:** [reviewable distribution](../../10-becoming-a-producer-theory.md)
and a [protected enforcement point](theory.md#6-governance-needs-a-reachable-authority-and-a-protected-enforcement-point).
**Inspected CLI:** 0.31.0.

`marketplace init --name meridian-marketplace --owner meridian-finance`
created one `apm.yml` with owner, `build.tagPattern`, map-form `outputs`, and
an example remote package. It did not resolve/publish that placeholder.
This worked with `marketplace-authoring` disabled; do not infer that a disabled
flag makes every authoring command unavailable.

The reusable contained-local example uses:

```yaml
marketplace:
  owner:
    name: Book Fixtures
  outputs:
    claude:
      path: catalog/marketplace.json
  packages:
    - name: review
      source: ./plugins/review
      description: A minimal review skill.
      version: 1.0.0
```

| Command / state | Exit and result |
| --- | --- |
| `pack --offline --strict-metadata` on the local fixture | 0; `local`, certifiable metadata |
| `pack --offline --check-clean` on generated catalog | 0; unchanged; no file writes/touches |
| Same after catalog name changed | 4; `marketplace_drift`; changed catalog not repaired |
| Missing override path with `--marketplace-path claude=alternate/marketplace.json` | 4; compares that effective path; does not create it |
| Mixed bundle + catalog + plugin manifests, `--check-clean --force --archive` | 0 when catalog clean; all normal outputs suppressed |
| Same mixed project with bundle ZIP deleted | Still 0 when catalog clean; missing ZIP not rebuilt. **This is a marketplace gate, not bundle certification.** |

A first attempt using **`./catalog/marketplace.json`** failed with exit 1:
`segment '.' is a traversal sequence`. The corrected fixture uses
`catalog/marketplace.json`. Some pinned examples still show leading `./`;
prefer the actually accepted spelling. [PACK]

For absent metadata on the pinned public marketplace source:

| Probe | Result |
| --- | --- |
| `metadata-offline-preview` | `pack --offline --dry-run --json`: 0, `certifiable: false`, status `offline` |
| `metadata-offline-strict` | `--offline --strict-metadata --json`: **5**, `metadata_incomplete`, no writes |
| `metadata-offline-clean` | `--offline --check-clean --json`: **4**, `marketplace_metadata_uncertifiable`, no writes |
| `metadata-strict-clean` | Both gates: **5**; strict metadata fails before clean comparison |
| `public-metadata-fetch` | Real public pinned-source fetch with strict dry-run: 0, `fetched`, certifiable, no project writes |

The closed status vocabulary also includes `explicit`, `empty`, and `failed`
in the pinned reference; those three were source-inspected, not separately
claimed as successful live probes. Ordinary packing may warn and proceed with
uncertifiable metadata; a clean comparison cannot bless that fallback.

**JSON caveat:** the 0.31.0 success envelope left **`bundle: null` even while
creating a ZIP** (`public-pinned-pack`). Source initializes that field and
populates marketplace/plugin sections, not bundle results. Do not claim it is
a complete artifact inventory or use null to prove no archive exists.
Marketplace and metadata fields above were populated as shown. [PACK-CODE]

**Use:** release checks that compare reviewed catalogs without modifying them.
**Do not use:** `--check-clean` to regenerate files, as a package security
attestation, or `--offline` to certify metadata never obtained.
**Minimal examples:** `producer/marketplace` and `producer/metadata-offline`.

## 7. Registry gates, flat archives, and what is actually provided

**Surface:** `experimental enable registries`, `registries`,
`publish --package ... --dry-run`. **Implements:** [implemented distribution versus standards/roadmap](theory.md#8-shipped-implementation-is-not-standards-maturity-or-a-roadmap-promise).
**Inspected CLI:** 0.31.0; registry client remains **experimental**.

Both an unenabled `registries:` manifest and `publish --dry-run` failed with
exit **1**, naming the feature gate. Enabling it in an isolated home allowed
the new local-only preview fixture to parse, install, freeze, and audit.
No registry-sourced dependency was resolved by those empty-dependency commands.

```powershell
& $Apm experimental enable registries
& $Apm publish --package book-fixtures/review --dry-run
& $Apm experimental disable registries
```

The preview returned **0** and wrote a local ZIP containing **root `apm.yml`
and `.apm/`**, not a plugin wrapper. Source returns before constructing/uploading
the registry client on the dry-run branch. **“No upload” is not “no writes.”**
Do not use `apm pack`'s plugin ZIP as if it were the same archive contract.
[PUBLISH] [REGISTRIES]

| Surface | Current, bounded statement |
| --- | --- |
| Git source | Default distribution; no central APM service needed |
| Marketplace | Generated discovery index, commonly Git-hosted; not the REST package server |
| Proxy | Transport/mirror path in front of upstream Git; not a dedicated package registry |
| REST registry | Shipped experimental consumption/publication, requiring an actual compatible server |
| Implementable HTTP API v1 | Version-list, archive-download, publish endpoints; this is not a hosted service announcement or search endpoint |
| Official public hub | **Not established by the pinned release evidence**; do not replace that with a claim that no registry implementation exists |

Pinned API paths are `GET /v1/packages/{owner}/{repo}/versions`,
`GET .../versions/{version}/download`, and `PUT .../versions/{version}`.
Server-side publish authorization and immutable-version conflict handling are
documented, **SKIPPED-needs-network**: no authorized registry backend or live
publish was supplied or permitted. The fixture's reserved example hostname
was not contacted. [API]

Configured defaults can reroute shorthand `owner/repo#selector` to the registry.
Explicit `git:` stays Git; registry objects use `id`, `version`, and optional
`registry` / path / selections. Registry locks record `source: registry`,
`resolved_url`, and `resolved_hash`; no such lock was fabricated here.
Current/Wanted/Latest registry reporting is shipped in 0.31.0; **Wanted** stays
constraint-bound while **Latest** can lie outside a pin and include prereleases.
That contract was source-inspected, not exercised against a live server.
[REGISTRIES] [OUTDATED]

Credential authority belongs to user-owned HTTPS destination bindings, not an
untrusted manifest's registry name. Project-only registry URLs are accessed
anonymously unless the user binding authorizes the destination; do not put
tokens in either YAML file. A proxy and registry can coexist, but one does not
authorize the other.

**Use:** a reviewed compatible backend when your organization needs it.
**Do not use:** `registry.example.com` as a real service, GitHub's MCP registry
as an APM package registry, or a proxy as an internal discovery API.
**Minimal example:** `producer/registry-preview` (local preview only).

## 8. CI audit and the independently pinned Action contract

**Surface:** `audit --ci`, `--no-cache`, `-o ...sarif`,
Action `setup-only`, `apm-version`, `audit-report`.
**Implements:** [fleet CI enforcement](../../11-enterprise-at-fleet-scale-theory.md)
and [reachable authority](theory.md#6-governance-needs-a-reachable-authority-and-a-protected-enforcement-point).
**Inspected CLI:** 0.31.0. **Inspected Action:** v1.10.0, commit
**`d723bb64ed70c135bbaf87d126b721dd2dae0439`**; do not call it “latest.”

A cold checkout containing the pinned manifest, genuine lock and deployed
skill, but no `apm_modules` or populated isolated cache, passed `audit --ci`.
The project was unchanged, including timestamps. A separate cold run with an
unreachable loopback proxy failed **1** on scratch `config-consistency` and
drift hydration; it did not become a green skip. A subsequent ASCII tamper
also failed **1**, and real SARIF was written with `-o`. These were **local
CLI commands**, not Actions. (`ci-cold-audit`, `ci-unreachable-source`,
`ci-tamper-audit`, `ci-cold-sarif`.) [AUDIT] [CI]

The clean examples displayed nine baseline checks **plus drift**, including
`deployment-ledger-owners`. Prefer check names and failure meaning to a timeless
“8+1” count. Ordinary drift and invalid deployment ownership have different
bare-audit effects; reuse core/operations evidence rather than making every
finding advisory. Frozen install remains a structural gate, not this audit.

| Pinned Action input/behavior | Source-inspected contract; not runner execution |
| --- | --- |
| `apm-version` | Action default **0.14.0**; explicit `0.31.0` is necessary. Pinned installs use tool-cache, not an arbitrary PATH CLI |
| `setup-only: 'true'` | CLI setup then return; no project install. Mutually exclusive with `target`, dependencies, audit-report, compile, pack/restore and other project work |
| Default mode | Runs ordinary `apm install`, not `install --frozen`; can repair bytes before a later audit sees them |
| `audit-report` | Runs **bare** SARIF/Markdown audit; nonzero findings are informational to the wrapper. It is **not** `audit --ci` and not the required gate |
| `pack: 'true'` | Explicit `--format apm` by default; `plugin` is the other supported Action format selector |
| `bundle` / `bundles-file` | Ensures CLI, then uses deprecated **`apm unpack`**; not the imperative plugin-bundle install route |
| `offline` | Forwards to **pack** marketplace resolution; does not make the preceding install or CLI acquisition air-gapped |
| `github-token` | Credential convenience, not organization-wide private repository authorization |
| `pack-json` / `bundle-path` | Report path versus actual artifact path. Pinned wrapper finds archives on disk; CLI JSON `bundle:null` caveat still matters to report consumers |

These dispatch and audit behaviors were checked in the pinned runner source,
not inferred only from input descriptions. [ACTION-RUNNER]

The action uses Node 24; its installer supports Linux/macOS, not the Windows
backend used here. Source downloads/extracts through tool-cache and probes
`--version`; no explicit publisher-sidecar checksum step appears in that
v1.10.0 installer. **Our checksum-verified native executable is not proof of
the wrapper's acquisition security or execution.** [ACTION] [ACTION-INSTALL]

**Use:** setup-only + an explicit audit command when committed deployed bytes
are the review contract. Use install-then-audit when materialization is intended;
use frozen explicitly where lock/manifest reconciliation must fail instead.
**Do not use:** `audit-report: true`, a major Action tag, or CLI `--ci` alone
as evidence of an authoritative, immutable organization gate.

**Minimal example:** `producer/ci/apm-audit.yml`, exact Action/CLI pins,
no `--no-drift`. **SKIPPED-needs-network:** GitHub runner, permissions,
branch/ruleset enforcement, and SARIF upload were not exercised. The local
underlying command is proven. Preserve all three old Ch11 workflow stamps as
historical; an edited YAML file is not a rerun.

## 9. gh-aw re-vendoring and the explicit compatibility boundary

**Surface:** local `shared/apm.md` import, `target`, `apm-version`,
`token-source`, Action pack/restore. **Implements:** [context versus runtime](theory.md#gh-aw-required-cross-chapter-correction).
**Inspected CLI:** 0.31.0; shared file pinned to the APM target commit;
Action v1.10.0 separately pinned.

The canonical file was **actually re-vendored in scratch**, byte-for-byte,
at `producer-probes/gh-aw/.github/workflows/shared/apm.md`.
SHA-256: **`6ebe127ee1ae527249b81239a8fa52f3a3ead298042b2d43122d6a68faf0f3ae`**.
Static assertions verified:

- `import-schema.target.required: true`; the prep script rejects blank and
  `all`, including normalized CSV members. The caller must match `engine`;
  it is not inferred from the host manifest.
- Shared default **`apm-version: '0.28.0'`**, distinct from Action's 0.14.0
  default and this book's 0.31.0 baseline.
- The same import input is threaded into **both** Action pack and restore.
- Pack uses `isolated: 'true'`, explicit target, inline dependencies and a
  separate work directory. Host `apm.yml` / lock / primitives are not
  automatically inherited. Re-vendoring and compilation are separate steps
  from changing a CLI version. [SHARED] [GH-AW]

Minimal host inputs, included in `producer/ci/gh-aw-review.md`:

```yaml
engine: copilot
imports:
  - uses: shared/apm.md
    with:
      apm-version: '0.31.0'
      target: copilot
      token-source: github-token
      packages:
        - microsoft/apm-sample-package/.apm/instructions/design-standards.instructions.md#fb2851683be0e0e7711421d518bd8dba23b0b1f6
```

For a consumer migration, vendor **the frozen commit, not `main`**, verify it,
then use a separately reviewed gh-aw compiler:

```powershell
# SKIPPED-needs-network as a consumer workflow: run only in its owned scratch checkout.
New-Item -ItemType Directory -Force .github/workflows/shared | Out-Null
Invoke-WebRequest 'https://raw.githubusercontent.com/microsoft/apm/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/.github/workflows/shared/apm.md' -OutFile .github/workflows/shared/apm.md
# Expected SHA-256: 6ebe127ee1ae527249b81239a8fa52f3a3ead298042b2d43122d6a68faf0f3ae
Get-FileHash .github/workflows/shared/apm.md -Algorithm SHA256
gh aw compile
```

**Not run:** gh-aw compilation, artifact jobs, authentication, and agent
loading. **SKIPPED-needs-network:** no separately frozen gh-aw compiler/runner
and authorized runtime integration was supplied. The byte-match and static
binding checks are not compile or Action-execution evidence.

`token-source: github-token` deterministically selects the ephemeral
**current-repository** read token for no-App rows. It does not grant private
cross-repository access. The default cascade selects configured overrides;
a rejected explicit identity is not silently rescued by another identity.
App rows use their installation token. Custom per-org APM credentials remain
a separate precedence surface. Do not suggest widening credentials to “fix”
an unrelated format or target failure.

### Real CLI compatibility evidence — both positive and negative

The Action's source constructs:

```powershell
& $Apm pack -o build --format apm --target copilot --archive
# Restore in a DIFFERENT scratch directory:
& $Apm unpack '<absolute path to the resulting ZIP>' -o .
```

| Input and evidence | Actual result |
| --- | --- |
| `producer/action-pinned`, one public instruction | Install 0, pack 0 with **one file**, unpack 0 with **one verified file**. Restored bytes matched; consumer `apm.yml`/lock were not created |
| `producer/pinned-bundle`, one Copilot skill at `.agents/skills/style-checker` | Install/audit succeeded, but legacy pack 0 said **“No files to pack for target 'copilot'”**. Archive contained no skill; unpack 0 restored nothing |
| Same altered skill, legacy `apm` format without explicit pack target | Again omitted under manifest target filtering; no attestation failure because no skill entered the bundle |
| Altered `.github/instructions/...` control | Legacy pack did reach attestation and returned 1 |

This is **not** a general attestation bypass for included files. In the target
source, legacy packing filters by `TargetProfile.effective_pack_prefixes`.
Copilot's root is `.github`, while its skill deployment root is `.agents`;
the profile has no matching pack-prefix override. The concrete omission is
consistent with that code. [PACKER] [PACK-TARGETS] [PROFILES]

**Author/verifier gate:** do not approve an all-skills or full-package gh-aw
0.31.0 refresh merely because the instruction control worked. Verify the
actual intended primitive inventory through pack and restore. The example
above intentionally uses only the tested instruction and still carries its
integration skip. Do not switch to a plugin format as an untested repair:
v1.10.0's Action format detector rejects current plugin archives with both
root `plugin.json` and lock markers, and plugin restore is unsupported there.
The shared workflow's default legacy format is deliberate. [ACTION-BUNDLE]

Multi-bundle ownership also needs review: the pinned Action applies bundles
in list order; later bundles win. Its collision preview remains a stub,
despite an older version-number roadmap comment. Artifact-name/matrix checks
in the shared file are not per-file collision detection. No multi-bundle
runner or collision test was executed. [ACTION-MULTI]

**Use:** treat APM as an imported context supplier to a separately controlled
runtime. **Do not use:** isolation to claim prompt injection is impossible,
automatic host-manifest/lock/policy carry-over, or output exit 0 as proof
every requested capability arrived.

## 10. Enterprise ownership and landscape wording

**Surface:** policy discovery/authority, proxy controls, target catalog,
OpenAPM and roadmap. **Implements:** [theory §§5–8](theory.md).
**Inspected CLI:** 0.31.0; the following unexecuted integrations are
source-grounded, not refreshed historical workflow results.

### Ch11: retain ownership, correct absolutes

- CLI help explicitly allows `audit --ci --no-policy`, while explicit
  `--policy` takes precedence. “CI ignores bypass flags” describes a
  **protected workflow's intended configuration**, not a magical CLI rule.
  Protect the workflow, reviewed lock, policy authority, credentials and
  ruleset bypasses. `--no-cache` refreshes **policy**, not the package cache.
- GitHub discovery now prefers `.github-private`, then `.github`, `.apm`,
  `_apm`; GitLab uses the top-level group's `apm-policy`; ADO uses project
  `apm`, repo `apm-policy`, with its documented fallback. Meridian can keep its
  fictional `.github` location. **SKIPPED-needs-network:** no private org
  discovery or inheritance was executed here. [POLICY]
- An unread org file's `fetch_failure: block` cannot secure its own first
  fetch. Consumer **`policy.fetch_failure_default: block`** controls the
  no-policy/no-cache boundary. Warm-cache tighten-only and direct-scoped pin
  rules follow the edition theory/source reconciliation; leave old
  unexecuted direct/transitive policy transcripts at 0.23.1 pending the
  operations verifier. Do not turn Ch11 into a second policy tutorial.
- Keep `compilation.target.allow`. Unknown top-level policy keys now warn;
  malformed known types fail. Do not repeat “silently ignored” or stale
  inheritance advice that an empty child deny list clears parent restrictions.
- `HTTPS_PROXY` / `PROXY_REGISTRY_*` are transport controls, not proof all
  traffic is mirrored. The pinned coverage table excludes ADO dependency,
  MCP-registry and policy-fetch paths from the GitHub archive proxy.
  **SKIPPED-needs-network:** no corporate proxy was supplied. The loopback
  negative control is not a proxy-infrastructure acceptance test. [PROXY]
- APM config's displayed defaults are not the universe of accepted keys:
  saved targets and gated registry keys exist. Avoid the old “only three
  persisted keys” claim merely because `config list` displays three defaults.
- Hashes/ownership are not publisher signatures. Authenticode/checksum
  distribution changes do not sign agent packages. Noninteractive/frozen
  plugin `bin/` is withheld without permitted consent even though the broader
  executable gate is opt-in. Hooks, lifecycle scripts, MCP consent and runtime
  permissions are different boundaries. These execution surfaces were not
  exercised in this producer wave. Windows admin lifecycle policy is
  **`%ProgramData%\APM\policy.d\*.json`**, not an org-policy YAML location.
  [SECURITY] [LIFECYCLE]

Retain Payments / Onboarding / Merchant Dashboard, staged rollout, named
on-call ownership, audit/drift trend and review cadence. Do not upgrade old
setup-time measurements into 0.31.0 performance promises.

### Ch12: separate independent versions and delivery claims

| Name | What the inspected version means |
| --- | --- |
| APM 0.31.0 | Shipped CLI release frozen for this book |
| Agent Plugins 1.0.0 | A portable plugin schema implemented as opt-in output/intake |
| Registry HTTP API v1 | Implementable wire API with experimental client support |
| OpenAPM 0.1 | **Editor's Working Draft**, not a ratified 1.0 standard |
| OpenAPM 0.2 / later horizons | Reserved normative/roadmap work, not automatic delivery |

OpenAPM's own status and scope reserve normative registry wire guarantees,
publisher signing/attestation and version-withdrawal work; that does not erase
the shipped informational API/client. Do not imply a public hub, signing,
yank/deprecate, or a committed delivery date from an API version or roadmap
label. [OPENAPM]

The target governance document names an active issue-backed public Project:
issues carry scope/evidence, Project **Now / Next / Later** carries priority,
milestones carry release cohorts. Placement, reactions, labels and automated
recommendations are not implementation permission or delivery guarantees.
This contributor governance is also not enterprise `apm-policy.yml`. [ROADMAP]

Grok Build, Kiro agents and stable explicit-only Hermes are shipped catalog
facts already reconciled by core/theory; Grok Cloud remains experimental.
Keep this as a bounded catalog correction, not a new harness walkthrough.
Keep competitor comparisons explicitly **2026-07-01 historical** unless
separately re-researched. An APM-only update does not reverify every competitor,
all-tools-pre-1.0 claims, or “broadest/alone/widest” superlatives.

**Use:** evaluate the four properties for the scope you actually need.
**Do not use:** roadmap vocabulary to imply hosted delivery, format maturity
to imply runtime safety, or the new APM date to recertify the whole market map.
**Minimal references:** `producer/registry-preview` and `producer/ci/gh-aw-review.md`
illustrate the shipped client/runtime boundary; the closing decision remains
conceptual, with no new Ch12 runnable tutorial.

## Per-chapter author changes and stamp discipline

| Historical anchor | Required update / preserved boundary |
| --- | --- |
| Ch10 package-shape and `type` table | `.apm` remains Meridian's chosen layout, not the only supported package layout. Retain reserved `type`; distinguish HYBRID layout |
| Ch10 “pack only last deployed files” | Split local source/includes from dependency attestation |
| Ch10 no-dependencies routing / `--archive -o dist` | Keep original sample's manifest-only behavior; show local-only bundle only as an explicit, coordinated change/new fixture |
| Ch10 “remote refs required for every bundle” | Replace with `dependencies: {}` local-only proof; runtime local dependencies still rejected |
| Ch10 “only plugin format installs” / scaffold | Claude-compatible default versus strict Agent Plugins, plus declarative native route and replay caveat |
| Ch10 offline “round-trip” | Label source-install proof separately from the actual new ZIP round-trip; pass explicit archive targets |
| Ch10 metadata / publish | Preserve tested fields; publish dry-run writes locally; flat registry archive is distinct from plugin bundle |
| Ch11 three workflows | Keep old stamps; new setup-only advice omits mandatory `--no-drift`; pin Action and CLI independently; `audit-report` is not the gate |
| Ch11 clean/direct/transitive gate transcripts | Fresh clean/SARIF/cold evidence here; old policy scenarios remain historical, not re-executed by this role |
| Ch11 authority/proxy/air gap | Protected enforcement and consumer first-fetch policy; not all-traffic proxy; actual local bundle proof replaces blanket network-only bundling |
| Ch11/12 gh-aw callout | Re-vendor, concrete target, explicit 0.31.0 for pack/restore; no host manifest carry-over; retain legacy shared-skill compatibility blocker |
| Ch12 registry/APM row/leader/open questions | Shipped experimental API/client versus hosted service and draft norms; no new competitor survey or delivery prediction |

## Full-gap accounting at this scope

| Release | Ch10–12 disposition |
| --- | --- |
| 0.24.0 | Dependency attestation and source-qualified ownership rechecked; hook/bin/transport hardening retained as bounded security context |
| 0.24.1 | Author-only dependency semantics and local identity relevant; dev exclusion probed. Private transport and update details remain operations scope |
| 0.25.0 | Pack source authority, includes, eligible layouts, preferred policy location; local controls plus core/source evidence |
| 0.26.0 | Pack/consume parity and actual materialization, metadata and ownership; inspect produced files, not exit alone. No platform/CI-internal tutorial |
| 0.27.0 | Cold CI hydration and fail-closed missing-source evidence; retained dev-MCP/source-authority boundaries |
| 0.28.0 | Empty dependency mapping local bundles, local marketplace metadata/output handling; current paths rechecked |
| 0.29.0 | Strict Agent Plugins/native support, declared skill authority, noninteractive executable consent, separate binary/package signing |
| 0.29.1 | Read-only clean gate, strict metadata, declaration-first behavior, no new-lock timestamp, scoped ownership. Actual failures retained |
| 0.30.0 | Exact isolated binary reuse/checksum and installer ownership notes; no global upgrades or cache-management expansion |
| 0.31.0 | Breaking gh-aw target/input contract and explicit CLI override; registry reporting source contract; catalog/roadmap updates. Native replay and legacy pack limitations explicitly bounded |

The full release-by-release impact ledger remains `RunRoot/impact.md`;
internal CI/dashboard/performance work and unrelated operations features do
not justify additional chapter material.

## Verifier handoff and artifacts written

**Reference written:** `content/research/updates/1.2/producer-reference.md`.
**Reusable examples only under:** `backend/examples/updates/1.2/producer/`.
Eight projects have genuine locks; `marketplace/catalog/marketplace.json`
is genuine generated output. No bundle ZIP, cache, or raw runtime log is
committed as an example.

| Fixture | Root lock SHA-256 |
| --- | --- |
| `local-bundle` | `2b906800526ba3942b583d75db6057551e9101447e733be60ef41a7beb66fe07` |
| `pinned-bundle` | `379bce78204582002c4070fb666c973a4194a131fb6afa0df31ebe819c542429` |
| `portable-plugin` | `b0f72429b19a157059b38ef2df7713f4fd15e3eb113908c5537392467001d136` |
| `marketplace` | `b0f72429b19a157059b38ef2df7713f4fd15e3eb113908c5537392467001d136` |
| `metadata-offline` | `b0f72429b19a157059b38ef2df7713f4fd15e3eb113908c5537392467001d136` |
| `registry-preview` | `74ce2c1703046e28e54bcdcac8e835bff731951ddb8ac13acba2f03b53878715` |
| `action-pinned` | `85c288dcde630dba16f82d691b9b43566e20e7ab873307599b67feaef6b941c2` |
| `dev-only` | `3ca0d3e5bbe49401cf3a1251b01eb950ec7878c5d6343bbbcae5a8c7bf335f14` |

Identical empty locks are legitimate CLI output, not fabricated identical
resolutions. Run the README recipes in fresh, short-path copies, not over old
examples. Verify actual inventories, lock bytes, negative exits, and read-only
behavior. For native plugins and legacy shared-skill packing, retain the real
failures; neither is `SKIPPED-needs-network`.

Remaining **SKIPPED-needs-network** integrations: private Meridian Git
distribution, live registry publish/consume, corporate proxy, remote org policy
and inheritance, required-check/ruleset enforcement, Actions/SARIF upload,
gh-aw compiler/runner and harness loading. Reasons are specified above; no
private credentials or remote write permission was requested.

The code-verifier handoff is this artifact and its exact command index; no
agent was spawned. The author should not advance historical workflow stamps,
chapter baselines, or edition metadata on the strength of local CLI or static
source inspection alone.

## Pinned official sources

[RELEASE]: https://github.com/microsoft/apm/releases/tag/v0.31.0
[PLUGIN]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/plugin.md
[FORMATS]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/bundle/formats.py
[TYPES]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/package-types.md
[MANIFEST]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/manifest-schema.md
[PACK]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/pack.md
[PACK-GUIDE]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/producer/pack-a-bundle.md
[PACK-CODE]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/commands/pack.py
[PACKER]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/bundle/packer.py
[PACK-TARGETS]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/bundle/lockfile_enrichment.py
[PROFILES]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/integration/targets.py
[ATTEST]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/bundle/attest.py
[NATIVE]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/consumer/copilot-agent-plugins.md
[LOCK-EXPORT]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/lock.md
[PUBLISH]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/src/apm_cli/commands/publish.py
[REGISTRIES]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/guides/registries.md
[API]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/registry-http-api.md
[OUTDATED]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/outdated.md
[AUDIT]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/reference/cli/audit.md
[CI]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/enterprise/enforce-in-ci.md
[POLICY]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/enterprise/policy-reference.md
[PROXY]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/enterprise/registry-proxy.md
[SECURITY]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/enterprise/security.md
[LIFECYCLE]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/enterprise/lifecycle-scripts.md
[GH-AW]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/integrations/gh-aw.md
[SHARED]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/.github/workflows/shared/apm.md
[ACTION]: https://github.com/microsoft/apm-action/blob/d723bb64ed70c135bbaf87d126b721dd2dae0439/action.yml
[ACTION-INSTALL]: https://github.com/microsoft/apm-action/blob/d723bb64ed70c135bbaf87d126b721dd2dae0439/src/installer.ts
[ACTION-RUNNER]: https://github.com/microsoft/apm-action/blob/d723bb64ed70c135bbaf87d126b721dd2dae0439/src/runner.ts
[ACTION-BUNDLE]: https://github.com/microsoft/apm-action/blob/d723bb64ed70c135bbaf87d126b721dd2dae0439/src/bundler.ts
[ACTION-MULTI]: https://github.com/microsoft/apm-action/blob/d723bb64ed70c135bbaf87d126b721dd2dae0439/src/multibundle.ts
[OPENAPM]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/docs/src/content/docs/specs/openapm-v0.1.md
[ROADMAP]: https://github.com/microsoft/apm/blob/8fd10ac5eafee7ca77d41cc34ba139d812fdacd5/GOVERNANCE.md
