# Chapter 7 — Lifecycle · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 7 is the **maintenance triad** that sits on top of Chapter 6's frozen lockfile —
> the deliberate *inspect → change → verify* loop that keeps a pinned setup **current without giving
> up frozen**. This reference proves all three verbs end to end on the canonical Meridian **v0.2.0**
> project: **`apm outdated`** (read-only drift report), **`apm update`** (`--dry-run` preview /
> `--yes` apply — the **only** version-moving verb), and **`apm audit`** (`--ci` gate — an
> **integrity** check, **not** a CVE feed). It also nails the division of labor: bare `apm install`
> **restores** locked bytes even for a floating ref; only `apm update` refreshes.
> **Concept it implements (Ch7 theory):** the *deliberate lifecycle* —
> [`07-lifecycle-theory.md`](07-lifecycle-theory.md), Concepts 1–4 (anchored **L1–L4** below).
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`, re-confirmed at session end).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dir (outside repo):**
> `%TEMP%\apm-ch07` (canonical Meridian **v0.2.0** project — identity; targets copilot/claude/cursor;
> one pinned public dep `microsoft/apm-sample-package#v1.0.0`; one transitive skill
> `github/awesome-copilot/skills/review-and-refactor` (unpinned `#main`); one local instruction; one
> local prompt; a `review` script). Built with `apm install --target copilot,claude,cursor`.
> **Network:** available; **one public package** + its one transitive skill; **no tokens, no live
> pushes**. Cold add ~30 s; every restore/update/audit was cache-served (~7–13 s).
> **⚠ One controlled simulation, clearly labeled.** A freshly-installed floating ref locks to the
> *current* branch tip, so `apm outdated`/`apm update` legitimately find **nothing to move** on a
> fresh build. To capture the *non-empty* report + a real lockfile diff, I rolled the transitive's
> **locked commit** back to its genuinely-older Chapter-5 commit (`a4aebcd4`, a real earlier commit
> on that same `main`, which advanced to `3169734b` by Ch6). This faithfully reconstructs "the branch
> moved since we locked." Every command run against that state — and its output/exit code — is **real
> apm v0.23.1 behavior**; only the *starting* commit was set by hand. Flagged inline as `[SIMULATED
> SETUP]`.

---

## Theory anchors (Chapter 7 — the deliberate lifecycle)

Each verb below links back to the lifecycle concept it implements.

| Ch7 concept (theory brief) | What it establishes | Confirmed here by |
|---|---|---|
| **L1 — Reproducibility must not become stagnation** | a frozen setup still needs a *deliberate* maintenance loop: inspect → change → verify | the three verbs exercised in order on the frozen Meridian v0.2.0 baseline |
| **L2 — Three single-purpose verbs** | `outdated` **reports** (read-only), `update` **changes** (consent-gated), `audit` **verifies** (integrity) — never blurred | `outdated` wrote nothing; `update` was the only verb that rewrote the lock; `audit` inspected + gated |
| **L3 — Refresh known deps vs. casually accepting drift** | bare `apm install` **restores** the locked commit; `apm update` is the **only** version-moving verb; drift is a property of the **ref**, not the command | bare install restored `a4aebcd4` (did **not** float to tip); `apm update` moved `a4aebcd4 → 3169734b` |
| **L4 — Ownership & cadence (lockfile diff = review artifact)** | a deliberate `apm update` lands as a reviewable `apm.lock.yaml` diff (resolved-commit + `generated_at`) | the captured before→after lock diff: one `resolved_commit` line + `generated_at`, nothing else |

> **Frame note.** Chapter 6 made the setup *frozen* (byte-for-byte restorable). Chapter 7 answers
> *"if everything is pinned, how does anything move forward — safely?"* The triad is the answer:
> **`apm outdated`** shows what drifted, **`apm update`** changes it on purpose, **`apm audit`**
> proves the result is intact. `apm update` is the hinge between Ch6 (frozen) and staying current.

---

## Feature reference (v0.23.1)

