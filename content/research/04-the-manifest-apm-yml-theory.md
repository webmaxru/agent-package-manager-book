# Concept Brief — Chapter 4: The Manifest (apm.yml)

- **Chapter:** 4 — The Manifest: apm.yml (Part II — Portable by manifest)
- **Objective it serves:** Author a valid `apm.yml` that declares Meridian's first shared agent-context
  dependencies — starting from one locally-authored instruction, targeting Copilot, Claude Code, and Cursor.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30; the Manifest Schema page is
  labelled "v0.3 Working Draft," dated 2026-05-20). Every `Implemented in APM by:` line names conceptual
  hand-offs — the `apm-cli-explorer` confirms the exact keys, forms, and defaults, and the `code-verifier`
  runs the resulting manifest. Because APM is pre-1.0 and the schema is a Working Draft, the author must
  re-verify shapes before publication ([Manifest Schema](https://microsoft.github.io/apm/reference/manifest-schema/)).
- **Frame note (which property this chapter feeds).** This is the chapter where **portability** stops being a
  slogan and becomes a file. APM's first promise is "portable by manifest"
  ([README / three promises](https://github.com/microsoft/apm)); `apm.yml` is the artifact that promise names.
  The manifest also *seeds* the other three properties without yet delivering them: it is the input the
  lockfile resolves (reproducibility, Chapters 5–6), the surface a policy inspects (governance, Chapter 9),
  and the declaration that makes provenance reviewable (security, Chapter 8).
- **Prerequisite recap.** Chapter 1 named the four properties and showed Meridian's drift; Chapter 2 mapped the
  package-manager shape (manifest, lockfile, pinning) onto agent context; Chapter 3 named the *primitives*
  (instruction, prompt, skill, agent, hook, plugin, MCP server) and separated *primitives* from *harnesses*,
  ending on a harness-agnostic **primitive map**. Chapter 4 writes the first file that actually contains those
  nouns — turning the map into declared, version-controlled project state.

---

## Concepts covered

1. **The manifest as reviewable project state** — the leap from scattered per-machine files to one declared,
   version-controlled file; the concrete implementation of portability.
2. **What a manifest declares** — project identity, harness targets, primitive and MCP dependencies, where
   those dependencies come from (git sources), and locally-authored primitives — all in one place.
3. **Local authoring vs. external dependencies** — primitives you write in-repo (under `.apm/`) vs.
   dependencies you pull from git sources; both are declared in the same manifest and deployed by the same
   install.
4. **Why declaration enables review** — a manifest change is a diff, so agent behavior, sources, and versions
   become code-review artifacts (the leader angle).

---

## Concept 1 — The manifest as reviewable project state

**Definition.** A *manifest* is the single, version-controlled file in which a project declares the agent
context it needs. In APM that file is `apm.yml`, and the docs describe it as a *contract*: it "declares the
full closure of agent primitive dependencies, MCP servers, scripts, compilation settings … for a project. It
is the contract between package authors, runtimes, and integrators"
([Manifest Schema, Abstract](https://microsoft.github.io/apm/reference/manifest-schema/)). Only two fields are
required to parse — `name` and `version` — and everything else is optional
([Manifest Schema §2](https://microsoft.github.io/apm/reference/manifest-schema/)).

**The problem it solves.** In Chapter 1, Meridian's agent context lived as scattered per-machine, per-harness
files — a `copilot-instructions.md` here, a copied `review.prompt.md` in three home directories, Cursor rules
that no one else could see. Nothing declared what the *project* needed; each machine was its own source of
truth, so the setups silently diverged. A manifest replaces "whatever happens to be on my disk" with "what
this repository declares" — a portable statement of intent that travels with the code. Portability begins the
moment the desired context is written down in one file every clone shares.

**Key distinctions.**
- *Manifest vs. the per-machine files it replaces.* The Chapter 1 anti-pattern was many hand-edited outputs
  scattered across machines; the manifest is one authored input, committed to the repo, that those outputs are
  generated *from*. You edit the declaration, not the deployed copies
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
- *Manifest vs. lockfile.* The manifest is **human-authored declared intent** — what you want, which may
  include a moving branch or a version range. The lockfile (`apm.lock.yaml`, Chapter 6) is the
  **machine-generated resolved state** — the exact commits and content hashes you actually got. The manifest
  says *what*; the lockfile records *exactly which*
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
- *Familiar shape.* "The shape mirrors `package.json` on purpose: `name`, `version`, `dependencies`,
  `devDependencies`, `scripts`" ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
  A reader who has opened a `package.json` already knows how to read an `apm.yml`.

**Common misconception.** *"`apm.yml` is just config for the CLI."* It is not tool-local configuration; it is
the project's shared, harness-agnostic contract. Any conforming resolver — not just the `apm` CLI — can consume
it "to install, compile, run, and pack agentic workflows"
([Manifest Schema, Abstract](https://microsoft.github.io/apm/reference/manifest-schema/)). It belongs to the
repository, not to a workstation.

**Meridian beat (for the author).** The chapter's turn is small and deliberate: the team stops maintaining
three private setups and commits *one* `apm.yml` at the root of `meridian-checkout`. Nothing about their
context is new — it is the same primitive map from Chapter 3 — but for the first time it is *declared* instead
of *scattered*. That single committed file is the whole point of the chapter.

**Implemented in APM by:** the `apm.yml` manifest itself (required `name` and `version`; all else optional),
scaffolded by `apm init`, which "creates exactly one file — the manifest"
([Your First Package](https://microsoft.github.io/apm/getting-started/first-package/)). (Exact required/optional
split and `apm init` template confirmed by the explorer.)

---

## Concept 2 — What a manifest declares

**Definition.** Conceptually, an `apm.yml` declares five kinds of thing, all in one place: **project identity**
(who this package is), **targets** (which harnesses to build for), **dependencies** (which primitives and MCP
servers it needs), **sources** (where those dependencies come from), and **local content** (the primitives the
repo authors itself). None of these is exhaustive here — the point is the *categories*, not a key-by-key tour
([Package anatomy field reference](https://microsoft.github.io/apm/concepts/package-anatomy/),
[Manifest Schema §3–4](https://microsoft.github.io/apm/reference/manifest-schema/)).

**The problem it solves.** Before a manifest, decisions about *which version*, *which source*, *which harnesses*,
and *which scripts* were made implicitly on individual machines and never written down. Collecting them into one
declared file gives the team a stable place to make — and see — those choices, instead of hiding them in personal
configuration. The manifest is where "which review prompt, from where, pinned to what, for which tools" becomes a
single answerable question.

**What gets declared (conceptually).**
- *Project identity.* `name` and `version` (and an optional `description`) say what this package is and which
  release of it you are looking at. These two are the only fields required to parse
  ([Manifest Schema §2–3](https://microsoft.github.io/apm/reference/manifest-schema/)).
- *Harness targets.* `targets:` lists which harnesses APM compiles and deploys for — Meridian's first manifest
  names `copilot`, `claude`, `cursor`. Pinning targets in the manifest makes output "deterministic for every
  developer, CI runner, and cloud agent," rather than silently tracking whichever tool folders happen to exist on
  the last person's machine ([Manifest Schema §3.6](https://microsoft.github.io/apm/reference/manifest-schema/)).
  (This is the Chapter 3 *target ≠ harness* distinction, now written down: you *declare* targets; the harness
  still *runs* independently.)
- *Dependencies and their sources.* `dependencies.apm` lists primitive packages, and `dependencies.mcp` lists
  MCP servers. A primitive dependency is declared as a **git source** — `owner/repo` on GitHub by default, or a
  fully-qualified host for GitLab, Bitbucket, Azure DevOps, or self-hosted git — optionally **pinned by a git
  ref** (a tag such as `#v1.0.0`, a branch such as `#main`, or a commit SHA)
  ([Manifest Schema §4.1](https://microsoft.github.io/apm/reference/manifest-schema/)). An MCP dependency is
  declared as a registry reference such as `io.github.github/github-mcp-server`
  ([Manifest Schema §4.2](https://microsoft.github.io/apm/reference/manifest-schema/)).
- *Local content and scripts.* `includes` governs which locally-authored `.apm/` primitives the project deploys
  and ships (Concept 3), and `scripts` names commands runnable with `apm run` (developed in Chapter 5). Meridian's
  *first* manifest declares no remote dependencies and no scripts yet — just identity, targets, and one local
  instruction via `includes`. Dependencies and scripts arrive in Chapter 5; keeping Chapter 4 minimal is
  intentional.

**Key distinctions.**
- *Declaring a dependency vs. copying files.* A dependency is a **reference** — a source plus a version — not a
  vendored copy of someone else's primitives. APM resolves the reference at install time by cloning the repo and
  locating its `.apm/` content ([Manifest Schema §9, Integrator Contract](https://microsoft.github.io/apm/reference/manifest-schema/)).
- *Required vs. optional.* Only `name` and `version` are required; targets, dependencies, includes, and scripts
  are all optional and added as the project needs them
  ([Manifest Schema §2](https://microsoft.github.io/apm/reference/manifest-schema/)). A valid manifest can be
  three lines long ([Package anatomy, "The minimal package"](https://microsoft.github.io/apm/concepts/package-anatomy/)).

**Common misconception.** *"I must enumerate every primitive and every file the project uses."* You declare
*packages* (units of distribution) and *targets*; you do not hand-list every file inside them. Your own local
primitives are governed by `includes` — `auto` simply walks the whole `.apm/` tree — not by naming each file
individually ([Your First Package](https://microsoft.github.io/apm/getting-started/first-package/)).

**Meridian beat (for the author).** Walk the reader down the minimal manifest field by field: identity
(`name: meridian-checkout-agent-context`, `version: 0.1.0`, a one-line `description`), the three `targets`, and a
single `includes` entry pointing at the one instruction. Each line answers a question the team used to answer
per-machine. Resist adding remote dependencies here — that is Chapter 5's beat.

**Implemented in APM by:** `name` / `version` / `description` (identity); `targets:` (harness selection);
`dependencies.apm` (primitive packages via git sources, pinned by ref) and `dependencies.mcp` (MCP servers via
registry reference); `includes` (local content); `scripts` (named commands). (Exact field forms, the
`target:`/`targets:` relationship, the dependency shorthand grammar, and supported hosts confirmed by the
explorer.)

---

## Concept 3 — Local authoring vs. external dependencies

**Definition.** A manifest describes two sources of primitives that look different but land in the same place.
**Locally-authored** primitives are files the repo writes itself, under the `.apm/` source tree
(`instructions/`, `skills/`, `prompts/`, `agents/`, `hooks/`) — `.apm/` is "the conventional source root for APM
packages" ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)). **External
dependencies** are primitives pulled from other repositories, declared under `dependencies.apm` (and MCP servers
under `dependencies.mcp`) and fetched from git sources at install time. Both are declared in one `apm.yml`, and
both are deployed by the same `apm install`.

**The problem it solves.** Real teams are simultaneously *consumers* of shared packages and *authors* of their
own conventions. Without one manifest, "our local rules" and "the packages we depend on" live in different places
and drift apart — exactly the split Chapter 1 diagnosed. Declaring both in the same file means there is no
separate home for "our stuff" versus "their stuff": the project's entire agent-context surface is one reviewable
declaration.

**Key distinctions.**
- *`.apm/` (source you author) vs. `apm_modules/` (dependencies you install).* `.apm/` holds "source primitives
  you author"; `apm_modules/` holds "installed dependencies" and is generated and gitignored. You edit `.apm/`;
  you never hand-edit installed or compiled output
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
- *Local content (governed by `includes`) vs. a dependency (a reference).* Local primitives are content that
  lives in your repo; `includes` declares which of that content the project consents to deploy and ship — `auto`
  publishes everything under `.apm/`, or an explicit path list ships a gated subset
  ([Manifest Schema §3.9](https://microsoft.github.io/apm/reference/manifest-schema/)). A dependency, by contrast,
  is a pointer to *another* repo at a *specific ref*, resolved by cloning and locating that repo's `.apm/`
  ([Manifest Schema §9](https://microsoft.github.io/apm/reference/manifest-schema/)).
- *Your repo can be its own package.* Local authoring is not a lesser mode: "APM treats your repo as the package
  and deploys its `.apm/` content" ([Your First Package](https://microsoft.github.io/apm/getting-started/first-package/)).
  With no remote dependencies declared, `apm install` "walks your local `.apm/` tree and deploys what it finds"
  ([Your First Package](https://microsoft.github.io/apm/getting-started/first-package/)). Meridian's first
  manifest is precisely this shape — one local instruction, zero remote dependencies.

**Common misconception.** *"APM is only for installing other people's packages."* A project's very first, most
valuable manifest may declare no external dependencies at all — just its own `.apm/` primitives, made portable
across harnesses. Consuming external packages (Chapter 5) is an *addition* to local authoring, not a
precondition for it.

**Meridian beat (for the author).** The team's one instruction —
`.apm/instructions/meridian-checkout.instructions.md` (use the `Money` value object, treat checkout retries as
idempotent, never log card data) — is authored locally and declared through `includes`. No remote package is
involved yet. The win to show: that single authored file, declared once, compiles into Copilot, Claude Code, and
Cursor outputs — the same source, three native destinations, exactly as Chapter 3 previewed. External
dependencies enter the story in Chapter 5.

**Implemented in APM by:** the `.apm/` source tree (locally-authored primitives) with `includes` governing which
of it deploys/ships; `dependencies.apm` and `dependencies.mcp` (external, git- and registry-sourced); the
generated `apm_modules/` directory holding resolved dependencies; `apm install` deploying both into each target
harness's directories. (Exact `.apm/` subdirectory names, `includes` forms, and `apm_modules/` behavior confirmed
by the explorer.)

---

## Concept 4 — Why declaration enables review

**Definition.** Because the manifest is a small, version-controlled text file, every change to it is a **diff** —
and a diff is something a teammate can review in a pull request. Declaring agent context in `apm.yml` pulls that
context into the same review workflow as application code: adding a dependency, moving a version, changing a
source, or targeting a new harness all become visible, reviewable edits rather than invisible per-machine
changes.

**The problem it solves.** Chapter 1's leader pain was an accountability gap: security could not say which MCP
servers were installed or whether a prompt came from an approved source, and onboarding depended on a wiki page
and a Slack thread. When the answers live in a committed manifest, they become an audit trail. Code review can
now include changes to agent behavior, dependency sources, and version choices — the exact governance surface
Chapters 8–9 build on.

**Key distinctions.**
- *Reviewing a declaration vs. reviewing generated output.* A manifest diff is semantic and compact — "added
  `microsoft/apm-sample-package#v1.0.0`," "targeted `cursor`," "moved a source from a branch to a tag." Reviewers
  inspect *intent*, not the thousands of lines of compiled harness files that intent produces (those are build
  output under `.github/`, `.claude/`, and the like, regenerated on install)
  ([Package anatomy](https://microsoft.github.io/apm/concepts/package-anatomy/)).
- *Declaration makes provenance and versions first-class.* A pinned ref in the diff (`#v1.0.0` vs. `#main`) shows
  a reviewer whether a dependency is immutable or moving; the source shows *whose* code it is. Version pinning and
  git sources are what make "where did this come from, and which version?" answerable at review time
  ([Manifest Schema §4.1](https://microsoft.github.io/apm/reference/manifest-schema/)).
- *The manifest can be tightened for stronger review.* Beyond identity and dependencies, declaration choices
  themselves are governable: an explicit `includes` path list is "the strongest governance form; changes are
  reviewable in PR diffs," and setting `targets:` makes the deployed output deterministic across machines and CI
  rather than dependent on local folder presence
  ([Manifest Schema §3.9, §3.6](https://microsoft.github.io/apm/reference/manifest-schema/)). Both turn implicit
  behavior into explicit, reviewable declaration.

**Common misconception.** *"A manifest is a developer-convenience / personal-productivity file."* The right frame
is dependency governance, not IDE personalization (Chapter 2's leader thesis). The manifest's value to a leader is
precisely that it makes agent-context change *reviewable and auditable* — the diff is where risk, provenance, and
version decisions surface before they ship, not a nicety for individual workflow.

**Meridian beat (for the author) — leader callout.** Frame the first `apm.yml` commit as the moment agent context
enters code review at Meridian. The PR that adds the manifest is small, but it is the first time a reviewer (and,
later, security) can see *in the repo* which harnesses are targeted and which instruction governs the checkout
service — no wiki, no Slack thread, no private workstation state. The leader question to pose: should adding or
changing `apm.yml` require review the same way changing `package.json` does?

**Implemented in APM by:** the version-controlled `apm.yml` diff as the review unit; `dependencies.apm` refs
(git source + pinned tag/branch/SHA) surfacing provenance and version choices; `targets:` making deployed output
deterministic; the explicit-path form of `includes` as the strongest, most reviewable declaration of shipped
local content. (Exact ref-pinning syntax, `targets:` determinism guarantees, and `includes` governance behavior
confirmed by the explorer; enforcement of these choices is Chapter 9's policy layer.)

---

## Sources

Official APM documentation (primary):
- Manifest Schema — required `name`/`version`; optional `description`/`targets`/`type`/`scripts`/`includes`;
  `dependencies.apm` git-source grammar and ref pinning; `dependencies.mcp` registry references; the manifest as
  a contract; `targets:` determinism; `includes` consent forms —
  <https://microsoft.github.io/apm/reference/manifest-schema/>
- Package anatomy — the minimal (three-line) package; `apm.yml` field reference; the `package.json` parallel;
  `.apm/` (source) vs. `apm_modules/` and compiled dirs (generated); manifest vs. lockfile —
  <https://microsoft.github.io/apm/concepts/package-anatomy/>
- Your First Package — `apm init` "creates exactly one file — the manifest"; `includes: auto` walks the local
  `.apm/` tree; "APM treats your repo as the package"; local authoring with no remote dependencies —
  <https://microsoft.github.io/apm/getting-started/first-package/>
- Use APM packages (consumer ramp) — the everyday `init` → `install <pkg>` → `install` → `run` loop; where the
  manifest sits in the consumer flow — <https://microsoft.github.io/apm/consumer/>
- What is APM? — install/deploy plane vs. runtime plane; "writes the files each tool already understands" —
  <https://microsoft.github.io/apm/concepts/what-is-apm/>
- Glossary — package vs. primitive vs. target vs. harness (carried forward from Chapter 3) —
  <https://microsoft.github.io/apm/concepts/glossary/>

Official repository:
- microsoft/apm README — the three promises ("Portable by manifest. Secure by default. Governed by policy.");
  `apm.yml` as the manifest — <https://github.com/microsoft/apm>

---

## Artifact path

`content/research/04-the-manifest-apm-yml-theory.md`
