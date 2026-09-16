# Edition 1.2: theory and release-impact brief

**Frozen range:** book 1.1 / APM 0.23.1 -> book 1.2 / **APM 0.31.0**, not latest.
Research uses all ten intervening release-note bodies and the v0.31.0 checkout at
**8fd10ac5eafee7ca77d41cc34ba139d812fdacd5**. The shared session checkout's HEAD matches
its recorded commit and stable release metadata. **Inspected CLI: none in this
theory task**; commands and output shapes below are source-grounded handoffs, not
fresh PASS results. Existing v0.23.1 research remains historical evidence.

The working release-by-release/chapter/example matrix is
`RunRoot/impact.md`, where RunRoot is the session's `files/book-v1.2` artifact directory.
Detailed source stays under that session's `source\apm-0.31.0`; citations identify
the matching raw target-tag files. Preserve all twelve slugs, Meridian's
Copilot/Claude/Cursor story, chapter beats, and engineering-leader track.

## Concepts covered

- Declared intent, authorized targets, and package layout.
- Materialization, reconciliation, and consented onboarding.
- Reproducibility without timestamp churn.
- Reporting, deliberate change, and integrity verification.
- Executable trust, transport authority, and runtime boundaries.
- Authoritative policy, tighten-only inheritance, and CI enforcement.
- Producer/consumer symmetry across distinct distribution formats.
- Shipped registry implementation versus standards and roadmap commitments.

## 1. Declaration is authority, not a directory heuristic

A package's eligible APM manifest and its component declarations determine what
may be deployed; directory conventions supply defaults only where the relevant
declaration is absent. Target selection defines the authorized destination set,
and package/per-dependency restrictions narrow it rather than add harnesses.
This prevents accidental capability or target expansion. [PACKAGE] [INSTALL] [HOOKS]

**Implemented in APM by:** manifest targets, dependency target/skill selections,
declaration-first plugin intake, and native Agent Plugin registration.
**Author update (Ch1/3/4/5/10):** replace "only .apm layouts" and "all plugins unpack"
absolutes. Explicit plugin skills are exhaustive; an empty declaration means none.
Agent Plugins v1 stay whole for Copilot; loading requires Copilot CLI >=1.0.81,
but APM does not need to locate or execute Copilot to register them. Preserve
Meridian's three-target projection and "same intent, not identical native bytes".
[PACKAGE] [PLUGIN-CONSUMER]

## 2. Restore replays unchanged intent; reconciliation follows changed intent

An unchanged manifest and lockfile reuse the locked graph, including transitive
manifests; explicitly changing a ref is new intent that normal install reconciles.
Discovery is a separate migration operation: it inventories admissible existing
packages without translating or moving their source, and consented apply merges
local references before a later install. Neither discovery nor a successful preview
proves that all requested capabilities were deployed. [INSTALL] [INIT] [LOCKFILE]

**Implemented in APM by:** install/add/restore, transactional replacement, and init
discovery/apply. **Author update (Ch4/5/7):** qualify "bare install never upgrades",
"--target never persists" (bootstrap can persist it), and "dry-run writes nothing"
(project bootstrap differs from global preview). Preserve no-target-detected exit 2.
Separately, native Agent Plugin target exclusion exits 1 only for a total real
no-deploy; mixed installs can succeed and dry-run can still exit 0. This is the
highest-value **Ch5 pilot**, not a reason to replace its four-command habit.
[INSTALL] [CHANGELOG]

## 3. Reproducibility is recorded identity and content, not a clock

The lockfile records a resolved graph plus materialization ownership; replay and
fresh resolution are different operations. New locks omit volatile `generated_at`;
legacy locks can retain it, while `resolved_at` and SBOM timestamps have separate
purposes. Deployed UTF-8 text hashes normalize CRLF, but package-tree hashes describe
actual materialized bytes, not a promise that all source bytes are rewritten. [LOCKFILE]

**Implemented in APM by:** lockfile pins/hashes/ownership, frozen install, lock-only
generation, and audit. **Author update (Ch5/6/7/11):** replace timestamp-based proof
and environment-specific-deployed-hash caveats. Frozen remains structural rather
than deployed-content audit, with MCP consistency and cold-cache cases to reverify.
`apm lock` preserves existing deployment records while leaving harness files alone;
"always omits deployed_files" is obsolete. Keep Priya's forgotten-lockfile CI break.
[INSTALL] [LOCK] [LOCKFILE]