| Verb / flag | Job | Implements | Exact behavior observed | Exit |
|---|---|---|---|---|
| `apm outdated` | **report** drift from upstream (read-only) | L1, L2 | Reads `apm.lock.yaml`, queries each remote. Clean → `All dependencies are up-to-date`. Drift → a **Package / Current / Latest / Status / Source** table + `[!] N outdated dependency found`. **Writes nothing.** Finding drift is **not** an error. | `0` up-to-date **and** `0` when outdated · `1` if no lockfile (per docs — see caveats) |
| `apm outdated --verbose` | + diagnostics | L2 | Adds `Skipping local dep: .`; with `-v` on a real remote check, would list available tags. | `0` |
| `apm update --dry-run` | **preview** the change | L2 | `Checking upstream for revision-pin freshness…` → `Update plan for apm.yml` → per-dep `[~]` rows → `N updated` → `Dry run: no changes applied.` **Never writes, never asks.** | `0` |
| `apm update --yes` | **apply** the change (non-interactive) | L1, L2, L3 | Plan phase, then a full deploy phase, then `Updated N APM dependencies.` **Re-resolves floating refs to the newest allowed commit and rewrites `apm.lock.yaml`.** The **only** version-moving verb. | `0` |
| `apm update` (interactive) | apply behind a consent gate | L2 | Prompts before writing; **defaults to No**; `--yes` required in CI/piped stdin (per docs — not directly exercised; used `--yes`). | `0` |
| `apm audit` | **verify** integrity (on-demand) | L2 | Hidden-Unicode **content scan** of deployed files **+** install-replay **drift** check. Clean → `N file(s) scanned -- no issues found`. | `0` clean · **`2`** hidden-Unicode findings · drift alone is **advisory** (exit `0`) |
| `apm audit --ci` | **CI gate** (lockfile consistency) | L2, L4 | Replay-drift check **+** a **9-check** APM Policy Compliance table. Clean → `All 9 check(s) passed`. Any violation fails the gate. | `0` clean · **`1`** on any violation |
| `apm audit --file <path>` | scan an arbitrary file | L2 | Content-scan only; used to isolate the hidden-Unicode exit code. | `0`/`2` |
| bare `apm install` | **restore** locked bytes (contrast) | L3 | Restores the **locked commit** from cache — even for a floating `#main` ref. **Never bumps versions.** (Ch5/Ch6.) | `0` |
| `apm install --frozen` | structural CI reproduce (contrast) | L3 | Fail-closed presence gate (Ch6). Named here only to complete the division of labor. | `0`/`1` |

> **`apm outdated` has no `--ci` and no `--json` flag** (v0.23.1). Its full option set is
> `-g/--global`, `-v/--verbose`, `-j/--parallel-checks INTEGER`. If you want a **CI gate**, that is
> `apm audit --ci`, not `apm outdated` — the docs say to *"wire `apm audit` into CI instead."*

---

## Verb 1 — `apm outdated` (report drift · read-only · L1/L2)

**`apm outdated --help` (v0.23.1), verbatim options:**

```text
Usage: apm.exe outdated [OPTIONS]
  Show outdated locked dependencies
Options:
  -g, --global                   Check user-scope dependencies (~/.apm/)
  -v, --verbose                  Show additional info (e.g., available tags for outdated deps)
  -j, --parallel-checks INTEGER  Max concurrent remote checks (default: 4, 0 = sequential)
  --help                         Show this message and exit.
```

**Purpose.** Answer *"what has drifted from upstream since we locked?"* without changing anything. It
reads the committed `apm.lock.yaml`, queries each remote, and labels every dependency. **Implements
concept:** L2 (the *report* verb) on top of L1 (inspect before you change).

### 1a — Clean project (fresh build): everything up-to-date

Caption: **`apm outdated` on the freshly-installed Meridian v0.2.0. The pinned tag has no newer match
and the transitive `#main` is locked at the current tip, so both are current. Verified on apm
v0.23.1.**

```text
apm outdated
  [*] All dependencies are up-to-date            # exit 0

apm outdated --verbose
  Skipping local dep: .
  [*] All dependencies are up-to-date            # exit 0
```

> **Key empirical finding — pinned vs. unpinned on a fresh build.** The task asked whether `apm
> outdated` reports the **unpinned transitive** (`github/awesome-copilot#main`) as drift-able. On a
> *fresh* install the answer is **no** — because `apm install` locked `#main` to the **current tip**
> (`3169734b`), so the lock already equals what the ref resolves to today. A freshly-locked floating
> ref is **not** "outdated"; it only becomes outdated once the branch tip advances **past** the
> locked commit. **`outdated` compares the *locked commit* to what the ref resolves to now** — drift
> is latent in the *ref*, surfaced by *time*, not by the freshness of the pin.

> **Second finding — `outdated` reads the lockfile, not a live manifest edit.** I loosened the direct
> dep in `apm.yml` from `#v1.0.0` to `#main` *without* re-installing; `apm outdated` still reported
> `up-to-date`. It keys off the committed lockfile's `resolved_ref` (still the tag), not an
> uncommitted manifest change. Loosening a pin only takes effect once you `apm update` (which
> re-locks).

### 1b — `[SIMULATED SETUP]` The branch advanced past the lock: a real `outdated` row

To capture the non-empty report shape, I rolled the transitive's locked commit back to its
genuinely-older Chapter-5 commit `a4aebcd4` (main has since advanced to `3169734b`). The `apm
outdated` run against that state is real behavior:

Caption: **`apm outdated --verbose` when the transitive `#main` lock sits behind the branch tip.
Full-width table. Verified on apm v0.23.1 (`[SIMULATED SETUP]`: the older locked commit was set by
hand; the report is real).**

```text
                                                  Dependency Status
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Package                                           ┃ Current    ┃ Latest     ┃ Status       ┃ Source               ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ microsoft/apm-sample-package                      │ v1.0.0     │ v1.0.0     │ up-to-date   │ git tags             │
│ github/awesome-copilot/skills/review-and-refactor │ (default)  │ 3169734b   │ outdated     │ git branch           │
└───────────────────────────────────────────────────┴────────────┴────────────┴──────────────┴──────────────────────┘
[!] 1 outdated dependency found                    # exit 0
```

**Column semantics (verified):**

| Column | Meaning | Pinned tag dep | Unpinned branch dep |
|---|---|---|---|
| **Package** | the resolved coordinate (incl. sub-path for a virtual dep) | `microsoft/apm-sample-package` | `github/awesome-copilot/skills/review-and-refactor` |
| **Current** | what you have locked | `v1.0.0` (the tag) | `(default)` (the default branch) |
| **Latest** | what the ref resolves to **now** | `v1.0.0` (same tag) | `3169734b` (new tip commit) |
| **Status** | `up-to-date` · `outdated` · `unknown` | `up-to-date` | `outdated` |
| **Source** | how staleness was checked | `git tags` | `git branch` |

**Reading it:** a **tag-pinned** dep is checked against **git tags** and stays `up-to-date` unless a
newer *matching* tag exists; a **branch** dep is checked against the **branch tip** and goes
`outdated` the moment the branch moves ahead of the locked commit. **"Outdated" = the locked commit
is behind what the ref would resolve to today.**

**Exit code:** `0` **whether or not** anything is outdated — *finding drift is not an error.* The
summary line `[!] 1 outdated dependency found` is informational. (Per the docs, exit `1` occurs only
when there is **no lockfile** at all; not directly exercised here — see caveats.)

**When to use.** As the **input to a chosen cadence** (L4): a scheduled `apm outdated` surfaces
staleness so a human decides whether to `apm update`. **When *not* to.** Do **not** use it as a CI
gate — it never fails on drift; that is `apm audit --ci`'s job.

---

## Verb 2 — `apm update` (the deliberate change · the ONLY version-moving verb · L2/L3)

**`apm update --help` (v0.23.1), verbatim options:**

```text
Usage: apm.exe update [OPTIONS] [PACKAGES]...
  Refresh APM dependencies to the latest matching refs
Options:
  -y, --yes                     Skip the confirmation prompt (for CI / automation)
  --dry-run                     Render the update plan and exit without changing anything
  -v, --verbose                 Show unchanged deps and detailed pipeline diagnostics
  -g, --global                  Refresh user-scope dependencies (~/.apm/) instead of the current project
  --force                       Overwrite locally-authored files on collision
  --parallel-downloads INTEGER  Max concurrent package downloads (0 to disable parallelism)  [default: 4]
  -t, --target TARGET           Agent target(s) to update for (…) Highest-priority entry in the resolution chain.
  --help                        Show this message and exit.
```

