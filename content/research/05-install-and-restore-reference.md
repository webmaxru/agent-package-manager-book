# Chapter 5 — Install & Restore · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 5 is where **Portability stops being a promise and becomes a fact** — the
> reader runs the four-command consumer loop and watches a declaration in `apm.yml` turn into
> on-disk agent context. This reference proves the loop end to end by evolving the Chapter 4
> Meridian manifest from **v0.1.0** (one local instruction, three targets) to **v0.2.0** (one
> **pinned public dependency** + one `scripts:` entry + one local prompt), running the real
> `apm install` / restore / `apm run` cycle and capturing the generated `apm.lock.yaml`.
> Theory brief: [`05-install-and-restore-theory.md`](05-install-and-restore-theory.md). The
> **lockfile itself** is Chapter 6's subject; here it is a by-product the reader should *notice*.
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dirs (outside repo):**
> `%TEMP%\apm-ch05` (canonical Meridian **v0.1.0 → v0.2.0** artifact) and `%TEMP%\apm-ch05x`
> (throwaway probes: the **no-target** install and the **harness-CLI-absent** `apm run`).
> **Network:** available; **one public package installed** (`microsoft/apm-sample-package#v1.0.0`),
> **no tokens, no live pushes**. The add step is network-bound (~56 s cold); restore is cache-served
> (~10 s). Where a step needs something not present in a clean CI box, it is flagged for the verifier.

---

## Theory anchors (Chapter 5)

Install/restore is the operation that **materializes** the manifest. Each command below links back
to the concept it implements.

| Ch5 concept (theory brief) | What it establishes | Confirmed here by |
|---|---|---|
| **C1 — Materialization** | install converts declared state (`apm.yml` + lockfile) into real files each harness reads | the add deployed 5 primitive kinds to 3 harnesses + wrote `apm.lock.yaml` |
| **C2 — The daily loop (4 commands)** | `apm init` · `apm install <pkg>` · `apm install` · `apm run <script>` is the whole everyday surface | every command in this note is one of the four (init recapped from Ch4) |
| **C3 — Restore vs. add** | bare `apm install` **restores** (idempotent, cache-served); `apm install <pkg>` **adds** (mutates `apm.yml`, re-locks) | add grew `dependencies.apm` + lockfile; bare restore was a byte-stable no-op |
| **C4 — Harness targeting at install time** | targets resolve by an explicit precedence chain; **no implicit "one true harness"** | `--target` flag beat manifest; **no-target install exits `2`** with a teaching message |

---

## The consumer loop — per-command reference (v0.23.1)

| Command | Job | Implements | Exact behavior observed | Exit |
|---|---|---|---|---|
| `apm init` | scaffold a manifest (**one-time**) | C2 | Covered in Ch4 — emits the canonical `apm.yml` (commented `targets:`, `includes: auto`, empty dep buckets). **Not re-run here.** | `0` |
| `apm install <pkg>#<ref> --target …` | **add** a dependency | C1, C3, C4 | Validates → **writes the pinned ref into `apm.yml` `dependencies.apm`** → resolves (incl. transitive) → deploys primitives to targets → writes/extends `apm.lock.yaml`. | `0` |
| `apm install` (bare) | **restore** from the lockfile | C1, C3 | Re-runs the pipeline **from the `apm_modules/` cache**; reports `(cached)` / `(files unchanged)`; lockfile **byte-stable**. The clone-onboarding path. | `0` |
| `apm install` (bare, **nothing to target**) | restore with no harness | C4 | **Fails closed:** `[x] No harness detected`, teaching message, **writes nothing**. | **`2`** |
| `apm list` | list declared scripts | C2 | Renders a `Script / Command` table from `apm.yml` `scripts:`. | `0` |
| `apm run <script>` | run a declared script (**experimental**) | C2, C4 | Compiles the script's prompt file, then **shells out to the named runtime CLI on `PATH`**. Success depends on that CLI existing. | `0` if runtime ran; `1` if runtime missing/failed |
| `apm preview <script>` | compile a script's prompt **without running it** | C2 | Shows original vs. compiled command + writes `.apm/compiled/<script>.txt`. **No runtime invoked** — offline & zero-cost. | `0` |

