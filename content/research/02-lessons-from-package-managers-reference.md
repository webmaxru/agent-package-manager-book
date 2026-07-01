# Chapter 2 — Lessons from Package Managers · APM feature reference (light)

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 2 is conceptual (the npm/pip/Cargo analogy + the *name-collision* cleanup), so
> this reference is deliberately **light** — it just confirms the **manifest / lockfile / pinning /
> git-sources** vocabulary and *names* the lifecycle-analogue commands against the *real* CLI. Deep
> dives land later: manifest → Ch4, install/restore → Ch5, lockfile → Ch6, the
> `outdated`/`update`/`audit` lifecycle → Ch7.
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`).
> **Inspected on:** 2026-07-02 (Windows). **Scratch project:** `%TEMP%\apm-ch02` (outside the repo).
> **Network:** available. Offline `--help` surfaces were captured cleanly; the **two live network
> probes** (`apm view … versions`, a pinned install) are marked **SKIPPED-shared-terminal** — the
> fleet's shared pwsh was concurrently in use by a sibling agent, which `KeyboardInterrupt`-ed every
> wide-window cold start (4 attempts). Their behaviour is documented from the CLI's own `--help`
> contract plus a **real unpinned install captured from the terminal scrollback**, and the live
> capture is deferred to Ch4/Ch5 where the manifest is authored for real.

## Theory anchors (Chapter 2)

Chapter 2's job is to make APM feel **familiar, not novel**: every idea maps to something the reader
already trusts from `npm` / `pip` / `Cargo` (`content/playbook-brief.md` §"Package-manager lessons,
made familiar"). Feature notes below link back to these four concepts (the `theory-researcher`'s
brief will live at `02-lessons-from-package-managers-theory.md`):

| Ch2 concept (the analogy) | Package-manager precedent | APM feature that implements it |
|---|---|---|
| **Manifest** — declared intent | `package.json`, `requirements.txt`, `Cargo.toml` | `apm.yml` |
| **Lockfile** — resolved reality | `package-lock.json`, `Cargo.lock`, `poetry.lock` | `apm.lock.yaml` |
| **Version pinning** — reproducibility | `^1.2.0`, `==1.4.2`, `pkg@1.0.0` | `owner/repo#<ref>` |
| **Registry** — where packages come from | npmjs.com, PyPI, crates.io | **git servers** (registry-as-git) |

The **name collision** the chapter clears up: *Microsoft APM* (this book, git-distributed, no central
registry yet) vs. *orthogonalhq/apm* (an independent Rust CLI with a real public registry at
`apm.orthg.nl`) — same three letters, different tools (`.source-docs/v2/research.md`, competitor
table). Naming a package manager after a category is exactly the npm/pip pattern; the twist is two
projects landed on `apm` at once.

---

## Feature reference

### 1. Manifest ↔ lockfile vocabulary (`apm.yml` / `apm.lock.yaml`)
- **Implements concept:** **Manifest** + **Lockfile** (the two-file split every package manager has).
- **Usage:** `apm.yml` is the **human-authored** declaration of intent (identity + typed
  `dependencies.apm` / `dependencies.mcp`); `apm.lock.yaml` is the **machine-generated** resolution
  (exact refs + content hashes). Reader's mnemonic: *manifest = what you asked for; lockfile = what
  you got.* Same relationship as `package.json` → `package-lock.json` and `Cargo.toml` → `Cargo.lock`.
- **When to use / when not:** Ch2 only needs the reader to recognise the *pair* and the *edit vs.
  derive* rule (author the manifest, commit the lockfile, never hand-edit the lockfile). Full manifest
  keys land in Ch4; lockfile internals + `--frozen` land in Ch6. Don't over-explain here.
- **Minimal example (real, captured):** a fresh project's manifest after one `apm install` grows a
  typed `apm:` dependency list — verbatim from the scratch tree (`%TEMP%\apm-ch03\apm.yml`, v0.23.1):
  ```yaml
  dependencies:
    apm:
    - microsoft/apm-sample-package   # note: written UNPINNED (bare owner/repo) -- see §2
    mcp: []
  ```

### 2. Version pinning — `owner/repo#<ref>`
- **Implements concept:** **Version pinning** → reproducibility (the `pkg@1.2.3` idea, git-native).
- **Usage:** A dependency is `owner/repo`, optionally pinned with `#<ref>` where **`<ref>` is a git
  tag, branch, or commit SHA** (e.g. `microsoft/apm-sample-package#v1.0.0` or `…#main` or `…#<sha>`).
  `apm install --help` (v0.23.1) documents the **`owner/repo` shorthand** and ref handling directly:
  `--refresh` "re-resolve all **ref pins**", `--update` fetch "**latest Git references**". Unpinned,
  APM tracks the source's **default branch**; the resolved commit is then recorded in the lockfile.
- **When to use / when not:** **Pin for anything shared or reproducible** (team repos, CI) so the
  lockfile is deterministic; leaving a dep unpinned is fine only for throwaway/local exploration.
  This is the chapter's reproducibility hook — pinning is *why* the lockfile can promise byte-for-byte.
