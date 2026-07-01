# Concept Brief — Chapter 1: The Context Problem

- **Chapter:** 1 — The Context Problem (Part I — Why)
- **Objective it serves:** Articulate why agent context needs a package manager and name the four
  properties APM is designed to protect.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30). Feature/file/command
  names tagged `Implemented in APM by:` are conceptual hand-offs — the `apm-cli-explorer` confirms exact
  behavior and flags; the `code-verifier` runs them.
- **Note on the four properties:** *Portability, reproducibility, provenance/security, governance* is
  **the book's pedagogical frame**, not APM's own wording. APM officially commits to **three promises**
  — *portable by manifest, secure by default, governed by policy*. Concept 3 makes the mapping explicit
  so authors don't misattribute the four-property language to the docs.

---

## Concepts covered

1. Agent context as an unmanaged project dependency (the drift / "works on my machine" failure mode).
2. The four properties: portability, reproducibility, provenance/security, governance.
3. APM's three promises and how they map to the four properties.
4. The three files + one habit: `apm.yml`, `apm.lock.yaml`, `apm-policy.yml`, and `apm install`.
5. Harness parity: one declared context, restored across many harnesses, without owning any runtime.

---

## Concept 1 — Agent context as an unmanaged project dependency

**Definition.** *Agent context* is the collection of files that configure an AI coding agent —
instructions/standards, prompts, skills, agent personas, plugins, and MCP server configurations. It has
quietly become a real project dependency: it shapes generated code, review behavior, and which external
tools an agent can reach. Yet most teams still manage it as scattered, hand-maintained artifacts — per-harness
instruction files, local prompt copies, and duplicated tool configs — with no single declared source of
truth. APM's own framing is blunt: "AI coding agents need context to be useful … but today every developer
sets this up manually. Nothing is portable nor reproducible. There's no manifest for it."
([repo README](https://github.com/microsoft/apm))

**The problem it solves.** Undeclared, per-machine context drifts. Two developers believe they share an
agent setup, but their instructions, prompts, or MCP servers differ — the classic *"works on my machine"*
failure mode, now applied to AI agents. Onboarding degrades into a wiki page plus a Slack thread plus copying
files from a colleague, and security cannot answer which agent tools are even installed. This is exactly the
pre-package-manager state of application code: essential to the work, shared by the team, but neither declared
nor pinned ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Key distinctions.**
- *Agent context* (the configuration files APM manages) vs. *the agent runtime* (what a harness does at
  inference time). APM manages the former and "stays out of the way at agent runtime"
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).
- *Personal productivity preference* vs. *shared project dependency*. The chapter's thesis is that agent
  context is the latter, so it deserves the same declaration and review discipline as `package.json` or
  `requirements.txt` ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Common misconceptions.**
- *"It's just my editor settings."* Agent context influences generated code and, through MCP servers, grants
  real tool access — it is dependency surface, not cosmetics.
- *"A shared README fixes it."* Documentation describes intent but doesn't restore state; drift returns the
  moment someone edits a local file. APM contrasts "follow this 12-step README" with a single install command
  ([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)).

**Meridian beat (for the author).** The `meridian-checkout` team finds `.github/copilot-instructions.md`
disagreeing with Claude's local rules, three copies of `review.prompt.md` checking three different threat
models, Cursor rules and Copilot rules that never reconciled, and no inventory of installed MCP servers. This
is the chapter's concrete picture of unmanaged dependency surface.

**Implemented in APM by:** the `apm.yml` manifest (the declared source of truth) plus `apm install` (which
materializes it) — introduced conceptually here, authored in Ch. 4–5.

---

## Concept 2 — The four properties

The book names four properties that a package-manager frame protects and returns to them in every chapter.
Each is defined below with the pain that appears when it is absent.

**Portability.** *The same declared context can be materialized on any machine and any supported harness.*
It solves the "it only works in my setup" problem: when context lives in one reviewable file instead of many
private locations, any teammate can reproduce the intended setup rather than reverse-engineering it. Absent
portability, each developer's agent behaves slightly differently and onboarding is manual.
*Distinction:* portability is about **where** context can be restored (any machine/harness), not yet about
**exactness** — that is reproducibility.

**Reproducibility.** *A later restore reproduces the previously known-good context exactly, down to the
bytes.* It solves silent variation: a moving branch or an upstream edit can change what a "review prompt" or
"security skill" actually contains, so the same name silently means different content. APM's lockfile answers
this with pinned refs plus content hashes, so "every clone and every CI run gets the same files"
([The three promises, "Why a lockfile?"](https://microsoft.github.io/apm/concepts/the-three-promises/)).
Absent reproducibility, a green CI run or a teammate's result cannot be trusted to match yours.
*Distinction:* portability gets you *a* setup on any machine; reproducibility guarantees it is *the same*
setup byte-for-byte ([landing page](https://microsoft.github.io/apm/)).

**Provenance / security.** *You can tell where each piece of context came from, and risky content is checked
before it reaches disk.* Agent context is effectively executable — "a prompt is a program for an LLM" — so
supply-chain risks (hidden-Unicode instructions that hijack behavior, unvetted transitive MCP servers) matter
([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). It solves the "we
installed something and can't say what or from where" problem: the lockfile "records resolved sources and
content hashes for full provenance," and installation is the point where content can be scanned and pinned
([repo README](https://github.com/microsoft/apm)). Absent provenance/security, an ungoverned MCP server or a
tampered prompt becomes local tool access before anyone reviews it.
*Distinction:* this is an **install-time / integrity** guarantee — what reaches disk and from where — not a
runtime sandbox ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Governance.** *An organization can decide which sources, scopes, and primitives are allowed, and have that
decision enforced automatically.* It solves the gap between "is this install safe enough?" and "is this
install allowed here?" APM enforces org rules "at install time, before MCP touches disk"
([landing page](https://microsoft.github.io/apm/)). Absent governance, policy lives in people's heads and is
applied inconsistently, so risk accumulates until it surfaces as an incident.
*Distinction:* governance is a **policy** decision applied to installs; security is a set of **integrity
checks** on content. They are related but not the same — Concept 3 and Chapters 8–9 separate them.

**Common misconception (whole frame).** These four are the *book's* organizing lens. Do not present them as
four labels printed in the APM docs; present them as the reader-facing properties that APM's **three official
promises** deliver (see Concept 3).

**Implemented in APM by:** portability → the `apm.yml` manifest and the harness `targets`; reproducibility →
the `apm.lock.yaml` lockfile (pinned refs + content hashes); provenance/security → install-time content
scanning, content-hash pinning in the lockfile, and `apm audit`; governance → `apm-policy.yml` enforced at
install time. (All confirmed in depth by the explorer in later chapters.)

---

## Concept 3 — APM's three promises, mapped to the four properties

**Definition.** APM commits to exactly three promises, described in the docs as "deliberately small and
load-bearing … Every command, every flag, every lockfile field exists to back one of these three": **portable
by manifest, secure by default, governed by policy**
([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). The book's tagline
condenses them: "One file describes every agent's context; one command reproduces it everywhere; one policy
controls what an org will allow" ([repo README](https://github.com/microsoft/apm)).

**The problem it solves (for the book).** Readers need one clean bridge from the four-property vocabulary to
what APM actually ships, so no property is left as an orphan slogan. The mapping:

| Book property (frame) | APM promise (official) | What carries it |
|---|---|---|
| Portability | Portable by manifest | `apm.yml` — one manifest, every harness, every machine |
| Reproducibility | *(carried under "Portable by manifest")* | `apm.lock.yaml` — exact versions + content hashes, byte-for-byte restore |
| Provenance / security | Secure by default | Install-time hidden-Unicode scan, content-hash pinning, transitive-MCP gating |
| Governance | Governed by policy | `apm-policy.yml` — enforced at install time, tighten-only inheritance |

Sources for each row: portability/reproducibility and the byte-for-byte lockfile
([landing page](https://microsoft.github.io/apm/)); secure-by-default scans, pins, and MCP gating
([landing page](https://microsoft.github.io/apm/), [The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/));
governed-by-policy install-time enforcement with enterprise → org → repo inheritance
([landing page](https://microsoft.github.io/apm/), [repo README](https://github.com/microsoft/apm)).

**Key distinctions.**
- **Four vs. three is intentional.** The book splits *reproducibility* out as its own property for teaching,
  even though APM presents the lockfile under Promise 1 ("Portable by manifest"). Authors should say so
  plainly rather than imply the docs list four promises.
- **Security ≠ governance.** "Secure by default" is *always-on integrity checking, no opt-in required"
  ([landing page](https://microsoft.github.io/apm/)); "governed by policy" is an *organization's* allow/deny
  decision. One asks "is this safe?", the other asks "is this allowed here?"

**Common misconception.** *"Governed by policy means APM controls what the agent can do at runtime."* No —
"apm-policy.yml governs what gets installed; your agent harness governs what runs. The two planes do not
overlap" ([repo README](https://github.com/microsoft/apm)).

**Implemented in APM by:** the three promises are the docs' own headings; the book maps them to the four
properties above and re-uses that mapping as the spine of Parts II–IV.

---

## Concept 4 — The three files + one habit

**Definition.** At a conceptual level, APM is "three files and one habit." `apm.yml` is the **manifest** — it
"lists agentic dependencies (skills, prompts, agents, plugins, full APM packages) and MCP servers."
`apm.lock.yaml` is the **lockfile** — it "pins every resolved package to an exact source ref and content
hash, so two developers running `apm install` against the same lockfile get byte-identical context."
`apm-policy.yml` is the **install-time governance** file — "enforced at install time, including transitive
MCP." And `apm install` is the **habit**: the one command that restores the declared context
([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/),
[landing page](https://microsoft.github.io/apm/)).

**The problem it solves.** It gives the reader a small, memorable map before any syntax: *what I declare*
(manifest), *what I reproduce* (lockfile), *what my org allows* (policy), and *the one gesture that ties them
together* (install). This mirrors the npm/pip/Cargo shape the audience already knows — APM "borrows the
manifest-plus-lockfile shape from npm, pip, and cargo and applies it to the files that configure AI coding
agents" ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Key distinctions.**
- *Manifest = intent; lockfile = exact result.* You edit `apm.yml`; APM generates `apm.lock.yaml`. The
  lockfile is not hand-edited ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).
- *Source vs. compiled output.* Authoring lives in `.apm/` inside the repo; APM compiles into the directories
  each harness already reads and "does not invent a runtime format"
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)). Chapter 1 only names the files —
  layout and syntax arrive in Ch. 4+.
- *One habit, two meanings.* `apm install <pkg>` adds a dependency; `apm install` with no argument restores
  from the lockfile ([consumer ramp](https://microsoft.github.io/apm/consumer/)).

**Common misconception.** *"The manifest is enough for reproducibility."* It isn't — the manifest can name a
moving ref; only the lockfile pins the exact resolved content. That gap is the entire premise of Part III and
is previewed here, not taught ([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)).

**Implemented in APM by:** `apm.yml` (manifest), `apm.lock.yaml` (lockfile), `apm-policy.yml` (policy), and
`apm install` (restore). Named here; syntax deferred to Ch. 4 (manifest), Ch. 5 (install), Ch. 6 (lockfile),
Ch. 9 (policy).

---

## Concept 5 — Harness parity

**Definition.** A *harness* is a specific AI coding tool that reads agent-context files — GitHub Copilot,
Claude Code, Cursor, OpenCode, Codex, Gemini, Windsurf, and Kiro (Antigravity is available as an explicit-only
target). *Harness parity* is APM's guarantee that one declared context restores the **same** skills, prompts,
instructions, hooks, and MCP servers across all of them: "any developer runs `apm install` and gets the same
agent context across GitHub Copilot, Claude Code, Cursor, OpenCode, Codex, Gemini, Windsurf, and Kiro"
([landing page](https://microsoft.github.io/apm/), [What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**The problem it solves.** Real teams are multi-harness by choice (e.g., Meridian uses Copilot, Claude Code,
and Cursor). Without parity, each harness needs its own hand-maintained files and they inevitably diverge.
APM compiles one source into each harness's native location — "`.github/` for Copilot, `.claude/` for Claude
Code, `.cursor/` for Cursor …" — so the same intent lands everywhere at once
([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Key distinctions.**
- *Restoring context ≠ owning the runtime.* APM writes "the files each tool already understands and stays out
  of the way at agent runtime" — it does not run, proxy, or sandbox the agent
  ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)). Runtime behavior "is your harness's
  domain" ([landing page](https://microsoft.github.io/apm/)).
- *Default vs. explicit targets.* Eight harnesses are configured by default; Antigravity is registered as an
  explicit-only target ([The three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)).
  This is why the chapter says "many harnesses" and lists the eight rather than promising "every tool ever."

**Common misconceptions.**
- *"APM is a new harness / replaces my agent."* No — APM is a dependency manager *for* harnesses; it neither
  replaces them nor deep-dives their runtime behavior.
- *"APM is a marketplace or registry."* No — "Any git repository is a valid APM package. Marketplaces are an
  optional discovery surface, not a requirement" ([What is APM?](https://microsoft.github.io/apm/concepts/what-is-apm/)).

**Implemented in APM by:** the harness `targets` declared in `apm.yml` and the fan-out performed by
`apm install` (and `apm compile`), writing to each harness's native directory. Exact target list, default vs.
explicit-only behavior, and per-harness paths are confirmed by the explorer.

---

## Sources

Official APM documentation (primary):
- What is APM? — <https://microsoft.github.io/apm/concepts/what-is-apm/>
- The three promises — <https://microsoft.github.io/apm/concepts/the-three-promises/>
- Docs landing page — <https://microsoft.github.io/apm/>
- Consumer ramp — <https://microsoft.github.io/apm/consumer/>
- Enterprise ramp — <https://microsoft.github.io/apm/enterprise/>

Official repository:
- microsoft/apm README (Why APM; the three promises; "portable nor reproducible"; policy vs. runtime planes) —
  <https://github.com/microsoft/apm>

Foundations APM is built on (named for context; detailed in Ch. 3):
- AGENTS.md — <https://agents.md>
- Agent Skills / SKILL.md — <https://agentskills.io>
- Model Context Protocol (MCP) — <https://modelcontextprotocol.io>

---

## Artifact path

`content/research/01-the-context-problem-theory.md`