---

## Worked example — Meridian v0.1.0 → v0.2.0 (verified end to end)

**Story beat (Ch5):** Meridian starts Chapter 5 with the Chapter 4 manifest already owned (v0.1.0:
one shared instruction, three targets). The team then does two everyday things — **adds** a public
dependency, and declares a **script** — advancing the manifest to **v0.2.0**. A new joiner clones and
runs bare `apm install` to get byte-identical context. All three moments are captured below.

### Step 0 — the v0.1.0 baseline (recap of Ch4, reproduced)

Bare `apm install` on the Chapter 4 manifest deployed the single local instruction to all three
harnesses and wrote a **local-only** lockfile — identical shape to Ch4:

```text
apm install
  [i] Targets: claude, copilot, cursor  (source: apm.yml)
    [+] <project root> (local)
    |-- 3 rule(s) integrated -> 3 targets
  [*] Installed 1 APM dependency in 0.7s.        # exit 0
```

```yaml
# apm.lock.yaml — v0.1.0 (local-only): no dependencies, three deployed local files
dependencies: []
local_deployed_files:
- .claude/rules/meridian-checkout.md
- .cursor/rules/meridian-checkout.mdc
- .github/instructions/meridian-checkout.instructions.md
```

### Step 1 — **add** a pinned public dependency (C3 "add" · C1 · C4)

Caption: **Adding one pinned public package to Meridian. Verified with `apm install
<pkg>#<ref> --target …` on apm v0.23.1; network-bound (~56 s cold).**

```text
apm install microsoft/apm-sample-package#v1.0.0 --target copilot,claude,cursor
  [*] Validating 1 package...
  [+] microsoft/apm-sample-package#v1.0.0
  [*] Updated apm.yml with 1 new package(s)
  [>] Installing 1 new package...
  [>] Resolving microsoft/apm-sample-package...
  [>] Resolving awesome-copilot-review-and-refactor...            # <- transitive
  [i] Targets: claude, copilot, cursor  (source: --target flag)   # <- C4 precedence: flag wins
    [+] microsoft/apm-sample-package #v1.0.0 @fb285168
    |-- 2 prompts integrated   -> .github/prompts/
    |-- 3 agents integrated    -> 3 targets
    |-- 4 commands integrated  -> .claude/commands/, .cursor/commands/
    |-- 3 rule(s) integrated   -> 3 targets
    |-- 1 skill(s) integrated  -> .agents/skills/, .claude/skills/
    [+] github.com/github/awesome-copilot/skills/review-and-refactor @a4aebcd4
    |-- Skill integrated       -> .agents/skills/, .claude/skills/
    [+] <project root> (local)
    |-- 3 rule(s) adopted -> 3 targets  (files unchanged)         # <- local instruction preserved
  [!] 1 dependency unpinned: github/awesome-copilot -- add #tag or #sha to prevent drift
  [*] Installed 2 APM dependencies in 56.0s.                      # exit 0
```

**(a) `apm.yml` gains the pinned entry** (APM **re-serialized** the manifest — see caveat 3):

```yaml
dependencies:
  apm:
  - microsoft/apm-sample-package#v1.0.0     # owner/repo#<ref> — pinned, deterministic
  mcp: []
```

**(b) `apm.lock.yaml` gains two dependency records** — the **direct pinned** dep and its **transitive
virtual** dep. This is the `resolved_commit` + `content_hash` the reader must notice (Ch6 studies it):

```yaml
dependencies:
- repo_url: microsoft/apm-sample-package
  name: apm-sample-package
  host: github.com
  resolved_commit: fb2851683be0e0e7711421d518bd8dba23b0b1f6   # exact SHA, from tag v1.0.0
  resolved_ref: v1.0.0                                        # the ref you pinned
  version: 1.0.0
  package_type: apm_package
  deployed_files: [ ... 16 files across .github/ .claude/ .cursor/ .agents/ ... ]
  deployed_file_hashes: { <each file>: sha256:... }
  content_hash: sha256:744cca54cc8ff7ca90aa1dd621c2f98c6291cd793815afe8518001cc94b8aba9
- repo_url: github/awesome-copilot
  name: awesome-copilot
  host: github.com
  resolved_commit: a4aebcd4bd354b59a6a6c12ab9c5c98a9d9e0276
  version: unknown            # <- unpinned transitive dep: no resolved_ref, hence the warning
  virtual_path: skills/review-and-refactor
  is_virtual: true
  depth: 2
  resolved_by: microsoft/apm-sample-package
  package_type: claude_skill
  content_hash: sha256:9236d06a1500089ddb46975b866e9a63478e502afe7095b1980c618678a7c7fe
```

