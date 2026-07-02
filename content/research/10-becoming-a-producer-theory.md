# Concept Brief — Chapter 10: Becoming a Producer

- **Chapter:** 10 — Becoming a Producer (Part V — Producing & sharing)
- **Objective it serves:** Package and publish reusable APM primitives so other teams can consume
  them through the normal install loop.
- **Focus:** dev-focused (per outline). This is the chapter where the reader **crosses the ramp** —
  from *consuming* other people's packages (Chapters 4–9) to *authoring their own*. The developer
  does the hands-on work; the leader callout is about turning tribal knowledge into a reusable
  platform asset. Keep the body practical and producer-centric.
- **Inspected APM CLI version:** sibling briefs reference **v0.23.1** (official producer docs last
  updated **2026-06-30**). Every feature/file/command tagged `Implemented in APM by:` is a
  conceptual hand-off — the `apm-cli-explorer` must **confirm the exact producer manifest fields,
  `apm pack` output shape, bundle-integrity behavior, and the `apm plugin` / `apm marketplace` /
  `apm publish` verbs empirically against the inspected version**, and the `code-verifier` must run
  the examples. Do not invent manifest keys or CLI flags.
- **Scope guard (do this first):** **Publishing with real credentials is out of scope — no live
  push.** The playbook's out-of-scope list is explicit: "Live publishing with real credentials; no
  secrets in examples" ([playbook §Explicitly out of scope](../playbook-brief.md)). The chapter
  proves the *shape-and-pack* half of producing (author `.apm/`, `apm pack`, install the bundle into
  a scratch repo) and describes distribution/marketplace **conceptually**. Any command that pushes,
  uploads, or needs a private repo is marked `SKIPPED-needs-network`.

## Frame note (which property this chapter feeds)

Producing does **not** add a fifth property. It **flips the reader's role**: everything the book
named as a consumer benefit — portability, reproducibility, provenance/security, governance — the
reader now becomes the *source of* for downstream teams. When Meridian ships `meridian-standards`,
the consumers of that package get:

- **portability** — one manifest compiles the same primitives onto Copilot, Claude Code, and Cursor;
- **reproducibility** — a lockfile plus a pack bundle that pins every file by SHA-256;
- **provenance/security** — a pinned, hashed, reviewable source that passes the same install-time
  scanners from Chapter 8;
- **governance** — the package installs through the same `apm-policy.yml` gate from Chapter 9 (a
  policy can even *require* it, exactly as the running example's `require: meridian-finance/meridian-standards`
  rule does).

The spine sentence lands hard here: this is the moment the reader stops being an *npm user* and
becomes an *npm publisher* — the same manifest/lockfile discipline, now pointed outward. APM states
this symmetry directly: "Every package you publish here installs through the [consumer ramp's]
`apm install` command" ([Producer overview](https://microsoft.github.io/apm/producer/)).

## Prerequisite recap (Chapters 4–9 hand-off)

