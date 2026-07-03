# Chapter 11 — Enterprise at Fleet Scale · APM feature reference

> **Role:** `apm-cli-explorer` notes for the `chapter-author`.
> **Scope:** Chapter 11 is the **capstone** — it does not introduce a fifth property; it asks whether
> the book's four properties (portability, reproducibility, provenance/security, governance) hold for
> *every* repo, **enforced and operated at org scale**. The single load-bearing shift is *"can **every**
> repo install safely and predictably?"* This reference proves the **one clearly runnable enterprise
> surface** — **`apm audit --ci` as the required CI gate** (exit `0` clean / `1` on violation, re-confirmed
> live at v0.23.1) — and **documents** the rest of the fleet story that a reader/sandbox cannot execute
> without infrastructure: the **`microsoft/apm-action` workflow shape** (CI-in-anger), the **registry
> proxy / air-gapped** config knobs, and **org policy at scale** (which reuses Chapter 9's verified
> behavior). Everything is tagged **RUNNABLE** or **`SKIPPED-needs-network`**.
> **Concept it implements (Ch11 theory):** *operating APM at fleet scale* — anchors **Concepts 1–4** in
> [11-enterprise-at-fleet-scale-theory.md](11-enterprise-at-fleet-scale-theory.md).
> **Inspected `apm` CLI version:** **0.23.1** (`apm --version`, confirmed at session start).
> **`microsoft/apm-action` version:** latest **v1.10.0** (README fetched this session); pin the CI step to
> the **major tag `@v1`** (docs' recommended form).
> **Inspected on:** 2026-07-02 (Windows, **exclusive terminal**). **Scratch dir (outside repo):**
> `%TEMP%\apm-ch11` (`apm-ch11` = clean project with one **pinned** public dep
> `microsoft/apm-sample-package#v1.0.0` + committed lockfile; `apm-ch11\block-demo` = same package as an
> **unpinned** `#main` direct dep, for the exit-1 case).
> **Network:** available. The `apm audit --ci` cases install **one public package** (`microsoft/apm-sample-package`,
> **no tokens, no live pushes**). Everything touching a **private registry, an Artifactory proxy, org-remote
> policy discovery, or a live GitHub Action run** is **`SKIPPED-needs-network`** — a reader's sandbox will not have it.
> **Preview / version-awareness (three specific flags — matters here):**
> 1. `apm audit --ci --policy` is tagged **`[experimental]`** ([apm audit reference](https://microsoft.github.io/apm/reference/cli/audit/)).
> 2. the **dedicated registry** (`registries:` in `apm.yml`, a real Registry HTTP API) is **experimental**,
>    gated behind `apm experimental enable registries` — the OpenAPM registry API is **deferred to v0.2**
>    ([Registries guide](https://microsoft.github.io/apm/guides/registries/); [OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v01/)).
> 3. policy **enforcement** is early preview (carried from Chapter 9).
>    By contrast, the **registry *proxy*** (env-var driven) and the **eight baseline lockfile checks** in
>    `apm audit --ci` are **stable**.

---

## Theory anchors (Chapter 11 — operating APM at fleet scale)

| Ch11 concept | What it establishes | Confirmed / documented here by |
|---|---|---|
| **C1 — One team vs a fleet** | The question shifts from "can *this* repo install?" to "can *every* repo install safely & predictably?" — needs repeatable rollout, policy **ownership**, audit **gates**, a **registry strategy**, exception handling. | `apm audit --ci` is the org-wide *gate*; org policy lives in `<org>/.github` (Ch9, consumer-only for repos); proxy = the registry strategy; waivers = policy-file amendments. |
| **C2 — CI gating** | `apm audit --ci` as the **required, unbypassable** PR check — the install-time gate from Ch7/Ch9 re-run in CI as **defence in depth**; `microsoft/apm-action` is the turnkey path. | **RUNNABLE:** exit **0** clean (9 checks) / exit **1** on a policy violation, both re-confirmed live. Workflow shape + rulesets = **`SKIPPED-needs-network`** (documented). |
| **C3 — Registry strategy** | Route/mirror dependency traffic (proxy) and build for offline (air-gapped) on APM's git-based-today model; integrity still anchored to the lockfile. | **`SKIPPED-needs-network`:** env-var knobs captured from docs; `apm config`/`apm cache` surfaces inspected live; **proxy is env-var driven, *not* a persisted `apm config` key** (verified). |
| **C4 — Adoption as change management** | Discover → Pilot → Harden → Scale → Sustain; measured by **leading indicators** (audit pass rate, drift trend), not manifest count. | Process, not runnable CLI. The only locally runnable pieces are `apm install --dry-run` + `apm audit` (Ch5/Ch7). Rollout = Ch9's `warn → block` proven behavior, fleet-wide. |

> **Frame note.** Nothing in this chapter is a novel capability. It is Chapters 6–10 made **repeatable,
> owned, gated, and measured** across N repos. The through-line: **one gate (Ch 6/8/9), re-run in CI and
> made authoritative; dependency traffic routed and mirrored but still lockfile-verified; rolled out in
> owned, gated phases.**

---

## Enterprise surface at a glance (v0.23.1) — RUNNABLE vs SKIPPED

| Surface | Job | Status | Where verified |
|---|---|---|---|
| `apm audit --ci` | The required CI gate: 8 baseline lockfile checks + drift (+ discovered policy) | **RUNNABLE** | live this session (exit 0 clean / exit 1 block) |
| `apm audit --ci --policy <src>` | Gate + the ~20 policy checks (`[experimental]`) | **RUNNABLE** (local file); org-remote discovery **SKIPPED** | live (exit 0 warn-shape / exit 1 block); Ch9 |
| `apm config get/set/unset` | Persisted CLI config (`auto-integrate`, `temp-dir`, `mcp-registry-url`) | **RUNNABLE** | live `--help` + `config get` |
| `apm cache info/prune/clean` | Local package cache (offline/hermetic story) | **RUNNABLE** | live `cache info` + `prune --help` |
| `microsoft/apm-action@v1` | Turnkey CI step: install / pack / audit-report (SARIF) | **`SKIPPED-needs-network`** | README (v1.10.0) + enforce-in-CI docs |
| GitHub Rulesets (required check) | Make the audit job unbypassable on merge | **`SKIPPED-needs-network`** | docs |
| `PROXY_REGISTRY_*`, `HTTPS_PROXY`, air-gapped `apm pack` | Registry strategy: mirror / route / offline | **`SKIPPED-needs-network`** | registry-proxy docs; `apm config` shows these are **not** persisted keys |
| Org policy discovery + `extends:` MERGE | Fleet-wide org baseline, tighten-only inheritance | **`SKIPPED-needs-network`** | Ch9 (local `extends:` does **not** merge; org-remote merge needs infra) |

---

## Feature 1 — `apm audit --ci`: the required, unbypassable CI gate  ·  **RUNNABLE**

**Implements concept:** **C2 (CI gating)** — the *same* integrity gate from Chapter 7 and the *same*
policy gate from Chapter 9, re-run on the pull request as **defence in depth**. Enterprise value: a
developer can pass `--no-policy`, `--force`, or `APM_POLICY_DISABLE=1` **locally; CI cannot**
([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)).

**What it runs (one command):** the **eight baseline lockfile checks** (`lockfile-exists`,
`ref-consistency`, `deployed-files-present`, `no-orphaned-packages`, `skill-subset-consistency`,
`config-consistency`, `content-integrity`, `includes-consent`), the **install-replay drift check**, and —
*if* an `apm-policy.yml` is discovered from the git remote — the **org policy checks**. **Exit code `0`
clean, `1` on any violation.** The clean run shows **8 baseline + drift = 9 checks**.

**Flags confirmed for CI** ([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/) + `apm audit --help`, v0.23.1):

| Flag | Job | Enterprise note |
|---|---|---|
| `--policy <src>` | explicit policy ref: `org` \| `<owner>/<repo>` \| `https://…` \| local path | **`[experimental]`**; without it, APM auto-discovers from the git remote (like `apm install`). |
| `--no-cache` | force a fresh policy fetch | **Recommended in CI** so a cached policy file does not mask a same-day policy update. |
| `--no-policy` | skip policy discovery (baseline + drift only) | **Does not work as a bypass in CI's intent** — the org still wires the *unflagged* gate; baseline is never bypassable. |
| `--no-fail-fast` | run every check even after one fails | Use for **reports / drift sweeps**; default stops at first failure. |
| `--no-drift` | skip the install-replay | Pair with `setup-only` (no warm cache); reduces coverage — use only when CI minutes are the bottleneck. |
| `-f json` / `-f sarif` | structured output | **Markdown is NOT supported in `--ci` mode.** SARIF feeds Code Scanning. |
| `-o <path>` | write the report to a file | Format inferred from extension (`.sarif`, `.json`). |

### 1a — Clean gate → exit 0 (RE-CONFIRMED live this session)

Caption: **`apm audit --ci` on the clean scratch project (one pinned public dep + lockfile). Nine checks
pass; exit 0. The `Could not determine org…` line is benign — a scratch dir has no git remote, so
auto-discovery is skipped (fail-open). Verified on apm v0.23.1.**

```text
apm audit --ci
  [!] Could not determine org from git remote; enforcement skipped (set policy.fetch_failure_default=block in apm.yml to fail closed)
  [>] Replaying install (cache-only)...
  [+] Replayed 2 package(s)
  [>] Diffing scratch vs working tree...
  [+] No drift detected

                           [>] APM Policy Compliance
  │ [+] │ lockfile-exists          │ Lockfile present                                    │
  │ [+] │ ref-consistency          │ All dependency refs match lockfile                  │
  │ [+] │ deployed-files-present   │ All deployed files present on disk                  │
  │ [+] │ no-orphaned-packages     │ No orphaned packages in lockfile                    │
  │ [+] │ skill-subset-consistency │ Skill subset selections match lockfile              │
  │ [+] │ config-consistency       │ No MCP configs to check                             │
  │ [+] │ content-integrity        │ No critical hidden Unicode or hash drift detected   │
  │ [+] │ includes-consent         │ No local content deployed -- includes … skipped     │
  │ [+] │ drift                    │ no drift detected against lockfile                  │

  [*] All 9 check(s) passed          # exit 0
```

### 1b — Policy violation → exit 1 (live this session; this is the "PR cannot merge" case)

A `block` policy (`enforcement: block`, `dependencies.require_pinned_constraint: true`) against an
**unpinned direct dep** (`microsoft/apm-sample-package#main`) fails the gate:

Caption: **`apm audit --ci --policy ./pol-block.yml` when a direct dependency tracks a bare branch. The
`dependency-pinned-constraint` check fails; exit 1 — the required check would block the PR. Verified on
apm v0.23.1.**

```text
  │     │ dependency-pinned-constraint │ 1 dependency(ies) use unbounded constraints
  │     │                              │ (hint: pin to a semver range, literal tag, or SHA)

  dependency-pinned-constraint details:
    - microsoft/apm-sample-package: bare branch 'main' tracks a moving tip

[x] 1 of 18 check(s) failed          # exit 1
```

> **NEW empirical nuance (verified this session — tell the author + verifier).**
> `dependencies.require_pinned_constraint` is evaluated against **direct manifest dependencies**, not
> transitive ones. With a **pinned direct** dep (`…#v1.0.0`) that pulls an **unpinned transitive**
> (`github/awesome-copilot#main`), the same block policy reports
> `dependency-pinned-constraint: All dependencies use pinned constraints` and **`All 29 check(s) passed`
> → exit 0**. Only when the **direct** dep is a bare branch does it fail (exit 1). So the install-time
> `[!] 1 dependency unpinned: github/awesome-copilot` warning is **advisory** and does **not** by itself
> trip this policy check. (Two run-shape details: the passing run enumerates 29 checks; the failing run
> shows `1 of 18` because the default **fail-fast** stops enumeration at the first failure — use
> `--no-fail-fast` to see them all. Both counts are correct; the number varies with what the project
> declares, matching Chapter 9.)

**When to use.** Wire `apm audit --ci` (org-discovered) into **branch protection as a required status
check** — it is the authoritative, unbypassable enforcer on every merge across every repo.
**When *not* to.** Do not rely on the *local* install gate as the org enforcer (it is bypassable);
do not use `apm outdated` as a gate (it never fails on drift — Chapter 7).

**Reproduction:** [../../backend/examples/ch11/README.md](../../backend/examples/ch11/README.md) (reuses
the Chapter 9 `require_pinned_constraint` recipe). Runnable exit codes above are the ground truth.

---

## Feature 2 — `microsoft/apm-action`: the CI workflow shape  ·  **`SKIPPED-needs-network`** (documented)

**Implements concept:** **C2 (CI gating)** — the turnkey integration path that installs the CLI, runs
`apm install`, and can emit SARIF for Code Scanning. **A GitHub Action cannot be run locally**, so all of
this is **documented, not executed** — the underlying `apm audit --ci` gate it invokes **is** verified
(Feature 1). Source: [microsoft/apm-action README](https://github.com/microsoft/apm-action) (v1.10.0) +
[Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/).

**Downstream consumer (documented cross-reference, `SKIPPED-needs-network`).** The same
`microsoft/apm-action` is how **GitHub Agentic Workflows (`gh-aw`)** consumes APM at runtime: a gh-aw
workflow adds a `shared/apm.md` import that runs the action to pack the declared packages into a bundle,
then restores it before the agent job starts — so the manifest, the `apm.lock.yaml` SHA pins (Ch6), and
the org `apm-policy.yml` baseline carry straight into the agent's execution environment. Pairing APM's
install-time governance with gh-aw's sandboxed runtime (the model holds no write token) is documented as
an enterprise pattern in GitHub's Well-Architected guidance. Cite the docs; never claim a locally-run
Action result. Sources: [gh-aw APM dependencies](https://github.github.com/gh-aw/reference/dependencies/) ·
[Governing agentic workflows with gh-aw and APM](https://learn.github.com/well-architected/governance/recommendations/governing-agentic-workflows).
Chapter 12 places gh-aw on the wider map as a *consumer* of APM, not a rival.

**Key inputs (README, pin to `@v1`):** `apm-version` (**pin a specific CLI version**), `setup-only`
(install CLI, then exit — no `apm.yml` read, no deploy), `audit-report` (generate SARIF + a
`$GITHUB_STEP_SUMMARY` markdown table), `compile`, `pack` / `bundle-format` (`apm`|`plugin`) / `target` /
`offline`, `update` (run `apm update --yes` instead of `install`), `working-directory`, `github-token`
(auto-forwarded as `GITHUB_APM_PAT` — same-org private repos work with zero config). **Key outputs:**
`apm-version`, `apm-path`, `audit-report-path` (SARIF), `bundle-path`, `pack-json`, `primitives-path`.

### 2a — Minimal required-check gate (the enterprise pattern)

The smallest job that fails a PR on any APM violation (docs' canonical recipe). Make it a **required
status check** via GitHub Rulesets and a violating PR cannot merge:

```yaml
# .github/workflows/apm-audit.yml   — SKIPPED-needs-network (documented; the apm audit --ci it runs is verified)
name: APM audit
on:
  pull_request:
    paths: ['apm.yml', 'apm.lock.yaml', '.apm/**', '.github/**', '.claude/**', '.cursor/**']
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: microsoft/apm-action@v1        # installs CLI + runs `apm install` (lockfile + files present)
      - run: apm audit --ci --no-cache        # the verified gate; --no-cache = fresh policy fetch
        env:
          GITHUB_APM_PAT: ${{ secrets.APM_PAT }}
```

### 2b — SARIF for Code Scanning (item 2's "SARIF output")

`if: always()` is load-bearing — SARIF must upload **even when the audit exits 1**, or the failing run
produces no Code Scanning entry:

```yaml
# .github/workflows/apm-audit-sarif.yml   — SKIPPED-needs-network (documented)
jobs:
  audit:
    runs-on: ubuntu-latest
    permissions: { contents: read, security-events: write }
    steps:
      - uses: actions/checkout@v4
      - uses: microsoft/apm-action@v1
      - name: Audit
        run: apm audit --ci --no-cache -o apm-audit.sarif
        env: { GITHUB_APM_PAT: '${{ secrets.APM_PAT }}' }
      - name: Upload SARIF
        if: always()                          # upload even on exit 1
        uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: apm-audit.sarif, category: apm-audit }
```

### 2c — Audit-only (`setup-only`) — catches post-install tampering

The default action runs `apm install` first, which **overwrites** managed files and can hide bytes that
were hand-edited after the last install. `setup-only: true` leaves deployed files exactly as checked out,
so the committed bytes are the ground truth (`content-integrity` still verifies SHA-256 vs the lockfile):

```yaml
# .github/workflows/apm-audit-setup-only.yml   — SKIPPED-needs-network (documented)
jobs:
  audit:
    runs-on: ubuntu-latest
    permissions: { contents: read }
    steps:
      - uses: actions/checkout@v4
      - uses: microsoft/apm-action@v1
        with: { setup-only: 'true' }          # CLI on PATH only; no install, no deploy
      - run: apm audit --ci --no-drift         # --no-drift: no warm cache to replay against
        env: { GITHUB_APM_PAT: '${{ secrets.APM_PAT }}' }
```

**Vendor-neutral.** `apm audit --ci` is a plain CLI call — the same gate works in **Azure Pipelines,
GitLab CI, and Jenkins**, not only GitHub Actions ([CI/CD integration](https://microsoft.github.io/apm/integrations/ci-cd/)).
`microsoft/apm-action` is only the GitHub convenience wrapper.

**Waivers (there is no per-PR override — by design).** Two shapes only:
(1) amend `<org>/.github/apm-policy.yml` through normal review (allow-list the package, raise
`max_depth`); (2) lower `enforcement` from `block` to `warn` for that scope — findings still appear in
SARIF, they just stop failing the job (treat as temporary). *"There is no per-PR override flag and there
will not be one. Bypass must be visible in the policy file's history."*
([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)).

Copy-paste-ready files: [../../backend/examples/ch11/workflows/](../../backend/examples/ch11/workflows/).

---

## Feature 3 — Registry proxy & air-gapped: the config knobs  ·  **`SKIPPED-needs-network`** (documented)

**Implements concept:** **C3 (registry strategy)** — because "enterprise networks rarely allow agents to
reach `github.com` directly," APM offers **three layered, composable controls** plus an offline path
([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/)). **Every knob is an
environment variable, not a persisted `apm config` key** — verified: `apm config get` lists only
`auto-integrate`, `temp-dir`, `mcp-registry-url` (see Feature 5). All live proxy/air-gapped behavior is
**`SKIPPED-needs-network`** — none runs without an Artifactory/private host.

**The controls, with exact env-var names (from the docs, "When to use what"):**

| Need | Knob | Notes (v0.23.1) |
|---|---|---|
| Allowlist outbound traffic at the firewall | `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` | Standard forward-proxy vars; **no APM-specific config** — "if `git clone` works through the proxy, `apm install` works too." |
| Mirror every dependency archive for audit + replay | `PROXY_REGISTRY_URL` | Full proxy base incl. any path prefix; rewrites every GitHub-hosted archive download to fetch via the mirror (Artifactory Archive Entry Download API). |
| Auth to the mirror | `PROXY_REGISTRY_TOKEN` | Bearer token on proxy requests; **independent of `GITHUB_APM_PAT`**. |
| Refuse direct-VCS fallback (mandatory + auditable) | `PROXY_REGISTRY_ONLY=1` | APM refuses to fall back to `github.com`/GHE.com/GHES; the lockfile records `registry_prefix`; on replay an entry pinned to a direct VCS host **aborts** the install → `apm install --update` to re-resolve. |
| Silence the plaintext-token warning on `http://` | `PROXY_REGISTRY_ALLOW_HTTP=1` | Use only inside an isolated network. |
| Serve internal marketplace listings | `apm marketplace add <slug> --host <ghes/gitlab-host> --ref main` | Stored in `~/.apm/marketplaces.json`; auth uses the same PAT as private installs. |
| Fully air-gapped CI (no egress at all) | **`apm pack`** on a connected host → restore offline | Chapter 10's `apm pack` reused as an air-gapped delivery mechanism ([Pack a bundle](https://microsoft.github.io/apm/producer/pack-a-bundle/)). |

> **Deprecated aliases:** `ARTIFACTORY_BASE_URL`, `ARTIFACTORY_APM_TOKEN`, `ARTIFACTORY_ONLY` still work
> but emit a `DeprecationWarning` — migrate to the `PROXY_REGISTRY_*` names. (The `apm-action` README's
> `env:` example still shows `ARTIFACTORY_APM_TOKEN` — note it is the legacy alias for `PROXY_REGISTRY_TOKEN`.)

**Integrity is anchored to the lockfile, NOT the proxy (tie-back to Chapter 6).** "Every install verifies
the `content_hash` recorded in `apm.lock.yaml` regardless of where the bytes came from. A tampered proxy
that rewrites archive contents is caught by the lockfile guard, not the cache." Routing through Artifactory
therefore does **not** weaken reproducibility — the mirror is a routing/audit convenience, and
`PROXY_REGISTRY_ONLY=1` makes the proxy path *mandatory and auditable*.

**Coverage has honest gaps (state them):**

| Surface | Proxy-covered? |
|---|---|
| `apm install` (GitHub-hosted deps) | **Yes** |
| `apm install` (Azure DevOps deps) | **No** — ADO uses a different path |
| `apm install --mcp` (MCP servers) | **No** — separate registry |
| `apm marketplace` (`marketplace.json` fetch) | **Yes**; falls back to GitHub Contents API unless `PROXY_REGISTRY_ONLY=1` |
| Policy file fetch (`apm-policy.yml`) | **No** — uses the GitHub API directly |

**Proxy ≠ dedicated registry (do not conflate).** The **proxy** transparently fronts an upstream git host
(per-machine `PROXY_REGISTRY_*`; **stable**). A **dedicated registry** is a separate, additive package
*source* with no git upstream (per-project `registries:` block in `apm.yml`; **experimental**, behind
`apm experimental enable registries`; OpenAPM registry HTTP API **deferred to v0.2**). "Both can be used
together; they're orthogonal." *There is no npm-style central registry today — distribution is git-based.*

**Lockfile env-dependence trade-off (mixed-fleet gotcha).** With `PROXY_REGISTRY_ONLY=1`, a 3-segment
GitLab shorthand (`group/subgroup/project`) parses differently vs. without the env set. For a fleet where
*some* agents have the env and others don't, expect lockfile drift — **pin the env in the same place you
pin Python and APM versions** (matches the theory brief's Meridian beat).

---

## Feature 4 — Org policy at fleet scale  ·  reference Chapter 9 (mostly **`SKIPPED-needs-network`**)

**Implements concepts:** **C1 (policy ownership) + C2 (the gate) + C4 (rollout)**. At fleet scale the org
policy is **owned centrally** and **enforced everywhere** via the CI gate. The *mechanism* is fully
verified in Chapter 9; Chapter 11 only changes *where it lives* and *who owns it* — which is exactly the
part that needs infrastructure. See [09-governance-and-policy-reference.md](09-governance-and-policy-reference.md)
for the confirmed `apm-policy.yml` schema and all exit-code proofs.

**What Chapter 9 already verified (reuse verbatim — do not re-teach the schema here):**
- **`warn` → `block` exit codes:** same violation, `enforcement: warn` prints the finding but renders
  `[+]` and **exits 0**; `enforcement: block` renders `[x]` and **exits 1**. Proven on
  `required-packages`, `dependency-pinned-constraint`, `mcp-self-defined`, `mcp-transport`. (Re-confirmed
  this session on `dependency-pinned-constraint`: block → exit 1.)
- **`apm audit --ci --policy <src>`** is the gate; `--policy` is **`[experimental]`**. Baseline (8–9
  checks) always runs and is **independent** of the `enforcement` dial.
- **Bypass contract:** `--no-policy` / `APM_POLICY_DISABLE=1` suppress **auto-discovered** org policy only;
  an **explicit `--policy` is always enforced**; baseline checks are **never** bypassable.

**The fleet-scale specifics (mostly SKIPPED-needs-network):**
- **Ownership boundary (C1).** The org policy lives in **`<org>/.github/apm-policy.yml`** behind
  CODEOWNERS / branch protection; a consuming repo (including the pilot) **only consumes** it. Discovery is
  from the git remote (candidate repos `.github → .apm → _apm`, first found wins; ADO tries only `_apm`),
  cached ~1h. **Live org-remote discovery = `SKIPPED-needs-network`** (a scratch dir with no remote prints
  `Could not determine org…` and fail-opens — see Feature 1a).
- **Org baseline shape.** The authoritative org file is `enforcement: block` once past the pilot. Minimal
  shape (Chapter 9 schema, target-key bug fixed):
  ```yaml
  # <org>/.github/apm-policy.yml   — the fleet baseline (authored + landed behind branch protection)
  name: acme-org-baseline
  version: "1.0.0"
  enforcement: block                     # off | warn | block  (single top-level dial)
  fetch_failure: block                   # fail closed if the policy can't be fetched
  dependencies:
    require_pinned_constraint: true      # verified to fire on a bare-branch DIRECT dep (Feature 1b)
    allow: ["acme/*", "microsoft/*"]     # null = no opinion · [] = allow nothing · [globs] = only these
  compilation:
    target: { allow: [copilot, claude, cursor] }   # NOT top-level `targets:` (silently ignored — Ch9)
  ```
- **Tighten-only inheritance (`extends:`).** Children can only *tighten* (allow-lists intersect, deny-lists
  union, `enforcement` escalates). **Verified in Chapter 9: a local-file `extends:` does NOT merge the
  parent** — real inheritance needs an `org` / `<owner>/<repo>` / `https://` ref, so **org-remote MERGE is
  `SKIPPED-needs-network`.** The merge table is documented (Ch9); the merge itself needs infra.
- **Rollout is Chapter 9's `warn → block`, fleet-wide (C4).** Author in `warn` on a canary (the pilot
  repo), read SARIF/Code Scanning, remediate, flip to `block`. Rollback is cheap (`block → warn` propagates
  within the policy-cache TTL); a blocked org is not — hence canary-then-widen.

> **Author trap (from Ch9, still applies).** `compilation.target` is the *correct* key but a **weak audit
> demo** — it needs a *resolved* target and reports "No compilation target set in manifest" on a candidate
> list (it bites at `apm install`/`compile`, org-remote → SKIPPED). Lead fleet demos with
> `dependencies.*` / `require_pinned_constraint` / `mcp.*`, which fire at audit time.

---

## Feature 5 — `apm config` & `apm cache`: the offline / caching surface  ·  **RUNNABLE** (introspection)

**Implements concept:** **C3 (registry strategy)** — the caching layer behind hermetic/offline CI, and
the config surface that proves the proxy knobs are env-vars (not persisted config). Inspected live.

### 5a — `apm config` (verbatim `--help` + `config get`, v0.23.1)

```text
apm config --help
  Configure APM CLI
  Commands:
    get    Get a configuration value
    set    Set a configuration value          # usage: apm config set KEY VALUE
    unset  Unset a configuration value

apm config get                                 # lists all persisted config
  [i] APM Configuration:
    auto-integrate: true
    temp-dir: Not set (using system default)
    mcp-registry-url: Not set (using default)
```

> **Verified finding for the author.** The **only** persisted `apm config` keys at v0.23.1 are
> **`auto-integrate`**, **`temp-dir`**, and **`mcp-registry-url`**. The registry-proxy controls
> (`PROXY_REGISTRY_URL`, `PROXY_REGISTRY_ONLY`, `HTTPS_PROXY`, …) are **NOT** `apm config` keys — they are
> **environment variables**, so at fleet scale they are pinned in CI secrets / dev-container env / shell
> profiles, *not* via `apm config set`. `mcp-registry-url` *is* the one enterprise-relevant persisted knob:
> point MCP resolution at an internal registry mirror.

### 5b — `apm cache` (verbatim, v0.23.1) — the hermetic-CI story

```text
apm cache --help
  Manage the local package cache
  Commands:
    clean  Remove all cached content
    info   Show cache location and size statistics
    prune  Remove cache entries older than N days      # --days INTEGER  [default: 30]

apm cache info
  [i] Cache root: C:\Users\<user>\AppData\Local\apm\cache
  [#] Git repositories (db): 10   Git checkouts: 18   HTTP cache entries: 2
  [#] Total size: 34.3 MB  (Git 34.3 MB · HTTP 30.1 KB)
```

**Enterprise relevance.** The cache (`~/.apm/cache/` on Unix, `%LOCALAPPDATA%\apm\cache` on Windows) holds
**git checkouts** + an **HTTP cache** (proxy responses, `marketplace.json` snapshots). It is **upstream of
the proxy**: a cached entry is keyed by the *resolved* URL, so switching `PROXY_REGISTRY_URL` forces a
fresh download; **integrity is unchanged** (content-hash still verified — Chapter 6). For hermetic CI, a
warm cache + committed lockfile lets `apm install` restore locked bytes with minimal network;
`apm cache prune --days N` / `apm cache clean` manage size on shared runners.

---

## When to use / pitfalls (for the author)

- **`apm audit --ci` (org-discovered) is the fleet gate — make it a *required* status check.** It is the
  only authoritative, unbypassable enforcer on merge. The local install gate is bypassable; `apm outdated`
  never fails on drift.
- **`--no-cache` in the CI gate.** Prevents a cached policy file masking a same-day org-policy update.
- **`require_pinned_constraint` is DIRECT-only.** A pinned direct dep with an unpinned *transitive* passes
  the check (verified: 29 checks, exit 0). The install-time `unpinned` warning is advisory. If the fleet
  wants transitive pinning too, that is a different lever (lockfile pinning / `max_depth`), not this check.
- **`microsoft/apm-action` is a convenience, not the enforcer.** The gate is `apm audit --ci`; the action
  just installs the CLI and runs it. It is **`SKIPPED-needs-network`** — never claim a locally-run result
  for a GitHub Action. Pin the action to `@v1` and pin the CLI with `apm-version:`.
- **`setup-only: true` for tamper detection.** The default install-then-audit **overwrites** managed files
  and can hide post-install edits; `setup-only` audits the committed bytes.
- **Proxy knobs are env-vars, not `apm config`.** Pin `PROXY_REGISTRY_*` / `HTTPS_PROXY` in CI secrets and
  dev containers *"in the same place you pin Python and APM versions."* Mixed-fleet env skew causes lockfile
  drift for 3-segment GitLab deps.
- **The proxy is not the trust anchor — the lockfile is.** A malicious mirror is caught by `content_hash`.
  Routing through Artifactory does not weaken reproducibility.
- **Proxy coverage gaps are real:** no ADO deps, no MCP servers, no `apm-policy.yml` fetch. Don't imply the
  proxy carries everything.
- **Dedicated registry (`registries:`) is experimental (v0.2 API).** Don't present it as today's default
  distribution — APM is git-based today.
- **Org-policy inheritance MERGE and org-remote discovery are `SKIPPED-needs-network`.** Local-file
  `extends:` does **not** merge (Ch9). Present org policy as *authored/tested locally, landed in
  `<org>/.github`.*
- **No per-PR override waiver — by design.** Exceptions are visible policy-file amendments or a scoped
  `block → warn`. There is no `--force-merge` flag.

---

## Caveats & flags (for the author + verifier)

1. **RUNNABLE:** `apm audit --ci` → **exit 0** clean (`All 9 check(s) passed`); `apm audit --ci --policy
   ./pol-block.yml` on a bare-branch **direct** dep → **exit 1** (`dependency-pinned-constraint … 1 of 18
   check(s) failed`). Both re-confirmed live this session on apm v0.23.1. The clean gate = **8 baseline +
   drift = 9**.
2. **NEW:** `require_pinned_constraint` targets **direct** deps only — pinned-direct + unpinned-transitive
   passed (**29 checks, exit 0**). Check count varies with declared rules **and** fail-fast (18 on failure,
   29 on pass); use `--no-fail-fast` for full reports.
3. **`apm audit --ci --policy` is `[experimental]`.** Baseline (8–9) is stable and always runs, independent
   of `enforcement`.
4. **`microsoft/apm-action` (v1.10.0) is `SKIPPED-needs-network`** — documented from README + enforce-in-CI
   docs; never run locally. Pin `@v1`; pin CLI via `apm-version:`. SARIF via `audit-report: true` or
   `-o *.sarif` + `github/codeql-action/upload-sarif@v3` with **`if: always()`**. Markdown is **not**
   supported in `--ci` mode.
5. **Registry proxy is `SKIPPED-needs-network`** — env-vars `PROXY_REGISTRY_URL` / `PROXY_REGISTRY_TOKEN` /
   `PROXY_REGISTRY_ONLY` / `PROXY_REGISTRY_ALLOW_HTTP` (deprecated `ARTIFACTORY_*` aliases); `HTTPS_PROXY` /
   `HTTP_PROXY` / `NO_PROXY`. **Not** `apm config` keys (verified). Lockfile `registry_prefix` +
   replay-abort under `PROXY_REGISTRY_ONLY=1`. Coverage excludes ADO, MCP, and policy-file fetch.
6. **Air-gapped = `apm pack` (Chapter 10) restored offline.** `SKIPPED-needs-network` for the connected
   pack host; the offline restore is the deliverable.
7. **`apm config` keys (v0.23.1):** only `auto-integrate`, `temp-dir`, `mcp-registry-url`. **`apm cache`:**
   `info` / `prune --days N` (default 30) / `clean`; cache at `%LOCALAPPDATA%\apm\cache` (Windows).
8. **Org policy at scale = Chapter 9 behavior, relocated to `<org>/.github`.** Discovery + `extends:` MERGE
   are `SKIPPED-needs-network` (local `extends:` does not merge). Org baseline shape: `enforcement: block`,
   `fetch_failure: block`.
9. **Preview surfaces:** `--policy` (experimental), dedicated `registries:` (experimental, v0.2 API),
   policy enforcement (early preview). Proxy + baseline checks are stable. **Pin apm to v0.23.1** before
   relying on any of this as a production gate.

---

## Commands run this session (reproducibility)

All prefixed with the PATH refresh; scratch dir `%TEMP%\apm-ch11` (outside the repo); public package only,
no tokens.

```powershell
apm --version                                        # 0.23.1
apm config --help ; apm config get                   # get/set/unset ; keys: auto-integrate, temp-dir, mcp-registry-url
apm cache --help ; apm cache info ; apm cache prune --help   # clean/info/prune ; --days [default 30]
# scratch project (pinned public dep + lockfile):
apm init -y --target copilot
apm install microsoft/apm-sample-package#v1.0.0      # exit 0 ; lockfile written
apm audit --ci                                       # exit 0 ; "All 9 check(s) passed"          (RUNNABLE)
apm audit --ci --policy ./pol-block.yml              # pinned direct + unpinned transitive: exit 0, 29 checks
# block-demo (unpinned DIRECT dep):
apm install microsoft/apm-sample-package#main
apm audit --ci --policy ./pol-block.yml              # exit 1 ; dependency-pinned-constraint fails  (RUNNABLE)
```

---

## Sources (official docs actually used)

- **Enforce in CI** — the gate, flags (`--policy`/`--no-cache`/`--no-fail-fast`/`--no-drift`/`-f`/`-o`), the
  minimal + SARIF + setup-only + drift-sweep recipes, the waiver contract:
  <https://microsoft.github.io/apm/enterprise/enforce-in-ci/>
- **`microsoft/apm-action`** (v1.10.0) — inputs/outputs, `setup-only`, `audit-report` (SARIF), `apm-version`
  pinning, auth: <https://github.com/microsoft/apm-action>
- **Registry proxy and air-gapped installs** — `PROXY_REGISTRY_*` env vars, `HTTPS_PROXY`, bypass
  prevention, coverage table, cache behavior, dedicated-registry orthogonality:
  <https://microsoft.github.io/apm/enterprise/registry-proxy/>
- **apm audit reference** — check names, exit codes, `--policy` experimental flag:
  <https://microsoft.github.io/apm/reference/cli/audit/>
- **Enterprise overview / making-the-case / adoption playbook** — the fleet framing, ROI, phases (C1/C4):
  <https://microsoft.github.io/apm/enterprise/> ·
  <https://microsoft.github.io/apm/enterprise/making-the-case/> ·
  <https://microsoft.github.io/apm/enterprise/adoption-playbook/>
- **Chapter 9 reference** (this repo) — verified `apm-policy.yml` schema, `warn → block` exit codes,
  tighten-only inheritance, local-`extends:`-does-not-merge:
  [09-governance-and-policy-reference.md](09-governance-and-policy-reference.md)
- **Chapter 10 reference** (this repo) — `apm pack` (reused for air-gapped delivery):
  [10-becoming-a-producer-reference.md](10-becoming-a-producer-reference.md)