- **Minimal example (pin syntax):**
  ```yaml
  # apm.yml -- pin a public sample package to a tag (reproducible)
  dependencies:
    apm:
      - microsoft/apm-sample-package#v1.0.0
  ```
  The **live pinned install** proving the `#<ref>` write-through to `apm.lock.yaml` is
  **SKIPPED-shared-terminal** here (deferred to Ch4/Ch5); the syntax is the documented APM convention
  and is corroborated by the `install --help` ref-pin flags above and the unpinned capture in §1.

### 3. Git sources — registry-as-git
- **Implements concept:** **Registry** (where packages live) — but git servers *are* the registry.
- **Usage:** APM resolves dependencies straight from **git hosts** — GitHub, GitLab, Azure DevOps,
  Bitbucket, Gitea, or any generic git URL (`content/playbook-brief.md`; official docs). The CLI
  confirms the transport surface: `apm install --help` (v0.23.1) exposes `--ssh` / `--https` for
  **"shorthand (owner/repo) dependencies"**, honours explicit `ssh://` / `https://` URLs, and
  `apm view --help` shows a **`https://github.com/org/repo`** form to *"Force the git path"*. No
  package needs to be published to a central index first — if it's in a git repo, it's installable.
- **When to use / when not:** Always — this is APM's distribution model. The teaching point for Ch2 is
  *conceptual reframing*: "the registry you already have is your git host," which is why APM needs no
  new hosting to get started (contrast npm/PyPI/crates.io, which are separate services).
- **Minimal example (real, captured from scrollback):** an unpinned public install resolving straight
  from GitHub (v0.23.1, `apm install microsoft/apm-sample-package --target copilot`):
  ```text
  [*] Created apm.yml
  [i] Targets set: copilot (persisted to apm.yml)
  [*] Validating 1 package...
  [+] microsoft/apm-sample-package
  [>] Installing 1 new package...
  [>] Resolving microsoft/apm-sample-package...
  ```

### 4. `apm view` — package metadata & remote versions
- **Implements concept:** **Registry / versions** — the `npm view` · `pip index versions` analogue.
- **Usage (from `apm view --help`, v0.23.1):** *"View package metadata or list remote versions."*
  - `apm view org/repo` → local metadata for an installed package.
  - `apm view org/repo versions` → **"List available remote tags and branches"** (the `versions`
    FIELD; may contact the remote).
  - `apm view https://github.com/org/repo versions` → force the git path.
  - `--registry [NAME]` → list versions **from a registry** instead of git (bare = default registry).
  This is the command that turns "which refs can I pin to?" into an answer — the natural companion to
  §2 (pinning) and §5 (`outdated`).
- **When to use / when not:** Use it to discover pinnable refs before writing `#<ref>`, or to inspect
  a dependency's metadata. Ch2 only needs to *name* it as the "versions" verb; hands-on use fits Ch4.
- **Minimal example:**
  ```bash
  apm view microsoft/apm-sample-package versions   # remote tags/branches (or registry)
  ```
  **Live output: SKIPPED-shared-terminal** (4 cold-start attempts each `KeyboardInterrupt`-ed by the
  concurrent sibling agent). Behaviour above is quoted from the CLI's own `--help`; the `versions`
  FIELD confirms **`apm view` *does* list remote versions**. Re-capture when the terminal is exclusive.

### 5. Lifecycle analogues — `apm outdated` · `apm update` · `apm audit` (name-only for Ch2)
- **Implements concept:** the **maintenance lifecycle** every package manager ships (the chapter names
  these so APM feels complete; the *worked* lifecycle is **Ch7**).
- **Usage — confirmed to exist via `--help` (v0.23.1):**
  | Command | `--help` one-liner (verbatim) | PM analogue |
  |---|---|---|
  | `apm outdated` | *"Show outdated locked dependencies"* | `npm outdated` / `pip list --outdated` |
  | `apm update` | *"Refresh APM dependencies to the latest matching refs"* | `npm update` / `pip install -U` |
  | `apm audit` | *"Scan installed packages for hidden Unicode characters"* (+ `--ci` lockfile checks) | `npm audit` / `pip-audit` |
- **When to use / when not:** Ch2 should **mention, not demonstrate** — a one-line "and yes, there's an
  `outdated`/`update`/`audit` trio, just like npm" that forward-references Ch7. `apm audit`'s scope is
  narrower/different from `npm audit` (it's a *hidden-Unicode / lockfile-integrity* scanner, not a CVE
  feed) — worth a footnote so the analogy isn't over-claimed; full treatment in Ch7/Ch8.
- **Minimal example:** none executed in Ch2 (name-only). Each `--help` was captured to
  `%TEMP%\apm-ch02\{outdated,update,audit}-help.txt`.

---

## The registry reality (a Ch2 must-say)

- **There is no central public APM registry yet.** Distribution is **git-based**; the "registry" is
  whatever git host holds the repo (`content/playbook-brief.md`; official docs). The **OpenAPM v0.1**
  spec **explicitly defers the registry HTTP API to v0.2** (`.source-docs/v2/research.md`,
  spec footnote) — so *registry-as-git* is the intended model today, not a temporary gap.
