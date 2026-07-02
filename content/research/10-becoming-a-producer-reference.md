# Chapter 10 — Becoming a Producer · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 10 turns the reader from **consumer** into **producer**. The consumer ramp
> (Ch 4–9) answered *"how do I install and govern someone else's context?"* Chapter 10 answers the
> inverse: *"how do I extract my repo's conventions into a package other teams install through the
> same loop?"* This reference proves, empirically against **apm v0.23.1**, the **producer package
> shape** apm actually accepts, the **manifest keys** it reads (and the one the running example
> assumes that is **real-but-inert**), the **`apm pack` routing** (bundle vs marketplace vs
> plugin.json vs *"Nothing to pack"*), and the **`apm plugin init` / `apm marketplace init` /
> `apm publish`** producer commands. The crux — the running example's `apm pack --archive -o dist`
> line — is **corrected against the live CLI**: for a primitives-only package (targets, no
> `dependencies:`) `apm pack` writes **plugin.json manifests in-tree**, not an archive, so
> `--archive -o dist` produces nothing.
> **Concept it implements (Ch10 theory):** **producing & sharing** — the "producer ladder" (author →
> compile → preview → pack → publish) that closes the four-properties loop by making *provenance* a
> first-class, versioned artifact. Anchors to
> [`10-becoming-a-producer-theory.md`](10-becoming-a-producer-theory.md) **(brief pending at time of
> writing — concepts below are anchored to the outline objective, the Meridian beat in
> `.source-docs/v2/running-example.md`, and the official [Producer ramp](https://microsoft.github.io/apm/producer/)).**
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`, confirmed at session start).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dir (outside repo):**
> `%TEMP%\apm-ch10` with sub-projects: `meridian-standards` (the producer package — the star of the
> chapter), `initprobe` / `pluginprobe` / `mktprobe` (scaffold shape probes), `keyprobe`
> (unknown-vs-reserved key probe), `consumer` (the offline round-trip), `notargets` (pack-routing
> probe).
> **Network:** available, but **no pushes**. The offline producer→consumer round-trip is done with a
> **local-path source install** (fully offline, proven below). Everything that pushes to a git remote,
> uploads to a registry, or resolves a remote dependency closure is marked
> **`SKIPPED-needs-network`**.
> **Preview flags:** `apm publish` requires the **`registries` experimental feature** (disabled by
> default); `apm marketplace`'s deeper authoring commands are gated behind `marketplace-authoring`
> (also experimental). The **manifest schema** the CLI implements is the **v0.3 Working Draft**
> ([Manifest schema](https://microsoft.github.io/apm/reference/manifest-schema/)) — "it may be
> updated, replaced, or made obsolete at any time." Every claim below is pinned to **v0.23.1**.

---

## Theory anchors (Chapter 10 — Producing & sharing)

> The Ch10 theory brief was not yet written when these notes were produced. The anchors below map the
> producer concepts (from the outline objective + the Meridian beat + the docs "producer ladder") to
> what the CLI confirmed. Re-link to numbered concepts once
> [`10-becoming-a-producer-theory.md`](10-becoming-a-producer-theory.md) lands.

| Producer concept | What it establishes | Confirmed here by |
|---|---|---|
| **Extraction / DRY reuse** | The consumer's local `.apm/` conventions become a shared, installable package — write once, install everywhere. | `meridian-standards` = the Meridian instruction + review prompt + secure-payment skill lifted out of `meridian-checkout` into a standalone package that installs through the **same** `apm install` loop (Ch5). |
| **The package *is* a directory** | A producer package is "just a directory with `apm.yml` + `.apm/` primitives + `README.md`" ([Producer mental model](https://microsoft.github.io/apm/producer/)). No build system; the CLI is the build pipeline. | `apm install` on the tree auto-discovered all three primitives via `includes: auto` and compiled them to every target — no packaging step required to consume it. |
| **The producer ladder** | Five ordered rungs: **author → compile → preview/validate → pack → publish** ([Producer ramp](https://microsoft.github.io/apm/producer/)). Step 4 (a bundle) is enough for internal teams; step 5 (marketplace/registry) is for public discovery. | `apm plugin init` scaffolds rung 1; `apm install`/`apm compile` do rung 2; `apm pack --dry-run` is rung 3–4; `apm marketplace init` + `apm publish` are rung 5. |
| **Provenance becomes a versioned artifact** | Producing closes the four-properties loop: the same manifest/lockfile/policy machinery now describes *what you ship*, and consumers get content-hash integrity on the way in. | `apm pack` embeds an `apm.lock.yaml` with `pack.bundle_files` (path→SHA-256) that `apm install <bundle>` re-hashes and rejects on mismatch/missing/extra/symlink ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). |
| **Distribution channels** | git ref · local bundle · marketplace · registry — four ways to hand a package off, each with different reach/trust. | Verified the **git** and **local-path** shapes; **bundle**, **marketplace**, and **registry/`publish`** paths are documented + partially probed and marked `SKIPPED-needs-network` where they push/resolve remotely. |

> **Frame note.** Chapters 4–9 built the *consumer* half of the four properties. Chapter 10 is the
> mirror: the producer authors portability (targets), reproducibility (lockfile/pack integrity),
> provenance (versioned package + SBOM license), and hands governance (Ch9 policy) a *new dependency*
> for the org to allow-list. Keep the vocabulary crisp: **a producer package ships primitives; it does
> not ship a running agent.**

---

## Command surface (v0.23.1) — confirmed via `--help`

| Command / flag | Job | Notes (confirmed) |
|---|---|---|
| `apm pack` | Pack distributable artifacts from `apm.yml` | **Routing is by manifest block** (see the pack section). `--format [plugin\|apm]` (plugin default), `--archive` (+`--archive-format [zip\|tar.gz]`, zip default), `-o/--output PATH` (**default `./build`**, *not* `dist`), `--dry-run`, `--force`, `-v/--verbose`, `--offline`, `-m/--marketplace`, `--check-versions`, `--check-clean`, `--json`. Exit codes **0/1/2/3/4**. |
| `apm plugin init [NAME]` | Scaffold a plugin (creates `plugin.json` + `apm.yml`) | Flags `-y/--yes`, `--target TARGET` (comma list), `-v`. Adds a **`devDependencies:`** block. Offline. |
| `apm marketplace init` | Add a `marketplace:` block to `apm.yml` (scaffolds `apm.yml` if missing) | Flags `--force`, `--no-gitignore-check`, `--name`, `--owner`, `-v`. Offline. `apm pack` then emits `.claude-plugin/marketplace.json`; consumers `apm marketplace add`. |
| `apm publish` | Publish a package to a **REST registry** | **Requires `apm experimental enable registries`** (disabled by default). Packs a *flat registry zip* (`apm.yml` + `.apm/` at root — **not** the `apm pack` plugin bundle), uploads via `PUT /v1/packages/{owner}/{repo}/versions/{version}`. Flags `--package OWNER/REPO` **[required]**, `--registry`, `--zip`, `--dry-run`, `-v`. **`SKIPPED-needs-network`.** |
| `apm unpack <BUNDLE>` | **[Deprecated]** extract an APM bundle | Help says: *"Use `apm install <bundle-path>` instead — this command will be removed."* Prefer `apm install <bundle>` for the consume side of a bundle. |
| `apm marketplace add\|list\|browse\|update\|remove\|validate` | Consumer-side marketplace registration/discovery | The consume side of a marketplace; remote registration is `SKIPPED-needs-network`. |

> The producer verbs the outline lists — `apm pack`, `apm plugin init`, `apm marketplace init`,
> `apm marketplace add` — all exist at v0.23.1. There is **no** `apm package publish` or standalone
> `apm bundle`; packing is `apm pack`, registry publish is `apm publish`.

---

## The CONFIRMED producer manifest schema (v0.23.1)

The `meridian-standards` manifest was authored with **every key the running example uses**, then each
key was checked against (a) the fresh `apm init` template, (b) the synthesised `plugin.json` that
`apm pack` writes, (c) the SBOM/pack warnings, and (d) the
[Manifest schema §3](https://microsoft.github.io/apm/reference/manifest-schema/) (v0.3 Working Draft).
**Two fields are REQUIRED at parse time — `name` and `version`. All others are OPTIONAL, and unknown
top-level keys are *preserved but ignored*** (schema §2).

```yaml
name: meridian-standards          # REQUIRED · package identifier
version: 1.0.0                    # REQUIRED · semver (non-semver -> non-blocking warning)
description: ...                  # OPTIONAL · human tagline; inherited by marketplace: block; pack warns if missing
author: Meridian Platform Engineering  # OPTIONAL · string -> {name: "..."} in plugin.json
license: MIT                      # OPTIONAL · SPDX; recorded as declared_license in the lockfile & SBOM
repository: https://github.com/meridian-finance/meridian-standards  # read by pack -> plugin.json
keywords: [meridian, checkout, fintech, ai-agents]                   # read by pack -> plugin.json (also marketplace tags)
type: hybrid                      # REAL enum, but RESERVED/INERT at v0.23.1 (see trap below)
targets: [copilot, claude, cursor]  # plural alias of `target`; drives compile + pack routing; values are validated
includes: auto                    # consent to publish all .apm/ content (default for new projects)
```

### Key-acceptance table (the headline)

| Manifest key | Verdict at v0.23.1 | Evidence |
|---|---|---|
| `name` | ✅ **REQUIRED, real** | schema §3.1; `apm init`; `plugin.json.name` |
| `version` | ✅ **REQUIRED, real** (semver pattern) | schema §3.2; `apm init`; `plugin.json.version` |
| `description` | ✅ **real** | schema §3.3; `plugin.json.description`; `apm pack` warns if missing |
| `author` | ✅ **real** (string → `{name}`) | schema §3.4; `plugin.json.author` = `{ "name": "Meridian Platform Engineering" }` |
| `license` | ✅ **real** (SPDX) | schema §3.5; `plugin.json.license`; **omitting it triggers** `"No 'license:' field … SBOM will record NOASSERTION"` (verified in bundle mode) |
| `repository` | ✅ **real** (pack → plugin.json) | not enumerated in schema §3 but **mapped by pack**; `plugin.json.repository` present |
| `keywords` | ✅ **real** (pack → plugin.json) | mapped by pack; `plugin.json.keywords` = the 4-item list |
| `targets` | ✅ **real** (plural alias of `target`) | schema §3.6; `apm init` emits it; drives compile **and** pack routing; **unknown target values raise a parse error** (unlike unknown top-level keys) |
| `includes: auto` | ✅ **real** (the default) | schema §3.9; `apm init` default; auto-discovered all 3 primitives on install |
| **`type: hybrid`** | ⚠️ **REAL enum, RESERVED/INERT** — *not* a bug, *not* a typo | schema §3.7: allowed values `instructions \| skill \| hybrid \| prompts`; *"behaviour is driven by package content … this field is **reserved for future explicit overrides**."* Absent from `plugin.json`; behaves as a no-op at v0.23.1. |
| *(unknown key, e.g. `zzz_bogus`)* | 🔸 **silently ignored** (preserved, no error) | schema §2; probe added `zzz_totally_bogus_key: true` → **no warning, exit 0** |

> **The `type` trap — distinct from the Ch9 `targets` trap.** In Ch9, a top-level `targets:` key in
> `apm-policy.yml` was a genuine *mistake* (the real key is `compilation.target.allow`) that apm
> silently ignored. Here, `type: hybrid` is the **opposite**: it is a **real, documented enum value**
> that is simply **reserved / not yet acting** at v0.23.1 (package behaviour is inferred from content —
> presence of `SKILL.md`, `.apm/<type>/` dirs, etc.). So it is *harmless and forward-looking* to keep,
> but the author must **not claim it changes any behaviour today**. The honest one-liner:
> **`type` is recognised-but-inert; an unknown key is unrecognised-but-preserved; both are no-ops at
> v0.23.1, for different reasons.**

The verified package tree and its manifest are committed at
[backend/examples/ch10/meridian-standards/](../../backend/examples/ch10/meridian-standards/) with a
[README](../../backend/examples/ch10/README.md) documenting reproduction.

---

## DIFF: running-example assumed shape → CONFIRMED v0.23.1 behavior

The running example's Chapter 10 (`.source-docs/v2/running-example.md`) is close, but two lines are
load-bearing and need correction; a third is a *reserved-key* nuance.

| Running-example line | Verdict (v0.23.1) | Correction / note |
|---|---|---|
| Producer package tree (`apm.yml` + `.apm/{instructions,prompts,skills}` + `README.md`) | ✅ **Correct** | Matches the docs "producer mental model" exactly; `apm install` auto-discovered all three via `includes: auto`. |
| `name` / `version` / `description` / `author` / `license` / `repository` / `keywords` | ✅ **All accepted** | `license`, `repository`, `keywords` flow into the synthesised `plugin.json`; `license` also drives the SBOM. |
| `targets: [copilot, claude, cursor]` / `includes: auto` | ✅ **Correct** | Real keys; `includes: auto` is the `apm init` default. |
| **`type: hybrid`** | ⚠️ **Real but inert** | Keep it (documented enum, matches the default synthesis), but it has **no effect** at v0.23.1 — behaviour is inferred from content. Do not teach it as "this makes it a hybrid package." |
| **`apm pack --archive -o dist`** (expected to "create a shareable archive") | ❌ **Misleading for this package** | `meridian-standards` has **no `dependencies:` block**, so `apm pack` is in **plugin.json mode**: it writes `.github/plugin/plugin.json` + `.claude-plugin/plugin.json` **in-tree** and creates **nothing in `dist`**. `--archive`/`-o` are inert here. Also the default output dir is **`./build`, not `dist`**. To get an actual **`.zip` bundle** the package needs a `dependencies:` closure (and **remote** deps — local paths are rejected). |
| "creates a shareable archive for private release assets" (comment) | ⚠️ **Partly** | True for a *bundle-mode* package (deps block) → `apm pack --archive` → `build/<pkg>-<version>.zip`. For `meridian-standards`, the real distribution is **git** (`apm install meridian-finance/meridian-standards#v1.0.0`) or a **marketplace/registry** — all `SKIPPED-needs-network`. |

**Proof (verbatim, `meridian-standards`, which sets `targets:` but no `dependencies:`):**

```text
$ apm pack --archive -o dist --verbose
[+] Generated plugin manifest: …\.github\plugin\plugin.json
[+] Generated plugin manifest: …\.claude-plugin\plugin.json
# dist/ : EMPTY.  No bundle. No .zip.
```

```text
# Same package with targets: removed (no deps, no marketplace, no target):
$ apm pack --verbose
Error: apm.yml has neither 'dependencies:' nor 'marketplace:' block, and 'target:'
does not include 'claude' or 'copilot'. Nothing to pack.        # exit 1
```

---

## `apm pack` — routing, outputs, and pitfalls (the core producer command)

**Implements:** the *pack* rung of the producer ladder — turning authored primitives into a
distributable artifact with content-hash integrity.

### Routing is decided by which blocks `apm.yml` declares (verified via the "Nothing to pack" error)

| `apm.yml` contains… | `apm pack` produces | Output location |
|---|---|---|
| `dependencies:` block | a **bundle** (plugin.json + primitive dirs + embedded `apm.lock.yaml`) | `./build/<pkg>/` (dir) or `<-o>/<pkg>-<version>.zip` with `--archive` |
| `marketplace:` block | **marketplace artifact(s)** | `.claude-plugin/marketplace.json` (default) |
| `target:`/`targets:` **includes `claude` or `copilot`** | **plugin.json manifest(s)** (no bundle) | in-tree: `.claude-plugin/plugin.json` (claude), `.github/plugin/plugin.json` (copilot) |
| both `dependencies:` + `marketplace:` | **bundle + marketplace artifacts** | as above, combined |
| none of the above | **"Nothing to pack"** | exit 1 |

> **`meridian-standards` lands in row 3** (targets incl. copilot + claude, no deps) → **plugin.json
> mode**. `cursor` is in `targets:` but gets **no** plugin.json — the plugin.json contract is
> claude/copilot-specific.

### `--dry-run --verbose`
- **Reports what *would* be written without touching disk.** For `meridian-standards`:
  `"Would write plugin manifest to …\.github\plugin\plugin.json"` and the `.claude-plugin` path.
- In **bundle mode** it lists **every file + any path remappings** — the docs' recommended
  pre-share check. (*"Any instruction or prompt you expect to be included should appear there before
  you share the bundle."*)

### `--archive` / `-o`
- `--archive` → a single archive; **`.zip` by default** (Windows-native extract), `--archive-format tar.gz`
  for legacy CI. `-o` changes the output dir (**default `./build`**).
- **Only meaningful in bundle mode.** On `meridian-standards` (plugin.json mode) they are inert — no
  archive is produced. This is the running-example correction.

### The synthesised `plugin.json` (what pack writes for `meridian-standards`)
```json
{
  "name": "meridian-standards",
  "version": "1.0.0",
  "description": "Shared Meridian engineering instructions, prompts, and review skills.",
  "author": { "name": "Meridian Platform Engineering" },
  "license": "MIT",
  "repository": "https://github.com/meridian-finance/meridian-standards",
  "keywords": ["meridian", "checkout", "fintech", "ai-agents"]
}
```
Mapped from `apm.yml`: `name` (required) · `version` · `description` · `author` · `license` ·
`homepage` · `repository` · `keywords` ([plugin.json contract](https://microsoft.github.io/apm/producer/pack-a-bundle/)).
`type` is **not** carried into `plugin.json`.

### Bundle-mode integrity (documented; the round-trip needs remote deps → `SKIPPED-needs-network`)
`apm pack` writes `pack.bundle_files` (path → SHA-256) into the bundle's embedded `apm.lock.yaml`.
`apm install <bundle>` **rehashes every file** and rejects the bundle on: any hash mismatch, any
listed file missing, any extra file not listed, or any symlink. *"You do not configure this — it runs
on every `apm install <bundle>`."*

### Exit codes (from `--help`)
`0` success · `1` build/runtime error · `2` manifest schema validation error · `3` version alignment
failed (`--check-versions`) · `4` marketplace working-tree drift (`--check-clean`).

### Pitfalls (verified + documented)
- **`--target` is deprecated.** *"Bundles are now target-agnostic; the consumer's project decides
  where files land at install time."* The value is recorded in `pack.target` as metadata only and
  **ignored by `apm install`**. Don't set it.
- **`--format apm` is legacy and `apm install` REJECTS it** (no `plugin.json`). Use the default
  `--format plugin`; repack legacy artifacts with `apm pack --format plugin --archive`.
- **"No deployed files found" / "Nothing to pack" → run `apm install` first.** `apm pack` packs the
  files your **last install deployed** (from the lockfile), not the raw `.apm/` tree.
- **Bundle mode rejects local-path dependencies (verified).**
  `Error: Cannot pack — apm.yml contains local path dependency … Local dependencies are for
  development only. Replace them with remote references (e.g., 'owner/repo') before packing.` → a real
  bundle needs **remote** deps → **`SKIPPED-needs-network`**.

**Minimal verified example:** [backend/examples/ch10/meridian-standards/apm.yml](../../backend/examples/ch10/meridian-standards/apm.yml)
(plugin.json mode). Reproduced with `apm install` then `apm pack --dry-run --verbose`.

---

## `apm plugin init` — scaffold a producer package

**Implements:** rung 1 of the producer ladder (author). Fastest way to a valid producer skeleton.

- `apm plugin init -y --target copilot` created **`apm.yml` + `plugin.json`** (exit 0). The `apm.yml`
  is the standard template **plus a `devDependencies:` block**:
  ```yaml
  name: pluginprobe
  version: 0.1.0
  description: APM project for pluginprobe
  author: Maxim Salnikov          # auto-filled from git/system identity
  targets: [copilot]
  dependencies: { apm: [], mcp: [] }
  includes: auto
  devDependencies: { apm: [] }    # dev-only deps; EXCLUDED from plugin bundles
  scripts: {}
  ```
- **`devDependencies`** (schema §5): installed locally by a bare `apm install`, but **excluded from
  the plugin bundle** `apm pack` produces. Add with `apm install --dev owner/repo`. Use a local-path
  devDependency to keep maintainer-only primitives out of shipped artifacts.
- **When to use:** starting a brand-new package from scratch. **When not to:** you already have an
  `apm.yml` (use `apm init` or hand-author); it defaults `version` to `0.1.0` (vs `1.0.0` for
  `apm init`) and pre-writes a root `plugin.json` you may not want to hand-maintain.
- **Network:** none. Fully offline.

---

## `apm marketplace init` — add a marketplace authoring block

**Implements:** rung 5 (publish/discovery), authoring side. Turns a repo into a **marketplace** that
lists one or more packages for `apm marketplace add` consumers.

- `apm marketplace init --name meridian-marketplace --owner meridian-finance` added a
  **`marketplace:` block** to `apm.yml` (exit 0):
  ```yaml
  marketplace:
    owner: { name: meridian-finance, url: https://github.com/meridian-finance }
    build: { tagPattern: "v{version}" }
    outputs: { claude: {} }          # codex optional; each output writes its profile-default path
    packages:
      - name: example-package
        description: Human-readable description of the package
        source: meridian-finance/example-package
        version: "^1.0.0"            # or ref:, subdir:, tag_pattern:, include_prerelease:, category:
  ```
- `apm pack` then generates `.claude-plugin/marketplace.json` (add `codex` for
  `.agents/plugins/marketplace.json`). Consumers reach it with `apm marketplace add`.
- **Unknown keys inside `marketplace:` are REJECTED at parse time** (schema §7.2) — *stricter* than
  the top-level manifest, which silently ignores unknowns. Good trap to mention.
- **When to use:** you curate several packages for discovery. **When not to:** a single internal
  package — a git ref or a bundle is simpler; a marketplace adds a manifest to maintain.
- **Network:** `init` itself is **offline** (verified). **Caveat:** the `marketplace-authoring`
  experimental flag is *disabled* by default yet `init` ran fine — so `init`/`add` work without it,
  but deeper authoring subcommands (`build`, `publish`, …) may require
  `apm experimental enable marketplace-authoring`. Resolving `packages[].source` against remotes is
  **`SKIPPED-needs-network`**.

---

## `apm publish` — publish to a REST registry (SKIPPED-needs-network)

**Implements:** rung 5 (publish), registry side — the *"install with a version selector from a
central service"* future of APM (OpenAPM v0.2 registry roadmap).

- **Gated behind an experimental feature (verified):**
  ```text
  $ apm publish --package meridian-finance/meridian-standards --dry-run
  Error: apm publish requires the experimental registries feature.
  Enable with: apm experimental enable registries.
  ```
  `apm experimental list` shows **`registries  disabled`** by default.
- Once enabled, `publish` **packs a *flat registry zip*** (`apm.yml` + `.apm/` at the archive root —
  **not** the `apm pack` plugin bundle) and **uploads** via
  `PUT /v1/packages/{owner}/{repo}/versions/{version}`. Flags: `--package OWNER/REPO` **[required]**,
  `--registry` (when multiple configured), `--zip` (pre-built), `--dry-run`, `-v`.
- **When to use:** an org running an APM registry proxy (Ch11) that wants semver-range installs.
  **When not to:** most teams — a **git ref is the zero-infra distribution channel** and needs no
  registry.
- **Network + preview:** uploading is **`SKIPPED-needs-network`**; the feature is **experimental** and
  the registry HTTP API is a **v0.2 working draft** — pin the CLI before depending on it.

---

## The producer → consumer round-trip

### ✅ Proven **offline** — local-path source install
From a fresh `consumer` repo (`apm init -y --target copilot`):
```powershell
apm install "$env:TEMP\apm-ch10\meridian-standards"
```
```text
[*] Validating 1 package...
[+] …\meridian-standards
[>] Resolving …\meridian-standards...
  |-- 1 prompts integrated -> .github/prompts/
  |-- 1 instruction(s) integrated -> .github/instructions/
  |-- 1 skill(s) integrated -> .agents/skills/
[*] Installed 1 APM dependency in 1.4s.        # exit 0
```
- apm added the package to `dependencies.apm` (as an **absolute local path**), resolved its `.apm/`
  **source** primitives (ignoring the producer's own compiled `.github`/`.claude`/`.cursor`), deployed
  them to the consumer's copilot target, and cached the package under `apm_modules/_local/`.
- **Caveat for the committed manifest:** the recorded dep is a machine-specific **absolute path**. For
  a portable/committable manifest, use a **relative `./` path** (dev-only) or, for the real story, a
  **git ref** — `meridian-finance/meridian-standards#v1.0.0` — which is **`SKIPPED-needs-network`**.

### ⏭ `SKIPPED-needs-network` — the remote paths
- **Git (the primary APM channel):** push `meridian-standards` to
  `github.com/meridian-finance/meridian-standards`, tag `v1.0.0`, then
  `apm install meridian-finance/meridian-standards#v1.0.0` in `meridian-checkout`.
- **Bundle:** requires a `dependencies:` closure with **remote** refs (local rejected) →
  `apm pack --archive` → `build/<pkg>-<version>.zip` → `apm install ./<pkg>-<version>.zip`
  (or the deprecated `apm unpack`). Integrity is verified from `pack.bundle_files`.
- **Registry:** `apm publish` (experimental + upload).

---

## Caveats for the author + verifier

1. **Correct the running example's pack line.** For `meridian-standards`, `apm pack --archive -o dist`
   produces **plugin.json manifests in-tree, nothing in `dist`**. Teach the **routing table**: a
   *bundle* needs a `dependencies:` block; a *plugin.json* needs `targets:` incl. claude/copilot; a
   *marketplace.json* needs a `marketplace:` block; otherwise **"Nothing to pack."**
2. **`type: hybrid` is real but does nothing at v0.23.1.** Keep it (documented, forward-looking,
   matches the default synthesis) but **do not** claim it changes install/compile behaviour. Behaviour
   is inferred from package content today.
3. **Two required keys only** (`name`, `version`); unknown top-level keys are silently preserved. But
   **`targets:`/`target:` values ARE validated** (a bad target name is a parse error) and **unknown
   keys inside `marketplace:` are rejected** — the strictness is uneven; state it.
4. **`--target` on `apm pack` is deprecated; `--format apm` is legacy and un-installable.** Default
   `--format plugin` is the only bundle format `apm install` accepts.
5. **`apm install` first, always.** Pack reflects the *last install's* deployed files; a stale/empty
   lockfile yields "No deployed files"/"Nothing to pack".
6. **Bundle round-trip needs the network** (remote deps; local paths rejected at pack). The offline
   round-trip in the chapter must use the **local-path source install** shown above, and the manifest
   note about absolute-vs-relative-vs-git paths must be included.
7. **`apm publish` = experimental (`registries`) + upload + v0.2 draft** → keep every publish step
   `SKIPPED-needs-network` and preview-flagged.
8. **`apm unpack` is deprecated** — prefer `apm install <bundle>` for the consume side.
9. **Verifier reproduction:** the committed package is
   [backend/examples/ch10/meridian-standards/](../../backend/examples/ch10/meridian-standards/); run
   `apm install` then `apm pack --dry-run --verbose` (both offline, exit 0). No lockfile is committed
   for the producer sample — it has no dependency closure, so its lock records only environment-
   specific compiled-file hashes (documented in the sample README).

---

## Artifacts written & commands run

**Artifacts (this session):**
- **This reference:** [content/research/10-becoming-a-producer-reference.md](10-becoming-a-producer-reference.md)
- **Verified producer package:** [backend/examples/ch10/meridian-standards/](../../backend/examples/ch10/meridian-standards/)
  (`apm.yml`, `README.md`, `.apm/instructions/…`, `.apm/prompts/…`, `.apm/skills/secure-payment-review/SKILL.md`,
  `plugin.json.generated`)
- **Sample README (reproduction):** [backend/examples/ch10/README.md](../../backend/examples/ch10/README.md)

**Commands run (all PATH-refreshed; `%TEMP%\apm-ch10`; public only, no pushes):**
```text
apm --version                                   # 0.23.1
apm --help ; apm pack --help ; apm publish --help
apm plugin --help ; apm plugin init --help ; apm marketplace --help ; apm marketplace init --help ; apm unpack --help
apm init -y --target copilot                    # initprobe -> canonical template (includes: auto default)
apm install                                     # meridian-standards -> lockfile + compiled targets
apm pack --dry-run --verbose                    # -> "Would write … plugin.json" (no bundle)
apm pack --archive -o dist --verbose            # -> plugin.json in-tree; dist EMPTY
apm pack --format apm --archive -o dist         # -> still no bundle (no deps)
apm install                                     # keyprobe (type: hybrid + zzz_bogus) -> no warning, exit 0
apm plugin init -y --target copilot             # pluginprobe -> apm.yml (+devDependencies) + plugin.json
apm marketplace init --name … --owner …         # mktprobe -> marketplace: block
apm install "<local meridian-standards>"        # consumer -> offline round-trip, exit 0
apm pack --format apm --archive -o dist         # consumer -> REJECTS local-path dep; SBOM license warning
apm publish --package … --dry-run               # -> requires `apm experimental enable registries`
apm experimental list                           # registries=disabled, marketplace-authoring=disabled
apm pack --verbose --force                      # meridian-standards clean re-test -> plugin.json only
apm pack --verbose                              # notargets probe -> "Nothing to pack" (exit 1)
```