## 4. Freshness, permission to change, and integrity are separate questions

`outdated` reports availability; `update` applies an allowed, consented change;
`audit` checks the resulting state. Registry reporting now distinguishes installed
Current, constraint-bound Wanted, and published Latest, which can be outside a pin
and include prereleases; that does not authorize an update outside the constraint.
CI audit can hydrate a lock-pinned scratch replay without rewriting the checkout,
so a cold cache is not a harmless green skip. [OUTDATED] [UPDATE] [AUDIT]

**Implemented in APM by:** the maintenance triad and canonical deployment-owner
checks. **Author update (Ch2/6/7/8/11):** retire "only update can ever move versions",
"pinned deps never show outdated", permanently overstated update-plan counts,
"audit is always offline", and fixed eight-plus-one checks. Ordinary bare-audit
drift remains advisory; invalid ownership fails both modes. Keep built-in audit
distinct from a CVE feed, and align Ch7 with Ch8's Critical/Warning severity split.
[INSTALL] [AUDIT] [BASELINE]

## 5. Trust is scoped consent, not proof of benign behavior

Install scans the authorized deployable source set before agent-readable
deployment, not every cached file before any disk write. Hashes detect changed
bytes; neither hashes nor a clean Unicode scan establish publisher identity or
benign intent. Harness hooks, APM lifecycle scripts, MCP depth-based trust, and
executable approvals are distinct execution/consent surfaces. [SECURITY] [LIFECYCLE]

**Implemented in APM by:** deploy-set scanning, canonical trust identities, deny
ceilings, plugin-bin invocation consent, and credential destination containment.
**Author update (Ch1/3/5/8/9/10/11):** the broad executable gate remains opt-in, but
plugin `bin/` defaults to withheld in noninteractive/frozen contexts without
permitted consent. Ordinary package approval keys are not per-version boundaries
merely because they display a version; local-bundle approval keys bind a digest.
Copilot CLI MCP and VS Code MCP have distinct paths. Lifecycle scripts can execute
with their own trust model; their Windows admin path is
`%ProgramData%\APM\policy.d\*.json`, not an org-policy YAML location. Release notes
describe signing work, but the exact Windows executable inspected by the
[operations explorer](operations-reference.md) reported `NotSigned`. Its archive's
publisher sidecar was verified; neither observation establishes agent-package
publisher authentication or runtime sandboxing. [INSTALL] [APPROVE] [MCP] [LIFECYCLE] [CHANGELOG]

## 6. Governance needs a reachable authority and a protected enforcement point

Organization policy is a reviewed authority discovered by host-specific rules:
GitHub prefers `.github-private` before existing fallbacks, GitLab uses the
top-level group's `apm-policy`, and ADO uses project `apm`, repo `apm-policy`.
Tighten-only inheritance preserves upstream restrictions; cache hits must preserve
the same effective policy. A required CI job is authoritative because its inputs
and bypasses are controlled, not simply because its command contains `--ci`.
[POLICY] [DISCOVERY] [INHERITANCE] [AUDIT]

**Implemented in APM by:** policy discovery, effective-rule inspection, warm-cache
enforcement, and install/CI gates. **Author update (Ch1/9/11):** unknown top-level
policy keys warn rather than disappear silently; malformed known types fail.
Keep `compilation.target.allow`, the early-preview label, and warn -> measure ->
remediate -> block. GitHub/registry owner-repository policy patterns now use
canonical casing; refs, subpaths and MCP identities are not all case-insensitive.
Cold first-fetch fail-closed needs consumer `policy.fetch_failure_default`, not
only an unread remote policy's `fetch_failure`. [PARSER] [POLICY-REF] [POLICY-SCHEMA]

**Source resolves misleading companion docs:** empty child deny/require lists do
not erase parent restrictions; fetch-failure severity escalates. The pin rule's
target implementation is direct-scoped, and plural-only target audit remains a
weak demonstration. Retain those boundaries and reverify them; Ch9's pin-rule
example must use an unbounded **direct** dependency to agree with Ch11.
`mcp.trust_transitive` remains documented as parsed but not enforced. [INHERITANCE]
[POLICY-CHECKS] [POLICY]

