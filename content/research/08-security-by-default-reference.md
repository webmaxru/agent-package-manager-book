# Chapter 8 — Security by Default · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 8 is where the four-properties frame reaches **provenance/security**. It answers
> a blunt question: *if a skill/instruction/prompt file "runs" the instant it lands on disk, where is
> the security gate?* APM's answer is **install-time, file-first**: scan before deploy, pin bytes by
> hash, and make **tool/code surfaces** (MCP servers, hooks, `bin/`, canvas) cross a **trust
> boundary** before they can act. This reference proves the three headline mechanisms end to end on
> apm **v0.23.1**: **hidden-Unicode scanning** (the flagship live demo — exit codes nailed down),
> **content-hash tamper detection** (`apm audit` drift + the `--ci` content-integrity check), and the
> **transitive self-defined-MCP block** (reproduced **live** with local packages, correcting the
> running example's message *and* the lockfile MCP shape). It also documents **Executable Trust
> Governance** (v0.22 — `apm approve`/`apm deny`), verified through a full gate → decline → approve
> cycle, and pins the **install-time-not-runtime** boundary against the official threat model.
> **Concept it implements (Ch8 theory):** **provenance / security** — the "Secure by default"
> property. **No `08-security-by-default-theory.md` brief exists yet**; the concept anchors **S1–S5**
> below are named so the author and theory-researcher can align.
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`, confirmed at session start).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dir (outside repo):**
> `%TEMP%\apm-ch08` with sub-projects: `proj` (local-only Meridian v0.3.0 tamper demo), `execpkg`
> (a package declaring a **self-defined** MCP server, `registry: false`), `pkgA` (depends on
> `execpkg`, to force the MCP **transitive**), `consumer` (direct-dep executable-trust demo),
> `consumer2` (transitive-MCP-block demo), plus two crafted hidden-Unicode files.
> **Network:** available; **no packages fetched from the network and no tokens used** — every result
> below is from **local packages + crafted files**, so the whole chapter's core is **deterministic
> and offline-safe**. The one scenario that genuinely needs network — a **registry**-referenced
> transitive MCP (e.g. `io.github.github/github-mcp-server`) and the private Meridian dep — is
> flagged **`SKIPPED-needs-network`**.

---

## Theory anchors (Chapter 8 — Secure by default) — proposed

Each mechanism below links back to the security sub-concept it implements. (Anchors proposed; align
with the theory brief when it lands.)

| Ch8 concept (proposed anchor) | What it establishes | Confirmed here by |
|---|---|---|
| **S1 — The prompt supply chain has no install→execute gap** | Unlike `npm` (install now, run later), an agent-context file is *live the moment it lands* — "**file presence IS execution**." So the security gate must be **pre-deploy**: scan first, deploy only if clean. | official threat model (docs); `apm install`'s built-in scan blocks **before** any integrator copies files |
| **S2 — Content safety (hidden-Unicode scanning)** | Invisible characters (bidi overrides, tag chars, zero-width, variation selectors) can smuggle instructions an LLM tokenizes but a human can't see. APM scans and can strip them. | crafted files → real `apm audit` findings: **U+202E = Critical (exit 1)**, **U+200B = Warning-only (exit 2)**, clean = 0; `--strip` round-trip |
| **S3 — Integrity (content-hash pinning)** | The lockfile pins **bytes** (`content_hash` for sources, `deployed_file_hashes` for on-disk files); a tampered deployed file is detectable. | tampered a deployed file → `apm audit` reports **drift** (advisory, exit 0); `apm audit --ci` **fails** the `content-integrity` + `drift` checks (exit 1) with `expected=…/actual=…` |
| **S4 — Trust boundaries for tool & code surfaces** | Two *separate* gates: (a) the **MCP trust model** — direct-dep MCP auto-trusted, **transitive MCP blocked**; (b) the opt-in **Executable Trust Gate** — hooks / `bin/` / self-defined MCP / canvas require approval. | **live**: transitive self-defined MCP **withheld** + real message; `--trust-transitive-mcp` flips it; enabling `executables:` gated a **direct** MCP behind a `[y/N]` prompt → `apm approve` |
| **S5 — Install-time gates, NOT runtime sandboxing** | APM has **no runtime footprint**; it does not sandbox MCP at runtime, sign packages, or watch the agent. Know the boundary so you don't over-trust it. | docs "What APM does NOT do"; every mechanism here fires during `install`/`audit`/`compile`, then the process exits |

> **Frame note.** Ch6 made bytes **reproducible** (`content_hash`); Ch7 made lifecycle **deliberate**
> (`outdated`/`update`/`audit`). Ch8 shows those same artifacts double as **security controls**: the
> hash that guarantees reproducibility also **detects tampering**, and the manifest that declares
> intent also **declares your tool-trust boundary**. Security here is *emergent from the model*, not
> bolted on.

---

## Feature reference (v0.23.1)

| Feature | Job | Implements | Exact behavior observed | Exit |
|---|---|---|---|---|
| `apm audit` (content scan) | scan deployed files for **hidden Unicode** + replay-**drift** | S2, S3 | Critical/Warning/Info severity table per finding; drift is **advisory** in bare audit. | `0` clean/info/drift-only · **`1`** any Critical · **`2`** Warning-only |
| `apm audit --file <path>` | scan **any** file (bypasses drift) | S2 | Isolates the content scan; same severity→exit mapping. | `0`/`1`/`2` |
| `apm audit --strip` | **remove** critical+warning chars in place | S2 | `[+] Cleaned:` / `[*] Cleaned N file(s)`; preserves emoji + ZWJ-in-emoji; does **not** touch source packages. | `0` |
| `apm audit --strip --dry-run` | **preview** what strip removes | S2 | Per-file Critical/Warning/Total table; `[i] N file(s) would be modified`; **writes nothing**. | `0` |
| `apm audit --ci` | CI gate: lockfile-consistency + **content-integrity** + drift | S3 | 8–9 check table incl. `content-integrity` (per-file SHA-256 hash drift, `expected=…/actual=…`). | `0` clean · **`1`** any failure |
| `apm install` (built-in scan) | **pre-deploy gate** | S1, S2 | Scans `apm_modules/` sources **before** integrators copy; **Critical blocks deploy** (package cached for inspection, nothing reaches agent dirs); Warnings deploy. | `0` · **`1`** if any package blocked |
| `apm install --force` | override the block | S1, S2 | "deploy despite critical security findings" (also overrides collisions). The explicit *"I know what I'm doing."* | `0` |
| `content_hash` / `deployed_file_hashes` (lockfile) | pin **bytes**, not just refs | S3 | SHA-256 of source tree + of each deployed file; cache verified on install; freshly-downloaded mismatch **aborts** (possible tampering). | — |
| **MCP trust model** (depth-based, always on) | gate MCP by dependency depth | S4 | Direct-dep MCP **auto-trusted**; **transitive** self-defined MCP **withheld** with a `[!]` warning; install still **succeeds**. | `0` (MCP skipped) |
| `apm install --trust-transitive-mcp` | opt into transitive self-defined MCP | S4 | Configures the withheld server; prints `[i] Trusting self-defined MCP server '<n>' from transitive package '<p>' (--trust-transitive-mcp)`. | `0` |
| **Executable Trust Gate** (`executables:`, opt-in, v0.22) | gate hooks / `bin/` / self-defined MCP / canvas | S4 | **Off by default** ("all executables deploy"). Enabled by an `executables:` block (even `{}`) or org policy. When on, unmatched executables are **gated pending approval** (interactive `[y/N]`, default **N**; parked in CI). | `0` (parked) |
| `apm approve [pkg]` / `apm deny [pkg]` | grant / block executable trust | S4 | Writes `executables.{allow,deny}` to `apm.yml` (shared) or `~/.apm/config.json` (`--user`). `--pending`/`--list`/`--all`/`--recommended`. | `0` |
| `apm policy explain <pkg>` | why a package is trusted/blocked | S4 | Prints the deciding layer per executable type + shadowed layers. | `0` |

---

## S1 — The prompt supply chain is different (the concept the chapter opens on)

Verbatim framing from the **official Security Model** (docs, [enterprise/security](https://microsoft.github.io/apm/enterprise/security/)):

> Traditional package managers install code that sits inert until … explicitly executed. Between
> `npm install` and `npm start` there is a gap — time for `npm audit`, code review, and policy checks.
> Agent configuration has no such gap. The moment a skill, instruction, or prompt file lands in
> `.github/prompts/` or `.claude/agents/`, any IDE agent watching the filesystem … may already be
> ingesting it. **There is no "execution step." File presence IS execution.** … APM treats package
> deployment as a **pre-deployment gate: scan first, deploy only if clean.**

That single idea justifies the whole chapter: the security work has to happen **at install time**,
because after install there is no second checkpoint. Everything below is a *pre-deploy* or
*on-demand-verify* gate — never a runtime monitor (see **S5**).

---

## S2 — Hidden-Unicode scanning (the flagship live demo) · verified

**The threat (docs).** Researchers found hidden Unicode in popular shared rules files. Bidi overrides
reorder visible text; tag characters map 1:1 to invisible ASCII; variation selectors 17–256 encode
invisible payload bytes (the **Glassworm** vector, 2026). **LLMs tokenize all of these**, so a model
reads instructions a human cannot see.

### Severity → exit code (empirically pinned; matches the docs' `apm audit` exit-code table)

| Severity | Example codepoints (docs) | `apm audit` exit | Blocks `apm install`? |
|---|---|---|---|
| **Critical** | tag chars `U+E0001–E007F`, **bidi overrides `U+202A–E, U+2066–9`**, variation selectors 17–256 `U+E0100–E01EF` (Glassworm) | **`1`** | **Yes** (deploy blocked) |
| **Warning** | **zero-width `U+200B–D`**, VS 1–15 `U+FE00–FE0E`, bidi marks `U+200E–F/U+061C`, invisible operators `U+2061–4`, soft hyphen `U+00AD`, mid-file BOM | **`2`** (only if no Critical) | No (flagged, deploys) |
| **Info** | non-breaking/unusual whitespace, emoji VS `U+FE0F`, ZWJ *between* emoji | `0` (only with `-v`) | No |

> **Correction to carry back to Ch7.** The Ch7 reference summarized hidden-Unicode findings as
> "exit **2**." That is only true for **Warning-only** files. **Critical** findings exit **`1`**;
> Warning-only exit **`2`**; clean/info/`--strip`/dry-run exit **`0`**. A usage error (mutually
> exclusive flags) also exits `2`; a config/infra error exits `3`.

### Verified — a Critical finding (bidi override `U+202E`) → exit 1

Crafted a markdown "review checklist" embedding `U+200B` (zero-width space) on line 4 and `U+202E`
(right-to-left override) on line 7; confirmed both byte sequences (`e2808b`, `e280ae`) are present,
then:

```text
apm audit --file .\checkout-review.prompt.md

                           [>] Content Scan Findings
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Severity   ┃ File              ┃ Location   ┃ Codepoint  ┃ Description       ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ CRITICAL   │ checkout-review.… │ 7:1        │ U+202E     │ Right-to-left     │
│            │                   │            │            │ override (RLO)    │
│ WARNING    │ checkout-review.… │ 4:1        │ U+200B     │ Zero-width space  │
└────────────┴───────────────────┴────────────┴────────────┴───────────────────┘

[x] 1 critical finding(s) in 1 file(s) -- hidden characters detected
[i]   These characters may embed invisible instructions
[i]   Review file contents, then run 'apm audit --strip' to remove
# exit=1
```

### Verified — a Warning-only finding (zero-width space `U+200B`) → exit 2

```text
apm audit --file .\warn-only.md
                        [>] Content Scan Findings
┃ WARNING │ warn-only.md │ 3:21 │ U+200B │ Zero-width space │
[!] 1 warning(s) in 1 file(s) -- hidden characters detected
[i]   Run 'apm audit --strip' to remove hidden characters
# exit=2
```

### Verified — `--strip` round-trip (`--dry-run` preview → strip → clean re-audit)

```text
apm audit --file .\checkout-review.strip.md --strip --dry-run
  [>] Dry run -- the following would be removed by --strip:
  ┃ File … ┃ Critical ┃ Warning ┃ Total ┃  ->  1  1  2
  [i] 1 file(s) would be modified
  [i] Run 'apm audit --strip' to apply          # exit 0; file UNCHANGED (U+202E still present)

apm audit --file .\checkout-review.strip.md --strip
  [+]   Cleaned: …\checkout-review.strip.md
  [*] Cleaned 1 file(s)                          # exit 0; U+202E and U+200B both removed

apm audit --file .\checkout-review.strip.md
  [*] 1 file(s) scanned -- no issues found       # exit 0
```

**Notes for the author (verified + docs):**
- `--strip` removes **both** Critical *and* Warning characters, **preserves emoji and ZWJ inside
  emoji sequences** (e.g. 👨‍👩‍👧), and **rewrites the file** (so a byte-count delta is expected — it is
  not a clean "minus N bytes"; don't assert a specific delta).
- `--strip` **does not modify the source package** in `apm_modules/`; the next `apm install`
  re-materializes the tainted bytes. **Persistent** remediation = fix upstream or pin a clean commit.
- `--file` scans **any** file (downloaded rules, PR diffs, pasted instructions) and **bypasses**
  drift detection — perfect for isolating the content scan.

### The built-in pre-deploy gate (docs; the "secure by default" bit)

Content scanning already runs **inside `apm install`** (and `apm compile`, `apm unpack`), *before*
any integrator copies a file: `download → scan source → block or deploy → report`. **Critical
findings block deployment** (the package is cached under `apm_modules/owner/package/` so you can
inspect it, but nothing reaches `.github/`, `.claude/`, …); **Warnings deploy** with a flag;
**`--force` overrides** the block. In a multi-package install, blocked packages don't stop the
others, but **`apm install` exits `1`** if any package was blocked — failing the CI step. *You do not
have to call `apm audit` to be safe by default* — `apm audit` is the on-demand power tool.

---

## S3 — Content-hash pinning & tamper detection · verified

**The mechanism (Ch6 R2, now used as a security control).** The lockfile records **two** SHA-256
families: `content_hash` (a fingerprint of a dependency's **source tree**, computed over sorted
paths+contents, excluding `.git/`/`__pycache__/`) and `deployed_file_hashes` /
`local_deployed_file_hashes` (a fingerprint of **each deployed file** on disk). On install, cached
sources are verified against `content_hash`; a freshly-downloaded mismatch **aborts** the install
(possible supply-chain tampering). `apm audit` verifies the **deployed** side.

### Verified — tamper a deployed file, then audit

On the local-only Meridian v0.3.0 project (`proj`), the lockfile recorded
`…/meridian-checkout.instructions.md: sha256:4acba6aa…`. I appended a malicious line to the deployed
file and ran audit:

```text
apm audit          # after tampering a deployed file
  [>] Scanning all installed packages...
  [>] Replaying install (cache-only)...
  [!] Drift detected: 1 file(s)
  [*] 3 file(s) scanned -- no issues found
  [!] Drift detected: 1 file(s)
    modified (1):
      - .github/instructions/meridian-checkout.instructions.md  [.]
    [i] Run 'apm install' to re-sync deployed files with the lockfile.
# exit=0   <-- drift alone is ADVISORY in bare audit
```

```text
apm audit --ci     # same tampered file, CI gate
  │          │ content-integrity │ 1 file(s) with hash drift -- run 'apm install' to restore …
  │          │ drift             │ drift detected: 1 file(s): .github/instructions/meridian-checkou…
  content-integrity details:
    - hash-drift: .github/instructions/meridian-checkout.instructions.md
      (dep=<self>, expected=4acba6aa1bee..., actual=bab6d9cb4f14...)
  [x] 2 of 8 check(s) failed
# exit=1
```

**The teaching point (S3).** The **same hash** that guarantees byte-for-byte reproducibility
(Chapter 6) is what **catches tampering** here: `apm audit --ci`'s `content-integrity` check compares
each deployed file's on-disk SHA-256 against the lockfile record and prints **`expected=` vs
`actual=`**. Note the two-tier behavior the author must get right:

- **Bare `apm audit`**: drift/hash-mismatch is **advisory** → **exit 0** (it *tells* you, it doesn't
  *fail*). Great for a local heads-up.
- **`apm audit --ci`**: the same mismatch is a **hard failure** → **exit 1**. This is the branch-
  protection gate. (This complements Ch6's `--frozen`, which is *structural presence only* and
  explicitly *not* a content check — the CLI itself says "run `apm audit` for on-disk integrity.")
- Local `.apm/` content is checked via a **synthesized self-entry** (`dep=<self>`), so even a repo's
  own deployed files are integrity-checked — no dependency required (my demo had `dependencies: []`).

---

## S4 — Trust boundaries: two SEPARATE gates (the headline) · verified live

This is the subtlest — and most misunderstood — part of the chapter. There are **two independent
mechanisms**, and conflating them will mislead readers:

| | **MCP trust model** | **Executable Trust Gate** (v0.22) |
|---|---|---|
| **On by default?** | **Always on** | **Opt-in** (needs an `executables:` block in `apm.yml`, even `{}`, or a non-empty org-policy `executables:`) |
| **Keyed on** | dependency **depth** (direct vs transitive) | **executable kind** from *any* dependency package |
| **Covers** | MCP servers | hooks (`.apm/hooks/`), `bin/` executables, **self-defined MCP** (`registry: false`), canvas extensions |
| **Direct dep** | **auto-trusted** | **gated** (when the gate is enabled) |
| **Transitive dep** | **blocked** (re-declare or `--trust-transitive-mcp`) | gated (when enabled) |
| **Manage with** | `--trust-transitive-mcp`, re-declaration | `apm approve` / `apm deny` / `apm policy explain` |

> Text primitives (skills, agents, instructions) are **never** gated by either mechanism, and local
> root `.apm/` content is always trusted.

### S4a — MCP trust model: transitive self-defined MCP is blocked (reproduced LIVE, offline)

I built a local chain to force the block without any network: `execpkg` declares a **self-defined**
MCP server (`registry: false`, stdio `npx`), `pkgA` depends on `execpkg`, and a fresh `consumer2`
installs `pkgA` — so the MCP arrives at **depth 2 (transitive)**.

**Direct install first (baseline) — auto-trusted:**

```text
apm install <execpkg>              # execpkg is a DIRECT dep of `consumer`
  [i] Trusting direct dependency MCP 'local-fetch' from 'checkout-review-tools'
  |  [+]  local-fetch -> Copilot, Vscode (configured)
# exit=0  -> direct-dep MCP is AUTO-TRUSTED (you chose the package)
```

**Transitive install — BLOCKED (the real message; corrects the running example):**

```text
apm install <pkgA>                 # pkgA -> execpkg, so the MCP is TRANSITIVE (depth 2)
  [+] …\pkgA (local)      |-- (files unchanged)
  [+] …\execpkg (local)   |-- (files unchanged)
  [!] Transitive package 'checkout-review-tools' declares self-defined MCP
  server 'local-fetch' (registry: false). Re-declare it in your apm.yml or use
  --trust-transitive-mcp.
  [*] Installed 2 APM dependencies in 0.8s.
# exit=0  -> the MCP is WITHHELD, but the install SUCCEEDS
```

**Confirmed withheld:** `consumer2`'s lockfile has **no** `mcp_servers`/`mcp_configs`, and **no**
`.vscode/mcp.json` was written. The transitive dep is recorded with `depth: 2` and
`resolved_by: _local/pkgA` (provenance), but its MCP is not configured.

**Remedy 1 — `--trust-transitive-mcp` (verified):**

```text
apm install --trust-transitive-mcp
  [i] Trusting self-defined MCP server 'local-fetch' from transitive package
  'checkout-review-tools' (--trust-transitive-mcp)
  |  [+]  local-fetch -> Copilot, Vscode (configured)
# exit=0  -> now .vscode/mcp.json IS written
```

**Remedy 2 — re-declaration:** add the server to your own `apm.yml` `dependencies.mcp`, promoting it
to a **direct** dep (which the direct-install baseline above proves is auto-trusted). *Corollary:*
the "trust boundary" the chapter sells is exactly this — **an MCP a tool can call must appear in a
manifest a human reviewed.**

> ### ⚠ Corrections to the running example (`.source-docs/v2/running-example.md`, Ch8)
> The planning doc guessed the block as a hard failure with a registry server. Real v0.23.1:
>
> | Running-example assumption | Real v0.23.1 behavior |
> |---|---|
> | `[x] Blocked transitive MCP server: io.github.github/github-mcp-server` | `[!] Transitive package '<pkg>' declares self-defined MCP server '<name>' (registry: false). Re-declare it in your apm.yml or use --trust-transitive-mcp.` |
> | Prefix `[x]` (error/block), implies install **fails** | Prefix `[!]` (warn); MCP **withheld** but install **succeeds, exit 0** |
> | "Declare it explicitly in dependencies.mcp or re-run … with `--trust-transitive-mcp`" | Flag name correct; the flag help is *"Trust **self-defined** MCP servers from transitive packages (skip re-declaration requirement)"* |
> | Applies to a **registry** server (`io.github.github/…`) | The verified path is a **self-defined** server (`registry: false`). Behavior for a **registry**-referenced transitive MCP is **`SKIPPED-needs-network`** (see below). |
>
> **Author fix:** teach the beat as *"a dependency-of-a-dependency tried to add a tool you never
> reviewed; APM withheld it and told you exactly how to opt in."* Keep the install **succeeding** —
> the story is *"the tool was quarantined,"* not *"the build broke."*

**Lockfile MCP shape — CORRECTED (verified from the direct install).** The running example (and the
Ch6 note, which flagged this as UNVERIFIED) guessed a shape that does **not** match v0.23.1:

```yaml
# REAL v0.23.1 lockfile MCP shape (from `consumer`'s apm.lock.yaml, direct self-defined MCP):
mcp_servers:                       # <- a FLAT LIST OF NAME STRINGS, not objects
- local-fetch
mcp_configs:                       # <- keyed by SERVER NAME, not by target/harness
  local-fetch:
    name: local-fetch
    transport: stdio
    args:
    - -y
    - '@modelcontextprotocol/server-fetch'
    registry: false                # <- false = self-defined (vs registry-resolved)
    command: npx
```

```yaml
# WRONG (running-example guess) — do NOT use:
mcp_servers:
  - name: io.github.github/github-mcp-server
    source: registry
    depth: 2
    resolved_by: meridian-finance/checkout-review-pack
mcp_configs:
  copilot:                         # <- NOT keyed by target
    github-mcp-server: { transport: http, url: … }
```

Also verified: a **local** dependency is locked as `repo_url: _local/<dir>`, `source: local`,
`local_path: <abs path>`, **no** `resolved_commit`/`content_hash` (local deps aren't git-pinned);
transitive deps carry `depth:` and `resolved_by:`.

**`SKIPPED-needs-network`** (Meridian story continuity): the private
`github.com/meridian-finance/checkout-review-pack` dep and any **registry**-referenced transitive MCP
(`io.github.github/github-mcp-server`, `registry: true`) require cloning private repos / hitting the
MCP registry. The **mechanism** (transitive MCP blocked; re-declare or `--trust-transitive-mcp`) is
verified via the self-defined path above and the docs' *MCP server trust model*; the exact wording
for a **registry** transitive server and its re-declared `dependencies.mcp` entry shape are
**not** exercised offline — mark those blocks `SKIPPED-needs-network`.

### S4b — Executable Trust Gate (`apm approve`/`apm deny`, v0.22) · verified cycle

**What it gates (docs):** executable primitives from **dependency** packages —

| Executable kind | Gated? | Why |
|---|---|---|
| Hooks (`.apm/hooks/`, `hooks/`) | **Yes** | auto-fire in the IDE on lifecycle events |
| `bin/` executables | **Yes** | deployed onto the agent PATH via symlinks |
| Self-defined MCP servers (`registry: false`) | **Yes** | write to IDE MCP config |
| Canvas extensions (`.apm/extensions/`) | **Yes** | deploy executable Node.js to IDE extensions |
| Text primitives (skills, agents, instructions) | **No** | no code-execution risk |

**It is OPT-IN (the nuance that makes the whole thing make sense).** With **no** `executables:`
block, the gate is **disabled** and executables deploy unconditionally (backward-compatible). Verified
before enabling — `apm approve --list` on `consumer`:

```text
[i] Executable-trust gate disabled -- all executables deploy. Add an `executables:` block to apm.yml to enable it.
  checkout-review-tools#0.3.0: mcp[+:gate-disabled]
```

> This resolves the apparent contradiction with S4a: my first **direct** install *auto-trusted* the
> self-defined MCP because the **executable gate was off**, so only the **MCP trust model** applied
> (direct ⇒ auto-trust). The two gates are orthogonal.

**Enable the gate → a DIRECT self-defined MCP is now gated (verified).** Adding `executables: {}` to
`consumer`'s `apm.yml` and re-installing prompts interactively:

```text
1 package(s) declare executable primitives:
  …\execpkg#0.3.0 (direct dependency)
    1 MCP server(s)
  These will execute code on your machine when triggered by
  your IDE or by 'apm run'.
  Trust …\execpkg? [y/N]:            # <- default N (secure by default)
```

**Decline (N) → parked, install still succeeds (verified):**

```text
  [i] 1 package(s) left parked. Their executables will not run until trusted.
  [i] Deploy later: apm approve …\execpkg (then re-run apm install)
       | Why parked?: apm policy explain …\execpkg
# exit=0
```

> **Trust ladder (docs) — deny-wins, first-match-wins:** `1 org deny_all/deny → denied (ceiling)` ·
> `2 user deny` · `3 project deny` · `4 project allow` · `5 user allow` ·
> `6 org recommend → allowed (overridable)` · `7 (no match) → gated pending approval`. In CI
> (`CI=true`/`APM_NON_INTERACTIVE=1`/non-TTY), unapproved executables are **parked** (no prompt) and
> the install prints the remedy — it does **not** fail. A **required-but-untrusted** executable is the
> case that hard-fails, via the `apm audit` signal `required-executable-untrusted`.

**Approve → trusted, persisted to `apm.yml` (verified).** `apm approve` keys on the **package name**,
not the path (see pitfall):

```text
apm approve checkout-review-tools
  Approved checkout-review-tools#0.3.0: 1 MCP server(s)
  [i] Updated apm.yml executables block (1 approved).
# exit=0

apm approve --list
  [i] 1 package(s) with executables (1 allowed type(s), 0 blocked type(s)).
    checkout-review-tools#0.3.0: mcp[+:project-allow]     # <- deciding layer flipped: gate-disabled -> project-allow
```

```yaml
# apm.yml after approval — the committed, shareable trust decision:
executables:
  allow:
    checkout-review-tools#0.3.0:
      mcp: true
```

**Command surface (verified via `--help` + docs):**
- `apm approve [PKG…]` — `--pending` (list unapproved), `--all`, `--recommended` (org
  `executables.recommend` set), `--list` (fleet-level effective decision + deciding layer),
  `--user` (write to `~/.apm/config.json` instead of `apm.yml`). `apm approve --pending` verified:
  `1 package(s) with unapproved executables:  checkout-review-tools#0.3.0: 1 MCP server(s)`.
- `apm deny PKG…` — `--user`; denying a not-yet-installed package is allowed (pre-emptive block).
- `apm policy explain <pkg>` — per-package deciding layer + shadowed layers (subcommand of
  `apm policy`). Fleet drift surfaces via `apm doctor`.
- **Store (docs):** `executables.allow`/`.deny` keyed by `owner/repo#version` (or version-blind
  `owner/repo`) with per-type booleans (`hooks`/`bin`/`mcp`/`canvas`). Personal store: same shape in
  `~/.apm/config.json`. Lockfile records per-dep `exec_status` (`deployed`,
  `gated_pending_approval`, `denied`, `absent`). **No `enforce` runtime, no signing, no content-hash
  binding this release** — an org `executables.enforce` degrades to `recommend`.

---

## S5 — Install-time gates, NOT runtime sandboxing (pin the boundary) · docs

The chapter's title promise — *"without confusing them with runtime sandboxing"* — is nailed by the
official threat model. **What APM defends:** reproducibility, integrity, provenance, and pre-deploy
content safety of files flowing *git source → `apm install` → project tree → harness*. **What APM
explicitly does NOT do:**

- **No runtime component / no background process** — `apm install`/`compile` run, then the process
  **exits**. It does not run alongside your app, read app data, or phone home.
- **Does NOT sandbox MCP servers at runtime.** The MCP trust model gates **whether a server is
  *configured*** at install time; once configured, what that server does at runtime is outside APM.
- **No arbitrary code execution by default** (exceptions are explicit opt-ins: lifecycle scripts
  behind `apm lifecycle trust`; experimental canvas extensions behind the executable gate).
- **No package signing, no SLSA provenance.** `content_hash` detects *corruption/tampering* of
  fetched bytes, not publisher identity. Describe it as **"dependency governance,"** not
  "supply-chain signing/attestation." (`apm lock export` emits CycloneDX/SPDX **inventory**, not a
  signed attestation.)

> **Author framing:** APM moves the checkpoint *earlier* (to install) precisely because there is no
> runtime checkpoint to rely on. It is a **gate**, not a **guard**. Over-selling it as a sandbox is
> the exact confusion the chapter must dispel.

---

## Meridian beat (Ch8) — how to stage it faithfully

Story beat (from the running example): *"transitive MCP sneaks in."* Stage it as the **verified
self-defined transitive block** above, mapped onto Meridian:

- Meridian adds an internal review pack (`checkout-review-pack`, our `pkgA`) that itself depends on a
  tools package (`checkout-review-tools`, our `execpkg`) declaring a **self-defined** MCP server.
- `apm install` **withholds** the transitive MCP with the real `[!]` message; the install still
  succeeds. Security can now *see* the tool because the fix is to **re-declare it in `apm.yml`**
  (making the trust boundary a reviewed manifest line) — resolving the Ch1 pain *"Security cannot
  answer which MCP servers are installed."*
- Advance Meridian to **v0.3.x**. Use the **corrected** lockfile MCP shape (`mcp_servers:` flat list
  + `mcp_configs:` keyed by server name). Mark the **private** `meridian-finance/*` dep and any
  **registry** MCP (`io.github.github/github-mcp-server`) `SKIPPED-needs-network`.

---

## When to use / pitfalls

- **Use `apm audit` on-demand**, but rely on the **built-in install scan** for baseline safety — you
  don't have to call `audit` to be protected against Critical Unicode.
- **Use `apm audit --ci` (not bare `audit`) as the gate.** Bare `audit` treats drift/hash-mismatch as
  **advisory (exit 0)**; only `--ci` fails (exit 1). Wiring bare `audit` into CI will silently pass a
  tampered file.
- **`--frozen` (Ch6) ≠ `apm audit` (Ch8).** `--frozen` is *structural presence* (manifest vs lock);
  content integrity is `apm audit`. Don't market `--frozen` as tamper detection.
- **`--strip` doesn't fix the source.** It cleans deployed copies; the next `install` restores the
  tainted bytes. Fix upstream / pin a clean commit for a durable fix.
- **Transitive MCP block is a *withhold*, not a build break.** Exit 0. If a reader expects a red CI
  failure, they'll be surprised; the signal is the `[!]` line + the missing MCP config.
- **Executable gate is OFF until you opt in.** Merely depending on a package with hooks/`bin`/canvas
  does **not** gate it unless you add an `executables:` block (or an org policy does). Say so plainly.
- **`apm approve` keys on the package *name*, not the local path** — even though the parked-install
  remedy prints the path. `apm approve <path>` prints `… not found in installed packages` **and still
  exits 0** (it silently no-ops). Approve with `owner/repo` / the package name (`checkout-review-tools`).
- **`--force` bypasses the Critical-Unicode block.** Treat it as break-glass; note it in prose.

---

## Caveats & flags (for the author + verifier)

1. **Hidden-Unicode exit codes: Critical=1, Warning-only=2, clean/info/strip/dry-run=0.** (`--ci`
   mode: 0 pass / 1 any failure.) Correct the Ch7 "exit 2" simplification.
2. **Two orthogonal trust gates.** MCP trust model (depth-based, always on) vs Executable Trust Gate
   (kind-based, opt-in). The self-defined MCP sits in *both* — which is why the *same* server was
   auto-trusted (gate off) yet prompt-gated (gate on). Do not merge them into one story.
3. **Transitive-MCP block message + exit (verified):** `[!] Transitive package '<pkg>' declares
   self-defined MCP server '<name>' (registry: false). Re-declare it in your apm.yml or use
   --trust-transitive-mcp.` → **exit 0**, MCP withheld. Flag `--trust-transitive-mcp` help:
   *"Trust self-defined MCP servers from transitive packages (skip re-declaration requirement)."*
4. **Lockfile MCP shape corrected** (`mcp_servers:` flat name list; `mcp_configs:` keyed by server
   name with `name/transport/command|args|url/registry`). Local deps: `_local/<dir>` + `source: local`
   + `local_path`, no commit/hash. This supersedes the Ch6 "UNVERIFIED" note and the running example.
5. **Executable gate is opt-in; default = parked-not-denied.** In CI it parks silently and prints the
   remedy (install does **not** fail); only `required-executable-untrusted` hard-fails.
6. **`apm approve` path-vs-name quirk** (caveat above) — reproduce with the package name.
7. **Install-time, not runtime.** No sandbox, no signing, no SLSA. Frame as *dependency governance*.
8. **Benign noise:** every `apm install`/`apm mcp install` auto-adds `apm_modules/` to `.gitignore`;
   MCP config for inactive targets is skipped (`[i] Skipped MCP config for claude …`). Not errors.
9. **Timing:** the long "321.2s" install in the transcript is **wall-clock waiting on my `[y/N]`
   answer**, not APM latency — do not cite it. All non-interactive runs were sub-second (local).

---

## For the `code-verifier`

- **Flagship (deterministic, offline — EXPECTED PASS):** write a file with `U+202E` + `U+200B`
  (verify bytes `e280ae`, `e2808b`), then `apm audit --file <f>` → **exit 1** (Critical present);
  a `U+200B`-only file → **exit 2**; `apm audit --file <f> --strip` → exit 0 + re-audit clean.
- **Tamper (deterministic, offline — EXPECTED PASS):** local-only project (`includes:` one
  instruction) → `apm install` → append a line to a deployed file → `apm audit` reports **drift, exit
  0**; `apm audit --ci` fails `content-integrity`+`drift`, **exit 1**, `expected=…/actual=…`.
- **Transitive MCP block (deterministic, offline — EXPECTED PASS):** `execpkg` (self-defined MCP,
  `registry: false`) ← `pkgA` depends on it ← fresh consumer `apm install <pkgA>` → the `[!]`
  transitive message, **exit 0**, **no** `mcp_servers`/`.vscode/mcp.json`. Then
  `apm install --trust-transitive-mcp` configures it.
- **Executable gate (deterministic, offline — EXPECTED PASS):** direct-dep consumer, add
  `executables: {}` → `apm install` prompts `[y/N]`; **decline** → parked, exit 0; `apm approve
  <name>` → `executables.allow.<name>.mcp: true` in `apm.yml`; `apm approve --list` → `mcp[+:project-allow]`.
  (Interactive prompt: feed `N` then approve non-interactively, or pre-commit the `executables.allow`.)
- **`SKIPPED-needs-network`:** the private `meridian-finance/checkout-review-pack` dep and any
  **registry**-referenced transitive MCP (`io.github.github/github-mcp-server`). Verify the mechanism
  via the **self-defined** path above; do **not** assert the registry entry's exact YAML/message.
- **Assert on messages, not the whole-file SHA / `generated_at`** (those vary). Assert exit codes and
  the presence of the quoted `[!]`/`content-integrity`/`Approved …` lines.

---

## Commands run (this session, apm v0.23.1, exclusive terminal)

```text
apm --version                                             # 0.23.1
apm --help ; apm approve --help ; apm deny --help ; apm mcp --help ; apm mcp install --help
apm install --help                                        # -> --trust-transitive-mcp, --force, --allow-insecure[-host], --audit
# Hidden-Unicode (scratch: crafted files with U+202E / U+200B):
apm audit --file .\checkout-review.prompt.md              # Critical -> exit 1
apm audit --file .\warn-only.md                           # Warning-only -> exit 2
apm audit --file .\checkout-review.strip.md --strip --dry-run   # preview, exit 0, file unchanged
apm audit --file .\checkout-review.strip.md --strip             # Cleaned, exit 0
apm audit --file .\checkout-review.strip.md               # clean, exit 0
# Tamper (scratch: proj = local-only Meridian v0.3.0):
apm install --target copilot,claude,cursor               # local deploy + local_deployed_file_hashes
apm audit                                                 # drift advisory -> exit 0
apm audit --ci                                            # content-integrity+drift fail -> exit 1
# Transitive self-defined MCP (execpkg -> pkgA -> consumer2):
apm install <execpkg> --target copilot                   # DIRECT: auto-trusted
apm install <pkgA>    --target copilot                   # TRANSITIVE: withheld, [!] message, exit 0
apm install --trust-transitive-mcp --target copilot      # opt-in: configured
# Executable Trust Gate (consumer, executables:{}):
apm approve --list ; apm approve --pending               # gate-disabled state; 1 pkg w/ executables
apm install --target copilot                             # prompts [y/N]; declined -> parked, exit 0
apm approve checkout-review-tools ; apm approve --list   # approved -> project-allow; apm.yml executables.allow
# Docs cross-checked (authoritative wording + exit-code table):
#   microsoft.github.io/apm/enterprise/security/  ·  /reference/cli/audit/  ·  /reference/cli/approve/
```

**Artifact:** `content/research/08-security-by-default-reference.md` (this file).
**Verified scratch tree:** `%TEMP%\apm-ch08\` (`proj`, `execpkg`, `pkgA`, `consumer`, `consumer2`,
plus the crafted hidden-Unicode files).