**(c) Primitives deployed** — one `apm install` fanned the sample package into every harness's native
shape (design-reviewer **agent** ×3 harnesses, accessibility-audit/design-review **commands** +
**prompts**, design-standards **rule** ×3, style-checker **skill**), plus the transitive
review-and-refactor **skill** into `.agents/skills/` + `.claude/skills/`. Your **local** instruction
was left untouched (`adopted … files unchanged`).

> **Author payoff (C1):** the manifest edit was *declaration*; this command was *materialization*.
> One pinned line + one command produced ~20 real files the three tools read natively — no
> hand-copying, and pinned by commit + content hash for the next person.

### Step 2 — **restore** on a fresh clone (C3 "restore" · C1)

Re-running **bare** `apm install` is the onboarding path. It is **idempotent and cache-served**, not
a fresh download:

```text
apm install
  [i] Targets: claude, copilot, cursor  (source: apm.yml)        # <- now from manifest, not a flag
    [+] microsoft/apm-sample-package #v1.0.0 @fb285168 (cached)   # <- served from apm_modules/
    |-- ... adopted ...
    [+] github.com/.../review-and-refactor @a4aebcd4 (cached)
    |-- (files unchanged)
    [+] <project root> (local)  |-- 3 rule(s) adopted (files unchanged)
  [*] Installed 1 APM dependency in 10.3s.                        # exit 0 (vs 56.0s cold)
```

**Idempotency proven:** the lockfile's `generated_at` stayed `2026-07-02T00:01:57.144937+00:00`
across the add *and* every restore, and the whole `apm.lock.yaml` was **byte-identical**
(SHA-256 `ABC1D860…DDA25`). The `apm_modules/` content-addressed cache (`github/`, `microsoft/`
subdirs, gitignored) is what makes restore fast and deterministic.

