# Chapter 4 — The Manifest: `apm.yml` · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 4 is where the reader **authors a real manifest** for the first time. This
> reference grounds every `apm.yml` key in the **actual `apm init` output** and proves the Meridian
> v0.1.0 example end to end: one local instruction under `.apm/`, deployed by a real `apm install`
> to three harnesses. Theory brief (forthcoming):
> [`04-the-manifest-apm-yml-theory.md`](04-the-manifest-apm-yml-theory.md) — the manifest is the
> **Portability** surface (declared intent, one file, restored identically everywhere). Dependency
> *installs* land in Ch5; the lockfile in Ch6; MCP/policy in Ch8–9.
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dirs (outside repo):**
> `%TEMP%\apm-ch04` (canonical Meridian v0.1.0 artifact), `%TEMP%\apm-ch04x` (throwaway
> shape-experiments: explicit `includes:` list, allowlist test, `scripts:`). **Network:** available;
> **no packages installed and no tokens used** — the whole chapter is *local* (a self-authored
> instruction), so every command in this note is deterministic and offline-safe.

---

## Theory anchors (Chapter 4)

The manifest implements **Portability**: you *declare* the agent context your repo needs in one
repo-owned file, and any developer on any supported harness restores the same intent. Feature notes
below link back to these anchors (to be finalized against the theory brief):

| Ch4 concept | What it establishes | Confirmed here by |
|---|---|---|
| **P1 — Manifest = declared intent** | `apm.yml` is the single human-authored source of truth; you edit it, APM derives the rest | verbatim `apm init` output; `apm install` reads `apm.yml` |
| **P2 — One source → every harness** | primitives are authored once under `.apm/` and *projected* to each harness's native shape | one instruction → `.github/instructions/` + `.claude/rules/` + `.cursor/rules/` |
| **P3 — Targets are portability, not lock-in** | `targets:` names *where* to deploy; the source never changes per-harness | `targets: [copilot, claude, cursor]` fans out from one file |
| **P4 — Typed dependency buckets** | `dependencies.apm` (packages) and `dependencies.mcp` (tools) are declared, pinnable, auditable | empty buckets in a fresh init; verified `mcp` object shape |

---

## The evidence: what `apm init` actually generates (v0.23.1)

`apm init -y` (non-interactive; `-y` = "skip prompts, use auto-detected defaults") in an empty dir
produced **exactly** this — the canonical key set the chapter must teach:

```yaml
# apm.yml — verbatim from `apm init -y` (v0.23.1), dir name "apm-ch04"
name: apm-ch04
version: 1.0.0
description: APM project for apm-ch04
author: Maxim Salnikov
# Which agent platforms to deploy to (uncomment to pin):
# targets:
#   - copilot
#   - claude

dependencies:
  apm: []
  mcp: []
includes: auto
scripts: {}
```

> **Author, this block is the anchor for the whole chapter.** Three things surprise readers coming
> from the running-example spec, and all three are corrected below: (1) `targets:` is **commented
> out** by default; (2) there is **no `license:` key** — the identity line is `author:`; (3)
> `includes:` defaults to the literal **`auto`**, not an explicit file list.

### Per-key reference

| Key | Type | Default from `init` | Meaning | Implements | When to use / pitfalls |
|---|---|---|---|---|---|
| `name` | string | dir name (`apm-ch04`) | Package identity (used when this repo is consumed as a dependency). | P1 | Use a stable, descriptive slug (`meridian-checkout-agent-context`). Changing it later is a rename. |
| `version` | string (semver) | `1.0.0` | The package's own version. | P1 | Start Meridian at `0.1.0` (pre-1.0, one instruction). Advances one beat per chapter. |
| `description` | string | `APM project for <name>` | Human summary shown in listings. | P1 | One sentence. Replace the boilerplate. |
| `author` | string | git `user.name` (`Maxim Salnikov`) | Optional attribution metadata. | P1 | Auto-detected. Set to the team/org for a shared repo. Not required for install to work. |
| `targets` | list (**commented**) | *(absent/commented)* | Which harnesses to deploy to. When **absent**, APM **auto-detects** from the repo. | P2, P3 | **Uncomment and pin** for a shared repo so everyone deploys the same set. Values: `copilot, claude, cursor, opencode, codex, gemini, windsurf, kiro` (+ `agent-skills`, `antigravity`). |
| `dependencies.apm` | list | `[]` | APM package dependencies (git-sourced primitives). | P4 | Items are `owner/repo[/subpath][#ref]`. **Pin the ref.** Empty is valid. Live install → Ch5. |
| `dependencies.mcp` | list of objects | `[]` | MCP server declarations (external tools). | P4 | **List of objects, not a name→map** (see §"Dependency shapes"). Undeclared transitive MCP is blocked (Ch8). |
| `includes` | `auto` \| list | `auto` | Which local `.apm/` primitive sources to compile & deploy. | P1, P2 | **Keep `auto`** — it auto-discovers everything under `.apm/`. An explicit list is accepted but **non-restrictive** (see caveat). |
| `scripts` | map | `{}` | Named shell commands: `name: "command"`. | P1 | Run with `apm run <name>` (experimental). Values are literal shell strings. |

