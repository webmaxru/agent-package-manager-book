# Concept Brief — Chapter 9: Governance & Policy

- **Chapter:** 9 — Governance & Policy (Part IV — Secure & governed)
- **Objective it serves:** Write and pilot an `apm-policy.yml` that enforces agent-package rules at
  install time.
- **Focus:** leader-heavy (per outline). The developer still authors and tests the policy, but the
  *decision* — which sources, MCP servers, and targets are allowed org-wide, and how strictly — is an
  engineering-leadership call. The author should carry a strong "For engineering leaders" thread
  throughout, not just in the callout.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30). **Version-awareness
  is unusually important here:** the docs mark the policy *engine* as **early preview** — "schema,
  inheritance, and discovery ship today; enforcement semantics may change between minor versions …
  Pin to a specific APM version before relying on it as a production gate"
  ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). Lockfile-based
  governance (`apm.lock.yaml`, `apm audit` baseline) is stable; `apm-policy.yml` *enforcement* is preview.
  Every feature/file/command tagged `Implemented in APM by:` is a conceptual hand-off — the
  `apm-cli-explorer` must **confirm the exact `apm-policy.yml` schema, field names, defaults, and
  enforcement behavior empirically against v0.23.1**, and the `code-verifier` must run the examples.
  Do not invent policy keys; the docs warn "do not invent others."

## Frame note (which property this chapter feeds)