> **This is the chapter's headline (C3):** `git clone` + `apm install` = the same bytes on any
> machine. Restore **reproduces**; it does **not** upgrade (that's `apm update`, Ch7).

### Step 3 — declare a **script** and run it (C2 · C4 · **experimental**)

The v0.2.0 manifest adds one `scripts:` entry and a local prompt primitive:

```yaml
scripts:
  review: "copilot -p .apm/prompts/checkout-review.prompt.md"   # runtime CLI + prompt file
```

`apm list` shows it:

```text
              Available Scripts
  Script   Command
  review   copilot -p .apm/prompts/checkout-review.prompt.md
```

`apm run --help` / `apm preview --help` (both stamped **experimental**):

```text
apm run [OPTIONS] [SCRIPT_NAME]      Run a script with parameters (experimental)
apm preview [OPTIONS] [SCRIPT_NAME]  Preview a script's compiled prompt files
  -p, --param TEXT   Parameter in format name=value
  -v, --verbose      Show detailed output
```

**`apm preview review` — compile without running (offline, zero-cost):**

```text
apm preview review
  Original command:  copilot -p .apm/prompts/checkout-review.prompt.md
  Compiled command:  copilot                                   # <- the -p <file> is compiled out
  Compiled prompt files:  .apm\compiled\checkout-review.txt    # <- prompt body, frontmatter stripped
  [*] Preview complete! Use 'apm run review' to execute.       # exit 0, no runtime invoked
```

**`apm run review` — real execution (runtime present in this environment):** `copilot` **was on
`PATH`** here, so the script ran end to end. `apm` compiled the prompt, then invoked the runtime with
the **compiled content injected** (not the file path):

```text
apm run review
  [>] Running script: review
  Compiling prompt...            +- .apm/prompts/checkout-review.prompt.md
  Executing copilot runtime...   Command: copilot   Prompt content: 253 characters
  Subprocess execution:  Args: copilot -p   Content: +253 chars appended
  ... <copilot ran a real review; correctly refused to fabricate findings — no checkout code present> ...
  [+] Copilot execution completed successfully (188.68s)
  [*] Script executed successfully!                            # exit 0
```

> **Harness-CLI caveat (C4) — the load-bearing point.** `apm` **does not ship the runtimes**; it
> shells out to whatever the script names (`copilot`, `claude`, `codex`, `cursor-agent`, `gemini`,
> `opencode`, `windsurf`, `kiro`, `llm`), which must be **on `PATH`**. When the runtime is **absent**,
> `apm` still compiles the prompt, then the shell fails — verified with a script naming a bogus
> runtime:
>
> ```text
> apm run broken     # script: "nonexistent-runtime-xyz -p .apm/prompts/probe.prompt.md"
>   [>] Running script: broken
>   Compiling prompt...  +- .apm/prompts/probe.prompt.md
>   'nonexistent-runtime-xyz' is not recognized as an internal or external command...
>   [x] Script execution error: Script execution failed with exit code 1   # exit 1
> ```
>
> That failure is **a missing harness CLI, not an apm bug**. In a clean CI box with no runtime
> installed, `apm run review` would fail exactly this way (**`SKIPPED-needs-harness-CLI`** for the
> verifier). The **runtime**, not `apm`, does the agent work and incurs its latency/credits
> (this run: ~189 s, 48 AI credits). Use **`apm preview`** to inspect a script offline with no cost.

### The final v0.2.0 artifacts

**`apm.yml` (v0.2.0 — what you commit).** Bare `apm install` (restore) does **not** rewrite the
manifest, so the clean hand-authored formatting is preserved on disk:

```yaml
name: meridian-checkout-agent-context
version: 0.2.0
description: Shared AI-agent context for the Meridian checkout service.
author: Maxim Salnikov
targets:
  - copilot
  - claude
  - cursor

dependencies:
  apm:
    - microsoft/apm-sample-package#v1.0.0
  mcp: []
includes: auto
scripts:
  review: "copilot -p .apm/prompts/checkout-review.prompt.md"
```

**`apm.lock.yaml` (v0.2.0 — full local block).** After the prompt was declared, a bare `apm install`
deployed it as a **copilot prompt** *and* a **claude/cursor command** (prompt→slash-command
projection), and the lockfile's local block grew accordingly (note the three checkout-review
deployments share **one identical hash** — the prompt body is harness-agnostic):

```yaml
local_deployed_files:
- .claude/commands/checkout-review.md
- .claude/rules/meridian-checkout.md
- .cursor/commands/checkout-review.md
- .cursor/rules/meridian-checkout.mdc
- .github/instructions/meridian-checkout.instructions.md
- .github/prompts/checkout-review.prompt.md
local_deployed_file_hashes:
  .claude/commands/checkout-review.md:                    sha256:f6ca45dabe0e35fedd68caa92540c239fd82200867833e168dd05256cf342e84
  .cursor/commands/checkout-review.md:                    sha256:f6ca45dabe0e35fedd68caa92540c239fd82200867833e168dd05256cf342e84
  .github/prompts/checkout-review.prompt.md:              sha256:f6ca45dabe0e35fedd68caa92540c239fd82200867833e168dd05256cf342e84
  .claude/rules/meridian-checkout.md:                     sha256:252807b6f6a9f0c784a1356ab271b5138fdb8a9997b555d5f3a39e25951d6894
  .cursor/rules/meridian-checkout.mdc:                    sha256:cb07ae85a22a2a94accf5be778502f93b5d9a1abb3c508a6bd0e66d5cc566ac1
  .github/instructions/meridian-checkout.instructions.md: sha256:a2246d0cf63f1b4ec65bfd167f3463dd8cf274f9af4eafdbc52a518dc5a850a6
```

(The two dependency records from Step 1 are unchanged in the final lockfile.)

---

## Resolved: what a **no-target** install does in v0.23.1 (the theory's OPEN nuance)

