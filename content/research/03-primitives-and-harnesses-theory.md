# Concept Brief — Chapter 3: Primitives & Harnesses

- **Chapter:** 3 — Primitives & Harnesses (Part I — Why)
- **Objective it serves:** Know the vocabulary of what APM manages and how those primitives relate to
  agent harnesses.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30). Feature/file/command
  names tagged `Implemented in APM by:` are conceptual hand-offs — the `apm-cli-explorer` confirms exact
  keys, directories, and flags; the `code-verifier` runs them.
- **Frame note (which property this chapter feeds).** Naming the primitives is the prerequisite for the
  whole four-property frame, but it lands hardest on **portability**: you cannot declare "one set of
  agent context, restored everywhere" until you have names for the things being declared. It also seeds
  **governance** — a security team can only allow/deny "a prompt," "a skill," or "an MCP server" once
  those categories exist (Chapters 8–9 build on this).
- **Prerequisite recap.** Chapter 1 established agent context as an unmanaged dependency and named the
  four properties; Chapter 2 mapped the package-manager shape (manifest, lockfile, pinning) onto it.
  Chapter 3 supplies the nouns those files will contain, before any manifest is written in Chapter 4.

---

## Concepts covered

1. **Primitives** — the atomic units of agent context APM manages, and why naming them matters.
2. **The primitive vocabulary** — the seven types (instruction, prompt, skill, agent, hook, plugin,
   MCP server), each solving a distinct problem, with the crisp instruction-vs-prompt-vs-skill split.
3. **The standards underneath** — AGENTS.md, Agent Skills / SKILL.md, and MCP; APM is built *on* these,
   not a replacement for them.
4. **Primitives vs. harnesses** — a harness is the runtime that consumes primitives; APM's value is
   declaring one source set and compiling it into each harness's native location.

---

## Concept 1 — Primitives: the atomic units of agent context