The reader arrives already fluent in the consumer surface: `apm.yml` as a manifest (Ch4), the daily
install/restore loop (Ch5), the lockfile as the reproducibility contract (Ch6), lifecycle (Ch7),
install-time security (Ch8), and policy (Ch9). Chapter 10 reuses **all of it from the other side**.
The single most important continuity to protect: a producer package is authored with the *exact same
files and verbs* the reader already knows — there is no separate "publishing toolchain." As APM puts
it, "There is no separate 'build pipeline' — the CLI is the build pipeline"
([Producer overview](https://microsoft.github.io/apm/producer/)).

## Terminology & scope notes (read before drafting)

- **"Producer" vs. "consumer" are ramps, not tools.** APM documents three ramps — consumer,
  producer, enterprise — over one CLI ([Producer overview](https://microsoft.github.io/apm/producer/)).
  The chapter is the producer ramp; do not imply a different binary or workflow.
- **The producer ladder has five rungs; this chapter walks two-and-a-half.** The official ladder is:
  (1) author primitives → (2) `apm compile` → (3) `apm preview` / `apm view` → (4) `apm pack` a
  bundle → (5) publish to a marketplace ([Producer overview](https://microsoft.github.io/apm/producer/)).
  Per the outline's mid-level depth, the chapter centers on **rung 1 (shape/authoring)** and
  **rung 4 (`apm pack`)**, then **closes the loop by installing the bundle into a scratch repo**
  (the consumer ramp, seen from the producer's chair). Name compile/preview/marketplace, but don't
  turn the chapter into a reference. "You don't need a marketplace to start. Step 4 is enough for
  internal teams; the marketplace step is for public discovery"
  ([Producer overview](https://microsoft.github.io/apm/producer/)).
- **`apm pack` packs what `apm install` last deployed — not the raw `.apm/` tree.** This is a real
  ordering constraint and a common failure: "If `apm pack` reports 'No deployed files found', your
  `apm.lock.yaml` has no `deployed_files` entries. Run `apm install` first"
  ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). The running example's
  command order (`apm install` → `apm pack --dry-run --verbose`) is correct *because* of this.
- **Author under `.apm/<type>/`, not root convention dirs.** `apm pack` is liberal (it collects from
  both `.apm/<type>/` and root `agents/`, `skills/`, `instructions/`, …), but `apm install` is
  stricter and **does not discover** instructions/prompts/commands from root convention directories —
  so a file that shows up in the bundle can be *silently skipped* on install. The docs warn this can
  "silently remov[e] those guardrails from consumer environments." **Use `.apm/<type>/` for every
  primitive** ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). This is a
  first-class pitfall for the chapter.
- **A "marketplace" is a discovery index over git — not a hosted registry.** APM has no central
  public package registry today; distribution is git-based (any supported host). A marketplace is
  "a curated index of packages that one repo publishes and many repos install from," authored as a
  `marketplace:` block and consumed with `apm marketplace add`
  ([Publish to a marketplace](https://microsoft.github.io/apm/producer/publish-to-a-marketplace/)).
  Frame it as an **emerging discovery layer**, consistent with Chapter 12's "registry gap." Do not
  call it a registry.
- **`apm publish` exists but is not the producer ramp's shipping verb.** The CLI reference lists
  `apm publish` alongside `apm pack` / `apm marketplace`
  ([CLI reference index](https://microsoft.github.io/apm/producer/)); the documented producer flow
  ships via `apm pack` + git + `apm marketplace add`. *Explorer to confirm* what `apm publish` does
  at the inspected version before the author mentions it.

---

## Concepts covered

1. **Copying between repos recreates drift** — once a team has useful prompts/skills/instructions,
   copy-paste reuse silently reintroduces the Chapter 1 problem. Producing turns local conventions
   into *versioned, distributable* packages that carry the same portability, reproducibility, and
   reviewability as any consumer dependency.
2. **A package is just a directory with `apm.yml` + `.apm/`** — the producer/consumer symmetry: what
   the reader *consumed* in Chapters 4–9 is exactly what they now *author*. There is no new artifact
   type and no separate build pipeline.
3. **Package shape & metadata** — a package is identity + optional `type` + the primitives it
   bundles; the producer manifest adds *distribution metadata* (`repository`, `keywords`, `license`,
   `author`, `homepage`, `type`) that a consumer manifest can omit.
4. **Pack & distribute** — `apm pack` produces an *integrity-checked* bundle (every file pinned by
   SHA-256, re-verified on install); distribution is git-based today (directory+git, archive+release,
   or a marketplace index), with marketplaces as an emerging discovery layer.

---

## Concept 1 — Copying between repos recreates drift

**Definition.** *Producing* is the act of extracting agent context that already works in one repo —
a prompt, a skill, an instruction set — into a standalone, versioned APM package that other repos
install through the normal `apm install` loop, instead of copying the files by hand.

**The problem it solves.** Chapter 1 opened on drift: three copies of a review prompt in three home
directories, each checking a different threat model. The uncomfortable truth this chapter names is
that *reuse-by-copy recreates that exact failure*. The moment a second Meridian service copies the
checkout-review prompt into its own repo, the two copies begin to diverge — no shared version, no
lockfile, no review trail, no way to answer "which prompt produced this behavior?" Producing closes
the loop the book opened: the useful convention becomes **one package with one version**, and every
consumer restores the *same bytes* rather than a fork. The reuse carries "the same portability,
reproducibility, and reviewability as consumer dependencies"
([outline, Ch10](../../.source-docs/v2/outline.md); framed against the drift narrative of Chapter 1).

**Key distinctions.**
- *Copy vs. depend.* A copy is a point-in-time snapshot that immediately starts drifting; a
  dependency is a pinned, hashed reference that a lockfile can reproduce and `apm outdated`/`apm
  update` can advance deliberately (Chapters 6–7). Producing converts copies into dependencies.
- *"It works locally" vs. "it's shippable."* Local primitives can rely on paths, tools, or context
  that only exist in the origin repo. Producing forces the author to make the package
  *self-contained* — which is why the chapter ends by **installing the packaged result into a
  scratch repo** to prove it stands alone ([Producer overview](https://microsoft.github.io/apm/producer/):
  "install your own package in a scratch repo before declaring it shipped").

**Common misconception.** *"We already reuse our prompts — we just copy the files."* Copying is the
anti-pattern, not the solution; it is the Chapter 1 drift problem wearing a helpful face. Reuse only
becomes *governed* reuse when it goes through a versioned package.

**Meridian beat (for the author).** A second Meridian service asks for the checkout-review prompt and
fraud instructions. Instead of pasting them into a Slack thread (the Chapter 1 move), the staff
engineer extracts the checkout-review prompt, the fraud-domain engineering instructions, and the
API-review skill into a new package, `meridian-standards`. That is the pivot from consumer to
producer.

**Implemented in APM by:** the producer ramp as the counterpart to the consumer ramp; the same
`apm.yml` + lockfile machinery pointed outward. *Explorer to confirm:* that a produced package,
once installed by a consumer, is pinned and hashed identically to any git-sourced dependency
(no special-casing).

---

## Concept 2 — A package is just a directory with `apm.yml` + `.apm/`

**Definition.** An APM package is, minimally, **a directory containing an `apm.yml` manifest and a
`.apm/` source tree of primitives** — nothing more is required. "An APM package is a directory with
two things: an `apm.yml` manifest and a `.apm/` source tree. Everything else … is generated,
optional, or both" ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
The docs' producer mental model is identical: "A producer package is just a directory with `apm.yml`
… `.apm/` … `README.md`" ([Producer overview](https://microsoft.github.io/apm/producer/)).

**The problem it solves.** It removes the intimidation of "authoring a package." There is no
scaffolding ceremony, no packaging manifest separate from the project manifest, no build config. The
reader already met `.apm/instructions/…` and `.apm/prompts/…` as *consumer* outputs and source; here
those same directories are the *authoring* surface. `.apm/` holds one subdirectory per primitive
type — `skills/`, `prompts/`, `instructions/`, `agents/`, `hooks/` — and `apm compile` (invoked by
`apm install`) "reads `.apm/`, applies any policy, and writes per-target output"
([Author primitives](https://microsoft.github.io/apm/producer/author-primitives/)). The producer and
consumer speak the *same* file language.

**Key distinctions.**
- *Source vs. build output.* `.apm/` is what the author writes and commits; `.github/`, `.claude/`,
  `.cursor/`, `apm_modules/`, and `apm.lock.yaml` are *generated* — "Edit the source under `.apm/`
  and re-run `apm install` — never edit the deployed copy"
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)). This is the same
  source-vs-compiled split from Chapter 3, now the author's responsibility.
- *`.apm/<type>/` is the authoritative source root for install-discovery.* As flagged in the scope
  notes, `apm pack` will also collect root convention directories, but `apm install` may not discover
  them — so authoring under `.apm/<type>/` is the only layout that round-trips through both pack and
  install ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)).
- *Commands ship as prompts.* There is no `.apm/commands/` directory; slash-commands are authored as
  `.apm/prompts/*.prompt.md` ([Author primitives](https://microsoft.github.io/apm/producer/author-primitives/)).
  A useful precision to keep the author from inventing a directory.

**Common misconception.** *"Publishing a package means building an artifact with a special tool."* No
— the package *is* the repo directory; `apm pack` later snapshots it, but the package's canonical
form is source-on-disk. The CLI is the build pipeline; there is no separate one.

**Meridian beat (for the author).** Show `meridian-standards/` as a plain directory: `apm.yml`,
`README.md`, and `.apm/` holding `instructions/meridian-engineering.instructions.md`,
`prompts/checkout-review.prompt.md`, and `skills/secure-payment-review/SKILL.md`. Point out that
every one of those files already existed inside `meridian-checkout` in earlier chapters — producing
is *relocation into a package shape*, not new authoring.

**Implemented in APM by:** the `.apm/<type>/` source convention (`skills/`, `prompts/`,
`instructions/`, `agents/`, `hooks/`); `apm plugin init` to scaffold a fresh package
([Producer overview](https://microsoft.github.io/apm/producer/)); `apm compile` as the deterministic
`.apm/` → per-target transform. *Explorer to confirm:* the exact set of `.apm/` subdirectories
recognized at the inspected version and whether `apm plugin init` is the current scaffold verb.

---

## Concept 3 — Package shape & metadata (identity + type + distribution fields)

**Definition.** A package's manifest carries three layers: **identity** (`name`, `version` — the only
required fields), an optional **content `type`** that constrains what the package contains, and — for
producers — **distribution metadata** (`description`, `author`, `license`, `homepage`, `repository`,
`keywords`) that a private consumer manifest can leave out but a shared package should fill in.
"`name` and `version` are the only required fields"
([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).

**The problem it solves.** A consumer manifest answers "what does *my* repo need?"; a producer
manifest additionally answers "who is this package, where does it come from, and what is it for?" so
that *other people* can evaluate and discover it. The distribution fields are the package's business
card: `repository` and `homepage` give provenance, `license` sets reuse terms, `keywords` feed
discovery, and `author` records ownership. Filling them in is how tribal knowledge becomes a
*catalogable* platform asset rather than an anonymous file drop.

**Key distinctions.**
- *Required vs. optional.* Only `name` + `version` are mandatory; everything else is optional but
  strongly recommended for a shared package ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
- *`type` constrains content.* `type` is one of `instructions`, `skill`, `hybrid`, or `prompts` and
  "Constrains what `.apm/` may contain. Useful for single-purpose packages"
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)). The running
  example's `meridian-standards` mixes instructions + a prompt + a skill, so it is `type: hybrid` —
  a good teaching case for *why* the type exists.
- *`includes: auto` vs. an explicit list.* `includes` is `"auto"` (auto-publish every primitive under
  `.apm/`) or a list of explicit repo paths to publish a subset
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)). The example uses
  `includes: auto`.
- *Manifest fields flow into the bundle's identity card.* `apm pack` maps `apm.yml`'s `name`,
  `version`, `description`, `author`, `license`, `homepage`, `repository`, and `keywords` into the
  bundle's `plugin.json` if you don't author one yourself — "keep `apm.yml` as the source of truth"
  ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). So the metadata you add
  here is what a consumer sees on the other end.
- *`devDependencies` are excluded from the shipped artifact.* Same shape as `dependencies` but "Excluded
  from `apm pack`" ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)) —
  the right home for a producer's test-only tooling.

**Common misconception.** *"A producer manifest is a different schema from a consumer manifest."* It
is the *same* `apm.yml` schema; producers simply populate the optional distribution fields (and often
a `type`) that consumers ignore. The shape "mirrors `package.json` on purpose"
([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)) — a `name`/`version`/
`repository`/`keywords`/`license` block will feel immediately familiar.

**Meridian beat (for the author).** Contrast the two manifests the running example already stages:
`meridian-checkout`'s *consumer* manifest (identity + `dependencies` + `scripts`) versus
`meridian-standards`'s *producer* manifest (identity + `description`, `author: Meridian Platform
Engineering`, `license: MIT`, `repository`, `keywords`, `type: hybrid`, `includes: auto`). Same file,
new fields — because now other teams are the audience.

**Implemented in APM by:** the `apm.yml` field set (`name`, `version`, `description`, `author`,
`license`, `homepage`, `repository`, `keywords`, `type`, `targets`, `includes`, `dependencies`,
`devDependencies`, `scripts`); the `type` enum (`instructions` / `skill` / `hybrid` / `prompts`);
`plugin.json` synthesis from `apm.yml` at pack time. *Explorer to confirm:* the current `type`
values, that `includes: auto` behaves as documented, and the exact metadata fields carried into
`plugin.json` at the inspected version.

---

## Concept 4 — Pack & distribute (integrity-checked bundle; git-based distribution)

**Definition.** `apm pack` snapshots the files your last `apm install` deployed into a portable,
**integrity-checked bundle** — a `plugin.json`, your primitive folders, and an *embedded*
`apm.lock.yaml` that "pins every file by SHA-256" — that a consumer installs with `apm install
<bundle>`, bypassing the git resolver entirely
([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). Distribution of that
result is **git-based**: commit the directory, attach an archive to a release, or list it in a
marketplace index.

**The problem it solves.** A package's *source* lives in git, but two other needs arise: (1) shipping
to an environment that can't reach the source repo (offline, air-gapped, a customer hand-off), and
(2) *guaranteeing* the recipient gets exactly what the producer built. `apm pack` solves both: it
produces a single artifact you can move by any channel, and it makes tampering detectable. "`apm
pack` writes `pack.bundle_files` into the embedded `apm.lock.yaml` — a mapping of every file's
relative path to its SHA-256 digest. On the consumer side, `apm install <bundle>` rehashes every
file and rejects the bundle if: any hash does not match · any listed file is missing · any file is
present but not listed · any path is a symlink … Tampering after pack time is detected before any
file lands in the project" ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)).
This is the Chapter 6 lockfile guarantee and the Chapter 8 content-hash pinning, now attached to the
*producer's* artifact.

**Key distinctions.**
- *Bundle vs. marketplace.* A **bundle** (`apm pack`) is enough for internal/offline sharing; a
  **marketplace** is an optional discovery index for many-repo consumption. "You don't need a
  marketplace to start" ([Producer overview](https://microsoft.github.io/apm/producer/)).
- *Three git-based distribution paths.* (1) directory + git — commit `build/<pkg>/`, consumers
  `apm install ./build/<pkg>`; (2) archive + release — `apm pack --archive` (a `.zip` by default,
  natively extractable on Windows), upload as a release asset, consumers
  `apm install ./<pkg>-<version>.zip`; (3) marketplace entry — with a `marketplace:` block, `apm
  pack` also writes `marketplace.json` ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)).
- *Directory vs. archive output.* Default `apm pack` writes a plugin-format directory under
  `./build/`; `--archive` produces a single `.zip` (`--archive-format tar.gz` for legacy CI); `-o`
  changes the output location ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)).
- *Marketplace = discovery over git, not a hosted registry.* Authored as a `marketplace:` block
  (`apm marketplace init --owner …`), built into `marketplace.json` by `apm pack`, registered by a
  consumer with `apm marketplace add <owner>/<repo>`, then installed as `apm install
  <pkg>@<marketplace>`. The generated `.claude-plugin/marketplace.json` is "byte-compatible with
  Anthropic's marketplace.json so Claude Code, Copilot CLI, and APM all read the same artefact"
  ([Publish to a marketplace](https://microsoft.github.io/apm/producer/publish-to-a-marketplace/)).
  Any supported git host works (GitHub.com, GitHub Enterprise, GitLab, Azure DevOps).
- *`apm pack` is not the policy gate.* Consistent with Chapter 9, `apm pack` "enforce[s] zero policy"
  — the governance gate is on the *consumer's* `apm install`
  ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). Producing an
  approved package and *governing* who may install it are separate concerns.

**Common misconception.** *"`apm pack` bundles my `.apm/` source."* It bundles the **deployed** files
from your last `apm install`, not the raw source tree — which is why you must `apm install` before
you pack, and why `apm pack --dry-run --verbose` (list every file first) is the recommended
pre-flight ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). A second
misconception: *"publishing needs a central registry."* There is none today; distribution is git, and
a marketplace is a discovery index layered on top — the "registry gap" Chapter 12 discusses.

**Meridian beat (for the author).** The running example's command order is deliberate and correct:
`apm install` (populate deployed files) → `apm pack --dry-run --verbose` (verify the file list) →
`apm pack --archive -o dist` (marked `SKIPPED-needs-network` because it produces a release asset).
Then the payoff: add `meridian-finance/meridian-standards#v1.0.0` to `meridian-checkout`'s
`dependencies.apm` and install it — the extracted conventions come *back in* as a governed dependency,
and the policy from Chapter 9 can now `require` that exact package.

**Implemented in APM by:** `apm pack` (directory + `--archive` / `--archive-format` / `-o` /
`--dry-run --verbose`); the embedded `apm.lock.yaml` `pack.bundle_files` SHA-256 map and its
verification on `apm install <bundle>`; `plugin.json` as the bundle identity card; `apm marketplace
init` / the `marketplace:` block / `apm marketplace add` for the discovery layer; `apm publish` (role
to be confirmed). *Explorer to confirm:* the exact `apm pack` default output path and success line,
the archive default/format flags, the bundle-rejection conditions, and the `apm marketplace` verb set
at the inspected version — and to run the pack/scratch-install loop end to end (no live push).

---

## Sources

Producer-ramp docs first, then supporting concept/reference and repo pages actually used:

- Producer overview — the ramp, the five-rung ladder, the "just a directory" mental model, and the
  consumer-symmetry / scratch-repo test: <https://microsoft.github.io/apm/producer/>
- Author primitives — primitive types and the `.apm/<type>/` on-disk layout:
  <https://microsoft.github.io/apm/producer/author-primitives/>
- Pack a bundle — `apm pack` output, `plugin.json` contract, SHA-256 bundle integrity, distribution
  paths, `.apm/<type>/` discovery pitfall, `--dry-run --verbose`:
  <https://microsoft.github.io/apm/producer/pack-a-bundle/>
- Publish to a marketplace — `marketplace:` block, `apm marketplace init` / `add`, marketplace.json
  compatibility, git-based distribution: <https://microsoft.github.io/apm/producer/publish-to-a-marketplace/>
- Package anatomy — minimal package, full file tree, `apm.yml` field reference (`type`, `includes`,
  distribution metadata), source-vs-build split:
  <https://microsoft.github.io/apm/concepts/package-anatomy/>
- Governance deep-dive — `apm pack` enforces zero policy; the gate is the consumer's install:
  <https://microsoft.github.io/apm/enterprise/governance-guide/>
- The three promises — portable/secure/governed framing the producer inherits:
  <https://microsoft.github.io/apm/concepts/the-three-promises/>
- microsoft/apm repository — sample package (`microsoft/apm-sample-package`) and CLI verbs:
  <https://github.com/microsoft/apm>

## Artifact path

`content/research/10-becoming-a-producer-theory.md`
