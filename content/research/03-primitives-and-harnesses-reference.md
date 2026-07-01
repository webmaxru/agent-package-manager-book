# Chapter 3 — Primitives & Harnesses · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 3 supplies the **vocabulary** — the seven primitive types and the
> primitive-vs-harness split (theory brief:
> [`03-primitives-and-harnesses-theory.md`](03-primitives-and-harnesses-theory.md)). This reference
> **grounds that taxonomy in what APM actually deploys**: it installs the public sample package with a
> target, lists the real files that land on disk, and shows the *same source* fanning out to two
> harnesses. Manifest authoring lands in Ch4; `apm install`/restore in Ch5.
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dirs (outside repo):**
> `%TEMP%\apm-ch03b` (copilot target), `%TEMP%\apm-ch03c` (claude target),
> `%TEMP%\apm-ch03-plugin` (plugin scaffold). **Network:** available; all installs used the **public**
> `microsoft/apm-sample-package` — no tokens, no private sources.

---

## Theory anchors (Chapter 3)

Each feature note below links to a concept from the theory brief:

| Ch3 concept | What it establishes | Confirmed here by |
|---|---|---|
| **C1 — Primitives: atomic units** | Only files under recognised primitive dirs are discovered/deployed | `.apm/{instructions,prompts,skills,agents}/` source → typed deploy |
| **C2 — The seven-type vocabulary** | instruction · prompt · skill · agent · hook · plugin · MCP server, each distinct | Real deploy of 4 types + CLI surface for plugin/MCP/hook |
| **C3 — Standards underneath** | instructions⇒AGENTS.md · skills⇒SKILL.md · MCP | `apm compile` → AGENTS.md; `SKILL.md` deployed verbatim; `dependencies.mcp` |
| **C4 — Primitives vs. harnesses** | one source set → each harness's native location, via `targets` | copilot vs. claude fan-out; `apm targets` deploy-dir table |

---

## The evidence: what the sample package actually deploys

**Source package** (`microsoft/apm-sample-package`, description: *"demonstrating all primitive types —
instructions, prompts, skills, and agents"*). Its authoring layout under `.apm/` (cached in
`apm_modules/`):

```text
.apm/agents/design-reviewer.agent.md
.apm/instructions/design-standards.instructions.md
.apm/prompts/accessibility-audit.prompt.md
.apm/prompts/design-review.prompt.md
.apm/skills/style-checker/SKILL.md
```

Its own `apm.yml` pulls **one transitive skill** via a monorepo **subpath** dependency:

```yaml
# apm_modules/microsoft/apm-sample-package/apm.yml (verbatim, v0.23.1)
name: apm-sample-package
version: 1.0.0
description: Sample APM package demonstrating all primitive types — instructions, prompts, skills, and agents.
dependencies:
  apm:
    - github/awesome-copilot/skills/review-and-refactor   # owner/repo/<subpath> → a single skill
```

### Deploy #1 — `--target copilot` (`%TEMP%\apm-ch03b`)

Command + install summary (verbatim):

```text
apm install microsoft/apm-sample-package --target copilot
  [+] microsoft/apm-sample-package @fb285168
  |-- 2 prompts integrated -> .github/prompts/
  |-- 1 agents integrated -> .github/agents/
  |-- 1 instruction(s) integrated -> .github/instructions/
  |-- 1 skill(s) integrated -> .agents/skills/
  [+] github.com/github/awesome-copilot/skills/review-and-refactor @a4aebcd4
  |-- Skill integrated -> .agents/skills/
  [i] Added apm_modules/ to .gitignore
```

**Exact files on disk (the deployed-file evidence):**

```text
.github/instructions/design-standards.instructions.md
.github/prompts/accessibility-audit.prompt.md
.github/prompts/design-review.prompt.md
.github/agents/design-reviewer.agent.md
.agents/skills/style-checker/SKILL.md            # package's own skill
.agents/skills/review-and-refactor/SKILL.md      # TRANSITIVE, from github/awesome-copilot
```