This chapter delivers **governance** — the fourth of the book's four properties, and APM's third
official promise, "**governed by policy**"
([the three promises](https://microsoft.github.io/apm/concepts/the-three-promises/)). It is the
capstone of Part IV: Chapter 8 made installs *safe by default*; Chapter 9 makes them *allowed by
policy*. The two are the **same gate seen from two angles** — both fire at install time, before any
file reaches disk — but they answer different questions (Concept 1).

The single most load-bearing distinction the chapter must protect is the one Chapter 1 already
planted: **`apm-policy.yml` governs what gets installed; the agent harness governs what runs. The two
planes do not overlap** ([microsoft/apm README](https://github.com/microsoft/apm)). Governance is an
**install-time gate, not a runtime sandbox**
([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). If a reader
walks away believing policy constrains what the live agent may *do*, the chapter has failed.

## Prerequisite recap (Chapter 8 hand-off)

Chapter 8 established the **install-time trust boundary**: hidden-Unicode content scanning, content-hash
pinning, and transitive-MCP blocking all fire *before* content touches disk. Chapter 9 reuses that
exact seam. Where Chapter 8's checks are **intrinsic** ("is this artifact tampered with or dangerous by
construction?"), Chapter 9's checks are **declared by the organization** ("is this artifact permitted
*here*?"). The author should present governance as *the second half of one install gate*, not a new
subsystem bolted on. If the Chapter 8 brief/chapter is not yet written when authoring, still lean on
this framing — it is the reader's on-ramp.

## Terminology & scope notes (read before drafting)

- **"Policy" ≠ "security."** Keep the vocabulary crisp: *security* = built-in, non-negotiable integrity
  checks (Chapter 8); *governance/policy* = an org-authored allow/deny contract (`apm-policy.yml`).
  Concept 1 is entirely about not blurring these.
- **`apm-policy.yml` is an org-remote artifact, not a repo default (reinforce Chapter 1).** It "lives in
  your org's policy repo" and is "auto-discovered by `apm install` and `apm audit --ci --policy org`
  from your project's git remote"
  ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)). APM resolves the org from
  the project's git remote and searches candidate repos — `.github`, then `.apm`, then `_apm` — first
  found wins (cached, ~1-hour TTL). This is exactly the "ORG-REMOTE" point Chapter 1 made when it said
  policy "isn't a per-repo default … it's an *org-level* artifact APM discovers from your
  organization's git remote." Chapter 9 is where that promise is cashed in.
- **The trust boundary is the `<org>/.github` repo itself.** CODEOWNERS and branch protection on that
  repo are what make the policy authoritative — "the file your security team owns and your repos
  inherit" ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)).
- **Preview vs. discovery (a subtlety the author must handle honestly).** The canonical path is
  org-remote auto-discovery. But a policy can be *previewed* against a local file or URL for testing
  before it lands in `.github` — `apm audit --ci --policy ./apm-policy.yml` and
  `apm policy status --policy-source ./apm-policy.yml`
  ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)). The Meridian running example
  starts with a **repo-local** `apm-policy.yml` pilot "before turning it into an org policy"; frame that
  as *authoring-and-testing locally, then landing it org-wide*, or as a **tighten-only child policy**
  that `extends:` the org — and flag for the explorer to confirm which framing the CLI's discovery and
  precedence actually support at v0.23.1. (Note: `apm install` has **no `--policy` flag** — discovery is
  automatic; only `apm audit` and `apm policy` accept an explicit source.)

---

## Concepts covered

1. **Security vs. governance** — Chapter 8 asks "is this install *safe enough*?"; Chapter 9 asks "is
   this install *allowed here*?" Policy must sit close enough to developers to be *visible*, yet be
   *authoritative* for the organization.
2. **Install-time enforcement** — `apm-policy.yml` is evaluated when context is installed (including a
   second pass over transitive MCP), on the *same* pre-disk gate as the security checks — plus a CI
   audit gate that makes the same rules a required PR check.
3. **Tighten-only inheritance: enterprise → org → repo** — a lower level can only make policy
   *stricter*, never looser. Policy is an org-level artifact discovered from the git remote, and the
   inheritance chain composes by intersecting allows, unioning denies, and escalating enforcement.
4. **`warn` → `block` rollout** — change management, not a config toggle: start with *visibility*
   (`warn`), measure the warnings, fix the top offenders, then flip the highest-risk rules to `block`,
   so governance earns trust instead of breaking every repo on day one.

---

## Concept 1 — Security vs. governance ("is it safe?" vs. "is it allowed here?")

**Definition.** *Security* (Chapter 8) is APM's set of **intrinsic, built-in** integrity checks —
hidden-Unicode scanning, content-hash pinning, transitive-MCP blocking — that protect every install
regardless of who runs it. *Governance* is the **organization's own allow/deny contract**, written in
`apm-policy.yml`, that decides which dependency sources, MCP servers and transports, compilation
targets, and manifest shapes are *permitted in this org*. APM frames governance as its third promise —
"every AI package your developers install is governed by org policy before it touches disk"
([Enterprise overview](https://microsoft.github.io/apm/enterprise/)). Critically, policy "does not scan
code semantics or behave like an antivirus. It enforces *declarations* against an allow/deny list
before APM writes any file" ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)).

**The problem it solves.** Security answers a question with a *universal* answer (a bidi-override
character is dangerous everywhere; a tampered hash is invalid everywhere). But "may our developers
install `some-org/some-skill`?" or "is the GitHub MCP server approved?" has **no universal answer** — it
depends on the organization's risk posture, contracts, and compliance regime. Before `apm-policy.yml`,
that judgment lived in people's heads and README warnings, applied inconsistently (the exact gap
Chapter 1 named under *Governance*). Policy turns an organizational decision into a **machine-enforced,
git-tracked contract** so it is applied identically on every install and every PR.

**Key distinctions.**
- *Intrinsic vs. declared.* Security checks ship with the CLI and cannot be configured away by an org
  (only bypassed with loud, reviewable flags); governance rules are *authored* by the org and vary
  between orgs. Same gate, different source of authority.
- *Safe vs. allowed.* A package can be perfectly safe (clean scan, valid hash) yet **denied** because it
  comes from an un-vetted source; conversely, an *allowed* source still passes through the security
  scan. The two verdicts are independent and both must pass.
- *Visible to developers, authoritative for the org.* Policy is deliberately close to the developer —
  it fires on their local `apm install` and prints an inline violation with a remediation hint — yet its
  source of truth is the org's `.github` repo, protected by CODEOWNERS/branch protection, not the
  developer's checkout ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/);
  [Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). This dual
  nature is the design tension the chapter should name explicitly.

**Common misconception.** *"Governance is just more security,"* or its inverse, *"if it's allowed by
policy it must be safe."* Neither holds. Policy is not an antivirus and runs no semantic/behavioral
analysis; security is not an org-preference system. Merging them leads teams to over-trust an allow-list
(assuming allowed = safe) or to expect policy to catch a malicious *prompt* (it won't — that's the
content scanner's job, and even that only catches hidden Unicode, not intent).

**Meridian beat (for the author).** Reopen the security-review thread from Chapter 8. The platform team
can now *block* the sketchy transitive MCP server for **everyone**, not just catch it in one install:
Chapter 8 stopped a bad artifact by construction; Chapter 9 lets Meridian encode "only
`meridian-finance/**`, `microsoft/**`, and `github/awesome-copilot/**` sources are allowed, and only the
approved GitHub MCP server" as a rule the whole org inherits. Same gate, new authority.

**Implemented in APM by:** `apm-policy.yml` as the governance surface (distinct from Chapter 8's
intrinsic scanners); the "governed by policy" promise; the schema's install-time-only scope ("no fields
for runtime permissions or agent sandboxing"). *Explorer to confirm:* that policy and security are the
same install gate with different authorities, and the current top-level schema sections
(`dependencies`, `mcp`, `compilation`, `manifest`, `unmanaged_files`, `registry_source`, `security`,
`executables`).

---

## Concept 2 — Install-time enforcement (the same pre-disk gate, plus a CI audit gate)

**Definition.** `apm-policy.yml` is enforced **when context is installed**, at the same point in the
pipeline as the security checks: `apm install` "resolves the dependency tree, then runs the policy gate
against the resolved set, then writes any files. A blocking violation halts the install with a non-zero
exit code; nothing is written to disk"
([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)). This is a **preflight gate**,
not a post-hoc audit — it "protects developers who run `apm install` locally … they cannot accidentally
deploy a denied package even without CI." Enforcement is evaluated at **two points that share one set of
rules**: the local install gate, and a CI **audit gate** — `apm audit --ci --policy org` — which runs
the same policy checks *plus* the baseline lockfile checks and emits SARIF for GitHub Code Scanning
([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)).

**The problem it solves.** For agent files, "file presence is execution" — an instruction or chat-mode
file is consumed by the harness as soon as the repo is opened
([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). So the only
*reliable* place to enforce an org rule is **before the bytes land**. A gate that ran after install, or
only in CI, would leave a window where denied context is already live on a workstation. Enforcing at
install closes that window locally; adding the CI audit gate makes the rule **authoritative on every
pull request** even if a developer bypassed it locally.

**Key distinctions.**
- *Transitive MCP is gated too (this is the tie-back to Chapter 8).* When an APM package pulls in its own
  MCP dependencies, those are resolved and then passed through a **second policy preflight** so "no
  transitive MCP server reaches your runtime config without passing the same `mcp.*` rules as a direct
  one" ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). The
  `mcp.allow` / `mcp.deny` / `mcp.transport` rules apply to *both* direct and transitive servers. **Do
  not conflate this with the `mcp.trust_transitive` policy field**, which the docs state is "parsed but
  not enforced" — the actual transitive gate is the `--trust-transitive-mcp` CLI flag (defaults to deny)
  ([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)). The author must state this
  precisely or risk a false claim; the explorer must confirm.
- *Install gate vs. CI audit gate.* Both use the same policy file and merge semantics. The install gate
  can *block* locally; the CI gate is what you wire into **branch protection** as a required check, and
  it is the *only* enforcer of the "audit-only" rules (e.g. `required_fields`, `scripts`,
  `unmanaged_files`, source attribution) that the install gate does not check
  ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). Keep the
  fleet-scale CI wiring light here — it is Chapter 11's subject — but name `apm audit --ci --policy` as
  the PR gate.
- *What install enforcement does **not** cover.* `apm compile`, `apm run`, and `apm pack` "enforce zero
  policy" — they trust the artifacts `apm install` already placed on disk
  ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). This is the
  exhaustive-enforcement-points fact, and it reinforces "install-time, not runtime."
- *Enforcement is bypassable — loudly.* `apm install --no-policy` and `APM_POLICY_DISABLE=1` skip the
  gate; these are "break-glass," print loudly, and appear in the PR diff / CI logs — while the baseline
  lockfile checks in `apm audit --ci` remain non-bypassable
  ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). The author
  should mention the escape hatch honestly rather than overclaim an unbreakable gate.

**Common misconception.** *"Policy is a CI-only thing,"* or *"the org policy only bites in the pipeline."*
In fact it fires first on the developer's own machine, before any file is written — which is *why* a
denied package can't quietly deploy locally. CI is the *authoritative* enforcement point for merges, but
it is not the *only* one.

**Meridian beat (for the author).** Show the gate firing on a normal `apm install`: a developer adds a
dependency from a denied source, and the install halts with a single-line
`[x] Policy violation: … -- denied by pattern: …` plus a hint to run `apm audit --ci --policy org` for
the full report — before anything reaches disk. Then show the same finding surfacing as a SARIF alert on
the PR once `apm audit --ci --policy org` is a required check.

**Implemented in APM by:** the install-time **preflight gate** in `apm install` (resolve → gate → write;
non-zero exit on block; nothing written); the **transitive-MCP second pass** applying `mcp.*` rules; the
CI audit gate `apm audit --ci --policy org` (same policy checks + baseline lockfile checks; SARIF);
`apm policy status` for diagnosis; bypasses `--no-policy` / `APM_POLICY_DISABLE=1`. *Explorer to
confirm:* the exact enforcement points, which rules are install-enforced vs. audit-only, the transitive
`mcp.*` behavior and the `mcp.trust_transitive`-is-parsed-not-enforced nuance, and current exit codes /
message text.

---

## Concept 3 — Tighten-only inheritance: enterprise → org → repo

**Definition.** Policies compose along a chain — canonically **enterprise hub → org policy → repo
override** — and the merge is **tighten-only**: "children can only tighten rules, never relax them … a
repo can be more restrictive than the org, but cannot widen what the org has allowed"
([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/)). Because `apm-policy.yml` is
discovered from the org git remote (Concept 1 / Chapter 1), the *default* authority is the org level;
lower levels may extend it via `extends:` up to a maximum chain depth of 5, and cross-host `extends:` is
refused as a credential-leakage mitigation
([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)).

**The problem it solves.** At fleet scale you need one authoritative baseline *and* the ability for a
high-risk team to add stricter rules — without any risk that a repo can quietly *loosen* the org's
guarantees. A naïve "child overrides parent" model would let any repo re-open a denied source. Tighten-only
composition guarantees that **the effective policy is always at least as strict as every level above it**,
so a CISO can reason about the floor once and trust that no downstream config erodes it.

**Key distinctions (the merge rules, in plain English).** The author can present these as a small table;
they are the concrete meaning of "tighten-only"
([Policy files](https://microsoft.github.io/apm/enterprise/apm-policy/);
[Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)):
- **allow lists → intersect** — a child sees only entries present in *both* parent and child (a child
  can *narrow* an allow-list, never widen it).
- **deny lists → union** — a child *adds* to the parent's denies; it can never remove one.
- **`enforcement` → escalates** on the order `off < warn < block` via `max(parent, child)` — a child can
  move `warn → block`, never the reverse (this is the mechanism Concept 4 exploits for staged rollout).
- **`max_depth` → `min(parent, child)`** — the smaller (stricter) transitive-depth cap wins.
- **`require_pinned_constraint` → logical OR** — if any level requires pinning, it is required.

Two more distinctions worth drawing:
- *Org-remote default vs. repo-local file.* The org policy is auto-discovered; a repo-level
  `apm-policy.yml` is understood as a tighten-only *child*, not a replacement. This is the reconciliation
  the author needs for the Meridian pilot (see the scope note above) — confirm framing with the explorer.
- *"Exceptions" are granted upward, not downward.* Because inheritance is tighten-only, a repo cannot
  waive a rule for itself; the only way to exempt a repo is to **relax the rule at the parent level**
  (narrow a `deny` glob or add the package to `dependencies.allow`), documented in the policy file
  itself — "that file is your audit log"
  ([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)). APM has no first-class
  waiver field.

**Common misconception.** *"A repo can override the org policy to unblock itself."* It cannot. A child
attempting to drop the org's `block` back to `warn`, or to re-allow a denied source, is **rejected** —
"org policy is block; child cannot relax"
([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). Overrides flow in
exactly one direction: stricter.

**Meridian beat (for the author).** Meridian starts with a single policy for the `meridian-checkout`
pilot, but the author should foreshadow scale: when the platform team later rolls governance to three
product groups (Chapter 11), the checkout repo's stricter rules can *coexist* with a broader org baseline
precisely because inheritance only tightens. The pilot policy becomes the org floor; a high-risk repo can
add to it, never subtract.

**Implemented in APM by:** the `extends:` chain (enterprise hub → org → repo; max depth 5; cross-host
refused); the tighten-only merge (allow=intersect, deny=union, `enforcement`=max, `max_depth`=min,
`require_pinned_constraint`=OR); org-remote discovery (`.github` / `.apm` / `_apm`); `apm policy status`
to inspect the *effective* merged policy. *Explorer to confirm:* the full per-field merge table
(including `mcp.self_defined`, `manifest.scripts`, `unmanaged_files.action`, `require_resolution`),
repo-local-vs-child precedence, and the exact discovery order/precedence at v0.23.1.

---

## Concept 4 — `warn` → `block` rollout (change management, not a toggle)

**Definition.** APM's `enforcement` field has three modes — **`off`**, **`warn`**, **`block`** — and the
recommended rollout is to author a new rule in `warn`, measure, remediate, then escalate to `block`
([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)). In `warn`, "every check runs;
each violation is reported; install proceeds" (exit 0); in `block`, the same checks run but a violation
"aborts with a non-zero exit code." The dial is the **top-level `enforcement`** field; per-rule modes
exist only for two sub-fields (`mcp.self_defined`: `allow|warn|deny`; `unmanaged_files.action`:
`ignore|warn|deny`) — every other rule inherits the top-level setting
([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)).

**The problem it solves.** A new rule is **retroactive**: "the next `apm install` in every consuming repo
runs the new rule against dependencies that were legal yesterday. If you flip straight to
`enforcement: block`, every CI job on every repo that already has a violation fails on its next run … You
will spend the day rolling back instead of rolling out"
([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)). Warn-first rollout converts a
potentially org-breaking change into a measured migration: governance **earns trust** by making the
problem *visible* before it becomes *blocking*.

**Key distinctions.**
- *The four-step sequence.* (1) **Author in `warn`** in `<org>/.github/apm-policy.yml`; nothing breaks.
  (2) **Read the warning telemetry** — from `apm install` output, from `apm audit --ci --policy org`
  SARIF in CI (the canonical way to collect a fleet-wide violation list), and from `apm install
  --dry-run` locally. (3) **Remediate** — upgrade/replace the offending dependency (the default fix), or
  grant an exception by relaxing the rule *at the parent level*, or use `--no-policy` as loud
  break-glass. (4) **Flip to `block`** once the violation count is zero (or surviving violations are
  documented exceptions) ([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)).
- *"Block narrowly," not "block everything."* There is **no per-rule `enforcement` knob** — top-level
  `enforcement` applies uniformly. To make one high-risk rule block while others still warn, you either
  **stage rules** (land rule A in `warn`, clean it, add rule B in `warn`, then flip the whole file to
  `block`) or **split policies via `extends:`** so a strict child escalates `warn → block` for its scope
  only ([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)). This is the accurate
  mechanism behind the playbook's "block the highest-risk cases first."
- *`warn` mode is quiet in CI — a trap to flag.* In `warn` mode `apm audit --ci` "rewrites violations to
  `passed=True` so the exit code stays 0. CI does not fail. The visibility is in the SARIF + Code
  Scanning UI, not in the green/red check"
  ([Governance deep-dive](https://microsoft.github.io/apm/enterprise/governance-guide/)). The team must
  watch Code Scanning during the warn phase and not read "CI green" as "no violations."
- *Rollback is cheap; a blocked org is not.* Flipping back to `warn`/`off` propagates within the cache
  TTL; the docs advise rolling back and fixing forward if a violation surge reveals legitimate use you
  missed ([Policy pilot](https://microsoft.github.io/apm/enterprise/policy-pilot/)).

**Common misconception.** *"Turn on the policy = flip to `block`."* Treating enforcement as a binary
on/off switch is exactly the day-one-breakage failure the pilot page warns against. `warn` is not a
lesser or throwaway mode — it is the **measurement phase** that makes `block` safe. A second misconception:
*"warn mode fails CI so I'll see red" — it does not;* warn-mode audit exits 0, and visibility lives in
SARIF/Code Scanning.

**Meridian beat (for the author) — the chapter's core story.** This is the running-example spine for
Chapter 9. Meridian's platform team ships an org policy in **`warn`** targeting the two things the
earlier chapters exposed: **unpinned dependencies** (`require_pinned_constraint`) and **unapproved MCP
servers** (`mcp.allow` / `mcp.deny`). For **two sprints** they watch the warnings roll in via SARIF, fix
the top offenders (pin the moving refs from Chapter 6; drop or approve the MCP servers from Chapter 8),
and only then flip the **highest-risk rules to `block`** — narrowly, via staged rules, so the rest of the
org keeps warning while the dangerous cases fail closed. Governance earns trust instead of breaking every
repo on day one. (The author should present the *pilot* `apm-policy.yml` and the *post-pilot* `block`
version as a before/after pair, matching the running-example spec — and mark them illustrative until the
`code-verifier` confirms the schema.)

**Implemented in APM by:** the top-level `enforcement: off | warn | block` field; per-rule modes on
`mcp.self_defined` and `unmanaged_files.action`; the warn→measure→remediate→block sequence; SARIF
telemetry via `apm audit --ci --policy org -f sarif`; `apm install --dry-run` for local preview;
`apm policy status --check` as a CI pre-flight; staged-rules / `extends:` as the way to block narrowly.
*Explorer to confirm:* the exact mode names and semantics, the two per-rule sub-fields, the warn-mode
"exit 0 / passed=True" CI behavior, and the dry-run message text at v0.23.1.

---

## Cross-concept summary (for the author's mental model)

| Question | Answered by | Where enforced |
|---|---|---|
| Is this artifact tampered with / dangerous by construction? | Security (Ch 8, intrinsic) | Install gate (pre-disk) |
| Is this artifact **allowed here**? | Governance (`apm-policy.yml`, org-authored) | Install gate **and** `apm audit --ci` |
| Whose rules apply, and can a repo loosen them? | Tighten-only inheritance (ent → org → repo) | Merged effective policy at every enforcement point |
| How do we turn a rule on without breaking everyone? | `warn` → measure → remediate → `block` | Top-level `enforcement` (staged/`extends:` to narrow) |

The through-line: **one install gate, org authority, tighten-only, rolled out by measurement.** Every
command or field the author shows must trace back to one of these four concepts — no orphan features.

---

## Sources (official docs actually used)

- Enterprise overview — governance as the third promise, the five phases (Decide / Secure / Author
  policy / Enforce / Operate): <https://microsoft.github.io/apm/enterprise/>
- Policy files (`apm-policy.yml` mental model — what it is, org-remote discovery `.github`/`.apm`/`_apm`,
  install + CI enforcement points, tighten-only inheritance, minimal policy, "schema in one screen"):
  <https://microsoft.github.io/apm/enterprise/apm-policy/>
- Policy pilot (three modes; why pilot first; the warn → measure → remediate → block sequence; per-rule
  vs. whole-policy flips; rollback): <https://microsoft.github.io/apm/enterprise/policy-pilot/>
- Governance deep-dive (security-vs-governance trust contract; four enforcement points; what you can /
  cannot govern; tighten-only merge rules; install-gate guarantees; bypass contract; early-preview
  status): <https://microsoft.github.io/apm/enterprise/governance-guide/>
- The three promises (portable by manifest, secure by default, **governed by policy**):
  <https://microsoft.github.io/apm/concepts/the-three-promises/>
- microsoft/apm README ("apm-policy.yml governs what gets installed; your agent harness governs what
  runs. The two planes do not overlap."): <https://github.com/microsoft/apm>
- Policy reference — **for the explorer to confirm the complete schema, every field, and the merge
  table** (not yet mined in detail here): <https://microsoft.github.io/apm/enterprise/policy-reference/>
- Supporting CLI references to confirm: `apm audit`
  (<https://microsoft.github.io/apm/reference/cli/audit/>), `apm policy`
  (<https://microsoft.github.io/apm/reference/cli/policy/>).

Chapter 1 (`content/chapters/the-context-problem.html`) is the internal cross-reference for the
"apm-policy.yml is ORG-REMOTE, discovered from the org git remote" framing reinforced throughout. No
Chapter 8 theory artifact exists yet at time of writing; the security↔governance distinction here is
grounded directly in the official docs above.

## Artifact

Written to: `content/research/09-governance-and-policy-theory.md`

**Empirical-confirmation flag:** This brief is **conceptual**. The exact `apm-policy.yml` schema (field
names, nesting, defaults), the precise enforcement points and modes, the inheritance/merge table, and
all command flags are **early preview** at v0.23.1 and **must be confirmed empirically by the
`apm-cli-explorer`** (against the installed CLI and the Policy Reference) and **run by the
`code-verifier`** before any of it appears in the authored chapter. Treat every `Implemented in APM by:`
line as a hand-off list to verify, not as settled syntax.