## 7. A distribution format must preserve the package you intend to share

Producer/consumer symmetry still closes Meridian's story, but a format is not
universally interchangeable with every other format. Default packing remains
Claude-compatible; portable Agent Plugins v1 is opt-in and carries skills/MCP,
rejecting unsupported primitives rather than silently discarding them.
Dependency content must be lock-attested, while local content follows the chosen
source layout and explicit pack includes. [PACK] [PACK-GUIDE]

**Implemented in APM by:** pack, plugin scaffolds, local bundles, marketplaces and
native plugin registration. **Author update (Ch4/10/11):** an explicit
`dependencies: {}` can produce a local-only bundle; remote dependencies are not a
prerequisite. The existing sample omits that mapping, so qualify its in-tree
plugin-manifest output rather than change it silently. Keep Meridian's instructions,
prompt and skill together; do not migrate it to Agent Plugins v1. `includes` is
exhaustive for plugin packing but not install discovery. Target docs still describe
`type: hybrid` as reserved. `--check-clean` is read-only; a local source install is
not proof an archive round-trip passed. [PACK] [PACK-GUIDE] [MANIFEST]

## 8. Shipped implementation is not standards maturity or a roadmap promise

APM 0.31.0 includes experimental REST registry consumption/publication and an
implementable HTTP API; this is not evidence of a Microsoft-operated public
searchable registry. OpenAPM v0.1 still calls itself an editor's Working Draft and
reserves a normative registry wire contract and further provenance/withdrawal
capabilities for v0.2. The target roadmap uses actual issues, Project horizons and
milestones; placement is planning, not delivery or approval. [REGISTRIES] [API]
[OPENAPM] [GOVERNANCE]

**Implemented in APM by:** experimental registries, Git/marketplace/bundle
distribution, and the published specs; roadmap entries are **not implementation**.
**Author update (Ch2/10/11/12):** replace registry-absence absolutes while retaining
the Git-first Meridian path. Grok Build, Kiro agent support and stable explicit-only
Hermes are shipped catalog facts; Grok Cloud remains experimental. Keep later
features and market forecasts outside edition 1.2. [TARGETS] [CHANGELOG]

## gh-aw: required cross-chapter correction

For Ch11/12, the target-tag shared import requires a concrete target matching the
engine and rejects `all`. It runs isolated, ignores the host `apm.yml`, and installs
only imported packages; do not claim the host manifest/lock automatically carries
over. The optional `github-token` selector gives deterministic read-only access to
same-repository private content, not other private repositories. Re-vendoring and
recompilation are separate from a CLI upgrade. [GH-AW] [SHARED]

The shared file still defaults to **APM 0.28.0**, with action **v1.10.0**.
Any refreshed edition example must explicitly select **0.31.0** for pack and restore
and obtain compatibility evidence. Keep this as the existing consumer/runtime
callout, not a gh-aw tutorial or a promise that sandboxing makes injection impossible.
[GH-AW] [SHARED]

## Empirical amendments to this source-grounded handoff

The later [operations](operations-reference.md), [producer](producer-reference.md),
and [pilot verification](ch05-verification.md) reports narrow several source-level
claims. Authors must apply their observed boundaries rather than present this
theory brief as an execution result:

- Frozen installation accepted a newly declared local-path dependency with an old
  lock, deployed it, and rewrote the lock. It is not a universal declaration-change
  veto.
- Explicit policy did not override `APM_POLICY_DISABLE=1`. A policy hash mismatch
  required consumer fail-closed configuration to fail CI; a clean exit alone is not
  evidence that the requested policy was enforced.
- Local MCP, parked hooks, and native-plugin replay exposed ownership/coverage
  limitations. Preserve the exact tested boundaries rather than generalize the
  successful instruction fixtures to every primitive.
- The legacy Copilot pack used by the gh-aw contract omitted the tested shared-path
  skill, while a nonempty pinned instruction packed and restored successfully.
  Required inputs and CLI version overrides do not establish blanket runtime
  compatibility.

## Handoff and scope decisions

**Pilot Ch5**, then propagate shared manifest/lock/audit conclusions to Ch4/6/7,
security/policy/CI to Ch8/9/11, and distribution/positioning to Ch10/12 with bounded
consistency edits in Ch1-3. The working matrix identifies each existing example and
accounts for every intervening release-note group, including internal/deferred work.