### Deploy #2 — `--target claude` (`%TEMP%\apm-ch03c`, same source package)

```text
apm install microsoft/apm-sample-package --target claude
  [+] microsoft/apm-sample-package @fb285168
  |-- 1 agents integrated -> .claude/agents/
  |-- 2 commands integrated -> .claude/commands/     # prompts PROJECTED to commands
  |-- 1 rule(s) integrated -> .claude/rules/         # instruction PROJECTED to rule
  |-- 1 skill(s) integrated -> .claude/skills/
  [+] github.com/github/awesome-copilot/skills/review-and-refactor @a4aebcd4
  |-- Skill integrated -> .claude/skills/
  [!] Claude command design-review: frontmatter keys not supported for claude commands
      and were dropped: mode. Supported keys: allowed-tools, argument-hint, description, input, model.
```

**Exact files on disk:**

```text
.claude/rules/design-standards.md
.claude/commands/accessibility-audit.md
.claude/commands/design-review.md
.claude/agents/design-reviewer.md
.claude/skills/style-checker/SKILL.md
.claude/skills/review-and-refactor/SKILL.md
```

> **This is portability made concrete (C4):** one source primitive set, zero source edits, two harnesses,
> two completely different on-disk layouts — and even different *names* (`instruction`→`rule`,
> `prompt`→`command`). The intent is identical; the file is whatever each harness natively reads.

---

## Primitive → deploy-path map (the map to return to the author)

| Primitive (source `.apm/…`) | Implements concept | Copilot (`.github/…`) — native | Claude (`.claude/…`) — compiled |
|---|---|---|---|
| **instruction** `instructions/*.instructions.md` | C2 (always-on guardrail) / C3 (AGENTS.md) | `.github/instructions/*.instructions.md` | `.claude/rules/*.md` (→ **rule**) |
| **prompt** `prompts/*.prompt.md` | C2 (user-invoked workflow) | `.github/prompts/*.prompt.md` | `.claude/commands/*.md` (→ **command**; `mode` key dropped) |
| **agent** `agents/*.agent.md` | C2 (persona) | `.github/agents/*.agent.md` | `.claude/agents/*.md` |
| **skill** `skills/<name>/SKILL.md` | C2 (model-invoked) / C3 (SKILL.md) | `.agents/skills/<name>/SKILL.md` (shared) | `.claude/skills/<name>/SKILL.md` (native) |

> **Skill placement nuance (real, observed):** targeting **copilot** put skills in the **cross-client**
> `.agents/skills/`, while targeting **claude** put them in claude-native `.claude/skills/`. `apm compile`
> confirms the model: the **`agent-skills`** meta-target deploys to `.agents/skills/` (read by
> VS Code/Copilot and other clients); `--legacy-skill-paths` forces per-client dirs (e.g. `.cursor/skills/`).

---

## Feature reference — the seven primitive types

### 1. Instruction — always-on guardrails
- **Implements concept:** C2 (*instruction = always on*, ambient, `applyTo`-scoped) and C3 (compiles toward
  **AGENTS.md**).
- **Source / deploy (real):** authored `.apm/instructions/design-standards.instructions.md` →
  **copilot** `.github/instructions/design-standards.instructions.md`; **claude** `.claude/rules/design-standards.md`.
- **Minimal example (verbatim deployed frontmatter, v0.23.1):**
  ```markdown
  ---
  applyTo: "**"
  ---
  # Design Standards
  - Use semantic HTML elements (`<nav>`, `<main>`, `<section>`) instead of generic `<div>` wrappers
  - Ensure all interactive elements have visible focus indicators
  ```