The theory brief flagged a discrepancy between two docs pages — the CLI reference says install "exits
`2` with a teaching message", the consumer guide mentions a "Fallback: minimal output to `AGENTS.md`
only". **Verified empirically** in an isolated dir with a **targetless** manifest and **no harness
marker dirs** (no `--target`, no configured default):

```text
apm install
  [x] No harness detected
  APM scanned for harness markers (.claude/, CLAUDE.md, .cursor/, .cursorrules,
  .github/copilot-instructions.md, .github/instructions/, .github/agents/,
  .github/prompts/, .github/hooks/, .codex/, .gemini/, GEMINI.md, .opencode/,
  .windsurf/, .kiro/) but found none in this project.

  Previously APM defaulted to copilot; this is now explicit.

  Fix with one of:
    apm targets                          # see all supported harnesses
    apm install <pkg> --target claude    # deploy to a specific harness
    apm install <pkg> --target copilot
  Or declare in apm.yml:
    targets:
      - claude
  [!] Install interrupted after 1.6s.
```

**Answer for the author (C4):** in **v0.23.1** the no-target case **exits `2`** with the
`No harness detected` teaching message and **writes nothing** — the resulting tree was just `apm.yml`
+ `.apm/`, **no `AGENTS.md` fallback**. The **CLI-reference behavior is the current one**; the
consumer-guide "AGENTS.md fallback" did **not** occur. The message even states *"Previously APM
defaulted to copilot; this is now explicit"* — direct confirmation of the chapter's claim that there
is **no implicit "one true harness"**: APM fails closed and teaches rather than guessing.

---

## Caveats & flags (for the author + verifier)

1. **Restore is an idempotent *replay*, not a silent "already up to date."** Bare `apm install`
   re-runs the full pipeline **from cache**, printing `(cached)` / `adopted` / `(files unchanged)`,
   and re-emits a **byte-identical** lockfile. Frame it as "same bytes, cache-served" — do **not**
   claim APM prints a "nothing to do" line; it does not.
2. **`--target` is a per-invocation override, not persisted.** On the add, `Targets: … (source:
   --target flag)`; on the next bare install, `(source: apm.yml)`. The flag did **not** write
   `targets:` into `apm.yml`. Precedence confirmed: **`--target` > `apm.yml` targets:** (config
   default and auto-detect are the lower rungs; the no-target probe exercised the bottom).
3. **`apm install <pkg>` (add) rewrites & re-serializes `apm.yml`; bare `apm install` (restore) does
   not.** The add normalized list style (`  - copilot` → `- copilot`) and dropped the blank line
   before `dependencies:`. Content is preserved; only formatting changes. Author the committed
   manifest cleanly; expect the *add* path to reflow it. (The v0.2.0 file above is the restore-stable
   authored form.)
4. **Pinning is per-edge — transitive deps can be unpinned.** Even though the **direct** dep is
   pinned (`#v1.0.0`, `resolved_ref: v1.0.0`), its transitive `github/awesome-copilot` skill resolved
   **unpinned** (`version: unknown`, no `resolved_ref`), triggering `[!] 1 dependency unpinned … add
   #tag or #sha to prevent drift`. The **lockfile still pins it by `resolved_commit`**, so *restore*
   is deterministic — the warning is about *future `apm update` drift*, not this install. Good Ch6
   seed; mention as a real-world wrinkle, don't overclaim it as a failure.
5. **`apm run` compiles prompt-file references — scripts are not purely "literal shell."** Refines the
   Ch4 note. For `review: "copilot -p .apm/prompts/checkout-review.prompt.md"`, `apm run` **compiles
   the `.prompt.md`** (frontmatter stripped → `.apm/compiled/review.txt`) and injects the **content**
   into `copilot -p <content>` — `apm preview` shows the compiled command as bare `copilot`. Plain
   shell tokens still pass through, but a `.prompt.md` argument is compiled, not passed verbatim.
6. **`apm run` cost/latency lives in the runtime.** A real `apm run review` invoked `copilot` for
   ~189 s / 48 AI credits. `apm` is the launcher; the harness CLI does (and bills) the work. Prefer
   `apm preview` for docs/CI where you only need to see the compiled prompt.
