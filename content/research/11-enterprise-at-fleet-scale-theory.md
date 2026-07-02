# Concept Brief — Chapter 11: Enterprise at Fleet Scale

- **Chapter:** 11 — Enterprise at Fleet Scale (Part VI — At scale & ahead)
- **Objective it serves:** Gate and govern APM usage across an organization without turning developer
  setup into a bottleneck.
- **Focus:** leader-heavy (per outline). The platform/security engineer still runs the commands, but the
  *decisions* — who owns policy, what the required CI check is, whether traffic routes through a proxy,
  how adoption is measured — are engineering-leadership calls. Carry a strong "For engineering leaders"
  thread throughout, not just in the callout.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30); `microsoft/apm-action`
  latest **v1.10.0**. **Version-awareness matters here in three specific ways:** (1) the `apm audit --ci`
  **`--policy` flag is marked *Experimental*** ([apm audit reference](https://microsoft.github.io/apm/reference/cli/audit/));
  (2) the **dedicated registry** (a real package-server speaking a Registry HTTP API) is **experimental**
  and gated behind `apm experimental enable registries`, because the OpenAPM **registry HTTP API is
  deferred to v0.2** ([Registries guide](https://microsoft.github.io/apm/guides/registries/);
  [OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v01/)); (3) policy *enforcement* is early
  preview (carried over from Chapter 9). By contrast, the **registry *proxy*** (env-var driven) and the
  **eight baseline lockfile checks** in `apm audit --ci` are stable. Every `Implemented in APM by:` line is
  a conceptual hand-off — the `apm-cli-explorer` must confirm exact flags, env-var names, check names, and
  which examples are **runnable locally vs. `SKIPPED-needs-network`** (org-policy discovery, an Artifactory
  proxy, and CI-in-anger all need infrastructure a reader/sandbox will not have).

## Frame note (which property this chapter feeds)

Chapter 11 does **not** introduce a fifth property. It is the capstone that asks whether the book's four
properties — **portability, reproducibility, provenance/security, governance** — hold for *every* repo,
*enforced* and *operated* at organizational scale. The single load-bearing question the chapter must plant
early and answer throughout is the shift Concept 1 names: **from "can *this* repo install?" to "can
*every* repo install safely and predictably?"**

This is APM's **enterprise ramp**, which the docs frame as delivering the third promise —
"**every AI package your developers install is governed by org policy before it touches disk**" — and
present as **five phases: Decide · Secure · Author policy · Enforce · Operate**
([Enterprise overview](https://microsoft.github.io/apm/enterprise/);
[the three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). Chapter 11 keeps the
focus on **operating APM at scale**, not on selling a general AI-transformation methodology — the outline
is explicit about this, and so are the docs (the adoption playbook is a rollout runbook, not a culture
essay).

## Prerequisite recap (what the earlier chapters already built)

- **Chapter 6 (lockfile / reproducibility)** gave us content-hash pinning. Chapter 11 reuses it as the
  *integrity anchor* behind a registry proxy: bytes may be mirrored through Artifactory, but the
  `content_hash` in `apm.lock.yaml` is still verified, so "a tampered proxy that rewrites archive contents
  is caught by the lockfile guard, not the cache"
  ([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/)).
- **Chapter 7 (lifecycle) + Chapter 9 (governance)** gave us `apm audit` and `apm-policy.yml`. Chapter 11
  wires the *same* gate into every pull request as a required check (`apm audit --ci`) — this is the
  install-time gate seen a third time, now made authoritative on merge.
- **Chapter 10 (producer)** gave us packages (`meridian-standards`, `apm pack`). Chapter 11 turns those
  into **internal marketplaces** that fleet teams install from, and into **air-gapped bundles** for
  disconnected CI.

The author should present Chapter 11 as *operationalizing* Chapters 6–10 across a fleet, not as a new
subsystem. Nothing here is a novel capability; it is the earlier capabilities made **repeatable, owned,
gated, and measured**.

## Terminology & scope notes (read before drafting)

- **"Fleet" = the whole org's repos, not a cluster of agents.** In this book, fleet scale means "N repos ×
  M developers × K harnesses" (the docs' worked figure: *50 repos, 200 developers, five AI coding tools*)
  ([Making the case](https://microsoft.github.io/apm/enterprise/making-the-case/)).
- **Two different "five-phase" models — do not conflate them.** The **enterprise *ramp*** is the doc
  section's structure (Decide / Secure / Author policy / Enforce / Operate). The **adoption *playbook*** is
  the rollout sequence (**Discover → Pilot → Harden → Scale → Sustain**), each phase with *a single owner,
  a deliverable, and a gate* ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)).
  Concept 4 uses the *playbook*. The outline's shorthand "pilot → measure → standardize → gate" maps onto
  it (measure = Discover + Pilot-in-warn; standardize = Harden; gate = Enforce-in-CI) — present the
  official five phases as authoritative and treat the four-word mnemonic as a memory aid.
- **Registry *proxy* ≠ dedicated *registry*.** The **proxy** transparently fronts an upstream git host
  (GitHub/GitLab) so clones flow through corporate infra; it is env-var driven (`PROXY_REGISTRY_*`) and
  stable. A **dedicated registry** is a separate, additive package *source* that speaks a Registry HTTP API
  with no git host upstream; it is per-project (`registries:` in `apm.yml`) and **experimental**. They are
  orthogonal ([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/);
  [Registries guide](https://microsoft.github.io/apm/guides/registries/)). Chapter 11's running example
  uses the **proxy**.
- **Policy ownership is a hard boundary.** The org policy lives in `<org>/.github/apm-policy.yml` behind
  CODEOWNERS/branch protection; a *consuming* team (including the pilot team) **only consumes it** — "policy
  belongs in the `.github` repo behind branch protection; the pilot only consumes it"
  ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)). This reinforces the
  Chapter 1 / Chapter 9 "org-remote, not per-repo" framing.
- **Keep it about operating APM.** Every claim should trace to an APM doc (adoption playbook, making-the-
  case, enforce-in-CI, registry-proxy). Resist drifting into generic change-management or AI-strategy
  content — that is explicitly out of scope.

---

## Concepts covered

1. **One team vs a fleet** — a single team adopts with a manifest + lockfile; an enterprise needs
   repeatable rollout, policy *ownership*, audit *gates*, a *registry strategy*, and *exception handling*.
   The question shifts from "can this repo install?" to "can *every* repo install safely & predictably?"
2. **CI gating** — `apm audit --ci` as the required PR check: the integrity + policy gate from Chapters 7
   and 9 wired into branch protection as **defence in depth**, with `microsoft/apm-action` as the CI/CD
   integration path.
3. **Registry strategy** — routing/mirroring dependency traffic (registry proxy) and building for offline
   (air-gapped) environments, on APM's git-based-today distribution model.
4. **Adoption as change management** — the phased **Discover → Pilot → Harden → Scale → Sustain** rollout,
   measured by *leading indicators* (audit pass rate, drift trend, marketplace uptake), not by package
   counts.

---

## Concept 1 — One team vs a fleet ("can *every* repo install safely and predictably?")

**Definition.** A single team gets almost all of APM's value from three files and one habit: `apm.yml`,
`apm.lock.yaml`, and `apm install`. An **enterprise** needs five additional things the single-team story
never forces: **repeatable rollout** (a runbook, not a hero), **policy ownership** (a named, protected
owner of `<org>/.github/apm-policy.yml`), **audit gates** (a required CI check on every PR),
**registry strategy** (controlled/mirrored dependency traffic), and **exception handling** (a visible,
reviewable way to grant a waiver). Fleet scale reframes the whole exercise: not "does my repo install?"
but "does *every* repo install safely and predictably, without me in the loop?"

**The problem it solves.** The docs' worked figure is a mid-to-large org: *50 repositories, 200 developers,
five AI coding tools*. Without centralized management, a predictable failure set emerges — **manual
config per repo** (conventions diverge, knowledge silos form), **no audit trail** ("what agent
configuration was active at release 4.2.1?" has no answer), **version drift** (dev A has v1.2, dev B has
v1.4, CI has whatever was last committed), **onboarding friction**, and **ungoverned dependencies** — "the
same problem regulated industries spent a decade solving for application code, now back in a new form"
([Making the case](https://microsoft.github.io/apm/enterprise/making-the-case/)). These are the Chapter 1
pains, multiplied by the repo count.

**Key distinctions.**
- *Consumer ramp vs. enterprise ramp.* The consumer ramp is one repo's daily loop (Chapters 4–7); the
  enterprise ramp (Chapter 11) is org-wide *control* — the same commands, but owned, gated, and operated
  centrally ([Enterprise overview](https://microsoft.github.io/apm/enterprise/)).
- *Consuming policy vs. owning policy.* A fleet team **consumes** the org policy discovered from its git
  remote; it does not author it. Authorship sits in `<org>/.github` behind branch protection. Letting a
  pilot team author org policy is called out as a **pitfall**
  ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)).
- *There is a threshold below which none of this is worth it.* The docs are refreshingly honest: APM is
  worth adopting when *you use more than 3 plugins/MCP servers, your team has more than 5 developers, you
  need reproducible CI config, you share standards across repos, or you need an audit trail* — and
  "below that threshold, manual setup is fine. APM is designed to help when manual management stops
  scaling" ([Making the case](https://microsoft.github.io/apm/enterprise/making-the-case/)). The chapter
  should name this threshold so leaders don't over-adopt.

**Common misconception.** *"Fleet scale is just the single-repo setup, copied N times."* It is not: N copies
without central ownership reproduce the drift problem at higher cost. The missing pieces are **ownership**
(a named on-call, not "the platform team"), **gates** (CI as the authoritative enforcer), **a registry
strategy**, and **exception handling** — none of which a single repo needs. A second, leader-facing
misconception: *"more repos with `apm.yml` = success."* The docs call that a **vanity metric** (Concept 4).

**Meridian beat (for the author) — sets up the whole chapter.** Meridian's platform team moves from the
`meridian-checkout` pilot (Chapters 4–10) to **three product groups**. The staff engineer's question is no
longer "does checkout install?" but "can Payments, Onboarding, and Merchant-Dashboard each clone, install,
and pass CI with the *same* guarantees — without the platform team hand-holding every repo?" That reframing
is the chapter's spine; Concepts 2–4 are how Meridian answers it (CI gate on every PR, an approved proxy,
a published adoption checklist, org policy at `block`).

**Implemented in APM by:** the **enterprise ramp** (five phases: Decide / Secure / Author policy / Enforce /
Operate); the **org-remote `apm-policy.yml`** in `<org>/.github` (ownership boundary); the
**adoption playbook** (repeatable rollout) and **making-the-case** (ROI + the adoption threshold);
exception handling via policy-file amendments (Concept 2). *Explorer to confirm:* the current enterprise-ramp
page structure and the adoption threshold wording; and that the ownership boundary (`<org>/.github`,
consumer-only for repos) matches v0.23.1 discovery behavior.

---

## Concept 2 — CI gating: `apm audit --ci` as the required, unbypassable check

**Definition.** `apm audit --ci` is **one command** that runs, on a pull request: the **eight baseline
lockfile checks** (`lockfile-exists`, `ref-consistency`, `deployed-files-present`, `no-orphaned-packages`,
`skill-subset-consistency`, `config-consistency`, `content-integrity`, `includes-consent`), the
**install-replay drift check**, and — *if* an `apm-policy.yml` is discovered from the repo's git remote —
the **org policy checks**. Exit code is **`0` clean, `1` on any violation**
([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/);
[apm audit reference](https://microsoft.github.io/apm/reference/cli/audit/)). It is the *same* integrity
gate from Chapter 7 and the *same* policy gate from Chapter 9 — now re-run in CI and, via **GitHub
Rulesets**, made a **required, unbypassable status check** so a violating PR cannot merge
([GitHub rulesets](https://microsoft.github.io/apm/enterprise/github-rulesets/)). `microsoft/apm-action` is
the turnkey integration path: it installs the CLI, runs `apm install`, and can emit SARIF for Code Scanning
([microsoft/apm-action](https://github.com/microsoft/apm-action)).

**The problem it solves.** The install-time gate (Chapters 8–9) protects the developer's own machine, but
it is **locally bypassable** — a developer can pass `--no-policy`, `--force`, or `APM_POLICY_DISABLE=1`. CI
re-runs the identical gates on the pull request itself: "that is defence in depth: a developer can pass
`--no-policy`, `--force`, or `APM_POLICY_DISABLE=1` locally; **CI cannot**"
([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)). At fleet scale, the CI gate is
what makes an org rule *actually* authoritative on every merge across every repo, regardless of local
behavior.

**Key distinctions.**
- *Local install gate vs. CI audit gate.* Both run the same checks on the same resolved set. The install
  gate is a *preflight* on the workstation (bypassable, loud); the CI gate is the *authoritative* enforcer,
  and the local bypass flags **do not work in CI** — "`--no-policy` does not work here — CI ignores the
  local bypass flag" ([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)).
- *Baseline checks are non-bypassable; policy is the discovered layer.* The eight lockfile baselines +
  drift always run; `--no-policy` in CI skips only *policy discovery*, leaving baseline + drift intact
  ([apm audit reference](https://microsoft.github.io/apm/reference/cli/audit/)). This is the tie-back to
  Chapter 6: reproducibility is enforced even when governance is off.
- *No per-PR override — waivers are visible by design.* "There is **no per-PR override flag and there will
  not be one**. Bypass must be visible in the policy file's history." The only two waiver shapes are:
  (1) amend `<org>/.github/apm-policy.yml` through normal review (allow-list the package, raise `max_depth`,
  etc.), or (2) lower `enforcement` from `block` to `warn` for that scope — findings still appear in SARIF,
  they just stop failing the job; treat as temporary
  ([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)). This *is* Concept 1's
  "exception handling," made concrete.
- *`--no-cache` matters in CI.* Recommended so a cached policy file does not mask a same-day policy update
  ([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)).
- *Install-then-audit vs. setup-only audit.* The default `apm-action` runs `apm install` first (good for
  fresh runners), but install overwrites managed files, which can hide post-install tampering; the
  **setup-only** pattern audits the committed bytes as ground truth. Both enforce policy + the eight
  baselines ([Enforce in CI](https://microsoft.github.io/apm/enterprise/enforce-in-ci/)).
- *Vendor-neutral.* `apm audit --ci` is a plain CLI call; the same gate works in Azure Pipelines, GitLab
  CI, and Jenkins, not only GitHub Actions
  ([CI/CD integration](https://microsoft.github.io/apm/integrations/ci-cd/);
  [microsoft/apm-action](https://github.com/microsoft/apm-action)).

**Common misconception.** *"CI gating is a new, separate check."* It is the **same** gate as `apm install`,
re-run in CI as defence in depth — not a different engine. Two related traps carried from Chapter 9: *"warn
mode fails CI"* (it does not — warn exits `0`; visibility lives in the SARIF/Code Scanning UI) and *"you can
force-merge a blocked PR with a flag"* (you cannot; the fix is an allowed alternative or a reviewed policy
amendment).

**Meridian beat (for the author).** Meridian adds an **`apm audit --ci`** job (via `microsoft/apm-action@v1`,
then `apm audit --ci --no-cache`) to pull requests in all three product groups and makes it a **required
status check** through GitHub Rulesets. When a Payments engineer adds a dependency from a non-approved
source, the PR check fails with a policy violation and a SARIF alert on the diff — and because there is no
per-PR override, the engineer either swaps to an allowed package or files a change request against
`meridian/.github/apm-policy.yml`. The gate is authoritative even though the same engineer could have
passed `--no-policy` on their laptop.

**Implemented in APM by:** `apm audit --ci` (the eight baseline checks + drift + discovered policy; exit
0/1); flags `--policy org|<owner/repo>|<url>|<path>` (**Experimental**), `--no-policy`, `--no-cache`,
`--no-fail-fast`, `--no-drift`, `-f sarif|json`, `-o <path>`; `microsoft/apm-action@v1` (default install;
`setup-only`; `audit-report` → SARIF + step summary; `update` mode); **GitHub Rulesets** to make the check
required/unbypassable; SARIF upload via `github/codeql-action/upload-sarif` with `if: always()`.
*Explorer to confirm:* the exact eight check names and exit codes at v0.23.1; the `--policy` experimental
status; the current `apm-action` inputs/outputs (latest v1.10.0); and mark **`apm audit --ci` on a local
repo as runnable**, but **org-policy discovery, required-check wiring, and CI-in-anger as
`SKIPPED-needs-network`**.

---

## Concept 3 — Registry strategy: proxy, air-gapped, and the git-based-today reality

**Definition.** Because "enterprise networks rarely allow agents to reach `github.com` directly," APM offers
**three layered, composable controls** for dependency traffic
([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/)):
1. **Standard forward proxy** — the ordinary `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY` env vars. "If
   `git clone` works against your private repos through the proxy, `apm install` works too" (no APM-specific
   config).
2. **Mirror through Artifactory (or compatible)** — `PROXY_REGISTRY_URL` rewrites every GitHub-hosted
   dependency download to fetch via the mirror; auth via `PROXY_REGISTRY_TOKEN`.
3. **Internal marketplaces** — `apm marketplace add --host …` to register discovery sources served from
   GHES, GHE.com, or GitLab self-managed.

For a **fully air-gapped** environment (no egress at all), the answer is a **pre-built bundle**: `apm pack`
on a connected host, restore offline (Chapter 10's `apm pack` reused as an air-gapped delivery mechanism).
A **dedicated registry** (a real package server speaking the Registry HTTP API, per-project via a
`registries:` block) also exists but is **experimental** and **orthogonal** to the proxy — it reflects the
OpenAPM **registry API deferred to v0.2** ([Registries guide](https://microsoft.github.io/apm/guides/registries/);
[OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v01/)).

**The problem it solves.** Regulated and security-conscious orgs already funnel npm and PyPI through a
controlled proxy; APM must fit the same operating model. The docs are blunt: treating the proxy "as optional
when your security org mandates Artifactory for npm and PyPI" is a pitfall — "APM is the same conversation —
do not ship on direct GitHub fetches" ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)).
The strategy gives an org **auditable, mirrored, replayable** dependency traffic plus a genuinely
**offline** path.

**Key distinctions.**
- *Proxy vs. dedicated registry.* The **proxy** fronts an upstream git host (per-machine `PROXY_REGISTRY_*`
  env vars; stable). The **dedicated registry** is a separate package *source* with no git upstream
  (per-project `registries:` in `apm.yml`; **experimental**, behind `apm experimental enable registries`).
  "Both can be used together; they're orthogonal"
  ([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/)).
- *Bypass prevention.* `PROXY_REGISTRY_ONLY=1` makes APM **refuse** to fall back to `github.com`/GHE.com/
  GHES; the lockfile records a `registry_prefix`, and on replay an entry pinned to a direct VCS host
  **aborts the install** until re-resolved through the proxy
  ([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/)).
- *Integrity is anchored to the lockfile, not the proxy (tie-back to Chapter 6).* "Every install verifies
  the `content_hash` recorded in `apm.lock.yaml` regardless of where the bytes came from. A tampered proxy
  that rewrites archive contents is caught by the lockfile guard, not the cache." Routing through a mirror
  therefore does **not** weaken reproducibility.
- *Coverage has gaps worth stating honestly.* The proxy covers `apm install` for **GitHub-hosted** deps and
  marketplace fetches, but **not** Azure DevOps deps, **not** MCP servers (separate registry), and **not**
  the `apm-policy.yml` fetch (uses the GitHub API directly)
  ([Registry proxy](https://microsoft.github.io/apm/enterprise/registry-proxy/)).

**Common misconception.** *"APM has a central registry like npm."* Not today — distribution is **git-based**;
the dedicated registry HTTP API is a **v0.2 / experimental** capability
([OpenAPM v0.1](https://microsoft.github.io/apm/specs/openapm-v01/);
[Registries guide](https://microsoft.github.io/apm/guides/registries/)). A second misconception: *"the proxy
is the trust anchor."* It is not — the **lockfile** is; a malicious mirror is caught by content-hash
verification. A third: *"routing through Artifactory hurts reproducibility."* The opposite — the same hashes
are verified, and `PROXY_REGISTRY_ONLY=1` makes the proxy path *mandatory and auditable*.

**Meridian beat (for the author).** Meridian's security org already mandates Artifactory for npm and PyPI, so
the platform team **routes APM dependency traffic through the same approved proxy**: `PROXY_REGISTRY_URL`
points at the Artifactory GitHub remote, `PROXY_REGISTRY_ONLY=1` blocks direct `github.com` fallback, and
the setting is pinned in the same place as the Python and APM versions so the whole CI fleet resolves
identically. The lockfile's content hashes still gate integrity, so the mirror is a routing/audit
convenience, not a new trust anchor. (Mark all proxy examples `SKIPPED-needs-network`.)

**Implemented in APM by:** `HTTPS_PROXY` / `HTTP_PROXY` / `NO_PROXY`; `PROXY_REGISTRY_URL`,
`PROXY_REGISTRY_TOKEN`, `PROXY_REGISTRY_ONLY`, `PROXY_REGISTRY_ALLOW_HTTP` (deprecated `ARTIFACTORY_*`
aliases); the lockfile `registry_prefix` + replay-abort guard; `apm marketplace add --host …`; `apm pack` /
restore for air-gapped delivery; the experimental `registries:` block + Registry HTTP API; `content_hash`
verification (Chapter 6) as the integrity anchor. *Explorer to confirm:* exact env-var names and the
`PROXY_REGISTRY_ONLY` replay-abort behavior; the `apm experimental enable registries` gate; the coverage
table (ADO / MCP / policy-fetch exclusions). **All Concept-3 examples are `SKIPPED-needs-network`** — none
run without an Artifactory/private host.

---

## Concept 4 — Adoption as change management (measure by leading indicators, not package counts)

**Definition.** Rolling APM out to a fleet is a **staged program**, not a switch. The official
**adoption playbook** is five phases, each with *a single owner, a deliverable, and a gate to clear before
advancing*: **Discover** (1–2 wks, platform team; shadow `apm install --dry-run` + `apm audit`; gate: answer
"what breaks if we turn this on tomorrow, and for whom?") → **Pilot** (~1 mo, one product team + platform;
manifest, lockfile, CI audit, and policy in **`warn`**; gate: two consecutive weeks of clean pilot CI with
every warning triaged) → **Harden** (~1 mo, security + platform; flip `warn → block`, add the registry proxy
if required, stand up internal marketplaces; gate: a fresh third-party repo installs against org policy +
proxy end-to-end with no manual help) → **Scale** (ongoing; self-service onboarding; gate: platform is no
longer in the critical path) → **Sustain** (steady state; weekly drift triage, monthly lockfile review,
quarterly marketplace refresh). "**Do not skip phases. Each one buys evidence the next one needs**"
([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)).

**The problem it solves.** Two org-breaking failure modes. First, flipping enforcement to `block` on day one
"fails on its next run … you will spend the day rolling back instead of rolling out" (the Chapter 9 lesson,
now fleet-wide) — hence Pilot-in-`warn` before Harden-to-`block`, with the **pilot repo as the canary**.
Second, "mandating adoption without offering a marketplace worth installing from" — **carrot before stick**
([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)). The playbook converts a
risky big-bang into a measured migration that earns trust.

**Key distinctions.**
- *Leading indicators vs. vanity metrics.* The docs are explicit: "measuring `apm.yml` count and nothing
  else (**audit pass rate and drift trend are the leading indicators — manifest count is vanity**)." The
  reported KPIs are: **repos with `apm.yml` committed**, **`apm audit --ci` pass rate per week**, **distinct
  packages installed from org marketplaces**, and **drift findings closed vs. opened (trend, not absolute)**
  ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)). For the leader
  callout, pair these with the **ROI framing** from *making-the-case*: **time saved** (manual setup
  15–60 min/repo → `apm install` under 30 s), **risk reduced** (drift, audit gaps, ungoverned proliferation),
  and **consistency gains** ([Making the case](https://microsoft.github.io/apm/enterprise/making-the-case/)).
  The outline's leader metrics — *setup time, policy warnings, blocked risky installs, update cadence,
  satisfaction* — are complementary; anchor each to a doc source rather than inventing thresholds.
- *Ownership is a person, not a team.* A pitfall in Sustain: "no named owner ('the platform team' is not an
  owner; a **named on-call** is)" ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)).
- *Shadow-mode Discover is a sizing exercise, not a buy decision.* Run `apm install --dry-run` + `apm audit`
  against representative repos (include at least one with hand-edited `.github/`/`.cursor/`/`.claude/`
  content, "that is where drift findings appear") to learn what would break — don't treat it as approval
  ([Adoption playbook](https://microsoft.github.io/apm/enterprise/adoption-playbook/)).
- *Rollback is cheap; a blocked org is not.* Carried from Chapter 9 — flipping `block → warn` propagates
  within the policy-cache TTL, so canary-then-widen is safe.

**Common misconception.** *"Adoption = getting `apm.yml` into every repo."* That is the vanity metric the docs
warn against; a repo with a manifest but a failing audit or rising drift is not adopted, it is *at risk*. A
second: *"once the pilot works, we're done."* No — Harden, Scale, and Sustain follow, and **Sustain is
permanent** (weekly/monthly/quarterly cadence). A third (leader-facing): *"success is measured in package
counts / seats."* Success is **audit pass rate up, drift trend down, marketplace uptake up, onboarding time
flat-or-down.**

**Meridian beat (for the author) — closes the chapter's arc.** Meridian runs the playbook: a **Discover**
shadow pass across the three product groups' representative repos; a **Pilot** already banked on
`meridian-checkout` (Chapters 4–10) with org policy in `warn`; a **Harden** step that flips org policy to
**`block`** (checkout as the canary), routes traffic through the approved proxy (Concept 3), and publishes
`meridian-standards` to an internal marketplace (Chapter 10); then **Scale** via a **published adoption
checklist** so Payments, Onboarding, and Merchant-Dashboard onboard self-service; and **Sustain** with a
named platform on-call running weekly drift triage. The platform team reports **audit pass rate and drift
trend**, not "repos with a manifest."

**Implemented in APM by:** the **adoption playbook** (five phases; owner + deliverable + gate each);
**making-the-case** (ROI framework, sample RFC, objection handling, the adoption threshold); the KPI set
(`apm audit --ci` pass rate; drift closed-vs-opened trend; marketplace package count; repos with `apm.yml`);
shadow-mode `apm install --dry-run` + `apm audit` for Discover; org marketplaces (Chapter 10) as the
"carrot." *Explorer to confirm:* the current phase names/durations/gates and the KPI list at the doc version;
note that Concept 4 is **process, not runnable CLI** — the only locally runnable pieces are
`apm install --dry-run` and `apm audit`.

---

## Cross-concept summary (for the author's mental model)

| Question | Answered by | Where it lives / fires |
|---|---|---|
| Can *every* repo install safely & predictably (not just this one)? | One team vs a fleet (Concept 1) | Enterprise ramp: Decide/Secure/Author policy/Enforce/Operate |
| How is the org rule made authoritative on every merge? | CI gating (Concept 2) | `apm audit --ci` as a required, unbypassable check (GitHub Rulesets) |
| How does dependency traffic flow in a controlled/offline network? | Registry strategy (Concept 3) | `HTTPS_PROXY` + `PROXY_REGISTRY_URL` + air-gapped `apm pack`; integrity still from the lockfile |
| How do we roll out without breaking every repo — and know it worked? | Adoption as change management (Concept 4) | Discover→Pilot→Harden→Scale→Sustain; measured by audit pass rate + drift trend |

The through-line: **one gate (Ch 6/8/9), re-run in CI and made authoritative; dependency traffic routed and
mirrored but still lockfile-verified; rolled out in owned, gated phases and measured by leading indicators.**
Every command or field the author shows must trace back to one of these four concepts — no orphan features,
and no drift into general AI-transformation content.

---

## Sources (official docs actually used)

- Enterprise overview — the third promise ("governed by policy … before it touches disk") and the five
  phases (Decide / Secure / Author policy / Enforce / Operate):
  <https://microsoft.github.io/apm/enterprise/>
- Making the case — problem-at-scale (50 repos / 200 devs / 5 tools), declare/lock/install/audit, ROI
  framework (time saved / risk reduced / consistency), objection handling, sample RFC, and the adoption
  threshold: <https://microsoft.github.io/apm/enterprise/making-the-case/>
- Adoption playbook — the five phases (Discover / Pilot / Harden / Scale / Sustain) with owners, deliverables,
  gates, KPIs, and "manifest count is vanity": <https://microsoft.github.io/apm/enterprise/adoption-playbook/>
- Enforce in CI — `apm audit --ci` as the gate (eight baseline checks + drift + discovered policy),
  defence-in-depth vs. local bypass, the minimal GitHub Actions recipe, SARIF, setup-only pattern, and the
  "no per-PR override; waivers visible in policy history" contract:
  <https://microsoft.github.io/apm/enterprise/enforce-in-ci/>
- GitHub rulesets — making the audit job a required, unbypassable status check:
  <https://microsoft.github.io/apm/enterprise/github-rulesets/>
- Drift detection — the eight non-bypassable lockfile baselines behind `--ci`:
  <https://microsoft.github.io/apm/enterprise/drift-detection/>
- Registry proxy & air-gapped — the three layered controls (`HTTPS_PROXY`, `PROXY_REGISTRY_URL`, internal
  marketplaces), `PROXY_REGISTRY_ONLY` bypass prevention, lockfile-anchored integrity, coverage gaps, and
  air-gapped `apm pack`: <https://microsoft.github.io/apm/enterprise/registry-proxy/>
- Registries guide — the dedicated (experimental) registry vs. the proxy; the Registry HTTP API:
  <https://microsoft.github.io/apm/guides/registries/>
- `apm audit` CLI reference — `--ci` mode, the `--policy` (Experimental) flag, the CI checks list, and exit
  codes: <https://microsoft.github.io/apm/reference/cli/audit/>
- CI/CD integrations — Azure Pipelines / GitLab / Jenkins / air-gapped runners (vendor-neutral gating):
  <https://microsoft.github.io/apm/integrations/ci-cd/>
- `microsoft/apm-action` — the CI/CD integration path (install/setup-only/update/pack/restore, SARIF
  `audit-report`, private-repo auth, vendor-neutral primitives); latest **v1.10.0**:
  <https://github.com/microsoft/apm-action>
- The three promises — "governed by policy" as the third promise:
  <https://microsoft.github.io/apm/concepts/the-three-promises/>
- OpenAPM v0.1 — registry HTTP API explicitly deferred to v0.2 (context for "git-based today"):
  <https://microsoft.github.io/apm/specs/openapm-v01/>

Internal cross-references for the author: `content/research/09-governance-and-policy-theory.md` (the
security-vs-governance distinction, tighten-only inheritance, and warn→block rollout this chapter scales to
the fleet); Chapter 1 (`content/chapters/the-context-problem.html`) for the "org-remote policy" framing;
Chapter 6 (lockfile/content-hash) as the integrity anchor behind the registry proxy; Chapter 10
(`apm pack`, marketplaces) as the producer inputs to Harden/Scale.

## Artifact

Written to: `content/research/11-enterprise-at-fleet-scale-theory.md`

**Empirical-confirmation flag:** This brief is **conceptual**. Treat every `Implemented in APM by:` line as a
hand-off list to verify, not settled syntax. Specifically, the `apm-cli-explorer` must confirm against
v0.23.1 (and `apm-action` v1.10.0): the exact eight `apm audit --ci` check names and exit codes; the
**Experimental** status of `--policy`; the `PROXY_REGISTRY_*` env-var names and the `PROXY_REGISTRY_ONLY`
replay-abort behavior; the `apm experimental enable registries` gate for the dedicated registry; and the
current `apm-action` inputs/outputs. The `code-verifier` should mark **`apm audit --ci` on a local repo as
runnable**, but flag **org-policy discovery, required-check wiring, registry-proxy/Artifactory, air-gapped
bundles, and CI-in-anger as `SKIPPED-needs-network`**. Keep the chapter about **operating APM at scale**, not
about general AI transformation.