**Definition.** A *primitive* is "a unit of agent context APM can manage" — the atomic building block a
package ships and a manifest declares. APM's own glossary is precise: "The atomic unit APM ships. The
supported kinds are: instructions, skills, prompts, agents, hooks, commands, plugins, MCP servers, and
experimental canvas extensions"
([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/),
[Glossary](https://microsoft.github.io/apm/concepts/glossary/)). Not every file in a repo is a primitive
— only files matching the recognised primitive layout are discovered, validated, and deployed
([Glossary](https://microsoft.github.io/apm/concepts/glossary/)).

**The problem it solves.** Before you can package agent context, you need names for the things being
packaged. In Chapter 1 the team's context was an undifferentiated pile — "an AI setup," "some rules,"
"that prompt." A shared vocabulary turns that pile into typed, reviewable, governable units: you can
now say *which* instruction drifted, *which* prompt has three copies, and *which* MCP server nobody
approved. Typing the context is what makes both a manifest (Chapter 4) and a policy (Chapter 9) possible.

**Key distinctions.**
- *Primitive vs. package.* A **package** is the unit of distribution — a directory with an `apm.yml`
  that may bundle many primitives. A **primitive** is one typed unit inside it. One package can ship
  several primitives ([Glossary](https://microsoft.github.io/apm/concepts/glossary/)).
- *Primitive vs. arbitrary file.* Only files under the recognised primitive directories (`instructions/`,
  `skills/`, `prompts/`, `agents/`, `hooks/`, `commands/`, `extensions/`) are treated as primitives and
  deployed; everything else is just repo content
  ([Glossary](https://microsoft.github.io/apm/concepts/glossary/)).

**Common misconception.** *"A primitive is a runtime feature APM executes."* No — APM discovers, validates,
routes, and deploys primitives; the harness executes them. APM "governs the install and integrity plane
… It does not govern the runtime plane"
([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Meridian beat (for the author).** The chapter's job is to hand the reader the seven nouns so that when
`meridian-checkout` inventories its scattered context, each item gets a *type* instead of a shrug.

**Implemented in APM by:** the primitive type system defined in the OpenAPM spec and surfaced in `apm.yml`;
source authoring under `.apm/` in a package; deployment performed by `apm install` (per target) and
`apm compile` (aggregated context files). (Exact directory names and schema confirmed by the explorer.)

---

## Concept 2 — The primitive vocabulary (the seven types)

**Definition.** APM manages seven primitive types that a team will meet daily (plus `commands`, a
projection of prompts, and an experimental `canvas` type). Each solves a *different* problem; the value
of the vocabulary is that these are not interchangeable. The authoritative one-line definitions come
straight from the docs' "What APM manages" table and primitive catalogue
([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/),
[Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)):

| Primitive | What it is (APM's words) | What triggers it | Distinct problem it solves |
|---|---|---|---|
| **Instruction** | "Repository-scoped guardrails and coding standards the agent reads on every turn," scoped by file glob | Nobody — ambient; applied automatically every turn | Persistent, always-on rules you never re-state |
| **Prompt** | "Executable, parameterized AI workflows … a callable program for an LLM"; "saved prompts the user invokes by name" | The **user**, explicitly, by name | A repeatable multi-step task/checklist on demand |
| **Skill** | "Reusable, model-invocable capabilities packaged as Agent Skills" (SKILL.md + bundled resources) | The **model**, on demand, when a task matches its description | Specialized know-how loaded only when relevant |
| **Agent** | "Specialized personas with their own scope, tools, and system prompt" | Selected as the acting persona for a task | A bounded specialist instead of one generalist |
| **Hook** | "Lifecycle handlers that run before or after agent tool calls" (e.g. `PreToolUse`, `PostToolUse`, `Stop`) | The harness runtime, automatically at that event | Deterministic automation around tool calls |
| **Plugin** | "Bundles of the primitives above, packaged for one-shot install" | Installed as one unit; unpacked into its primitives | Shipping/installing a set of primitives together |
| **MCP server** | "External tools the agent connects to via Model Context Protocol" | The agent at runtime, when it calls that tool | Governed access to outside tools and data |

**The problem it solves.** Distinct names prevent category errors. "Add a security review" could mean a
persistent *instruction* (always warn about card-data logging), a *prompt* the reviewer runs on a PR, a
*skill* the model pulls in when it recognises a payment change, or an *agent* that owns review end to
end. Each has different cost, trigger, and blast radius; conflating them produces the "why did the agent
do that?" confusion the book is trying to end.

**The crisp split most readers get wrong — instruction vs. prompt vs. skill.** All three are "markdown
that steers the agent," so they blur together. They differ on **who triggers them** and **what shape they
take**:
- An **instruction** is *never invoked*. It is ambient guidance the agent reads on every turn within its
  `applyTo` glob — background guardrails
  ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).
- A **prompt** is *invoked by a human*, by name — a parameterized, runnable workflow, "a callable program
  for an LLM" ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).
- A **skill** is *invoked by the model*, autonomously, through **progressive disclosure**: the agent sees
  only the skill's name and description until a task matches, then loads the full `SKILL.md` and any
  bundled scripts/resources ([Agent Skills overview](https://agentskills.io/)).

Mnemonic for the author: *instruction = always on; prompt = you run it; skill = the model reaches for it.*

**Other distinctions worth keeping straight.**
- *Agent vs. skill.* An **agent** is *who* is acting — a persona with its own tools and boundaries; a
  **skill** is *how* to do a task — a procedure the acting agent can pull in. One agent can use many
  skills ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).
- *Prompt vs. command.* They are the *same source*. Commands are "Sourced from `.apm/prompts/` — there is
  no separate `.apm/commands/` directory. The same `.prompt.md` file becomes Copilot's prompt and Claude's
  `/command`" ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).
  So "command" is a harness projection of a prompt, not a fourth thing to author.
- *Plugin vs. the rest.* A plugin is a **packaging format**, not a new capability: "a self-contained bundle
  … that ships a set of primitives. APM normalizes plugins at install time into the same primitives"
  ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).
- *MCP server — managed, but not "shipped."* APM lists MCP servers among what it manages, yet the glossary
  draws a sharp line: "MCP servers are external processes; APM declares and gates them but does not ship
  their code" ([Glossary](https://microsoft.github.io/apm/concepts/glossary/)). APM writes each harness's
  MCP config and applies policy; the server itself runs elsewhere.

**Common misconceptions.**
- *"Instruction, prompt, and skill are three words for the same thing."* They differ by trigger and shape
  (above). This is the single most important clarification in the chapter.
- *"A skill is just a long prompt."* A skill is a folder with a `SKILL.md` plus optional scripts, references,
  and assets, loaded on demand — it can carry executable resources and is invoked by the model, not typed
  by the user ([Agent Skills overview](https://agentskills.io/)).
- *"Declaring an MCP server means APM runs the tool."* It configures and gates the connection; the harness
  and the external server do the running ([Glossary](https://microsoft.github.io/apm/concepts/glossary/)).

**Meridian beat (for the author).** Meridian classifies its existing context into a **primitive map**:
checkout-domain engineering rules → **instruction**; the fraud-review checklist → **prompt**; the
frontend-design know-how → **skill**; the API-architect persona → **agent**; the payment-sandbox tool
connection → **MCP server**. That map is the seed of the Chapter 4 manifest — each row becomes a
declared dependency.

**Implemented in APM by:** primitive source directories under `.apm/` (`instructions/`, `prompts/`,
`skills/`, `agents/`, `hooks/`); MCP servers under `dependencies.mcp` (the `mcp:` block); packaged
primitives pulled in under `dependencies.apm`; plugins detected from a `plugin.json` bundle. (Exact keys
and per-type frontmatter confirmed by the explorer; authored in Chapter 4.)

---

## Concept 3 — The standards underneath (AGENTS.md, SKILL.md, MCP)

**Definition.** APM does not invent its formats; it is "built on standards: AGENTS.md · Agent Skills /
SKILL.md · MCP" ([repo README](https://github.com/microsoft/apm)). Each standard is an independent, open
format APM adopts for a slice of the primitive vocabulary:
- **AGENTS.md** — "a simple, open format for guiding coding agents … a dedicated, predictable place to
  provide the context and instructions" that "works across many agents," now stewarded by the Agentic AI
  Foundation under the Linux Foundation ([agents.md](https://agents.md/)). APM's *instructions* compile
  into AGENTS.md-style files.
- **Agent Skills / SKILL.md** — "a lightweight, open format for extending AI agent capabilities … a skill
  is a folder containing a `SKILL.md` file" with `name`/`description` metadata plus instructions, loaded by
  progressive disclosure; "originally developed by Anthropic, released as an open standard"
  ([agentskills.io](https://agentskills.io/)). APM's *skill* primitive **is** this format.
- **MCP (Model Context Protocol)** — "an open-source standard for connecting AI applications to external
  systems … data sources … tools … and workflows," described as "a USB-C port for AI applications"
  ([modelcontextprotocol.io](https://modelcontextprotocol.io/)). APM declares *MCP servers* as
  dependencies against this protocol.

**The problem it solves.** Standing on shared standards is what makes APM a *manager* rather than yet
another silo. Because instructions are AGENTS.md, skills are SKILL.md, and tools are MCP, APM-produced
context is readable by tools that never installed APM — and APM can consume primitives authored by people
who never used it. It borrows credibility and reach instead of asking the ecosystem to adopt a proprietary
format ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Key distinctions.**
- *Standard vs. manager.* AGENTS.md, SKILL.md, and MCP define **file/protocol formats**; APM adds the
  **dependency layer** on top — resolution, pinning, a lockfile, policy, and multi-harness compilation.
  The standards say *what a skill or instruction looks like*; APM says *where it came from, which version,
  and where it deploys*.
- *Built on ≠ owns.* These standards are governed elsewhere (Agentic AI Foundation / Linux Foundation for
  AGENTS.md; an open `agentskills` community, Anthropic-originated, for SKILL.md; the MCP community).
  APM is a consumer and compiler of them, not their owner ([agents.md](https://agents.md/),
  [agentskills.io](https://agentskills.io/), [modelcontextprotocol.io](https://modelcontextprotocol.io/)).
- *One-to-one where it exists.* The cleanest mapping is skill ⇒ SKILL.md and MCP server ⇒ MCP. Instructions
  relate to AGENTS.md as a **compile target** (many scoped instructions can fan out into distributed
  AGENTS.md files), not a byte-for-byte identity
  ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).

**Common misconceptions.**
- *"APM replaces AGENTS.md / SKILL.md / MCP."* The opposite — it implements and distributes them. APM is
  "not a runtime" and "not a marketplace"; it packages the standards' artifacts
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).
- *"AGENTS.md and SKILL.md are the same idea."* AGENTS.md is *always-on project guidance for agents*;
  SKILL.md is an *on-demand, model-invoked capability with bundled resources* — the instruction-vs-skill
  split from Concept 2, expressed at the standards layer
  ([agents.md](https://agents.md/), [agentskills.io](https://agentskills.io/)).

**Meridian beat (for the author).** The team already produced these standards by hand without naming them:
their `.github/copilot-instructions.md` is AGENTS.md-shaped guidance; a copied review checklist is a
would-be prompt; the payment-sandbox tool is an MCP server. The chapter reframes their existing files as
*instances of open standards* APM can now manage — nothing exotic, just typed.

**Implemented in APM by:** `apm compile` emitting AGENTS.md-style context files from instructions; the
`skill` primitive authored directly in SKILL.md format; MCP servers declared under `dependencies.mcp`.
(Exact compile outputs and MCP config paths confirmed by the explorer.)

---

## Concept 4 — Primitives vs. harnesses

**Definition.** A *harness* is "the agent runtime that executes primitives: GitHub Copilot (CLI + IDE),
Claude Code, Cursor, Codex, Gemini, Antigravity, OpenCode, Windsurf, and Kiro. Each harness has its own
primitive directory layout and file format" ([Glossary](https://microsoft.github.io/apm/concepts/glossary/)).
A *primitive* is the harness-agnostic source unit (Concept 1). APM's central move is to sit between them:
you author one set of primitives, and APM compiles them into each harness's native location — "APM does
not invent a runtime format. It writes the files each tool already understands and stays out of the way at
agent runtime" ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**The problem it solves.** Real teams are multi-harness by choice (Meridian uses Copilot, Claude Code, and
Cursor). Without a shared source, every harness needs its own hand-maintained files, and they drift — the
exact failure from Chapter 1. Separating the *primitive* (what you mean) from the *harness* (who runs it)
lets one declaration land correctly everywhere: "Every developer who clones the repo runs `apm install` and
gets the same skills, prompts, instructions, hooks, and MCP servers wired into Copilot, Claude, Cursor,
OpenCode, Codex, Gemini, Windsurf, and Kiro"
([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Same source primitive → harness-specific outputs.** Because each harness has its own format, APM either
writes a primitive *natively* or *compiles* it. The docs' compatibility matrix gives the legend — `native`
(the harness reads the primitive directly), `compiled` (APM transforms it into another format the harness
understands), `unsupported`, and `gated`
([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)). One prompt
illustrates all of it: for Copilot it stays a **native** prompt; for Claude Code the same
`.apm/prompts/<n>.prompt.md` is **compiled** into `.claude/commands/<n>.md` and becomes a `/command`
([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)). One source,
many native destinations — that is portability made concrete.

**Key distinctions.**
- *Harness vs. target.* This is the pair readers most often merge. A **harness** is the runtime; a
  **target** is "the declaration … the manifest or CLI selector for which harnesses to compile for." "Target
  is the declaration; the harness is the runtime that consumes the compiled output"
  ([Glossary](https://microsoft.github.io/apm/concepts/glossary/)). You *list targets* in `apm.yml`; the
  *harness* is what actually runs.
- *Restoring context ≠ owning the runtime.* APM writes the files each tool understands and then steps
  aside; what the agent may *do* at runtime "belongs to your agent harness. The two planes do not overlap"
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).
- *Default vs. explicit targets.* Eight harness targets are configured by default (copilot, claude, cursor,
  opencode, codex, gemini, windsurf, kiro); Antigravity is available only as an explicit CLI target
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/),
  [Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)). This is why
  the book says "many harnesses" and lists them, rather than promising "every tool ever."
- *Reach is not uniform.* Not every primitive reaches every harness — some cells are `compiled` or
  `unsupported` (e.g. OpenCode has no hooks; Gemini has no native agents primitive). The chapter should set
  the expectation that parity is *high but bounded*, and point to the matrix as the source of truth
  ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).

**Common misconceptions.**
- *"APM is a new harness / replaces my agent."* No — APM is a dependency manager *for* harnesses; it neither
  runs the agent nor deep-dives any harness's runtime
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).
- *"One primitive means an identical file in every tool."* The *intent* is identical; the *file* is whatever
  each harness natively reads. APM may write a native file for one harness and a compiled transform for
  another ([Primitives and targets](https://microsoft.github.io/apm/concepts/primitives-and-targets/)).

**Meridian beat (for the author).** The primitive map from Concept 2 is deliberately harness-agnostic. The
chapter closes by showing the same map fanning out to three targets — `copilot`, `claude`, `cursor` — so the
reader sees one instruction and one prompt landing as three tools' native files. That preview is the exact
promise Chapter 4's manifest and Chapter 5's `apm install` will deliver.

**Implemented in APM by:** the `targets:` field in `apm.yml` (declaring which harnesses to build for); the
fan-out performed by `apm compile` / `apm install` into each harness's native directory (e.g. `.github/`
for Copilot, `.claude/` for Claude Code, `.cursor/` for Cursor); and the primitive-by-harness reach
described in the targets/compatibility matrix. (Exact target slugs, per-harness paths, and matrix cells
confirmed by the explorer.)

---

## Sources

Official APM documentation (primary):
- Primitives and targets (primitive catalogue, target catalogue, compatibility matrix, native/compiled/
  unsupported/gated legend) — <https://microsoft.github.io/apm/concepts/primitives-and-targets/>
- What is APM? ("What APM manages" table; built on standards; "does not invent a runtime format";
  install/plane boundaries) — <https://microsoft.github.io/apm/concepts/what-is-apm/>
- Glossary (definitions of primitive, harness, target, hook, plugin, MCP server, package, compile) —
  <https://microsoft.github.io/apm/concepts/glossary/>
- The three promises (portable by manifest; secure by default) —
  <https://microsoft.github.io/apm/concepts/the-three-promises/>

Official repository:
- microsoft/apm README ("built on standards: AGENTS.md · Agent Skills / SKILL.md · MCP"; three promises;
  install-vs-runtime planes) — <https://github.com/microsoft/apm>

Foundations APM is built on (the standards underneath):
- AGENTS.md — <https://agents.md/>
- Agent Skills / SKILL.md — <https://agentskills.io/>
- Model Context Protocol (MCP) — <https://modelcontextprotocol.io/>

---

## Artifact path

`content/research/03-primitives-and-harnesses-theory.md`