**Purpose.** Re-resolve every dependency in `apm.yml` to the **newest ref/commit allowed by its
constraint**, print a plan, and (with consent) **rewrite `apm.lock.yaml`** and redeploy. This is
*"the command that actually changes versions."* **Implements concept:** L3 (refresh, as opposed to
`apm install`'s restore) and L2 (the *change* verb). Optional `[PACKAGES]...` scopes the update to
named deps.

### 2a — `apm update --dry-run` (preview — writes nothing)

Caption: **`apm update --dry-run` `[SIMULATED SETUP]` (transitive lock behind at `a4aebcd4`). The
preview plan; it wrote nothing to the lock. Verified on apm v0.23.1.**

```text
apm update --dry-run
  [>] Checking upstream for revision-pin freshness...
  [i] Update plan for apm.yml

    [~] github/awesome-copilot/skills/review-and-refactor
        ref: - (a4aebcd -> -)
        files: .agents/skills/review-and-refactor, .agents/skills/review-and-refactor/SKILL.md, .claude/skills/review-and-refactor, +1 more

    [~] microsoft/apm-sample-package
        ref: v1.0.0 (fb28516 -> -)
        files: .agents/skills/style-checker, .agents/skills/style-checker/SKILL.md, .claude/agents/design-reviewer.md, +13 more

    2 updated
    [~] updated

  [i] Dry run: no changes applied. Re-run without --dry-run to update.   # exit 0 — lock unchanged
```

> **⚠ Two important caveats about the plan (verified, must reach the author):**
> 1. **The plan is a *re-deploy* plan, not a precise "these commits will change" diff.** It marks
>    **every re-resolvable dep** as `[~] updated` — including the **pinned `v1.0.0`** dep that will
>    **not** move. The `2 updated` count over-states real movement. Only *one* commit actually
>    changed (the transitive); the pinned dep re-resolved to the same `fb285168`.
> 2. **`--dry-run` does not pre-compute the destination SHA** — the plan renders the target as `-`
>    (`a4aebcd -> -`), even though the subsequent real run *did* move `a4aebcd4 → 3169734b`. To see
>    the actual new commit, run the real update and read the deploy-phase `@<commit>`, or diff the
>    lockfile. Do **not** tell readers `--dry-run` shows the exact incoming SHA.

**`--verbose` dry-run** adds the SHA-comparison diagnostics (still `[~] updated` / `-> -`):

```text
apm update --dry-run --verbose
  [>] Checking upstream for revision-pin freshness...
  Loaded apm.lock.yaml for SHA comparison (3 dependencies)
      microsoft/apm-sample-package: locked at fb285168
      github/awesome-copilot/skills/review-and-refactor: locked at 3169734b
  Resolved dependency tree: 1 direct + 1 transitive deps (max depth 2)
      microsoft/apm-sample-package > awesome-copilot-review-and-refactor
  Phase: resolve -> 0.029s
  [i] Update plan for apm.yml
  … (same plan) …
```

### 2b — `apm update --yes` (apply — rewrites the lock)

Caption: **`apm update --yes` `[SIMULATED SETUP]` moving the behind transitive. Non-interactive
consent (as a scheduled job). Verified on apm v0.23.1.**

```text
apm update --yes
  [>] Checking upstream for revision-pin freshness...
  [i] Update plan for apm.yml
    [~] github/awesome-copilot/skills/review-and-refactor    ref: - (a4aebcd -> -)   files: …, +1 more
    [~] microsoft/apm-sample-package                         ref: v1.0.0 (fb28516 -> -)   files: …, +13 more
    2 updated
    [~] updated
  [i] Targets: claude, copilot, cursor  (source: apm.yml)
    [+] microsoft/apm-sample-package #v1.0.0 @fb285168 (cached)     # <- pinned: commit UNCHANGED
    |-- 2 prompts adopted -> .github/prompts/
    |-- 3 agents adopted -> 3 targets
    |-- 4 commands integrated -> .claude/commands/, .cursor/commands/
    |-- 3 rule(s) adopted -> 3 targets
    |-- 1 skill(s) integrated -> .agents/skills/, .claude/skills/
    [+] github.com/github/awesome-copilot/skills/review-and-refactor #default @3169734b   # <- MOVED to tip
    |-- (files unchanged)                                          # <- content identical: bytes didn't change
    [+] <project root> (local)
    |-- 1 prompts adopted -> .github/prompts/
    |-- 2 commands integrated -> .claude/commands/, .cursor/commands/
    |-- 3 rule(s) adopted -> 3 targets
  Updated 2 APM dependencies.                                       # exit 0
```

The deploy phase tells the **true** story the plan blurred: the pinned dep re-resolved to the *same*
`@fb285168 (cached)`; the transitive **moved** `a4aebcd4 → @3169734b` (the branch tip) with `(files
unchanged)` because the file bytes were identical.

**Consent gate (per docs, not directly exercised — used `--yes`):** an interactive `apm update`
prompts before writing and **defaults to No**; declining exits cleanly with *no* manifest/lockfile/FS
change. In CI or piped stdin you **must** pass `-y/--yes`. `--dry-run` is the safe, write-free
preview.

### 2c — The lockfile-diff-after-update story (L4 — the review artifact)

Caption: **The `apm.lock.yaml` diff a deliberate `apm update` produced — the entire reviewable
surface. Verified on apm v0.23.1.**

```diff
--- apm.lock.yaml (before update)
+++ apm.lock.yaml (after update)
-generated_at: '2026-07-02T01:17:41.266376+00:00'
+generated_at: '2026-07-02T01:23:19.474392+00:00'   # advanced: update rewrote the resolved content

   - repo_url: github/awesome-copilot                 # the transitive #main dep
-  resolved_commit: a4aebcd4bd354b59a6a6c12ab9c5c98a9d9e0276   # old (behind)
+  resolved_commit: 3169734bc2fb25d5e092130fc93d24b0dee3ac3a   # new (branch tip)
```

**What changed, and — just as important — what did *not*:**

| Field | Before | After | Note |
|---|---|---|---|
| `generated_at` | `…01:17:41…` | `…01:23:19…` | **advanced** — `update` writes; a pure restore would leave it byte-stable (Ch6) |
| `github/awesome-copilot` `resolved_commit` | `a4aebcd4…` | `3169734b…` | the **only** real move — floating `#main` re-resolved to the tip |
| `github/awesome-copilot` `content_hash` | `sha256:9236d06a…` | `sha256:9236d06a…` | **unchanged** — commit moved, bytes didn't (content-addressing, Ch6 R2) |
| `microsoft/apm-sample-package` `resolved_commit` | `fb285168…` | `fb285168…` | **unchanged** — a tag pin does not move under `apm update` |

> **Author payoff (L4):** an agent-context update is **as reviewable as any dependency bump** — a
> concrete `apm.lock.yaml` diff (one `resolved_commit`, plus `generated_at`) that a PR reviewer reads
> exactly like an `npm`/`pip` lock diff. *"What changed, when, and who approved it?"* is answered in
> the same review surface. **Don't hand-edit the lock** — it's regenerated on every install/update
> and a manual change trips `apm audit`.

### 2d — Nothing to move: the no-op update

On the now-current project (transitive back at tip), `apm update --dry-run` still prints the same
`2 updated` / `-> -` plan (see caveat 1 — it re-deploys rather than proving zero commit change);
running it for real would rewrite `generated_at` and re-deploy identical bytes. **When to use
`apm update`:** on a **chosen cadence** (Meridian's monthly refresh), routed through a PR.
**When *not* to:** never as an unattended step in a *restore* path — that is bare `apm install`.
`apm update` ≠ `apm self-update` (that upgrades the CLI binary, not project deps).

---

## Verb 3 — `apm audit` (verify integrity · NOT a CVE feed · L2)

**`apm audit --help` (v0.23.1), key options** (full list is long; the lifecycle-relevant ones):

```text
Usage: apm.exe audit [OPTIONS] [PACKAGE]
  Scan installed packages for hidden Unicode characters
Options:
  --file PATH        Scan an arbitrary file (not just APM-managed files)
  --strip            Remove hidden characters from scanned files (preserves emoji and whitespace)
  --dry-run          Preview what --strip would remove without modifying files
  -f, --format [text|json|sarif|markdown]   Output format (sarif = GitHub Code Scanning)
  -o, --output PATH  Write output to file (auto-detects format from extension)
  --ci               Run lockfile consistency checks for CI/CD gates. Exit 0 if clean, 1 if violations found.
  --no-drift         Skip the install-replay drift check.
  --no-policy / --policy TEXT   Org policy discovery/enforcement (experimental).
  --external NAME    Ingest findings from an external SARIF-native scanner (experimental).
```

**Purpose.** Verify that deployed agent context is **intact** — two independent checks:
1. a **content scan** for *hidden Unicode* (zero-width, bidi overrides, tag chars) in deployed
   prompt/instruction/skill/rules files, and
2. an **install-replay drift** check (re-materialize from cache into a scratch tree, diff against the
   working tree).
`--ci` adds a machine-readable **lockfile-consistency** gate. **Implements concept:** L2 (the
*verify* verb). This protection **already runs inside `apm install`**; `apm audit` is the *on-demand*
re-verification.

> **⚠ `apm audit` is NOT `npm audit`.** There is **no CVE / vulnerability database** and it reports
> **zero** "known advisories." A clean audit means *"no hidden characters and nothing has drifted
> from the lockfile"* — **not** "no known vulnerabilities." The only vulnerability-style analysis is
> opt-in **experimental external scanners** (`--external skillspector|sarif`), which underlines that
> APM itself is not a CVE feed. Confirmed empirically: every audit run below is integrity/drift only.

### 3a — Default `apm audit` — clean pass

Caption: **Default `apm audit` on the clean Meridian project: content scan + install-replay drift,
both clean. Verified on apm v0.23.1.**

```text
apm audit
  [>] Scanning all installed packages...
  [>] Replaying install (cache-only)...
  [+] Replayed 3 package(s)
  [>] Diffing scratch vs working tree...
  [+] No drift detected

  [*] 26 file(s) scanned -- no issues found          # exit 0
```

### 3b — `apm audit --ci` — the CI gate (9 checks)

Caption: **`apm audit --ci` on the clean project — the lockfile-consistency gate. Verified on apm
v0.23.1.**

```text
apm audit --ci
  [!] Could not determine org from git remote; enforcement skipped (set policy.fetch_failure_default=block in apm.yml to fail closed)
  [>] Replaying install (cache-only)...
  [+] Replayed 3 package(s)
  [>] Diffing scratch vs working tree...
  [+] No drift detected

                                            [>] APM Policy Compliance
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Status   ┃ Check                    ┃ Message                                                                  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ [+]      │ lockfile-exists          │ Lockfile present                                                         │
│ [+]      │ ref-consistency          │ All dependency refs match lockfile                                       │
│ [+]      │ deployed-files-present   │ All deployed files present on disk                                       │
│ [+]      │ no-orphaned-packages     │ No orphaned packages in lockfile                                         │
│ [+]      │ skill-subset-consistency │ Skill subset selections match lockfile                                   │
│ [+]      │ config-consistency       │ No MCP configs to check                                                  │
│ [+]      │ content-integrity        │ No critical hidden Unicode or hash drift detected                        │
│ [+]      │ includes-consent         │ 'includes:' declared -- local content deployment is explicitly consented │
│ [+]      │ drift                    │ no drift detected against lockfile                                       │
└──────────┴──────────────────────────┴──────────────────────────────────────────────────────────────────────────┘

  [*] All 9 check(s) passed          # exit 0
```

**The 9 `--ci` checks (verified):** `lockfile-exists`, `ref-consistency`, `deployed-files-present`,
`no-orphaned-packages`, `skill-subset-consistency`, `config-consistency`, `content-integrity`,
`includes-consent`, `drift`. (The `Could not determine org…` line is benign here — the scratch dir
has **no git remote**, so *org-policy* discovery is skipped; in a real repo with a remote, org policy
would be fetched. That is Chapter 11's fleet story, not this chapter.)

### 3c — What a failure looks like (drift → `--ci` exit 1)

I deleted one deployed file (`.github/instructions/design-standards.instructions.md`) to induce
drift, then re-ran the gate:

Caption: **`apm audit --ci` failing on drift (a deleted deployed file). Note exit 1 and the
remediation. Verified on apm v0.23.1.**

```text
apm audit --ci
  [>] Replaying install (cache-only)...
  [+] Replayed 3 package(s)
  [>] Diffing scratch vs working tree...
  [!] Drift detected: 1 file(s)

                                               [>] APM Policy Compliance
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Status   ┃ Check                  ┃ Message                                                                          ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ [+]      │ lockfile-exists        │ Lockfile present                                                                 │
│ [+]      │ ref-consistency        │ All dependency refs match lockfile                                               │
│          │ deployed-files-present │ 1 deployed file(s) missing -- run 'apm install' to restore                       │
│          │ drift                  │ drift detected: 1 file(s): .github/instructions/design-standards.instructions.md │
└──────────┴────────────────────────┴──────────────────────────────────────────────────────────────────────────────────┘

  [x] 2 of 4 check(s) failed
  [!] Drift detected: 1 file(s)
    unintegrated (1):
      - .github/instructions/design-standards.instructions.md  [microsoft/apm-sample-package]
    [i] Run 'apm install' to re-sync deployed files with the lockfile.       # exit 1
```

The gate **fail-fast** stops after the drift-related failures (only 4 checks ran, `2 of 4` failed —
`deployed-files-present` + `drift`); `--no-fail-fast` would run all 9. The missing file is classified
`unintegrated` (one of the drift kinds: **unintegrated** / **modified** / **orphaned**), and
remediation is `apm install`. Running `apm install` re-synced the file and the gate returned to
`All 9 check(s) passed` (exit 0).

### 3d — The default form is advisory on drift; the content scan drives its exit code

Caption: **Default `apm audit` on the *same* drifted state — it reports the drift but exits 0.
Verified on apm v0.23.1.**

```text
apm audit                  # same deleted file as 3c
  [>] Scanning all installed packages...
  [>] Replaying install (cache-only)...
  [!] Drift detected: 1 file(s)
  [*] 25 file(s) scanned -- no issues found
  [!] Drift detected: 1 file(s)
    unintegrated (1):
      - .github/instructions/design-standards.instructions.md  [microsoft/apm-sample-package]
    [i] Run 'apm install' to re-sync deployed files with the lockfile.       # exit 0  (!)
```

> **⚠ Critical exit-code distinction (verified):** the **same drift** exits **1** under `--ci` but
> **0** under default `apm audit`. The default form's exit code tracks the **content scan** (hidden
> Unicode); **drift is advisory** there. `apm audit --ci` is the form whose exit code enforces
> lockfile consistency. **Use `apm audit --ci` — not bare `apm audit` — as a CI gate.**

### 3e — The content scan finding + its exit code (hidden Unicode → exit 2)

Isolated with `--file` on an arbitrary file containing a `U+200B` zero-width space:

Caption: **`apm audit --file` flags a zero-width space and exits 2 — the content-scan failure code
(distinct from `--ci`'s exit 1). Verified on apm v0.23.1.**

```text
apm audit --file hidden-demo.md
                         [>] Content Scan Findings
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Severity   ┃ File           ┃ Location   ┃ Codepoint  ┃ Description      ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ WARNING    │ hidden-demo.md │ 3:12       │ U+200B     │ Zero-width space │
└────────────┴────────────────┴────────────┴────────────┴──────────────────┘
  [!] 1 warning(s) in 1 file(s) -- hidden characters detected
  [i]   Run 'apm audit --strip' to remove hidden characters
  [i]   Plus 1 info-level finding(s) (use --verbose to see)                  # exit 2
```

**`apm audit` exit-code summary (verified):**

| Situation | Default `apm audit` | `apm audit --ci` |
|---|---|---|
| Clean | `0` | `0` |
| Drift only (missing/modified deployed file) | **`0`** (advisory) | **`1`** (gate fails) |
| Hidden-Unicode findings | **`2`** (content scan) | `1` (via `content-integrity` check) |

---

## Division of labor — the whole verb map (verified · L3)

The task's point 4, proven empirically:

| Command | Role | Moves versions? | Fails on drift? | Verified proof |
|---|---|---|---|---|
| `apm install` (bare) | **restore** locked bytes | **No** | No | restored `@a4aebcd4 (cached)` even for floating `#main` — did **not** float to tip |
| `apm install --frozen` | **structural CI reproduce** (Ch6) | No | presence only | fail-closed presence gate (Ch6 reference) |
| `apm outdated` | **report** drift | No (read-only) | No (exit 0) | wrote nothing; exit 0 with `1 outdated dependency found` |
| `apm update` | **change** (the only mover) | **Yes** | n/a | moved `a4aebcd4 → 3169734b`, rewrote lock + `generated_at` |
| `apm audit` | **verify** content + drift | No | advisory (exit 0) / content exit 2 | reported drift but exited 0; flagged `U+200B` exit 2 |
| `apm audit --ci` | **gate** lockfile consistency | No | **Yes (exit 1)** | 9-check table; drift → `2 of 4 failed`, exit 1 |

> **The one-line mental model for the chapter:** **install restores · `--frozen` enforces · outdated
> reports · update changes · audit verifies · `audit --ci` gates.** Only `apm update` moves a version;
> only `apm audit --ci` fails a build.

---

## Caveats & flags (for the author + verifier)

1. **`apm outdated` on a fresh build reports the unpinned transitive as `up-to-date`, not
   drift-able** — because install locked `#main` to the *current* tip. Teach: *a floating ref is not
   "outdated" until the branch advances past your lock.* The non-empty table in §1b required rolling
   the lock **behind** the tip (`[SIMULATED SETUP]`). Do not imply a fresh unpinned dep shows as
   outdated immediately.
2. **`apm outdated` keys off the committed lockfile, not the live `apm.yml`.** Loosening a pin in the
   manifest without re-installing does **not** change its report. Pin changes take effect via
   `apm update`.
3. **`apm outdated` exit code is `0` even when outdated.** Finding drift is not an error. `1` only
   when there is **no lockfile** (documented; not directly exercised — verifier could delete the lock
   to confirm). It has **no `--ci`/`--json` flag** — the CI gate is `apm audit --ci`.
4. **`apm update`'s plan over-states movement.** It marks every re-resolvable dep `[~] updated`
   (including pinned tags that won't move) and renders the destination SHA as `-` in `--dry-run`.
   The *real* movement is only visible in the deploy phase (`@<commit>`) or the lockfile diff. Don't
   claim `--dry-run` shows the exact incoming SHA, and don't read `N updated` as `N commits changed`.
5. **The lockfile diff is the reviewable artifact (L4).** A real `apm update` changed exactly:
   `generated_at` + one transitive `resolved_commit` (`a4aebcd4 → 3169734b`). The pinned dep and the
   transitive's `content_hash` were **unchanged** (commit moved, bytes didn't — Ch6 content-addressing).
6. **`apm update` is the ONLY version-moving verb.** Bare `apm install` restores the *locked* commit
   even for a floating ref (verified). `apm update` ≠ `apm self-update` (CLI binary vs. project deps).
7. **`apm audit` ≠ `npm audit` — no CVE database.** It checks hidden Unicode + lockfile/drift
   consistency only. A clean audit ≠ "no vulnerabilities." Emphasize this — it is the chapter's most
   important misconception to prevent.
8. **Three audit exit codes:** `0` clean · `2` hidden-Unicode content findings · `1` for a `--ci`
   gate violation. **Default `apm audit` is advisory on drift (exit 0); `apm audit --ci` gates it
   (exit 1).** Use `--ci` in CI.
9. **`apm audit --ci` runs 9 checks;** the benign `Could not determine org from git remote` line
   appears only because the scratch dir has no git remote (org-policy discovery skipped). Not an
   error; not part of this chapter's scope (Ch11).
10. **Same benign install noise as Ch4–Ch6:** the sample package drops the unsupported `mode:`
    frontmatter key on Claude/Cursor commands; the transitive is `unpinned`. Expected; not lifecycle
    errors.

---

## For the `code-verifier`

- **Build (network for the initial add):** author Meridian **v0.2.0** in `%TEMP%\apm-ch07` (identity;
  targets `copilot, claude, cursor`; `dependencies.apm: [ microsoft/apm-sample-package#v1.0.0 ]`;
  `mcp: []`; `includes: auto`; `scripts.review`; one local instruction + one local prompt under
  `.apm/`). Run `apm install --target copilot,claude,cursor` → **exit 0**; lock records the pinned
  dep `@fb285168` (v1.0.0) + the transitive `github/awesome-copilot` `@3169734b` (unpinned `#main`).
- **`apm outdated` (clean):** `All dependencies are up-to-date`, **exit 0**. `--verbose` adds
  `Skipping local dep: .`.
- **`apm outdated` (drift) — `[SIMULATED SETUP]`:** in the lockfile, replace the transitive's
  `resolved_commit` `3169734bc2fb25d5e092130fc93d24b0dee3ac3a` → `a4aebcd4bd354b59a6a6c12ab9c5c98a9d9e0276`,
  then `apm outdated`. Expect the **Package/Current/Latest/Status/Source** table with the pinned dep
  `up-to-date` (git tags) and the transitive `outdated` (git branch), `[!] 1 outdated dependency
  found`, **exit 0**. (Assert the *shape* + statuses, not the exact tip SHA — `main` may advance.)
- **`apm update --dry-run`:** plan prints `[~] updated` rows with `-> -` targets, `2 updated`,
  `Dry run: no changes applied`, **exit 0**, lock **unchanged**.
- **`apm update --yes`:** from the behind state, moves the transitive to the current tip; deploy phase
  shows pinned `@fb285168 (cached)` unchanged + transitive `@<tip> (files unchanged)`; `Updated 2 APM
  dependencies.`, **exit 0**. Assert lock diff = `generated_at` advanced **and** the transitive
  `resolved_commit` changed; pinned `resolved_commit` and transitive `content_hash` **unchanged**.
- **`apm audit` (clean):** content scan + replay drift → `N file(s) scanned -- no issues found`,
  **exit 0**.
- **`apm audit --ci` (clean):** 9-check table → `All 9 check(s) passed`, **exit 0**.
- **`apm audit --ci` (fail):** delete one deployed file (e.g.
  `.github/instructions/design-standards.instructions.md`) → `deployed-files-present` + `drift` fail,
  `unintegrated`, **exit 1**. Restore with `apm install` → gate green again.
- **`apm audit` (drift, advisory):** same deleted file, default form reports drift but **exit 0**
  (content scan clean). Restore with `apm install`.
- **`apm audit --file` (hidden Unicode):** write a temp file containing `U+200B`; `apm audit --file
  <path>` → `Content Scan Findings` table (`WARNING … U+200B … Zero-width space`), **exit 2**.
- **Division of labor:** roll the transitive lock behind, run **bare `apm install`** → it restores
  the *locked* (behind) commit `@a4aebcd4 (cached)`, **does not** float to the tip, **exit 0**. Only
  `apm update` moves it.
- **Network:** only the very first `apm install` add is network-bound; all other steps are
  cache-served. No tokens, no live pushes. Mark nothing `SKIPPED-needs-network` beyond the initial
  add. **Verified against apm v0.23.1.**

---

## Sources

Official APM documentation (behavior cross-checked against the live CLI, v0.23.1):
- apm outdated — <https://microsoft.github.io/apm/reference/cli/outdated/>
- apm update — <https://microsoft.github.io/apm/reference/cli/update/>
- apm audit — <https://microsoft.github.io/apm/reference/cli/audit/>
- Update and refresh (install restores; the *"Run 'apm update'"* nudge; `--frozen`↔`--update`;
  `apm update` ≠ `apm self-update`) — <https://microsoft.github.io/apm/consumer/update-and-refresh/>
- Manage dependencies (lockfile as the *"what am I running?"* review artifact; branches move, tags/SHAs
  don't; don't hand-edit) — <https://microsoft.github.io/apm/consumer/manage-dependencies/>
- Drift and secure by default (drift kinds unintegrated/modified/orphaned; hidden-Unicode scope) —
  <https://microsoft.github.io/apm/consumer/drift-and-secure-by-default/>
- Lifecycle (cadence: *"install and run daily, audit in CI"*) — <https://microsoft.github.io/apm/concepts/lifecycle/>

## Artifact path

`content/research/07-lifecycle-reference.md`
