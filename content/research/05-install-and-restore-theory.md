# Concept Brief — Chapter 5: Install & Restore

- **Chapter:** 5 — Install & Restore (Part II — Portable by manifest)
- **Objective it serves:** Install and restore a project's agent context with the daily APM consumer
  loop.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30). Feature/file/command
  names tagged `Implemented in APM by:` are conceptual hand-offs — the `apm-cli-explorer` confirms exact
  flags, precedence, exit codes, and generated files; the `code-verifier` runs them.
- **Frame note (which property this chapter feeds).** This chapter is where **portability** stops being a
  promise and becomes a fact. Chapter 4 declared "what this project needs"; Chapter 5 is the operation
  that turns that declaration into on-disk agent context in every developer's tools. It also *seeds*
  **reproducibility** — every install writes `apm.lock.yaml` — but the lockfile itself is Chapter 6's
  subject; here it is a by-product the reader should notice, not yet study.
- **Prerequisite recap.** Chapter 3 named the primitives and the harness/target split; Chapter 4 authored
  the manifest (`apm.yml`) that names Meridian's first shared dependencies. Chapter 5 answers the obvious
  next question — *"I have a manifest; how does everyone get the actual context?"* — without turning into a
  flag reference. The goal is a habit, not a man page.
- **Experimental-surface note.** `apm run` is documented as **experimental** ("the `run` command surface is
  marked experimental. Flags and behavior may change before 1.0";
  [apm run](https://microsoft.github.io/apm/reference/cli/run/)) and "optional and off the critical path"
  ([Run scripts](https://microsoft.github.io/apm/consumer/run-scripts/)). The chapter should present it as
  the fourth everyday command but stamp it experimental. The explorer/verifier confirm current behavior.

---

## Concepts covered

1. **Materialization** — a manifest is only useful if everyone can turn it into the *same* on-disk
   context; install/restore is the operation that does it, and where portability is realized.
2. **The daily consumer loop** — the intentionally small four-command habit: initialize once, add when
   needed, restore on clone, run a declared script.
3. **Restore vs. add** — bare `apm install` restores what is already declared; `apm install <pkg>` adds a
   new dependency. This is the `clone + install` onboarding promise that replaces the wiki-and-Slack ritual.
4. **Harness targeting at install time** — install compiles into the *declared or detected* harnesses via
   an explicit precedence chain (no implicit "default harness"); scripts then run a prompt through a
   harness CLI the developer supplies.

---

## Concept 1 — Materialization: turning a declaration into on-disk context

**Definition.** *Install/restore* is the operation that converts the declared state in `apm.yml` (plus its
lockfile) into real agent-context files inside each tool. The docs describe it precisely: `apm install`
"resolves the dependencies declared in `apm.yml`, downloads them (with transitive resolution and a
content-addressed cache), runs the built-in security scan, and deploys the resulting primitives plus the
project's own `.apm/` content into every harness target it detects. It writes `apm.lock.yaml` so the next
install on any machine reproduces the same files"
([apm install](https://microsoft.github.io/apm/reference/cli/install/)). The consumer guide names the five
ordered phases — **Resolve → Policy gate → Scan → Integrate → Lockfile** — and stresses that "each phase
must pass before the next runs" ([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)).

**The problem it solves.** A manifest is a *recipe*, not a meal. On its own, `apm.yml` changes nothing about
what an agent sees — no skill is loaded, no instruction is in force, no MCP server is wired up. Chapters 1–4
built the case that scattered, hand-copied context drifts; a manifest only ends that drift if there is a
single, mechanical way to *realize* it identically everywhere. Install is that mechanism: "The next
contributor runs bare `apm install` and gets the same bytes, pinned by commit and content hash"
([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)). This is the moment the
book's first property — *portable by manifest* — becomes observable
([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)).

**Key distinctions.**
- *Declared state vs. materialized state.* `apm.yml` is potential; the files under `.github/`, `.claude/`,
  `.cursor/`, … are actual. Install is the arrow between them. Editing the manifest without installing
  leaves the two out of sync — the same gap Chapter 6 will formalize as drift.
- *Install ≠ "just downloading packages."* It is a fail-closed pipeline: a policy gate and a hidden-Unicode
  security scan run **before anything touches disk**, which is exactly how APM differs from a naive fetch —
  "APM also runs a security scan and, if present, an org policy gate before writing anything to disk"
  ([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)). (Security is Chapter 8;
  here it is enough that the reader sees install as *gated deployment*, not a copy.)
- *Materialize-from-source vs. commit-the-output.* APM recommends committing the deployed harness files too,
  so teammates and cloud Copilot get "instant agent context on clone, before they run `apm install`"; the
  package cache `apm_modules/` is gitignored and "rebuilt from the lockfile on every `apm install`"
  ([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)). The committed output is a
  convenience; the *reproducible* path is always install.

**Common misconception.** *"If I commit `apm.yml`, my teammates have the context."* Not by itself — the
manifest is a declaration; nothing is loaded into a harness until an install materializes it (or until the
already-deployed files, if committed, are present). The manifest guarantees *what should exist*; install is
what makes it exist.

**Meridian beat (for the author).** Chapter 4 ended with `meridian-checkout` owning a manifest. Chapter 5
opens by making it real: the team runs install once and watches one instruction and one prompt appear as
Copilot, Claude Code, and Cursor files — the same "one source, three tools" fan-out Chapter 3 previewed,
now executed rather than promised.

**Implemented in APM by:** `apm install` (the Resolve → Policy gate → Scan → Integrate → Lockfile pipeline);
the content-addressed cache in `apm_modules/`; the generated `apm.lock.yaml`. (Exact phase order, cache path,
and lockfile fields confirmed by the explorer; the lockfile is studied in Chapter 6.)

---

## Concept 2 — The daily consumer loop (four commands, one habit)

**Definition.** APM's everyday consumer surface is deliberately tiny. The consumer ramp names "the four
commands you'll use almost every day": `apm init` ("one-time per project"), `apm install <pkg>` ("add a
dependency"), `apm install` ("restore from `apm.lock.yaml`"), and `apm run <script>` ("invoke a script
declared in `apm.yml`") ([Use APM packages](https://microsoft.github.io/apm/consumer/)). The docs then draw
the boundary explicitly: "That's the loop. Everything else is either lifecycle automation (`update`,
`outdated`, `audit`) or a workflow extension (MCP servers, local bundles, scripts)"
([Use APM packages](https://microsoft.github.io/apm/consumer/)).

**The problem it solves.** New tools fail on their command surface as often as on their concepts. By naming a
four-verb loop, APM lets a developer become productive without reading the whole CLI: initialize a project,
add a dependency when a need appears, restore on a fresh machine, and run a declared workflow. Everything
heavier — updating versions, auditing, policy — is deferred to later chapters and is *not* part of the daily
path. Habit formation, not flag memorization, is the point.

**Key distinctions.**
- *One-time vs. recurring.* `apm init` is scaffolding — it "creates a minimal `apm.yml` … so you can start
  running `apm install` immediately" ([apm init](https://microsoft.github.io/apm/reference/cli/init/)) — and
  is run **once** per project. The other three recur.
- *Daily loop vs. lifecycle.* `update`, `outdated`, and `audit` are real and important, but they are
  *deliberate* maintenance, not everyday motions; the docs file them under "lifecycle automation" and this
  book under Chapter 7 ([Use APM packages](https://microsoft.github.io/apm/consumer/)).
- *The loop is the same under governance.* Adopting policy does not add new everyday commands: "Consumer
  commands are unchanged when policy is enforced — you'll just see more `[x]` blocks at install time when
  something is denied" ([Use APM packages](https://microsoft.github.io/apm/consumer/)). The habit survives
  Chapters 8–9 intact.

**Common misconception.** *"There must be dozens of commands to learn before I'm productive."* No — four
cover the consumer's daily work. APM has a large CLI, but the consumer loop is intentionally a small,
memorable subset, and the docs say so outright.

**Meridian beat (for the author).** Frame the loop through the team's rhythm: the context owner ran
`apm init` once when the manifest was born (Chapter 4); Lena adds a dependency with `apm install <pkg>`
when she needs a new skill; Anika (the new joiner) runs bare `apm install` after cloning; anyone runs
`apm run review` to execute the checkout-review prompt. Four verbs map onto four real moments.

**Implemented in APM by:** `apm init` (scaffold, one-time), `apm install <pkg>` (add), `apm install`
(restore), `apm run <script>` (run — **experimental**). (Exact behaviors and the experimental status of
`apm run` confirmed by the explorer.)

---

## Concept 3 — Restore vs. add (and the onboarding promise)

**Definition.** The single command `apm install` does two conceptually different jobs depending on whether
you give it an argument. "With no arguments it installs everything from `apm.yml`. With one or more
`PACKAGE_REF` arguments it adds those packages to `apm.yml` (creating one if needed) and installs only what
was added" ([apm install](https://microsoft.github.io/apm/reference/cli/install/)). Bare install is a
**restore** — a reproduce-what-is-declared operation that replays the manifest and lockfile and deploys the
same bytes. `apm install <pkg>` is an **add** — a manifest-mutating operation that resolves a new dependency,
writes it into `dependencies.apm:`, and re-locks.

**The problem it solves.** These two jobs are the two halves of team dependency work. *Add* is how the
manifest grows — a reviewable change to project state, the same way `npm install <pkg>` edits
`package.json`. *Restore* is how everyone else catches up without thinking — the operation that makes
onboarding a two-step ritual. The onboarding promise the whole book builds toward lands here: **`git clone`
+ `apm install`** replaces the wiki page, the Slack thread, and the "copy my prompt files" dance from
Chapter 1. Committed deployed files even give context "on clone, before they run `apm install`," and the
explicit restore then guarantees byte-identical setup
([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)).

**Key distinctions.**
- *Restore is reproduce, not upgrade.* Bare `apm install` replays what is already pinned; it does **not**
  chase newer versions. Moving versions is a separate, consent-gated act (`apm update`, Chapter 7) — "To
  refresh dependencies to their latest matching versions or refs, use `apm update`"
  ([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)). Conflating "restore"
  with "update" is the most common error this chapter must prevent.
- *Add mutates a reviewable file.* Because `apm install <pkg>` edits `apm.yml` (and the lockfile), the change
  shows up in a pull request — agent-context dependencies enter code review, exactly like application deps.
- *Strict restore exists (Chapter 6 preview).* A stricter form, `apm install --frozen`, is a "lockfile-only
  install: refuse to resolve anything new and fail if `apm.yml` and `apm.lock.yaml` have drifted. Mirrors
  `npm ci`" ([apm install](https://microsoft.github.io/apm/reference/cli/install/)). Name it here as the CI
  cousin of restore; develop it in Chapter 6.
- *What to commit.* Restore's guarantee depends on committing the right things: `apm.yml`, `apm.lock.yaml`,
  and the deployed harness directories; `apm_modules/` is gitignored
  ([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)).

**Common misconception.** *"Running `apm install` on a fresh clone pulls the latest versions."* No — bare
install *restores* the pinned set from the lockfile; it reproduces, it does not upgrade. (And bare
`apm install` with no `apm.yml` doesn't guess — it "exits with a hint to run `apm init` or
`apm install <org/repo>`"; [apm install](https://microsoft.github.io/apm/reference/cli/install/).)

**Meridian beat (for the author).** This is the chapter's headline beat: Anika clones `meridian-checkout`,
runs `apm install`, opens the repo in Claude Code and Cursor, and has the *same* shared context as the rest
of the team — no wiki, no Slack, no borrowed prompt files. Separately, the team's manifest grows from local
context (v0.1.0) to pinned public dependencies (v0.2.0) when someone runs `apm install <pkg>` to add a
sample package and a public skill — the `add` half of the concept, captured as a reviewable manifest diff.

**Implemented in APM by:** bare `apm install` (restore; replays manifest + lockfile; auto-bootstrap hint when
no manifest exists) vs. `apm install <pkg>` (add; persists to `apm.yml`, re-locks); `apm install --frozen`
(strict restore, `npm ci` parity — Chapter 6); the commit set (`apm.yml` + `apm.lock.yaml` + deployed harness
dirs; `apm_modules/` ignored). (Exact reference forms, bootstrap messages, and `--frozen` semantics confirmed
by the explorer.)

---

## Concept 4 — Harness targeting at install time

**Definition.** Install does not deploy into a vacuum; it deploys into **targets** — the harnesses the
project has declared or that APM detects. Which harnesses receive files is resolved by an explicit
precedence chain, not a hardcoded favorite: the `--target` selector wins, then the `targets:` field in
`apm.yml`, then a configured default, then auto-detection of harness directories already in the workspace —
"`--target` > `apm.yml` targets: > `apm config set target …` > auto-detect"
([apm install](https://microsoft.github.io/apm/reference/cli/install/); mirrored in
[Install packages](https://microsoft.github.io/apm/consumer/install-packages/)). Deployment writes each
primitive into that harness's **native** directory (`.github/`, `.claude/`, `.cursor/`, `.opencode/`,
`.codex/`, `.gemini/`, `.windsurf/`, `.kiro/`, plus the converged `.agents/skills/`)
([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)).

**The problem it solves.** Real teams are multi-harness (Meridian uses Copilot, Claude Code, and Cursor).
Targeting at install time is what lets one declared source set land correctly in each developer's *own*
tools without anyone hand-editing per-harness files. Because there is **no implicit "one true harness"**,
APM never silently picks a favorite: it follows the precedence chain, and when there is nothing to go on it
stops and teaches rather than guessing — with nothing detectable, "install exits `2` with a teaching
message" ([apm install](https://microsoft.github.io/apm/reference/cli/install/)). Pinning `targets:` in the
manifest is the recommended way to make deployment identical across machines
([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)).

**Key distinctions.**
- *Target vs. harness (reinforced from Chapter 3).* A **target** is the declaration/selector for which
  harnesses to build; a **harness** is the runtime that consumes the output. You list targets; the harness
  runs. Chapter 5 is where that pairing does visible work.
- *Install-time deployment vs. run-time execution.* Install **writes files** each tool natively reads. It
  does **not** run the agent. Executing a prompt is a separate, later step done by `apm run`, which "shells
  out to a runtime CLI — `copilot`, `claude`, `codex`, `cursor-agent`, `gemini`, `opencode`, `windsurf`,
  `kiro`, or `llm` — with a prompt file argument" ([Run scripts](https://microsoft.github.io/apm/consumer/run-scripts/)).
- *APM does not ship the runtimes.* "APM does not bundle these runtimes; you install them yourself and APM
  invokes whichever the script names," and "the runtime CLI must be on your `PATH`"
  ([Run scripts](https://microsoft.github.io/apm/consumer/run-scripts/)). Scripts are the portability promise
  at run-time: "one script per runtime … the prompt file is the same; only the runtime CLI differs"
  ([Run scripts](https://microsoft.github.io/apm/consumer/run-scripts/)).
- *Open nuance for the explorer.* The two official pages describe the "nothing to target" case slightly
  differently: the CLI reference says install "exits `2` with a teaching message"
  ([apm install](https://microsoft.github.io/apm/reference/cli/install/)), while the consumer guide lists a
  final "Fallback: minimal output to `AGENTS.md` only"
  ([Install packages](https://microsoft.github.io/apm/consumer/install-packages/)). The chapter's claim — *no
  implicit harness default; APM resolves via the chain and does not silently favor one tool* — holds either
  way, but the exact terminal behavior should be verified against v0.23.1 by the explorer/verifier.

**Common misconception.** *"APM installs (or is) the agent, and picks a default harness for me."* Neither.
APM deploys files into the harnesses you declare or that it detects, and it invokes runtime CLIs you already
have — it does not install `copilot`/`claude`/`codex`, and it has no built-in "one true harness" default.

**Meridian beat (for the author).** The manifest pins `targets: [copilot, claude, cursor]`, so every
developer's install lands in exactly those three tools regardless of what else is on their machine — Lena on
Copilot, Omar on Claude Code, Priya on Cursor all get the same primitives in their native locations. Then the
team adds a small `scripts:` entry (e.g. `review`) so `apm run review` executes the checkout-review prompt
through whichever runtime CLI a developer has installed — clearly labeled experimental until verified.

**Implemented in APM by:** the `targets:` field in `apm.yml`; the `--target` / `--exclude` selectors and the
precedence chain (flag > manifest `targets:` > configured default > auto-detect); per-harness native
deployment directories; the `scripts:` block invoked by `apm run` (**experimental**), which shells out to a
runtime CLI on the developer's `PATH`. (Exact precedence, terminal/no-target behavior, target slugs, and
`apm run` compilation confirmed by the explorer.)

---

## Sources

Official APM documentation — consumer ramp (primary):
- Use APM packages / consumer overview (the four everyday commands; "that's the loop"; unchanged commands
  under policy) — <https://microsoft.github.io/apm/consumer/>
- Install packages (the Resolve → Policy gate → Scan → Integrate → Lockfile pipeline; add-a-dependency two
  ways; where files land + detection priority; what to commit; `apm_modules/` gitignored; transitive deps)
  — <https://microsoft.github.io/apm/consumer/install-packages/>
- Run scripts (the `scripts:` block; one-script-per-runtime portable pattern; runtimes not bundled / must be
  on `PATH`; `apm run` experimental) — <https://microsoft.github.io/apm/consumer/run-scripts/>

Official APM documentation — CLI reference (behavior confirmation):
- apm init (creates a minimal `apm.yml`; auto-detected fields; target seeding) —
  <https://microsoft.github.io/apm/reference/cli/init/>
- apm install (restore vs. add semantics; deterministic phases; target precedence chain and exit `2`;
  auto-bootstrap; `--frozen` = `npm ci` parity) — <https://microsoft.github.io/apm/reference/cli/install/>
- apm run (experimental script runner; script resolution; `--param` prompt compilation) —
  <https://microsoft.github.io/apm/reference/cli/run/>

Official APM documentation — concepts (framing):
- The three promises (portable by manifest; run anywhere) —
  <https://microsoft.github.io/apm/concepts/the-three-promises/>
- Primitives and targets (target vs. harness; native vs. compiled deployment) —
  <https://microsoft.github.io/apm/concepts/primitives-and-targets/>

---

## Artifact path

`content/research/05-install-and-restore-theory.md`