---

## Worked example — Meridian v0.1.0 (verified end to end)

**Story beat (Ch4):** Meridian's first repo-owned manifest ships **one** shared instruction and
compiles it to all three harnesses the team uses (Copilot, Claude Code, Cursor). No dependencies
yet, no network.

### 1. The verified manifest (`apm.yml`)

Caption: **Minimal Meridian manifest — one local instruction, three targets. Verified with
`apm install` on apm v0.23.1; no network.** This is the exact file that produced the deploys below;
it is `apm init`'s output with `name`/`version`/`description` set and `targets:` uncommented.

```yaml
name: meridian-checkout-agent-context
version: 0.1.0
description: Shared AI-agent context for the Meridian checkout service.
author: Maxim Salnikov
targets:
  - copilot
  - claude
  - cursor

dependencies:
  apm: []
  mcp: []
includes: auto
scripts: {}
```

> **Minimality note for the author:** `dependencies:` (empty buckets), `includes: auto`, and
> `scripts: {}` are what `apm init` emits, so keeping them is *faithful* even though they're inert
> at v0.1.0. If the chapter wants the tightest possible block, the required lines are
> `name` + `version` + `targets` + the `.apm/` source; the empty scaffolding can be elided in prose
> but the verified file keeps it to match a real `apm init`.

### 2. The source primitive (authored once)

Path: `.apm/instructions/meridian-checkout.instructions.md` — a recognized primitive dir (Ch3, C1),
so `includes: auto` discovers it with zero extra config.

```markdown
---
description: Meridian checkout service engineering rules
applyTo: "**/*.{ts,tsx,md}"
---

Use the Meridian `Money` value object for currency math. Treat checkout retries as
idempotent operations keyed by `paymentAttemptId`. Never suggest storing card data in
application logs.
```

### 3. The deploy command + real output

```text
apm install
  [i] Targets: claude, copilot, cursor  (source: apm.yml)
    [+] <project root> (local)
    |-- 3 rule(s) integrated -> 3 targets
  [i] Added apm_modules/ to .gitignore
  [*] Installed 1 APM dependency in 2.5s.
```

`apm install` with **no package argument** = "restore/deploy from `apm.yml`". The local project is
treated as one `<project root> (local)` "dependency"; its single instruction is deployed to the 3
targets. APM also auto-adds `apm_modules/` to `.gitignore`.

### 4. The deployed outputs — one source, three native shapes (P2 made concrete)

Exact files on disk after `apm install`:

```text
.github/instructions/meridian-checkout.instructions.md   # copilot
.claude/rules/meridian-checkout.md                       # claude
.cursor/rules/meridian-checkout.mdc                      # cursor
```

And the **frontmatter is projected per harness** (verbatim):

| Harness | Deployed path | Frontmatter (verbatim) | Transform vs. source |
|---|---|---|---|
| **copilot** | `.github/instructions/meridian-checkout.instructions.md` | `description:` + `applyTo:` | **unchanged** (native `.instructions.md`) |
| **claude** | `.claude/rules/meridian-checkout.md` | `paths:` only | `applyTo` → **`paths`**; `description` **dropped**; `.md` |
| **cursor** | `.cursor/rules/meridian-checkout.mdc` | `description:` + `globs:` | `applyTo` → **`globs`**; `description` kept; **`.mdc`** ext |

```markdown
# .claude/rules/meridian-checkout.md  (verbatim)
---
paths:
  - "**/*.{ts,tsx,md}"
---
...
```
```markdown
# .cursor/rules/meridian-checkout.mdc  (verbatim)
---
description: Meridian checkout service engineering rules
globs: "**/*.{ts,tsx,md}"
---
...
```

> **This is the chapter's payoff (P2/P3):** the reader edits *one* file, runs *one* command, and the
> same intent lands as `.github/instructions/*.instructions.md`, a Claude **rule** (`paths:`), and a
> Cursor **`.mdc` rule** (`globs:`) — different dirs, different frontmatter keys, different
> extensions, **zero per-harness edits**. It's the Ch3 taxonomy proven on the reader's *own* content.

### 5. The generated lockfile (local-only shape)

`apm install` also wrote `apm.lock.yaml`. With only local primitives (no git deps), it records the
**deployed files and their content hashes** — no `dependencies`. Full lockfile treatment is Ch6;
this is what it looks like at v0.1.0:

```yaml
# apm.lock.yaml — verbatim (v0.23.1), local-only
lockfile_version: '1'
generated_at: '2026-07-01T23:50:31.310975+00:00'
dependencies: []
local_deployed_files:
- .claude/rules/meridian-checkout.md
- .cursor/rules/meridian-checkout.mdc
- .github/instructions/meridian-checkout.instructions.md
local_deployed_file_hashes:
  .claude/rules/meridian-checkout.md: sha256:3f8ff5771908aa7f602fd6279a2ff775b54613d1c9fc44b4b1dcc31c6ead5be1
  .cursor/rules/meridian-checkout.mdc: sha256:87d93a43c378ba9933e4b9e5db4b7df8d84e8e258480649122ae0829774ff8d2
  .github/instructions/meridian-checkout.instructions.md: sha256:bf0a95675dd08131c972acfa85ba61e73e9d9ab0c042f1fcb59fb12cb601da49
```

---

## Dependency declaration shapes (for the manifest, shown not installed)

Ch4 authors the *shape*; Ch5 runs the live install. Both buckets confirmed against v0.23.1.

### `dependencies.apm` — git-sourced packages

List of shorthand refs. The verified Ch3 install grew this bucket to `- microsoft/apm-sample-package`
(bare). The **pinned** form the book should teach (deterministic lockfile, per
[`apm-examples.instructions.md`](../../.github/instructions/apm-examples.instructions.md)):

```yaml
dependencies:
  apm:
    - microsoft/apm-sample-package#v1.0.0                 # owner/repo#<ref> (tag/branch/SHA)
    - github/awesome-copilot/skills/review-and-refactor#main   # owner/repo/<subpath>#<ref>
```

`apm install --help` (v0.23.1) confirms shorthand `owner/repo` resolution with `--ssh`/`--https`
transport control; `#<ref>` pins the git ref (Ch2 pinning grammar). Subpath (`/skills/<name>`)
selects a single primitive from a monorepo (Ch3 transitive evidence).

### `dependencies.mcp` — external tools (**corrected shape**)

**Verified by `apm mcp install fetch -- npx -y @modelcontextprotocol/server-fetch`** (which writes
to `apm.yml`). The real v0.23.1 shape is a **list of objects**, not a name-keyed map:

```yaml
dependencies:
  apm: []
  mcp:
    - name: fetch
      registry: false            # false = self-defined (stdio) vs. resolved from an MCP registry
      transport: stdio           # stdio | http | sse | streamable-http
      command: npx               # stdio: the launcher
      args:
        - -y
        - '@modelcontextprotocol/server-fetch'
      # remote transports use `url:` (+ optional `header:`) instead of command/args
```

> ⚠️ **Correction to flag:** the Ch3 reference sketched `dependencies.mcp` as a **name→map** (`fetch:
> {command, args}`). The CLI actually writes a **list of `{name, registry, transport, …}` objects**.
> Ch4 (and any earlier chapter that shows the shape) should use the list-of-objects form above.
> Full MCP install + policy gating is Ch8; here we only show the manifest shape.

### `scripts` — named shell commands

**Verified by `apm list`** after adding two scripts: `scripts` is a **map of `name → shell command
string`**.

```yaml
scripts:
  review: "copilot -p .apm/prompts/checkout-review.prompt.md"
  claude-review: "claude -p .apm/prompts/checkout-review.prompt.md"
```

`apm list` renders them in a Script/Command table; `apm run <name> --param key=value` executes one
(`apm run` is flagged **experimental** in v0.23.1). Scripts are literal shell — no APM-specific DSL.

---

## `includes: auto` vs. an explicit list — tested, and it matters

The running-example spec assumed an **explicit** `includes:` list. Here is what v0.23.1 actually does:

- **`includes: auto` (the `apm init` default)** — auto-discovers every primitive under `.apm/`. The
  dry-run compile reported `1 instruction patterns detected` from the sole `.apm/instructions/*.md`
  with **zero** include entries. This is the recommended, zero-maintenance form. ✅
- **Explicit `includes: [".apm/instructions/meridian-checkout.instructions.md"]`** — **accepted** and
  deployed identically for the single-file case. ✅ …**but it is not a restrictive allowlist.** With a
  **second, unlisted** primitive (`.apm/instructions/second-rule.instructions.md`) present, `apm
  install` deployed **both** (`6 rule(s) integrated -> 3 targets` = 2 instructions × 3 targets). The
  unlisted primitive still shipped. ⚠️

**Recommendation for the author:** use **`includes: auto`** in every Ch4+ manifest — it matches
`apm init`, needs no upkeep, and avoids the misleading impression (from an explicit list) that you're
scoping deployment. Do **not** reproduce the running-example's explicit-list block; it diverges from
the generated manifest and does not behave as an allowlist in v0.23.1.