- **But the CLI already has registry *plumbing*.** `apm view … --registry [NAME]` lists versions from
  a registry when one is configured, and an interrupted cold start surfaced internal
  `apm_cli/deps/registry/…` and `publish.py` modules — i.e. the seams for a future registry exist,
  with **git tags/branches as today's default source**. Frame this as "the socket is wired; the
  central registry is a v0.2 roadmap item," not "APM has a registry."
- **Name-collision tie-in:** the *other* `apm` (orthogonalhq) *does* ship a public registry — a clean
  way for the chapter to contrast the two projects while teaching what a registry is.

## Teachable detail — the *unpinned dependency* (flag this in Ch2)

When you `apm install owner/repo` **without** a `#<ref>`, APM records the **bare shorthand** in
`apm.yml` (captured live: `- microsoft/apm-sample-package`) and tracks the source's **default
branch**. That's convenient but **not reproducible on its own** — tomorrow's `apm install` could
resolve a newer commit. This is the perfect Ch2 hook into Part III: *pinning (`#<ref>`) + the lockfile*
are what convert "works on my machine today" into "byte-for-byte, forever." (In the fleet run the
sibling's unpinned install was mid-`Resolving…` when interrupted, so no lockfile was written — a
neat, if accidental, illustration that **unpinned + no lockfile = nothing guarantees the version**.)

## npm / pip / Cargo → APM cheat-sheet (for the author's analogy table)

| You know… | …in APM |
|---|---|
| `package.json` / `requirements.txt` / `Cargo.toml` | `apm.yml` |
| `package-lock.json` / `Cargo.lock` | `apm.lock.yaml` |
| `pkg@1.2.3` version pin | `owner/repo#<ref>` (tag/branch/SHA) |
| npmjs.com / PyPI / crates.io | git host (GitHub/GitLab/Azure DevOps/Bitbucket/Gitea/URL) |
| `npm view` / `pip index versions` | `apm view <pkg> versions` |
| `npm outdated` | `apm outdated` |
| `npm update` / `pip install -U` | `apm update` |
| `npm audit` | `apm audit` (hidden-Unicode + lockfile integrity, *not* a CVE feed) |
| `npm install` (restore) | `apm install` |

---

## Caveats & surprises for the author

1. **The analogy is strong but not exact.** Two honest asymmetries to keep the chapter credible:
   (a) **registry-as-git** — no central index (yet); (b) **`apm audit` ≠ `npm audit`** — it scans for
   hidden-Unicode / lockfile drift, not CVEs. Name both so the reader trusts the mapping.
2. **Unpinned is the default write.** `apm install owner/repo` persists a *bare* entry (not a pinned
   one). The reproducibility story is opt-in via `#<ref>` + lockfile — exactly the Part III payoff.
3. **`apm view` is the "versions" verb.** Readers coming from npm will look for `npm view`; APM's is
   `apm view <pkg> versions`, and it can target a registry (`--registry`) *or* raw git.
4. **Cold-start is slow + the fleet terminal is shared.** The packaged CLI (PyInstaller) takes several
   seconds to start; in a concurrent fleet run that widens the window for cross-agent interference.
   Not a book fact — an ops note for the verifier (prefer an exclusive shell for live network probes).

## Commands run (v0.23.1; PATH refreshed per call; scratch `%TEMP%\apm-ch02`)

```powershell
apm --version                                   # -> Agent Package Manager (APM) CLI version 0.23.1
apm install --help                              # git shorthand owner/repo, --ssh/--https, ref pins, --frozen, --root(=pip/npm)
apm view --help                                 # "View package metadata or list remote versions"; `versions` FIELD; --registry
apm outdated --help                             # "Show outdated locked dependencies"
apm update  --help                              # "Refresh APM dependencies to the latest matching refs"
apm audit   --help                              # "Scan installed packages for hidden Unicode characters"; --ci
# captured from fleet scrollback (sibling scratch %TEMP%\apm-ch03):
apm install microsoft/apm-sample-package --target copilot   # real git resolution; apm.yml written UNPINNED
# SKIPPED-shared-terminal (4x KeyboardInterrupt by concurrent sibling; deferred to Ch4/Ch5):
apm view microsoft/apm-sample-package versions              # live remote tag/branch list
apm install microsoft/apm-sample-package#v1.0.0 --target copilot   # live #<ref> pin proof
```

## Sources
- Installed CLI **apm 0.23.1** — `--version` and per-command `--help` (primary, empirical; help text
  saved under `%TEMP%\apm-ch02\*.txt`).
- Real install output + generated `apm.yml` captured from the fleet's terminal scrollback and the
  sibling scratch tree (`%TEMP%\apm-ch03\apm.yml`).
- [`content/playbook-brief.md`](../playbook-brief.md) — the npm/pip/Cargo framing and name-collision.
- [`.source-docs/v2/research.md`](../../.source-docs/v2/research.md) — no-central-registry reality,
  OpenAPM v0.2 registry-API deferral, and the `orthogonalhq/apm` name collision.
- Official docs — <https://microsoft.github.io/apm/> (git sources, three files) and the Consumer ramp
  <https://microsoft.github.io/apm/consumer/>.
