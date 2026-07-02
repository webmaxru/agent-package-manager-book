# Chapter 6 — The Lockfile & Reproducibility · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 6 is where the by-product the reader was told to *notice* in Chapter 5 —
> `apm.lock.yaml` — becomes the *subject*. This chapter turns **reproducibility** from a promise
> into a mechanism: the lockfile records **exact commits + content hashes** so any machine restores
> byte-identical agent context, `apm install --frozen` makes that a **fail-closed CI gate**,
> `apm lock` writes the contract **without deploying**, and `apm find` traces any materialized file
> back to the **dependency edge** that produced it. The running-example beat for this chapter is
> *"CI broke when a ref moved"* — verified here, with one important correction to how that break
> actually presents (see **The `--frozen` CI-break story**).
> **Concept it implements (Ch6 theory):** **Reproducibility** (the "Reproducible by lockfile"
> property). No `06-…-theory.md` brief exists yet; the concept anchors **R1–R4** below are named so
> the author and theory-researcher can align.
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`, re-confirmed at session end).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dir (outside repo):**
> `%TEMP%\apm-ch06` (canonical Meridian **v0.2.0** project — same shape as Ch5: identity, three
> targets, one pinned public dep, one local instruction, one local prompt, one `review` script).
> **Network:** available; **one public package** (`microsoft/apm-sample-package#v1.0.0`) + its one
> transitive skill (`github/awesome-copilot`); **no tokens, no live pushes**. Cold add ~66 s; every
> restore/`--frozen`/`lock` was cache-served (~8–15 s). Steps that need something absent in a clean
> CI box are flagged for the verifier.

---

## Theory anchors (Chapter 6 — Reproducibility)

The lockfile is the artifact that makes "works on my machine" impossible to *silently* violate.
Each feature below links back to the reproducibility sub-concept it implements.

| Ch6 concept (proposed anchor) | What it establishes | Confirmed here by |
|---|---|---|
| **R1 — The lockfile is the reproducibility contract** | `apm.yml` says *what you want*; `apm.lock.yaml` records *exactly what you got* — pinned commits + content hashes + the deployed-file manifest. Generated, never hand-edited. | the real `apm.lock.yaml` below: `resolved_commit` (40-char SHA) + `content_hash` (sha256) + `deployed_file_hashes` per file |
| **R2 — Content-addressing: the hash follows the bytes, not the ref** | pinning is by **commit**, integrity is by **content hash**; identical content keeps an identical `content_hash` even when a floating ref moves to a new commit | the transitive dep's `resolved_commit` moved (`a4aebcd4` in Ch5 → `3169734b` here, unpinned `#main` floated) yet its `content_hash` is **byte-identical** (`9236d06a…`) |
| **R3 — Frozen restore is the CI gate** | `apm install --frozen` **refuses** to install when the lockfile is **missing or structurally out of sync** with the manifest — fail-closed, before any network work | missing-lockfile → **exit 1** in 0.3 s; declared-but-unlocked package → **exit 1** in 0.1 s (pre-resolution); in-sync → **exit 0**, byte-stable |
| **R4 — Provenance & traceability** | every materialized file can be traced to the exact package (and transitive chain) that produced it; the lockfile can be regenerated without deploying | `apm find <file>` → owning package + `apm.yml -> … -> pkg` chain; `apm lock` writes a resolution-only lockfile without touching harness files |