---

## Caveats & flags (for the author + verifier)

1. **`targets:` is commented by default.** `apm init` emits `# targets:` with a `copilot`/`claude`
   hint. Absent targets = **auto-detect**. For a shared repo, **uncomment and pin** the set
   (Meridian: `copilot, claude, cursor`). *(Differs from running-example, which showed it
   uncommented — that direction is correct; just note init's default state.)*
2. **No `license:` key from init.** The running-example's `license: MIT` is **not** part of the
   generated shape (the identity line is `author:`). `license` is optional metadata; to stay faithful
   to a real `apm init`, the verified Meridian v0.1.0 manifest **omits it**. Flag if the author wants
   it: it's harmless but not init-generated.
3. **`includes: auto`, not a list** (see section above). The single most important correction for a
   chapter whose whole job is authoring a correct manifest.
4. **`dependencies.mcp` is a list of objects** (see §Dependency shapes) — corrects the earlier
   name→map sketch.
5. **`apm install` vs. `apm compile` — use `install` for the three-file outcome.** `apm compile`
   ("compile APM context into distributed AGENTS.md files") runs a **placement optimizer**: in this
   empty scratch project (no `.ts/.tsx/.md` files matching `applyTo`), a dry-run **consolidated the
   instruction into a root `AGENTS.md`** and warned *"applyTo … matched no files - placing at project
   root."* `apm install` instead deploys the instruction **verbatim to each harness's native per-file
   location** (`.github/instructions/`, `.claude/rules/`, `.cursor/rules/`). The chapter's worked
   example must run **`apm install`** to get the clean one-source→three-files result. (Compile/AGENTS.md
   placement is a Ch5+/advanced topic; don't open it in Ch4.)
6. **`copilot` resolves to `vscode` internally.** `apm compile --target copilot,…` echoed
   `Targets: … vscode`. `apm install` echoed `copilot`. Same harness; the reader writes `copilot` in
   `targets:`. Note it so the author isn't thrown by `vscode` in compile output.
7. **`.gitignore` side effect.** Both `apm install` and `apm mcp install` auto-append `apm_modules/`
   to `.gitignore`. Expected; mention so it isn't mistaken for drift.
8. **Deploy dirs (from `apm targets`):** copilot → `.github/` (instructions under
   `.github/instructions/`), claude → `.claude/`, cursor → `.cursor/`. Other harnesses show
   `inactive` until their marker dir/file exists.

---

## For the `code-verifier`

- **Deterministic & offline:** the Meridian v0.1.0 example needs **no network** — it's a
  self-authored local instruction. Reproduce with: `apm init -y` → set `name/version/description` and
  uncomment `targets: [copilot, claude, cursor]` → author
  `.apm/instructions/meridian-checkout.instructions.md` → `apm install` → assert the three deployed
  paths exist. **Expected PASS**, no `SKIPPED-needs-network` needed.
- **Assertions:** (a) `apm install` prints `3 rule(s) integrated -> 3 targets`; (b) the three files in
  §4 exist; (c) claude frontmatter uses `paths:` (no `description`), cursor uses `globs:` + `.mdc`,
  copilot is unchanged; (d) `apm.lock.yaml` lists the three `local_deployed_files` with sha256 hashes.
- **Do NOT** ship the explicit-`includes:`-list variant or the `license:` line — both diverge from a
  real `apm init` (caveats 2–3).
- **`dependencies.apm` pinned install** (`microsoft/apm-sample-package#v1.0.0`) is **Ch5**; if shown
  in Ch4 as shape-only, no run required.

---

## Commands run (this session, apm v0.23.1, exclusive terminal)

```text
apm --version
apm init --help
apm init -y                                     # → canonical default apm.yml (verbatim above)
apm --help ; apm compile --help
apm compile --target copilot,claude,cursor --local-only --dry-run   # includes:auto discovery + placement optimizer
apm install                                     # deploy local instruction → 3 harnesses (canonical Meridian v0.1.0)
apm targets                                     # resolved deploy dirs
apm mcp install --help
apm mcp install fetch --no-policy -- npx -y @modelcontextprotocol/server-fetch   # → real dependencies.mcp shape (then reverted)
apm list                                        # → scripts: name→command shape
apm run --help
apm install --help                              # → dependencies.apm source/pin syntax
# experiments dir apm-ch04x: explicit includes: list accepted but non-restrictive (6 rules from 2×3)
```

**Artifact:** `content/research/04-the-manifest-apm-yml-reference.md` (this file).
**Canonical verified project:** `%TEMP%\apm-ch04` (Meridian v0.1.0: `apm.yml` + `.apm/…` + three
deployed harness files + `apm.lock.yaml`).