7. **The "Installed N APM dependencies" count is informational, not a stable assertion.** It read `2`
   (add: direct + transitive), `1` (first restore), `2` (final). Don't assert a fixed number in prose.
8. **Same command-frontmatter drops as Ch4.** The sample package's Claude/Cursor **commands** drop the
   unsupported `mode:` key (`Supported keys: allowed-tools, argument-hint, description, input,
   model`); Cursor commands intentionally keep Claude-compatible frontmatter. Expected, benign.
9. **`apm_modules/` is auto-gitignored** on first install (same as Ch4). Commit `apm.yml`,
   `apm.lock.yaml`, and the deployed harness dirs; **not** `apm_modules/` (rebuilt from the lockfile).

---

## For the `code-verifier`

- **Reproduce (network required for Step 1):** in a scratch dir, author the Ch4 Meridian v0.1.0
  manifest + `.apm/instructions/meridian-checkout.instructions.md` → `apm install` (baseline, offline)
  → `apm install microsoft/apm-sample-package#v1.0.0 --target copilot,claude,cursor` (**add**,
  ~56 s, public, no token) → bare `apm install` (**restore**) → add the `review` script +
  `.apm/prompts/checkout-review.prompt.md` → `apm install` (deploy prompt).
- **Assertions:** (a) add prints `Updated apm.yml with 1 new package(s)` and exits `0`; (b) `apm.yml`
  `dependencies.apm` contains `microsoft/apm-sample-package#v1.0.0`; (c) `apm.lock.yaml` has a
  `microsoft/apm-sample-package` record with `resolved_ref: v1.0.0`, a 40-char `resolved_commit`, and
  a `content_hash:`; (d) a **second** lockfile record for `github/awesome-copilot` with
  `is_virtual: true`, `depth: 2`, `resolved_by: microsoft/apm-sample-package`; (e) bare `apm install`
  leaves `apm.lock.yaml` **byte-identical** (stable `generated_at`); (f) `apm list` shows the `review`
  script; (g) `apm preview review` writes `.apm/compiled/checkout-review.txt` and invokes no runtime.
- **`apm run review` is `SKIPPED-needs-harness-CLI`** in any box without the `copilot` runtime on
  `PATH`. If `copilot` **is** present it exits `0` but costs real time/credits — do **not** gate
  verification on it. The harness-absent failure (exit `1`, `Script execution failed`) is documented
  above via a bogus-runtime probe; no need to reproduce the credit-spending success path.
- **No-target install** is deterministic & offline: targetless manifest + no marker dirs → **exit
  `2`**, `No harness detected`, **no files written**. Assert exit `2` and that no `AGENTS.md` appears.
- **Content-hash values will differ** per environment for the *local* files (line endings), but the
  **dependency `content_hash`/`resolved_commit`** for `microsoft/apm-sample-package#v1.0.0` are fixed
  (`fb285168…`, `744cca54…`) — safe to assert.

---

## Commands run (this session, apm v0.23.1, exclusive terminal)

```text
apm --version                                                              # 0.23.1
apm install                                                                # v0.1.0 baseline (local-only)
apm install microsoft/apm-sample-package#v1.0.0 --target copilot,claude,cursor   # ADD (56.0s, exit 0)
apm install                                                                # RESTORE (cached, 10.3s, byte-stable)
apm list                                                                   # review script visible
apm run --help ; apm preview --help                                        # experimental surfaces
apm run review                                                             # real run (copilot on PATH, exit 0, 188.68s)
apm preview review                                                         # compile-only -> .apm/compiled/checkout-review.txt
apm install                                                                # materialize v0.2.0 (deploy prompt)
# probe dir apm-ch05x:
apm install                                                                # NO-TARGET -> exit 2, "No harness detected", nothing written
apm run broken                                                             # harness-absent -> exit 1, "Script execution failed"
```

**Artifact:** `content/research/05-install-and-restore-reference.md` (this file).
**Canonical verified project:** `%TEMP%\apm-ch05` (Meridian **v0.2.0**: `apm.yml` + `.apm/…` +
deployed harness files across `.github/ .claude/ .cursor/ .agents/` + `apm.lock.yaml`).
**Probe project:** `%TEMP%\apm-ch05x` (no-target + harness-absent evidence).
