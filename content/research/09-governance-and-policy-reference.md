# Chapter 9 — Governance & Policy · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 9 is where the four-properties frame reaches **governance** — APM's third
> promise, *"governed by policy."* It answers a different question than Chapter 8: not *"is this
> install safe?"* but *"is this install **allowed here**?"* This reference proves, empirically, the
> **`apm-policy.yml` schema apm actually accepts at v0.23.1**, the **`apm policy` command surface**,
> the **install-time + CI audit enforcement points**, the **warn → block exit-code story** (run on
> real violating projects), the **bypass contract**, and **tighten-only inheritance**. The crux —
> the running example's policy shape — is **corrected against the live CLI**: the single load-bearing
> bug (a top-level `targets:` key that apm **silently ignores**) is fixed to `compilation.target.allow`.
> **Concept it implements (Ch9 theory):** **governance** — anchors **Concept 1–4** in
> [`09-governance-and-policy-theory.md`](09-governance-and-policy-theory.md).
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`, confirmed at session start).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dir (outside repo):**
> `%TEMP%\apm-ch09` with sub-projects: `consumer` (no deps — clean baseline for schema-parse +
> required/target/manifest tests), `pinned` (public `microsoft/apm-sample-package#main` = an
> **unpinned** dep, for the `require_pinned_constraint` story), `mcp` (a **self-defined** inline MCP,
> for `mcp.self_defined` / `mcp.transport`).
> **Network:** available. The `require_pinned_constraint` and MCP-lockfile demos install **one public
> package** (`microsoft/apm-sample-package`, no tokens). The `required-packages`, `manifest`, target,
> schema-parse, bypass, and inheritance findings are **fully offline**. Anything touching a **private
> repo, a registry MCP, or org-remote policy discovery** is marked **`SKIPPED-needs-network`**.
> **Preview flag:** the docs mark the policy **engine** *early preview* — "schema, inheritance, and
> discovery ship today; enforcement semantics may change between minor versions … Pin to a specific
> APM version before relying on it as a production gate"
> ([Policy reference](https://microsoft.github.io/apm/enterprise/policy-reference/)). Every claim
> below is pinned to **v0.23.1**.

---

## Theory anchors (Chapter 9 — Governance & policy)

| Ch9 concept | What it establishes | Confirmed here by |
|---|---|---|
| **C1 — Security vs. governance** | Ch8 = intrinsic "is it safe?"; Ch9 = org-authored "is it allowed here?". Same install gate, different authority. | The schema has **no runtime fields**; every accepted key governs *what installs*. `apm-policy.yml` is a *separate* org contract from the built-in scanners. |
| **C2 — Install-time enforcement (+ CI audit gate)** | Policy fires **pre-disk** on `apm install` and again as a required **CI check** via `apm audit --ci --policy`. | `apm audit --ci --policy <file>` run against real violations: **warn → exit 0**, **block → exit 1**; baseline (8–9 checks) runs independently. Install-gate/`--no-policy` semantics confirmed from `--help` + docs. |
| **C3 — Tighten-only inheritance (ent → org → repo)** | Children can only *tighten*; policy is discovered from the git remote. | `extends_chain` recorded; child `enforcement` escalates. **Local-file `extends:` does NOT merge a parent** (verified); real merge needs `org`/`owner/repo`/`https` → `SKIPPED-needs-network`. Merge table from docs. |
| **C4 — `warn` → `block` rollout** | Change management, not a toggle: warn = measure, block = fail-closed. | Same violation, two modes: `enforcement: warn` prints the finding as `[+] passed` and exits **0**; `enforcement: block` prints `[x] … failed` and exits **1**. Verified on 3 independent rules. |

> **Frame note.** Ch8's gate and Ch9's gate are the **same pre-disk seam** seen from two angles.
> Ch8's checks are *intrinsic* (ship with the CLI); Ch9's are *declared* by the org in `apm-policy.yml`.
> The vocabulary must stay crisp: **security = built-in integrity; governance = org allow/deny contract.**

---

## Command surface (v0.23.1) — confirmed via `--help`

| Command / flag | Job | Notes (confirmed) |
|---|---|---|
| `apm policy status` | Show policy posture (discovery, cache, effective rules) | Flags: `--policy-source TEXT` (`org` \| `owner/repo` \| `https://…` \| **local path**), `--no-cache`, `--json` / `-o [table\|json]`, `--check`. **Always exits 0** unless `--check` (then exit 1 when `outcome != found`). Table row `Effective rules`; JSON has `rule_counts` + `extends_chain`. |
| `apm policy explain <PACKAGE>` | Explain the effective **executable-trust** decision for an installed package | Takes a `PACKAGE` arg only; this is the **Chapter 8** executable-trust surface (`apm approve`/`deny`), **not** the `apm-policy.yml` gate. Reuse Ch8's write-up; do not re-teach it here. |
| `apm audit --ci` | CI gate: 8 baseline lockfile/integrity checks | Auto-discovers org policy from the git remote when `--policy` is omitted. Exit 0 clean / 1 on any failure. |
| `apm audit --ci --policy TEXT` | CI gate **+ the ~20 policy checks** | `--policy` = `org` \| `owner/repo` \| `https://…` \| **local path**. Flag is tagged **`[experimental]`**. Also `--no-cache`, `--no-policy`, `-f sarif\|json\|markdown`, `--no-fail-fast`. |
| `apm install` | Install; runs the policy **preflight gate** (resolve → gate → write) | **No `--policy` flag** — discovery is automatic from the git remote (confirmed: not in `--help`; docs say the override "is audit-only today … not yet wired through `apm install`"). |
| `apm install --no-policy` | Break-glass: skip org policy for one invocation | `--help`: *"Skip org policy enforcement for this invocation. **Does NOT bypass `apm audit --ci`.**"* |

> There is **no** `apm policy check`, `apm policy diagnose`, or `apm policy show` at v0.23.1 — only
> `status` and `explain`. (`--check` is a *flag* on `apm policy status`.)

---

## The CONFIRMED `apm-policy.yml` schema (v0.23.1)

Every top-level key below was accepted by `apm policy status --policy-source` (`outcome: found`) and/or
appeared as a wired check in `apm audit --ci --policy`. Field names come straight from the schema —
**do not invent others; unknown keys are silently ignored** (see the `targets:` trap below).

```yaml
name: ""                    # display name (audit output)
version: ""                 # informational; not used for resolution
extends: null               # "org" | "<owner>/<repo>" | "https://..."   (NOT a local path — see C3)
enforcement: warn           # off | warn | block
fetch_failure: warn         # warn | block  (org-side: posture when policy can't be fetched)
cache:
  ttl: 3600                 # seconds; cache lives in apm_modules/.policy-cache/

dependencies:
  allow: null               # null = no opinion · [] = allow NOTHING · [globs] = only these
  deny: []                  # deny beats allow
  require: []               # packages every repo must declare (supports "#v1.2.3" pins)
  require_resolution: project-wins   # project-wins | policy-wins | block
  max_depth: 50             # max transitive dependency depth
  require_pinned_constraint: false   # true = ban unbounded refs (bare branch / wildcard / open range)

mcp:
  allow: null
  deny: []
  transport:
    allow: null             # subset of: stdio | sse | http | streamable-http
  self_defined: warn        # allow | warn | deny  (inline MCPs declared in apm.yml)
  trust_transitive: false   # PARSED BUT NOT ENFORCED — see the caveat below

compilation:                # <-- target rules live HERE (not a top-level `targets:` key)
  target:
    allow: null             # subset of: claude | copilot | cursor | opencode | codex | gemini | windsurf | kiro | agent-skills
    enforce: null           # a single target that MUST be present in the resolved list
  strategy:
    enforce: null           # distributed | single-file
  source_attribution: false

manifest:
  required_fields: []       # fields that must be present + non-empty in every apm.yml
  scripts: allow            # allow | deny
  content_types: null       # {allow: [...]}  (parsed; historically not enforced)
  require_explicit_includes: false

unmanaged_files:
  action: ignore            # ignore | warn | deny
  directories: []           # dirs to scan (defaults to the governance dirs)
  exclude: []               # globs to suppress

registry_source:
  require: []               # registry names every dep must use
  allow_non_registry: true  # false = block git/local sources

security:
  audit: {}                 # on_install, fail_on_drift, external scanners
  integrity: {}             # require_hashes

executables: {}             # deny_all, deny, require, recommend, enforce (Ch8 surface; enforce degrades to recommend)
```

**Allow-list semantics (important):** `null` = *no opinion* (allow anything not denied); `[]` = *allow
nothing*; a populated list = *only these*. In `apm policy status --json`, an unset list shows a
`rule_count` of **`-1`** (the sentinel for "no rule"); a populated list shows its length. This sentinel
is what proves the `targets:` correction below.

**Pattern glob rules:** `*` = one path segment; `**` = any depth; `deny` is evaluated first and wins.

---

## DIFF: running-example assumed shape → CONFIRMED v0.23.1 schema

The running example's Chapter 9 policy (`.source-docs/v2/running-example.md`) is **almost entirely
correct** — but it has one silent, load-bearing bug, plus a couple of nuances the author must state.

| Running-example field | Verdict (v0.23.1) | Correction / note |
|---|---|---|
| `enforcement: warn` / `block` | ✅ **Correct** | Also `off`. Top-level, single dial. |
| `dependencies.allow` / `deny` / `require` | ✅ **Correct** | `require` supports `#version` pins (e.g. `…/meridian-standards#v1.0.0`). |
| `dependencies.require_pinned_constraint: true` | ✅ **Correct** | Verified to fire on a bare-branch dep (below). |
| `mcp.allow` / `mcp.deny` | ✅ **Correct** | Glob patterns on server names. |
| `mcp.transport.allow: [http, stdio]` | ✅ **Correct** | Verified to fire (a `stdio` server fails `transport.allow: [http]`). |
| `mcp.self_defined: warn` → `deny` | ✅ **Correct** | Values `allow \| warn \| deny`. Verified to fire on an inline MCP. |
| `manifest.required_fields` / `manifest.scripts: allow` | ✅ **Correct** | Parsed and wired (`required-manifest-fields`, `scripts-policy`). |
| `unmanaged_files.action: warn` → `deny` | ✅ **Correct** | Values `ignore \| warn \| deny`. |
| **`targets:` (top-level) `allow: [copilot, claude, cursor]`** | ❌ **WRONG — silently ignored** | **Real key is `compilation.target.allow`.** With top-level `targets:`, `apm policy status` reports `compilation_targets_allowed: -1` (no rule); with `compilation.target.allow`, it reports `3`. **No error is raised** — the mistake is invisible unless you inspect `apm policy status`. |

**Proof (verbatim `apm policy status --json`, same three target values, two keys):**

```text
# running-example shape:  targets: { allow: [copilot, claude, cursor] }
"compilation_targets_allowed": -1        # <- IGNORED (no rule registered)

# corrected shape:        compilation: { target: { allow: [copilot, claude, cursor] } }
"compilation_targets_allowed": 3         # <- rule registered
```

**Two nuances to teach honestly:**
1. Even with the correct key, the **`compilation-target` audit check needs a *resolved* target.** On a
   static manifest that only *lists candidate* `targets:` (e.g. `[claude, cursor, vscode]`), `apm audit
   --ci --policy` reports **"No compilation target set in manifest"** and **passes**. The rule bites at
   `apm install` / `apm compile` time, against the target actually being compiled (docs: "evaluated
   post-targets phase, so CLI overrides are honoured"). Install-time policy uses **org-remote
   discovery** → `SKIPPED-needs-network`. So `compilation.target` is the *correct* key but a *weak*
   choice for an audit-gate demo; lead with `dependencies.*` / `mcp.*` / `require_pinned_constraint`.
2. The running example labels the file a **repo-local pilot "before turning it into an org policy."**
   Confirmed framing for v0.23.1: a repo-local file is **authored and tested** with
   `apm policy status --policy-source ./apm-policy.yml` and `apm audit --ci --policy ./apm-policy.yml`,
   then **landed in `<org>/.github/apm-policy.yml`** to become authoritative. It is **not** a
   tighten-only *child* of a local parent — `extends:` does not accept local paths (see C3). Treat the
   pilot as *"test locally, publish to the org repo,"* not *"local child extends local org."*

The corrected before/after pair is committed and validated:
[`backend/examples/ch09/apm-policy.warn.yml`](../../backend/examples/ch09/apm-policy.warn.yml) ·
[`backend/examples/ch09/apm-policy.block.yml`](../../backend/examples/ch09/apm-policy.block.yml).

---

## C1 — Security vs. governance: the schema is install-time-only

Every accepted key governs **what may be installed / compiled** — sources, MCP servers + transports,
compilation targets, manifest shape, unmanaged files, registries. There are **no fields for runtime
permissions or agent sandboxing** ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)).
That is the machine-checkable form of Concept 1: policy answers *"is it allowed here?"* at the same
pre-disk gate where Ch8's intrinsic scanners answer *"is it safe?"* — different authority, same seam.
Load-bearing distinction to protect (Chapter 1 + README): **`apm-policy.yml` governs what installs; the
agent harness governs what runs. The two planes do not overlap.**

---

## C2 — Enforcement points & exit codes (verified on real violations)

### The two gates share one rule set
- **Install-time preflight** — `apm install` resolves the tree, runs the policy gate, *then* writes.
  A `block` violation aborts with exit 1 and **nothing reaches disk**. No `--policy` flag; discovery is
  automatic from the git remote (org-remote → `SKIPPED-needs-network`).
- **CI audit gate** — `apm audit --ci --policy org` runs the **same policy checks + 8 baseline checks**
  and emits SARIF for Code Scanning. This is the branch-protection gate.

### Check families (from `apm audit --ci --policy`, v0.23.1)
- **Baseline (always with `--ci`, 8 checks + a drift replay):** `lockfile-exists`, `ref-consistency`,
  `deployed-files-present`, `no-orphaned-packages`, `skill-subset-consistency`, `config-consistency`,
  `content-integrity`, `includes-consent`, plus a `drift` replay. **These run regardless of
  `enforcement` and fail the audit on their own** (they are *not* governed by the policy's warn/block
  dial). *Author trap:* a project with a declared dep but no lockfile fails `lockfile-exists` (exit 1)
  even under `enforcement: warn` — isolate policy demos from baseline noise.
- **Policy (added by `--policy`, ~20 checks):** `dependency-allowlist`, `dependency-denylist`,
  `required-packages`, `required-packages-deployed`, `required-executable-untrusted`,
  `required-package-version`, `transitive-depth`, `dependency-pinned-constraint`, `registry-source`,
  `mcp-allowlist`, `mcp-denylist`, `mcp-transport`, `mcp-self-defined`, `compilation-target`,
  `compilation-strategy`, `source-attribution`, `required-manifest-fields`, `explicit-includes`,
  `scripts-policy`, `unmanaged-files`. **Only checks relevant to the declared rules *and* present
  artifacts run** — the total count varies (observed 4 → 22 depending on what the project declares).

### warn → block, verified (three independent rules)

Same violating project, two policies differing only in `enforcement`. In **warn** the violation prints
but is rendered `[+]` and the run **exits 0**; in **block** it prints `[x]` and **exits 1**.

| Rule / check | Violation used | `warn` result | `block` result |
|---|---|---|---|
| `required-packages` | policy `dependencies.require: [meridian-finance/meridian-standards]`; repo doesn't declare it (offline) | `[+] required-packages … (enforcement: warn)` → **exit 0** | `[x] 1 of 4 check(s) failed` → **exit 1** |
| `dependency-pinned-constraint` | `require_pinned_constraint: true`; repo has `microsoft/apm-sample-package#main` (bare branch) | `[+] … 1 dependency(ies) use unbounded …` → **exit 0** | `[x] 1 of 18 check(s) failed` → **exit 1** |
| `mcp-self-defined` | `mcp.self_defined: deny`; repo has an inline self-defined stdio MCP | `[+] … 1 self-defined MCP server(s)` → **exit 0** | `[x] 1 of 22 check(s) failed` → **exit 1** |

Also verified: **`mcp.transport.allow: [http]`** against a `stdio` server → `mcp-transport` fails →
**exit 1** under block. The `dependency-pinned-constraint` detail line is quotable:
`microsoft/apm-sample-package: bare branch 'main' tracks a moving tip`.

**Verbatim contrast (the `required-packages` pair):**
```text
# enforcement: warn
│ [+] │ required-packages │ 1 required package(s) missing from manifest (enforcement: warn) │
[*] All 4 check(s) passed          # exit 0

# enforcement: block
│     │ required-packages │ 1 required package(s) missing from manifest │
[x] 1 of 4 check(s) failed         # exit 1
```

**Implements C2 + C4:** `warn` is the *measurement* mode (exit 0, violation visible in the table /
SARIF); `block` is the *fail-closed* mode (exit 1). The dial is the **top-level `enforcement`** field —
uniform across rules (the only per-rule modes are `mcp.self_defined` and `unmanaged_files.action`, which
have their own `allow/warn/deny` values but still surface through the top-level dial for pass/fail).

---

## C2 (cont.) — the bypass / non-bypass contract (verified)

| Bypass | Effect (v0.23.1) | Verified |
|---|---|---|
| `apm audit --ci --no-policy` | Skip policy discovery/enforcement; the **8 baseline checks still run** | ✅ clean baseline → **exit 0** (9 checks pass, policy skipped) |
| `apm install --no-policy` | Skip org policy for that install; **does NOT bypass `apm audit --ci`** (loud, per-invocation warning) | ✅ from `--help` + docs; org-remote firing = `SKIPPED-needs-network` |
| `APM_POLICY_DISABLE=1` | Env-var equivalent of `--no-policy` for **auto-discovered** policy | ✅ from docs |
| **explicit `--policy <src>` beats both bypasses** | An explicitly-passed policy source is **authoritative** and is *not* skipped by `--no-policy` / `APM_POLICY_DISABLE=1` | ✅ **verified**: `APM_POLICY_DISABLE=1 apm audit --ci --policy ./block.yml` **still enforced** → **exit 1** |
| `APM_POLICY` | **Reserved** for a future override; **not** equivalent to `APM_POLICY_DISABLE` | ✅ docs |

> **Author/verifier caveat — a real gotcha.** The docs say `APM_POLICY_DISABLE=1` "skips all 20 policy
> checks when `apm audit --ci` runs." That is true for **auto-discovered** policy. It is **NOT** true
> when you pass `--policy <src>` explicitly — the explicit source wins and the gate still fires (I saw
> exit 1 with the env var set). So the honest rule is: **bypass flags suppress the *auto-discovered*
> org policy only; an explicit `--policy` is always enforced.** Every bypass is single-invocation, is
> not persisted, and does **not** change CI behaviour — the baseline lockfile checks remain
> non-bypassable.

---

## C3 — Tighten-only inheritance (`extends:`)

- **`extends:` accepts `org` | `owner/repo` | `https://…`** — the parent is fetched with the same
  fetcher as direct discovery. Chain depth ≤ **5**; cycles rejected; **cross-host `extends:` refused**
  (credential-leak mitigation) ([Policy reference](https://microsoft.github.io/apm/enterprise/policy-reference/)).
- **VERIFIED limitation — a local-file `extends:` does NOT merge the parent.** With
  `extends: ./parent-org-policy.yml`, `apm policy status` *records* the ref
  (`Extends chain: ./parent-org-policy.yml`) but the **parent's rules are not merged**: the child's
  `deny` count stayed **1** (its own entry) instead of the **2** a union with the parent would produce;
  the effective policy was the child's own rules alone (its `enforcement: block` applied). So a repo-local
  pilot **cannot** inherit a local parent — inheritance requires an `org`/`owner/repo`/`https` ref.
  Live multi-level merge is therefore **`SKIPPED-needs-network`**.
- **Tighten-only merge table (documented; the merge itself is org-remote → `SKIPPED-needs-network`):**

| Field | Merge rule |
|---|---|
| `enforcement` | escalates `off < warn < block` (max) |
| allow lists (`dependencies.allow`, `mcp.allow`, `mcp.transport.allow`, `compilation.target.allow`) | **intersection** (child narrows) |
| deny lists (`dependencies.deny`, `mcp.deny`) | **union** (child adds) |
| `dependencies.require` | **union** |
| `require_resolution` | escalates `project-wins < policy-wins < block` |
| `max_depth`, `cache.ttl` | `min(parent, child)` |
| `require_pinned_constraint` | logical **OR** |
| `mcp.self_defined` | escalates `allow < warn < deny` |
| `manifest.scripts` | escalates `allow < deny` |
| `unmanaged_files.action` | escalates `ignore < warn < deny` |
| `unmanaged_files.exclude` | **union** (additive; a child cannot clear it) |
| `source_attribution` | parent **OR** child |
| `mcp.trust_transitive` | parent **AND** child (both must allow) |

- **Discovery (org-remote, reinforces Chapter 1):** auto-discovered from the project's git remote,
  searching candidate repos **`.github` → `.apm` → `_apm`** (first found wins; ADO tries only `_apm`),
  cached ~1h. **Verified negative:** with no git remote, `apm audit --ci` prints *"Could not determine
  org from git remote; enforcement skipped"* and proceeds (fail-open) — so local scratch projects skip
  auto-discovery, which is why every enforcement demo above used an explicit `--policy <file>`. Live
  org-remote discovery = **`SKIPPED-needs-network`**.
- **Exceptions flow upward only:** a repo cannot waive a rule for itself; you relax at the parent
  (narrow a `deny`, add to `allow`). No first-class waiver field.

---

## C4 — `warn` → `block` rollout (change management)

The mechanism is proven above (C2): `enforcement` is the dial, `warn` exits 0 with the finding visible,
`block` exits 1. The rollout sequence the author teaches — **author in `warn` → read SARIF/telemetry →
remediate → flip to `block`** — maps directly onto these exit codes. Two verified specifics:
- **`warn` is quiet in a green/red CI check** — the audit **exits 0**, so the check is *green*; the
  violations live in the table and in SARIF/Code Scanning, not in the exit code. Teams must watch Code
  Scanning during the warn phase (matches the theory's "warn-mode is quiet in CI" trap).
- **No per-rule `enforcement` knob** — the top-level dial is uniform. To block one rule while others
  warn, **stage rules** (land in warn, clean, then flip the file) or **split via `extends:`** (a strict
  child escalates `warn → block` for its scope). `mcp.self_defined` and `unmanaged_files.action` are the
  *only* fields with their own `allow/warn/deny` sub-mode.

---

## Verified minimal policies the author can show (guaranteed green)

The smallest pair that demonstrates warn → block end to end, **fully verified** on the `pinned` project
(`microsoft/apm-sample-package#main`, an unpinned dep). Baseline passes; only the policy check flips.

```yaml
# apm-policy.min-warn.yml  —  apm audit --ci --policy ./apm-policy.min-warn.yml  => exit 0
name: min-warn
version: "1.0.0"
enforcement: warn
dependencies:
  require_pinned_constraint: true     # verified to FLAG the bare-branch dep, but exit 0 (warn)
```

```yaml
# apm-policy.min-block.yml  —  apm audit --ci --policy ./apm-policy.min-block.yml  => exit 1
name: min-block
version: "1.0.0"
enforcement: block
dependencies:
  require_pinned_constraint: true     # same finding, now FAILS the audit (exit 1)
```

The full **corrected Meridian** before/after pair (running-example shape, `targets:` bug fixed) is at
[`backend/examples/ch09/apm-policy.warn.yml`](../../backend/examples/ch09/apm-policy.warn.yml) and
[`backend/examples/ch09/apm-policy.block.yml`](../../backend/examples/ch09/apm-policy.block.yml); both
parse (`outcome: found`) with `compilation_targets_allowed: 3`. Reproduction recipe + expected exit
codes: [`backend/examples/ch09/README.md`](../../backend/examples/ch09/README.md).

---

## When to use / pitfalls (for the author)

- **`apm-policy.yml` is an *org-remote* artifact, not a repo default.** Author/test locally with
  `apm policy status --policy-source ./file` + `apm audit --ci --policy ./file`, then publish to
  `<org>/.github/apm-policy.yml`. `apm install` has **no `--policy` flag**.
- **Wire `apm audit --ci --policy org` (not bare `audit`) into branch protection.** It is the
  authoritative gate and the *only* enforcer of audit-only rules; bare `apm install` enforces locally
  but is bypassable.
- **`targets:` at the top level is a silent no-op.** Use `compilation.target.allow`. If a reviewer sees
  a top-level `targets:` in a policy, it is doing **nothing**.
- **Don't demo `compilation.target` through `apm audit`** — it needs a resolved target and reports "No
  compilation target set in manifest" on a candidate list. Demo target rules at `apm install`/`compile`
  (org-remote → SKIPPED-needs-network) or pick a rule that fires at audit time.
- **`mcp.trust_transitive` is a trap** — it **parses but is not enforced** (see caveats). The real
  transitive-MCP gate is the **`--trust-transitive-mcp` CLI flag** (default deny), verified live in
  Chapter 8. Do not claim the policy field blocks transitive MCP.
- **Isolate policy from baseline** in every example: an MCP-only manifest (no APM package deps) fails
  `lockfile-exists` because `apm install` writes no lockfile for it — add a pinned APM dep, or the demo
  exits 1 for the wrong reason.
- **`apm policy status` never fails** (exit 0) unless you add `--check`. Use `--check` for a CI
  pre-flight that fails when the org policy is unreachable/misconfigured; use `apm audit --ci --policy`
  to gate on rule *violations*.

---

## Caveats & flags (for the author + verifier)

1. **`compilation.target.allow`, not top-level `targets:`.** The single running-example correction;
   the wrong key is *silently* ignored (`compilation_targets_allowed: -1`). Verified both ways.
2. **warn = exit 0, block = exit 1** — verified on `required-packages`, `dependency-pinned-constraint`,
   and `mcp-self-defined`; plus `mcp-transport` under block. Baseline (8–9 checks) is independent of the
   `enforcement` dial and can fail on its own.
3. **Explicit `--policy` overrides `--no-policy` and `APM_POLICY_DISABLE=1`** — verified (`env var +
   --policy ./block.yml` still exited 1). Bypasses suppress *auto-discovered* org policy only. Baseline
   checks are never bypassable.
4. **Local-file `extends:` does not merge** — verified (child deny stayed 1, not unioned to 2). Real
   inheritance needs `org` / `owner/repo` / `https`. Merge table is documented; live merge is
   **SKIPPED-needs-network**.
5. **`mcp.trust_transitive` parsed-but-not-enforced** — confirmed in docs
   ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)) and in the Ch8 reference;
   the real gate is `--trust-transitive-mcp` (default deny).
6. **`apm policy` has only `status` + `explain`** at v0.23.1 (no `check`/`diagnose`/`show`). `explain`
   is the Ch8 executable-trust surface.
7. **Preview.** The policy engine is *early preview*; schema/enforcement may change between minors. All
   claims pinned to **v0.23.1**. Re-run `backend/examples/ch09/README.md` on any CLI bump.
8. **`SKIPPED-needs-network`:** org-remote discovery + inheritance merge; install-time policy
   enforcement (no `--policy` on install); resolving the private `meridian-finance/*` package and the
   registry `io.github.github/github-mcp-server` MCP. The *rules* for these are verified; the *specific
   remote artifacts* are not fetched.

---

## Artifacts written & commands run

**Artifacts (this session):**
- `content/research/09-governance-and-policy-reference.md` (this file).
- `backend/examples/ch09/apm-policy.warn.yml` — corrected Meridian pilot (warn); validated `outcome: found`.
- `backend/examples/ch09/apm-policy.block.yml` — corrected Meridian enforce (block); validated `outcome: found`.
- `backend/examples/ch09/README.md` — reproduction recipe + expected exit codes for the `code-verifier`.

**Key commands run (v0.23.1, `%TEMP%\apm-ch09`):**
```text
apm --version                                             # 0.23.1
apm policy --help ; apm policy status --help ; apm policy explain --help
apm audit --help ; apm install --help                     # confirm --ci/--policy/--no-policy; no --policy on install
apm init -y --target copilot,claude,cursor                # consumer (targets normalized: copilot -> vscode)
apm policy status --policy-source ./pol-running-example.yml -o json   # compilation_targets_allowed: -1 (targets: ignored)
apm policy status --policy-source ./pol-compilation-target.yml -o json# compilation_targets_allowed: 1  (correct key)
apm audit --ci --policy ./pol-required-warn.yml           # exit 0 (warn)
apm audit --ci --policy ./pol-required-block.yml          # exit 1 (block)
apm install microsoft/apm-sample-package#main             # unpinned dep (pinned/ project)
apm audit --ci --policy ./pol-pin-warn.yml                # exit 0 ; ./pol-pin-block.yml => exit 1
APM_POLICY_DISABLE=1 apm audit --ci --policy ./pol-pin-block.yml      # STILL exit 1 (explicit --policy wins)
apm audit --ci --no-policy                                # exit 0 (baseline only)
apm policy status --policy-source ./child-repo-policy.yml -o json     # extends local file NOT merged (deny stays 1)
apm install --mcp local-fetch --transport stdio -- npx -y @modelcontextprotocol/server-fetch  # self-defined MCP
apm audit --ci --policy ./pol-self-warn.yml               # exit 0 ; ./pol-self-block.yml => exit 1
apm audit --ci --policy ./pol-transport-block.yml         # exit 1 (stdio not in transport.allow=[http])
apm policy status --policy-source <repo>/backend/examples/ch09/apm-policy.{warn,block}.yml -o json  # outcome=found, compilation_targets_allowed: 3
```

**Sources (official docs, v0.23.1, last updated 2026-06-30):**
[Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/) ·
[Policy reference](https://microsoft.github.io/apm/enterprise/policy-reference/) ·
[Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/) ·
[Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/) ·
[microsoft/apm README](https://github.com/microsoft/apm). Cross-refs:
[`08-security-by-default-reference.md`](08-security-by-default-reference.md) (MCP trust model,
`--trust-transitive-mcp`, executable trust / `apm policy explain`),
[`09-governance-and-policy-theory.md`](09-governance-and-policy-theory.md) (Concepts 1–4).