> **Frame note.** Chapter 5 realized **portability** (a declaration became on-disk files). Chapter 6
> realizes **reproducibility** (those files are the *same* files, everywhere, forever — until you
> deliberately change them, which is Chapter 7's `apm update`).

---

## Feature reference (v0.23.1)

| Feature | Job | Implements | Exact behavior observed | Exit |
|---|---|---|---|---|
| `apm.lock.yaml` (the file) | record resolved state | R1, R2 | Written by `apm install` and `apm lock`. Top-level `lockfile_version` / `generated_at` / `apm_version` + a `dependencies:` list (direct **and** transitive) + a `local_deployed_*` block. Pins by `resolved_commit`; fingerprints by `content_hash`. | — |
| `apm install` (writes lock) | resolve **+ deploy + lock** | R1 | The full pipeline; the lockfile it writes includes the **deployment record** (`deployed_files` + `*_hashes`). | `0` |
| `apm install --frozen` | **fail-closed restore** for CI | R3 | **Structural presence gate.** Refuses if `apm.lock.yaml` is **missing** or a package **declared in `apm.yml` is absent from the lock**. Otherwise behaves like a normal restore and prints `Lockfile presence verified…`. Writes nothing on refusal. | `0` in sync · **`1`** missing / out-of-sync |
| `apm lock` | resolve **+ lock**, **no deploy** | R1, R4 | Resolves deps (+policy) and writes `apm.lock.yaml` **without deploying any files**. The lockfile it writes is **resolution-only** — it **omits** `deployed_files` / `deployed_file_hashes` / `local_deployed_*`. Has an `export` subcommand (SBOM/inventory). | `0` |
| `apm find <file>` | **trace a file to its package** | R4 | Prints the owning package name for a deployed file. `--path` adds the **root-to-target chain** (`apm.yml -> parent -> pkg`); `--source` appends the resolved **`pkg@ref|commit`** coordinate. Untracked file → error, exit `1`. | `0` hit · **`1`** miss |
| determinism (byte-stability) | reproducibility guarantee | R1, R2 | Two consecutive bare `apm install` runs left `apm.lock.yaml` **byte-identical**, incl. a **frozen `generated_at`**. The timestamp only advances when the *resolved content* changes. | `0` |

---

## The real `apm.lock.yaml` — full, annotated (verified)

Caption: **The complete lockfile `apm install --target copilot,claude,cursor` generated for Meridian
v0.2.0. Every field annotated. Verified on apm v0.23.1.** (`generated_at` and the file's overall
SHA vary per run; every **dependency** field below — commits, refs, content hashes — is stable.)

```yaml
lockfile_version: '1'                         # <- R1: schema version of the lockfile format itself
generated_at: '2026-07-02T00:53:23.053481+00:00'  # <- UTC time the RESOLVED CONTENT last changed; stable across restores
apm_version: 0.23.1                           # <- the CLI that wrote this lock (provenance / debugging)
dependencies:                                 # <- every resolved package: DIRECT and TRANSITIVE, in one flat list
- repo_url: microsoft/apm-sample-package      # <- the source repo (owner/repo shorthand)
  name: apm-sample-package                    # <- the package's short name
  host: github.com                            # <- git host it resolved from
  resolved_commit: fb2851683be0e0e7711421d518bd8dba23b0b1f6  # <- R1: EXACT 40-char SHA — the immutable pin restore fetches
  resolved_ref: v1.0.0                        # <- the human ref you pinned in apm.yml that produced that SHA
  version: 1.0.0                              # <- the package's declared semver (from its own apm.yml)
  package_type: apm_package                   # <- kind of package; drives how it deploys (apm_package | claude_skill | ...)
  deployed_files:                             # <- DEPLOYMENT RECORD: every file this package materialized (all targets)
  - .agents/skills/style-checker
  - .agents/skills/style-checker/SKILL.md
  - .claude/agents/design-reviewer.md
  - .claude/commands/accessibility-audit.md
  - .claude/commands/design-review.md
  - .claude/rules/design-standards.md
  - .claude/skills/style-checker
  - .claude/skills/style-checker/SKILL.md
  - .cursor/agents/design-reviewer.md
  - .cursor/commands/accessibility-audit.md
  - .cursor/commands/design-review.md
  - .cursor/rules/design-standards.mdc
  - .github/agents/design-reviewer.agent.md
  - .github/instructions/design-standards.instructions.md
  - .github/prompts/accessibility-audit.prompt.md
  - .github/prompts/design-review.prompt.md
  deployed_file_hashes:                       # <- R1: SHA-256 of each deployed file — what `apm audit` checks on disk
    .agents/skills/style-checker/SKILL.md: sha256:1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829
    .claude/agents/design-reviewer.md: sha256:616988766ebc7d42cc6f599a17d1ad3ab8164e139fad82e111af5441fe3986cb
    .claude/commands/accessibility-audit.md: sha256:6d5c7d5d0038683e5658f4a90cdee61b2fc3a27b3023fc63ed6649d1ea6b6b92
    .claude/commands/design-review.md: sha256:ed0741675cb37dd3fe77fbd199800582f745b4ee84e34ce6a92b8eb0bd6d7b81
    .claude/rules/design-standards.md: sha256:5756b425ca79c83912e67102b32d623192bef7349ee7696275312b92c283a05e
    .claude/skills/style-checker/SKILL.md: sha256:1142700284d253c15e561434362ae6203db08e41ef07e7082386df3651738829
    .cursor/agents/design-reviewer.md: sha256:616988766ebc7d42cc6f599a17d1ad3ab8164e139fad82e111af5441fe3986cb
    .cursor/commands/accessibility-audit.md: sha256:6d5c7d5d0038683e5658f4a90cdee61b2fc3a27b3023fc63ed6649d1ea6b6b92
    .cursor/commands/design-review.md: sha256:ed0741675cb37dd3fe77fbd199800582f745b4ee84e34ce6a92b8eb0bd6d7b81
    .cursor/rules/design-standards.mdc: sha256:136481f1158a5678a3d07a6ca8044b83598463b2ed69adb6762a226372534c4b
    .github/agents/design-reviewer.agent.md: sha256:616988766ebc7d42cc6f599a17d1ad3ab8164e139fad82e111af5441fe3986cb
    .github/instructions/design-standards.instructions.md: sha256:6f5d994d6437416e14e4ca5540f4d1cf06fad079728a1419acfb1dd7038ec38d
    .github/prompts/accessibility-audit.prompt.md: sha256:c3382c6b7ac6ba38cf66d345923be79c5a46b8783a0d33aac457ff60f1b6597a
    .github/prompts/design-review.prompt.md: sha256:f10919f07eec83c62c7912e318382b472ad27eb1c22c11525b813522960e8e06
  content_hash: sha256:744cca54cc8ff7ca90aa1dd621c2f98c6291cd793815afe8518001cc94b8aba9  # <- R2: fingerprint of the SOURCE; follows bytes, not the ref
- repo_url: github/awesome-copilot            # <- the TRANSITIVE dep (pulled in by the package above)
  name: awesome-copilot
  host: github.com
  resolved_commit: 3169734bc2fb25d5e092130fc93d24b0dee3ac3a  # <- R2: MOVED vs Ch5 (a4aebcd4) — unpinned #main floated
  version: unknown                            # <- unpinned: no tag resolved, hence the [!] "unpinned" warning at install
  virtual_path: skills/review-and-refactor    # <- R4: the sub-path carved out of the monorepo (one primitive, not a whole pkg)
  is_virtual: true                            # <- a "virtual" package: a slice of a repo, not a full apm package
  depth: 2                                     # <- dependency depth: 1 = direct from your apm.yml; 2 = transitive
  resolved_by: microsoft/apm-sample-package    # <- R4: the parent edge that introduced this dep (provenance)
  package_type: claude_skill                  # <- resolved as an agent/Claude skill
  deployed_files:
  - .agents/skills/review-and-refactor
  - .agents/skills/review-and-refactor/SKILL.md
  - .claude/skills/review-and-refactor
  - .claude/skills/review-and-refactor/SKILL.md
  deployed_file_hashes:
    .agents/skills/review-and-refactor/SKILL.md: sha256:95b48ed4b137777ddc87b77cb0873ed7f485141a517825e71af1a984cf5a6cd6
    .claude/skills/review-and-refactor/SKILL.md: sha256:95b48ed4b137777ddc87b77cb0873ed7f485141a517825e71af1a984cf5a6cd6
  content_hash: sha256:9236d06a1500089ddb46975b866e9a63478e502afe7095b1980c618678a7c7fe  # <- R2: IDENTICAL to Ch5 though the commit moved
local_deployed_files:                         # <- your project's OWN .apm/ sources, materialized (no dependency involved)
- .claude/commands/checkout-review.md
- .claude/rules/meridian-checkout.md
- .cursor/commands/checkout-review.md
- .cursor/rules/meridian-checkout.mdc
- .github/instructions/meridian-checkout.instructions.md
- .github/prompts/checkout-review.prompt.md
local_deployed_file_hashes:                   # <- SHA-256 of each local deployed file (env-specific: line endings etc.)
  .claude/commands/checkout-review.md: sha256:1d37794c69fead7e0d5d26310b27929a7766ac33416989eedcf7be9fff010311
  .claude/rules/meridian-checkout.md: sha256:3f8ff5771908aa7f602fd6279a2ff775b54613d1c9fc44b4b1dcc31c6ead5be1
  .cursor/commands/checkout-review.md: sha256:1d37794c69fead7e0d5d26310b27929a7766ac33416989eedcf7be9fff010311
  .cursor/rules/meridian-checkout.mdc: sha256:87d93a43c378ba9933e4b9e5db4b7df8d84e8e258480649122ae0829774ff8d2
  .github/instructions/meridian-checkout.instructions.md: sha256:bf0a95675dd08131c972acfa85ba61e73e9d9ab0c042f1fcb59fb12cb601da49
  .github/prompts/checkout-review.prompt.md: sha256:f85a4b00b3d63985916c5d7dea4f42ca27c43cd77bb21ecb95707148d331b707
```

### Field reference (every field the reader will see)

| Field | Scope | Meaning | Reproducibility role |
|---|---|---|---|
| `lockfile_version` | top | schema version of the lock format (`'1'`) | lets APM evolve the format without breaking old locks |
| `generated_at` | top | UTC time the resolved content **last changed** | **stable across restores** — see determinism proof |
| `apm_version` | top | CLI version that wrote the lock | provenance; spot locks written by another CLI |
| `repo_url` / `name` / `host` | per-dep | source repo, short name, git host | identifies *where* the package came from |
| `resolved_ref` | per-dep | the human ref you pinned (tag/branch/sha) | your *intent* |
| `resolved_commit` | per-dep | the **exact 40-char SHA** it resolved to | **the immutable pin** — R1 |
| `version` | per-dep | package's declared semver (`unknown` if none) | human-readable version; `unknown` ⇒ unpinned |
| `package_type` | per-dep | `apm_package` \| `claude_skill` \| … | drives deployment shape |
| `deployed_files` | per-dep | every file materialized on disk | the **deployment record** (only in `install` locks) |
| `deployed_file_hashes` | per-dep | SHA-256 of each deployed file | what `apm audit` verifies on disk |
| `content_hash` | per-dep | fingerprint of the **source** content | **content-addressing** — R2 |
| `virtual_path` | per-dep (virtual) | sub-path carved from a monorepo | one primitive, not a whole package |
| `is_virtual` | per-dep (virtual) | `true` for a repo slice | distinguishes slices from full packages |
| `depth` | per-dep | `1` direct, `2`+ transitive | dependency-graph depth |
| `resolved_by` | per-dep (transitive) | the parent that introduced it | **provenance edge** — R4 |
| `local_deployed_files` / `_hashes` | top | files from your own `.apm/` sources | the local half of the deployment record |

> **No `mcp:` section here.** This project declares `mcp: []`, so the lockfile has **no MCP block**.
> How MCP servers are represented in the lockfile is **not** exercised in this chapter (it belongs
> to Chapter 8's transitive-MCP story) — treat it as **UNVERIFIED** until then; do not invent a shape.

---

## The `--frozen` CI-break story (verified — with a correction)

**What `--frozen` actually is** (from `apm install --help`, v0.23.1, verbatim):

> `--frozen`  Refuse to install when apm.lock.yaml is missing or out of sync with apm.yml
> (CI-safe; mutually exclusive with --update). **Structural presence check only**; use 'apm audit'
> for on-disk integrity.

That one line rewrites the running-example beat. *"CI broke when a **ref** moved"* is **not** quite
how `--frozen` breaks. `--frozen` is a **structural presence gate**, not a ref/commit comparator.
Here is exactly what does and does not trip it, all verified:

### (1) In-sync project → passes, byte-stable (exit 0)

```text
apm install --frozen
  [i] Targets: claude, copilot, cursor  (source: apm.yml)
  [+] microsoft/apm-sample-package #v1.0.0 @fb285168 (cached)  |-- ... adopted ...
  [+] github.com/.../review-and-refactor @3169734b (cached)    |-- (files unchanged)
  [+] <project root> (local)  |-- ... adopted ...
  [*] Installed 2 APM dependencies in 13.0s.
  [i] Lockfile presence verified. Run 'apm audit' for on-disk content integrity.   # <- the --frozen tell
```

Exit `0`; the lockfile SHA was **unchanged** before and after. The trailing
`Lockfile presence verified…` line is the observable difference from a bare install, and it names
its own boundary: `--frozen` checks **presence/structure**, `apm audit` checks **on-disk content**.

### (2) The break that *is* real — a declared package missing from the lock (exit 1)

This is the faithful "someone added a dependency and didn't commit the regenerated lockfile" CI
failure. We added one line to `apm.yml` **without** re-locking:

```yaml
dependencies:
  apm:
    - microsoft/apm-sample-package#v1.0.0
    - acme/checkout-guardrails#v1.0.0        # <- declared, but never locked (illustrative package)
```

```text
apm install --frozen
  [>] Installing dependencies from apm.yml...
  --frozen: apm.lock.yaml is out of sync with apm.yml.
    - acme/checkout-guardrails is declared in apm.yml but missing from apm.lock.yaml
  [i] Tip: run 'apm outdated' to see what changed, then 'apm update'.
  [!] Install interrupted after 0.1s.        # <- exit 1
```

**Exit `1`, in 0.1 s, with no network access** — it never tried to clone `acme/checkout-guardrails`.
The structural gate fires **before** resolution, names the offending package precisely, and **writes
nothing** (lockfile SHA unchanged). This is the CI-break to teach.

### (3) The other break — a missing lockfile entirely (exit 1)

```text
# apm.lock.yaml deleted (e.g. never committed)
apm install --frozen
  [>] Installing dependencies from apm.yml...
  --frozen requires apm.lock.yaml to exist. Run 'apm install' (without --frozen) or 'apm update' first.
  [i] Tip: run 'apm outdated' to see what changed, then 'apm update'.
  [!] Install interrupted after 0.3s.        # <- exit 1
```

### (4) Reconcile → green again (exit 0)

Fix the manifest (or run `apm install` / `apm lock` to re-lock the added package), then:

```text
apm install            # reconcile: resolves + re-locks + deploys   -> exit 0
apm install --frozen   # now in sync                                -> exit 0
```

### What does **NOT** trip `--frozen` (the correction the author must make)

Both of these **passed with exit 0** and were reconciled into the lock, because the *package* was
still structurally present:

- **Changing a pinned ref to another ref that resolves to the same commit.** We changed
  `#v1.0.0` → `#main`; because `main` currently points at the same commit `fb285168`, `--frozen`
  passed and merely updated `resolved_ref: main` (and `generated_at`) in the lock. The literal ref
  string is **not** what `--frozen` guards.
- **Adding a dependency whose repo is already in the lock** (even transitively). We added
  `github/awesome-copilot/skills/review-and-refactor#…` as a *direct* dep; since `github/awesome-copilot`
  was already a (transitive) lock entry, `--frozen` did not consider it "missing" — it passed and
  promoted the entry from transitive to direct.

> **UNVERIFIED / open for the verifier:** we did **not** get a floating ref to resolve to a
> *different* commit than the one locked (our `#main` == the locked commit today). Given
> "structural presence check only," the likely behavior is that `--frozen` still **passes** on a
> moved-to-different-commit dep (the package is present) and a normal install would reconcile it —
> i.e. `--frozen` does **not** protect against silent *commit* drift; the lockfile's
> `resolved_commit` pin + `apm audit` (content) do. Flag this as the boundary of `--frozen`.

---

## `apm lock` — resolve and write the lock, **without deploying** (verified)

`apm lock --help` (v0.23.1): *"Resolve dependencies and write apm.lock.yaml without deploying files."*
Options include `--update` (re-resolve refs to latest SHAs), `--no-policy`, `-t/--target` (scopes
policy only — "No files are deployed regardless of this value"), and an **`export`** subcommand
("Export an SBOM/inventory from the existing lockfile").

**Proof it does not deploy.** We deleted the lockfile **and** one already-deployed file
(`.github/instructions/design-standards.instructions.md`) as a canary, then ran `apm lock`:

```text
apm lock
  [+] microsoft/apm-sample-package #v1.0.0 @fb285168
  [+] github.com/github/awesome-copilot/skills/review-and-refactor #default @3169734b
  [+] Lockfile written to apm.lock.yaml
# LOCKFILE_EXISTS_AFTER = True     (lock regenerated)
# CANARY_AFTER_EXISTS   = False    (deleted deployed file NOT recreated)   -> exit 0
```

**Structural difference from an `install` lock.** The `apm lock` file is **resolution-only** — it
records `resolved_commit` / `resolved_ref` / `content_hash` per dependency but **omits the
deployment record**:

| Section | `apm install` lock | `apm lock` lock |
|---|---|---|
| `resolved_commit`, `content_hash` | present | **present** |
| `deployed_files` / `deployed_file_hashes` | present | **omitted** |
| `local_deployed_files` / `_hashes` | present | **omitted** |

(Confirmed by counting keys: after `apm lock`, `deployed_files=0`, `local_deployed_files=0`,
`content_hash=2`, `resolved_commit=2`.)

**When to use.** `apm lock` = "compute/refresh the contract" without materializing anything — useful
in CI to validate that the graph resolves, to (re)generate a lockfile headlessly, or to produce an
SBOM via `apm lock export`. **Pitfall:** a lockfile produced by `apm lock` alone has **no
`deployed_files`**, so a later `apm install` will add them (and change the file). Don't treat a
`lock`-only file as the final committed artifact if you also commit deployed harness files.

---

## `apm find <file>` — trace a materialized file to its origin (verified)

`apm find [OPTIONS] FILE_PATH`: prints the package that owns a deployed file. `--source` appends the
resolved `pkg@ref|commit`; `--path` prints the full root-to-target chain (like `apm deps why`).
Output shapes (all verified):

```text
# direct-dep file (plain)
apm find .github/instructions/design-standards.instructions.md
  microsoft/apm-sample-package

# direct-dep file (--source)  -> appends the resolved coordinate (pinned -> @tag)
apm find .github/instructions/design-standards.instructions.md --source
  microsoft/apm-sample-package  microsoft/apm-sample-package@v1.0.0

# TRANSITIVE file (--path)  -> the full provenance chain, incl. the transitive edge
apm find .agents/skills/review-and-refactor/SKILL.md --path
  github/awesome-copilot
    apm.yml -> microsoft/apm-sample-package -> github/awesome-copilot

# transitive file (--source) -> unpinned -> appends the resolved COMMIT prefix
apm find .agents/skills/review-and-refactor/SKILL.md --source
  github/awesome-copilot  github/awesome-copilot@3169734bc2fb

# LOCAL file -> traced to the workspace, not a package
apm find .github/instructions/meridian-checkout.instructions.md --source
  .  (workspace)

# untracked file -> error, exit 1
apm find .github/does-not-exist.md
  [x] '.github/does-not-exist.md' is not tracked by any installed package in apm.lock.yaml.
```

> **Why this belongs in a *reproducibility* chapter (R4).** Reproducibility is worthless if you
> can't answer *"where did this file come from?"* `apm find` closes that loop: any file an agent
> reads can be traced to a package, a version/commit, and — for transitive deps — the exact edge
> (`resolved_by`) that pulled it in. It reads straight from `apm.lock.yaml`, so it's only ever as
> honest as the committed lock.

---

## Determinism — the byte-stability contract (verified)

Two consecutive bare `apm install` runs on the unchanged project:

```text
RUN1  generated_at: '2026-07-02T00:58:03.063745+00:00'  hash=EAD3EE9B…747D
RUN2  generated_at: '2026-07-02T00:58:03.063745+00:00'  hash=EAD3EE9B…747D
BYTE_STABLE = True
```

`generated_at` did **not** advance and the file was **byte-identical**. Across the whole session,
`generated_at` (and the file hash) changed **only** when the *resolved content* changed
(`v1.0.0`↔`main` flips), never on a pure restore. Note it stamps the *time of the last content
change* and does **not** revert to a prior timestamp when content returns to a prior state.

> **The chapter's headline (R1/R2):** `git clone` + `apm install` = the same bytes on any machine,
> and re-running install is a byte-stable no-op. That is reproducibility made mechanical.

---

## Caveats & flags (for the author + verifier)

1. **Correct the running-example caption.** `--frozen` breaking is about **package presence**, not a
   moved **ref string**. Teach the break as *"a dependency is declared in `apm.yml` but missing from
   `apm.lock.yaml`"* (someone added a dep and didn't commit the re-locked file) or *"the lockfile
   isn't committed at all."* Both give **exit 1**; the out-of-sync case fails in **0.1 s with no
   network**. Do **not** claim `--frozen` catches a ref that merely changed label.
2. **`--frozen` ≠ `apm audit`.** `--frozen` is a **structural presence** check (manifest vs lock);
   it does **not** verify on-disk file content. The CLI itself says so:
   `Lockfile presence verified. Run 'apm audit' for on-disk content integrity.` Content/tamper
   checking is Chapter 8. Don't conflate them.
3. **Content-hash follows bytes, not the ref (R2).** The transitive `content_hash` (`9236d06a…`) is
   **identical** to Ch5 even though its `resolved_commit` moved (`a4aebcd4` → `3169734b`, unpinned
   `#main`). Great teaching moment: pinning is by commit, integrity is by content — a floated ref
   that lands on identical content keeps an identical fingerprint. But it *did* move the commit, so
   **pin transitive refs** if you want the *commit* frozen too (Ch7 `apm update` drift).
4. **`generated_at` is content-stable, not a run clock.** It advances only when resolution changes,
   and is preserved byte-for-byte across restores. Don't describe it as "when you last ran install."
5. **`apm lock` writes a *resolution-only* lock.** It omits `deployed_files` / `local_deployed_*`.
   Useful for CI/SBOM (`apm lock export`), but a `lock`-only file isn't the same artifact `install`
   commits. A subsequent `install` will add the deployment record (and change the file).
6. **`apm find --source` coordinate depends on pinning.** Pinned dep → `pkg@v1.0.0` (the tag);
   unpinned/transitive → `pkg@<commit-prefix>`. Local files → `.  (workspace)`. Miss → exit `1`.
7. **The manifest is preserved by restore; the *lock's* `generated_at`/SHA are not asserted.** Bare
   `apm install` did **not** rewrite `apm.yml` (authored form intact). Assert **dependency** fields
   in the lock (commits, refs, `content_hash`), never the whole-file SHA or `generated_at`.
8. **Same benign install noise as Ch4/Ch5.** The sample package's Claude/Cursor commands drop the
   unsupported `mode:` frontmatter key; the transitive dep is `unpinned`. Expected; not lock errors.

---

## For the `code-verifier`

- **Build (network for the add):** author Meridian **v0.2.0** in a scratch dir (identity; targets
  copilot/claude/cursor; `dependencies.apm: [ microsoft/apm-sample-package#v1.0.0 ]`, `mcp: []`;
  `includes: auto`; local `.apm/instructions/meridian-checkout.instructions.md` +
  `.apm/prompts/checkout-review.prompt.md`; `scripts.review`). Run
  `apm install --target copilot,claude,cursor` (~66 s cold, public, **no token**).
- **Lockfile assertions (stable):** `apm.lock.yaml` has `lockfile_version: '1'`, `apm_version:
  0.23.1`; a `microsoft/apm-sample-package` record with `resolved_ref: v1.0.0`, 40-char
  `resolved_commit` **`fb2851683be0e0e7711421d518bd8dba23b0b1f6`**, and
  `content_hash: sha256:744cca54…`; a second **virtual/transitive** `github/awesome-copilot` record
  with `is_virtual: true`, `depth: 2`, `resolved_by: microsoft/apm-sample-package`,
  `content_hash: sha256:9236d06a…`. **Do not** assert `github/awesome-copilot`'s `resolved_commit`
  (unpinned `#main` floats — it was `3169734b` this session, `a4aebcd4` in Ch5) nor `generated_at`
  nor the whole-file SHA. Local `*_hashes` are environment-specific (line endings) — don't assert.
- **Determinism (offline):** run bare `apm install` twice; assert the lockfile is **byte-identical**
  (stable `generated_at`).
- **`--frozen` PASS (offline, cached):** on the in-sync project, `apm install --frozen` → exit `0`,
  prints `Lockfile presence verified…`, lockfile unchanged.
- **`--frozen` FAIL — missing lock (offline, deterministic):** delete `apm.lock.yaml` →
  `apm install --frozen` → **exit 1**, message `--frozen requires apm.lock.yaml to exist…`, writes
  nothing.
- **`--frozen` FAIL — out of sync (offline, deterministic):** add a package **not** in the lock
  (e.g. `acme/checkout-guardrails#v1.0.0`) → `apm install --frozen` → **exit 1** in ~0.1 s, message
  `--frozen: apm.lock.yaml is out of sync with apm.yml.` + `- acme/checkout-guardrails is declared
  in apm.yml but missing from apm.lock.yaml`, **no network**, lockfile unchanged. Reconcile by
  removing the line (or `apm install`), then `apm install --frozen` → exit `0`.
- **`apm lock` (network to resolve):** delete `apm.lock.yaml` + one deployed file →
  `apm lock` → exit `0`, `Lockfile written to apm.lock.yaml`, the deployed file **not** recreated,
  and the new lock has **no** `deployed_files` (assert `deployed_files` absent). Run `apm install`
  afterward to restore the deployment record.
- **`apm find` (offline, reads the lock):** `apm find .github/instructions/design-standards.instructions.md`
  → `microsoft/apm-sample-package`; `--path` on `.agents/skills/review-and-refactor/SKILL.md` →
  chain `apm.yml -> microsoft/apm-sample-package -> github/awesome-copilot`; a nonexistent path →
  exit `1`.

---

## Commands run (this session, apm v0.23.1, exclusive terminal)

```text
apm --version                                                      # 0.23.1 (start + end)
apm install --target copilot,claude,cursor                        # build v0.2.0 + write lock (66.5s, exit 0)
apm install --frozen                                              # in-sync -> exit 0, byte-stable, "Lockfile presence verified"
# drift probe A: apm.yml #v1.0.0 -> #main (same commit)
apm install --frozen                                              # PASSED (exit 0) -> resolved_ref updated to main; NOT a real break
# revert #main -> #v1.0.0
apm install                                                       # reconcile
apm install ; apm install                                         # DETERMINISM: byte-identical lock, generated_at frozen (BYTE_STABLE=True)
# drift probe B: add github/awesome-copilot/...#a4aebcd4 (repo already in lock)
apm install --frozen                                              # PASSED (exit 0) -> promoted transitive->direct; NOT a break
# revert; apm install (reconcile)
Copy apm.lock.yaml .bak ; del apm.lock.yaml
apm install --frozen                                              # MISSING LOCK -> exit 1, "requires apm.lock.yaml to exist", 0.3s
# restore .bak (byte-identical 76F80D77…)
# drift: add acme/checkout-guardrails#v1.0.0 (NOT in lock)
apm install --frozen                                              # OUT OF SYNC -> exit 1, names package, 0.1s, NO network, lock unchanged
# revert acme line
apm install ; apm install --frozen                               # reconcile -> exit 0 ; frozen green -> exit 0
apm lock --help                                                   # "Resolve … without deploying files" (+ export subcmd)
del apm.lock.yaml ; del .github/instructions/design-standards.instructions.md
apm lock                                                          # exit 0, lock written, canary NOT redeployed, deployed_files omitted
apm install                                                       # restore full deployment record
apm find --help                                                   # FILE_PATH; --source; --path
apm find <direct> [--source] [--path] ; apm find <transitive> --path --source ; apm find <local> --source ; apm find <missing>
```

**Artifact:** `content/research/06-the-lockfile-and-reproducibility-reference.md` (this file).
**Canonical verified project:** `%TEMP%\apm-ch06` (Meridian **v0.2.0**: `apm.yml` + `.apm/…` +
deployed harness files across `.github/ .claude/ .cursor/ .agents/` + `apm.lock.yaml`).