Coordinate before authoring: retain or deliberately change Ch10's output mode;
freeze compatible gh-aw/action inputs independently of CLI 0.31.0; validate the
policy source/doc conflicts; and keep competitor claims explicitly dated rather
than relabel an APM-only refresh as a new market survey. No new target, registry
server, LSP, scanner, lifecycle-webhook, or exhaustive flag tutorial is needed.

## Sources actually used

- [Target changelog][CHANGELOG] and all ten release-note bodies from the discovery
  JSON: [0.24.0](https://github.com/microsoft/apm/releases/tag/v0.24.0),
  [0.24.1](https://github.com/microsoft/apm/releases/tag/v0.24.1),
  [0.25.0](https://github.com/microsoft/apm/releases/tag/v0.25.0),
  [0.26.0](https://github.com/microsoft/apm/releases/tag/v0.26.0),
  [0.27.0](https://github.com/microsoft/apm/releases/tag/v0.27.0),
  [0.28.0](https://github.com/microsoft/apm/releases/tag/v0.28.0),
  [0.29.0](https://github.com/microsoft/apm/releases/tag/v0.29.0),
  [0.29.1](https://github.com/microsoft/apm/releases/tag/v0.29.1),
  [0.30.0](https://github.com/microsoft/apm/releases/tag/v0.30.0),
  [0.31.0](https://github.com/microsoft/apm/releases/tag/v0.31.0).
- Target-tag [install][INSTALL], [init][INIT], [update][UPDATE],
  [outdated][OUTDATED], [audit][AUDIT], [baseline checks][BASELINE],
  [lock][LOCK], [lockfile][LOCKFILE], [manifest][MANIFEST],
  [package types][PACKAGE], [targets][TARGETS], [MCP][MCP] and [hooks][HOOKS].
- Target-tag [security][SECURITY], [approvals][APPROVE],
  [lifecycle scripts][LIFECYCLE], [policy][POLICY],
  [policy schema][POLICY-SCHEMA], [policy reference][POLICY-REF],
  [parser][PARSER], [inheritance][INHERITANCE],
  [policy checks][POLICY-CHECKS] and [discovery][DISCOVERY].
- Target-tag [pack][PACK], [bundle guide][PACK-GUIDE],
  [native plugin consumer][PLUGIN-CONSUMER], [registries][REGISTRIES],
  [HTTP API][API], [OpenAPM status][OPENAPM], [gh-aw guide][GH-AW],
  [shared import][SHARED] and [project governance/roadmap][GOVERNANCE].

**Artifact:** `content\research\updates\1.2\theory.md`.

[CHANGELOG]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/CHANGELOG.md
[INSTALL]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/install.md
[INIT]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/init.md
[UPDATE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/update.md
[OUTDATED]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/outdated.md
[AUDIT]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/audit.md
[BASELINE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/baseline-checks.md
[LOCK]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/lock.md
[LOCKFILE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/lockfile-spec.md
[MANIFEST]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/manifest-schema.md
[PACKAGE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/package-types.md
[TARGETS]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/targets-matrix.md
[HOOKS]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/producer/author-primitives/hooks-and-commands.md
[MCP]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/consumer/install-mcp-servers.md
[SECURITY]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/security.md
[APPROVE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/approve.md
[LIFECYCLE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/lifecycle-scripts.md
[POLICY]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/apm-policy.md
[POLICY-SCHEMA]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/policy-schema.md
[POLICY-REF]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/enterprise/policy-reference.md
[PARSER]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/parser.py
[INHERITANCE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/inheritance.py
[POLICY-CHECKS]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/policy_checks.py
[DISCOVERY]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/src/apm_cli/policy/discovery.py
[PACK]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/cli/pack.md
[PACK-GUIDE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/producer/pack-a-bundle.md
[PLUGIN-CONSUMER]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/consumer/copilot-agent-plugins.md
[REGISTRIES]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/guides/registries.md
[API]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/reference/registry-http-api.md
[OPENAPM]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/specs/openapm-v0.1.md
[GH-AW]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/docs/src/content/docs/integrations/gh-aw.md
[SHARED]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/.github/workflows/shared/apm.md
[GOVERNANCE]: https://raw.githubusercontent.com/microsoft/apm/v0.31.0/GOVERNANCE.md