- **When to use:** persistent rules the agent must read every turn (coding standards, "never log card data").
  **When not:** anything a human should trigger on demand (that's a prompt) or the model should reach for
  contextually (that's a skill).
- **Caveat:** `apm compile` warned this file is *"Missing 'description' in frontmatter"* — instructions
  compile cleanest with a `description`. Copilot reads `.github/instructions/` directly, so APM **omits
  AGENTS.md** to avoid duplicate context (pass `--force-instructions` to emit it anyway).

### 2. Prompt — user-invoked, parameterized workflow
- **Implements concept:** C2 (*prompt = you run it*, "a callable program for an LLM"); prompt⇄command are the
  **same source** (C2's prompt-vs-command note).
- **Source / deploy (real):** `.apm/prompts/design-review.prompt.md` → **copilot**
  `.github/prompts/design-review.prompt.md` (native prompt); **claude** `.claude/commands/design-review.md`
  (compiled to a `/command`).
- **Minimal example (verbatim deployed frontmatter):**
  ```markdown
  ---
  mode: agent
  description: "Review code for design system compliance and visual consistency"
  ---
  # Design Review
  Review the current codebase for design system compliance. Check for: ...
  ```
- **When to use:** a repeatable, named, multi-step task a human kicks off ("run the design review").
  **When not:** background rules (instruction) or autonomous know-how (skill).
- **Caveat (compile-time normalization, observed):** Claude commands support only
  `allowed-tools, argument-hint, description, input, model` — APM **dropped the `mode` key** and warned.
  This is a concrete "compiled, not native" cell: the projection is lossy by design.

### 3. Skill — model-invoked capability (SKILL.md)
- **Implements concept:** C2 (*skill = the model reaches for it*, progressive disclosure) and C3 (**is** the
  Agent Skills / SKILL.md standard).
- **Source / deploy (real):** `.apm/skills/style-checker/SKILL.md` → **copilot**
  `.agents/skills/style-checker/SKILL.md`; **claude** `.claude/skills/style-checker/SKILL.md`. A skill is a
  **folder** (`SKILL.md` + optional bundled resources), not a single file.
- **Minimal example (verbatim deployed head):**
  ```markdown
  # Style Checker
  Check code against the project's style guidelines and design system standards.
  ## When to Use
  Use this skill when:
  - Reviewing pull requests for style compliance
  ```
- **When to use:** specialized procedure loaded only when a task matches its description (keeps context lean).
  **When not:** always-on rules (instruction) or a fixed human-run checklist (prompt).
- **Transitive evidence:** the package's `apm.yml` pulled `github/awesome-copilot/skills/review-and-refactor`
  — deployed alongside as a second skill. The lockfile types it `package_type: claude_skill`,
  `is_virtual: true`, `resolved_by: microsoft/apm-sample-package` (a dependency-of-a-dependency).

### 4. Agent — a bounded persona
- **Implements concept:** C2 (*agent = who is acting*; a persona with its own scope/tools/system prompt).
- **Source / deploy (real):** `.apm/agents/design-reviewer.agent.md` → **copilot**
  `.github/agents/design-reviewer.agent.md`; **claude** `.claude/agents/design-reviewer.md`.
- **Minimal example (verbatim deployed head):**
  ```markdown
  ---
  description: "A design review specialist that enforces design system standards"
  ---
  # Design Reviewer
  You are a design review specialist. Your role is to ensure code follows the project's design system ...
  ```
- **When to use:** a specialist that *owns* a task end to end (its own tools/boundaries). **When not:** a
  reusable procedure any agent can pull in — that's a skill (one agent can use many skills).

### 5. Plugin — a bundle of primitives
- **Implements concept:** C2 (*plugin = packaging format*, "bundles of the primitives above, packaged for
  one-shot install"; normalized into primitives at install time).
- **Deploy mechanism (real scaffold, `apm plugin init sample-plugin -y`):** a plugin is a package whose
  root carries a **`plugin.json`** marker beside `apm.yml`:
  ```json
  { "name": "sample-plugin", "version": "0.1.0",
    "description": "APM project for sample-plugin",
    "author": { "name": "..." }, "license": "MIT" }
  ```
  The scaffolded `apm.yml` also gains a `devDependencies.apm: []` bucket (plugin-author dev deps).
  `apm plugin --help` → only `init`; distribution is via `apm pack` / `apm publish`.
- **When to use:** ship several related primitives (an instruction + prompt + skill) as **one installable
  unit**. **When not:** a single primitive — declare it directly. At install, a plugin **unpacks into the
  same typed primitives** as above; it is not a new runtime capability.

### 6. MCP server — governed access to external tools
- **Implements concept:** C2 (*MCP server = external tools the agent connects to*) and C3 (the **MCP**
  standard). APM **declares and gates** the connection; it **does not ship the server's code**.
- **Deploy mechanism (surface confirmed; `apm mcp --help` → `install|list|search|show`):** declared in the
  manifest's **second bucket**, `dependencies.mcp` (empty in a fresh `apm init`: `mcp: []`). Added with
  `apm mcp install` (alias for `apm install --mcp`):
  ```text
  apm mcp install fetch -- npx -y @modelcontextprotocol/server-fetch      # stdio (command)
  apm mcp install api --transport http --url https://example.com/mcp      # remote
  # transports: stdio | http | sse | streamable-http ; --env KEY=VALUE ; --header KEY=VALUE ; --no-policy
  ```
  Minimal manifest shape (from the two-bucket manifest + `mcp install` contract):
  ```yaml
  # apm.yml — MCP declared explicitly (APM blocks undeclared/transitive MCP by default)
  dependencies:
    apm: []
    mcp:
      fetch:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-fetch"]
  ```
- **When to use:** give the agent a governed tool/data connection (each harness gets its MCP config written).
  **When not:** anything runnable as an in-repo primitive — MCP is for *external* processes.
- **Status:** **SKIPPED-live** here — the sample package ships `mcp: []`, and a live `mcp install` is deferred
  to the security/policy chapters (Ch8–9) where gating (`--no-policy`, transitive blocking) is the point.
  Exact per-harness MCP config paths to be confirmed when a real server is added.

### 7. Hook — lifecycle handler around tool calls
- **Implements concept:** C2 (*hook = deterministic automation* at `PreToolUse`/`PostToolUse`/`Stop`, run by
  the harness runtime, not invoked by user or model).
- **Deploy mechanism:** authored under `.apm/hooks/` (a recognised primitive dir per C1) and compiled into
  each harness's hook config; **there is no dedicated `apm hook` CLI verb** (absent from `apm --help`).
- **When to use:** enforce something *every* tool call must respect (block a command, log an action).
  **When not:** guidance the model may weigh — that's an instruction.
- **Status:** **not in the sample package** (no `.apm/hooks/`), so **no live deploy captured**. Reach is
  bounded — per the theory brief's matrix note, some harnesses have no hooks (e.g. OpenCode). Treat hooks as
  **declare-and-compile, harness-dependent**; confirm per-harness hook paths against the compatibility matrix
  when a hooks-bearing package is available.

---

## The harness-target mechanism (C4)

### `targets` — the declaration; the harness — the runtime
`apm targets` resolves which harnesses a project builds for and **where each deploys** (verbatim table,
v0.23.1, in `%TEMP%\apm-ch03b` after the copilot install):

```text
  TARGET       STATUS     SOURCE                    DEPLOY DIR
  copilot      active     .github/instructions/     .github/
  claude       inactive   needs CLAUDE.md           .claude/
  cursor       inactive   needs .cursor/            .cursor/
  codex        inactive   needs .codex/             .codex/
  gemini       inactive   needs GEMINI.md           .gemini/
  opencode     inactive   needs .opencode/          .opencode/
  windsurf     inactive   needs .windsurf/          .windsurf/
  kiro         inactive   needs .kiro/              .kiro/
```

**Harness → deploy-dir map (confirmed):**

| Target slug | Deploy dir | Notes |
|---|---|---|
| `copilot` (alias **`vscode`**) | `.github/` | `active` here — auto-detected because `.github/instructions/` exists |
| `claude` | `.claude/` | |
| `cursor` | `.cursor/` | |
| `codex` | `.codex/` | |
| `gemini` | `.gemini/` | |
| `opencode` | `.opencode/` | |
| `windsurf` | `.windsurf/` | |
| `kiro` | `.kiro/` | |
| `antigravity` (alias `agy`) | `.agents/` | **explicit-only** — *not* part of `all` |
| `agent-skills` (meta) | `.agents/skills/` | cross-client skills location |

- **Eight default targets** = `copilot claude cursor codex gemini opencode windsurf kiro` (this is exactly
  `--target all` per `apm compile --help`). `antigravity` and `agent-skills` are opt-in extras.
- **Target vs. harness (C4):** you *list* `targets` in `apm.yml` (or pass `--target`); the *harness* is what
  consumes the compiled output. `apm targets` is the resolver in between.
- **Auto-detect vs. pin:** with no `targets:` in `apm.yml`, APM marks a harness `active` when its marker
  dir/file is present (here, `.github/instructions/` → copilot active). `apm targets --help` advises pinning
  `targets:` explicitly when auto-detection guesses wrong (e.g. a `CLAUDE.md` that's just documentation).

### `--target` as a run override (behavioral nuance)
Because `apm-ch03b` was created with `apm init` **first**, the manifest already existed — so
`--target copilot` reported *`Targets: copilot (source: --target flag)`* and did **not** persist a
`targets:` key to `apm.yml`. (Contrast: installing into an *empty* dir, where APM creates `apm.yml` and
**persists** the target.) Rule of thumb for the author: **`--target` overrides for that run; pin in
`apm.yml` to make it durable.**

### `apm compile` — the AGENTS.md compiler (C3)
`apm compile` — *"Compile APM context into distributed AGENTS.md files."* Key facts from `--help` + a
`--dry-run`:
- **Targets accepted:** `copilot, claude, cursor, opencode, codex, gemini, antigravity, windsurf, kiro,
  agent-skills, all` — and **`vscode` is accepted and normalizes to the Copilot `.github/` family**
  (see below).
- `--dry-run` previews *placement decisions*; `--validate` checks primitives without writing; `--clean`
  removes orphaned `AGENTS.md`/`CLAUDE.md` (never hand-authored files); `--root DIR` writes outputs under a
  scratch dir (pairs with `apm install --root` for verification).

### copilot ↔ vscode normalization (caveat resolved)
`apm compile --target vscode --dry-run` (v0.23.1) accepts `vscode` and routes it to the Copilot family:

```text
[i] Targets: vscode  (source: --target flag)
[i] Compiling for AGENTS.md + .github/copilot-instructions.md + .github/prompts/ + .github/agents/
```

So **`vscode` is an accepted alias that normalizes to `copilot` → `.github/`** (VS Code's GitHub Copilot).
The canonical slug printed by `apm targets` / `compile --help` is **`copilot`**; `vscode` is honored as an
input and does not create a separate `.vscode/` layout.

---

## Primitive → deploy-path map (compact, for the author)

```text
SOURCE (.apm/…)                     COPILOT (--target copilot)              CLAUDE (--target claude)
instructions/*.instructions.md  ->  .github/instructions/*.instructions.md  .claude/rules/*.md
prompts/*.prompt.md             ->  .github/prompts/*.prompt.md             .claude/commands/*.md   (mode: dropped)
agents/*.agent.md               ->  .github/agents/*.agent.md               .claude/agents/*.md
skills/<name>/SKILL.md          ->  .agents/skills/<name>/SKILL.md          .claude/skills/<name>/SKILL.md
plugin.json (marker)            ->  (unpacked into the primitives above)    (same)
dependencies.mcp: {...}         ->  <harness MCP config> (declared+gated, not shipped)
.apm/hooks/…                    ->  <harness hook config> (declare+compile, harness-dependent)
```

---

## Caveats & surprises for the author

1. **One source → many harnesses is real and *lossy by design*.** Same package, `--target copilot` vs.
   `--target claude`, produced different dirs *and different names* (`instruction`→`rule`,
   `prompt`→`command`) — and dropped an unsupported frontmatter key (`mode`) with a warning. Use this as the
   chapter's concrete portability demo; note that "compiled ≠ byte-identical."
2. **Skill location depends on target.** copilot → cross-client `.agents/skills/`; claude → native
   `.claude/skills/`. The `agent-skills` meta-target (`.agents/skills/`) is the shared home; per-client
   layouts are opt-in via `--legacy-skill-paths`.
3. **`vscode` ⇒ `copilot`.** `vscode` is accepted and normalizes to the `.github/` Copilot family; the
   canonical slug is `copilot`. No separate `.vscode/` output.
4. **Hooks: declare-and-compile, no CLI verb, harness-dependent.** There is no `apm hook` command; hooks are
   authored under `.apm/hooks/` and compiled per harness, and not every harness supports them. The sample
   package ships none, so no live hook deploy was captured.
5. **MCP is the manifest's *second bucket*, declared not shipped.** `dependencies.mcp` (empty by default);
   add with `apm mcp install`. APM writes each harness's MCP config and gates it; the server runs elsewhere.
   Live MCP + policy gating deferred to Ch8–9.
6. **`--target` is a per-run override when `apm.yml` exists.** It does *not* persist a `targets:` key unless
   APM is creating the manifest fresh. Pin `targets:` in `apm.yml` for durable multi-harness builds.
7. **Only recognised primitive dirs deploy (C1).** The sample's `README.md`, `LICENSE`, `SECURITY.md`, etc.
   are ignored; only `.apm/{instructions,prompts,skills,agents}/` content became typed, deployed primitives.
8. **Lockfile records content integrity per primitive.** `apm.lock.yaml` lists `deployed_files` and a
   per-file `sha256` plus a package `content_hash` (foundation for the Ch6 lockfile chapter) — e.g. the
   sample resolved to `resolved_commit: fb2851683…`, transitive skill to `a4aebcd4…`.

---

## Commands run (v0.23.1; PATH refreshed per call; exclusive terminal)

```powershell
# %TEMP%\apm-ch03b — copilot target
apm --version                                                # -> APM CLI version 0.23.1
apm init -y                                                  # fresh apm.yml (apm: [], mcp: [], targets commented)
apm install microsoft/apm-sample-package --target copilot   # REAL install; 6 files deployed (+1 transitive skill)
apm --help                                                  # top-level surface (no `hook` verb)
apm mcp --help ; apm mcp install --help                     # install|list|search|show ; transports/flags
apm plugin --help ; apm plugin init --help                  # plugin init -> plugin.json + apm.yml
apm compile --help                                          # -> distributed AGENTS.md; target legend
apm targets ; apm targets --help                            # harness -> DEPLOY DIR table
apm compile --target vscode --dry-run                       # proves vscode -> .github/ (copilot) normalization

# %TEMP%\apm-ch03c — claude target (same source package)
apm init -y ; apm install microsoft/apm-sample-package --target claude   # deploys to .claude/{agents,commands,rules,skills}

# %TEMP%\apm-ch03-plugin — plugin scaffold
apm plugin init sample-plugin -y                            # real plugin.json marker + devDependencies bucket
```

## Sources
- Installed CLI **apm 0.23.1** — `--version`, per-command `--help`, and **live installs** into
  `%TEMP%\apm-ch03b` / `apm-ch03c` (primary, empirical). Deployed-file lists and `apm.lock.yaml` captured
  from the scratch trees.
- Sample package tree + its `apm.yml` (`apm_modules/microsoft/apm-sample-package/`), showing `.apm/` source
  layout and the transitive `github/awesome-copilot/skills/review-and-refactor` subpath dependency.
- Theory brief — [`03-primitives-and-harnesses-theory.md`](03-primitives-and-harnesses-theory.md)
  (concept definitions C1–C4).
- Official docs — <https://microsoft.github.io/apm/concepts/primitives-and-targets/> (primitive catalogue,
  target legend, native/compiled matrix) and <https://microsoft.github.io/apm/concepts/glossary/>
  (primitive/harness/target/hook/plugin/MCP definitions).
