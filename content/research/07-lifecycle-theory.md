# Concept Brief — Chapter 7: Lifecycle

- **Chapter:** 7 — Lifecycle (Part III — Reproducible by lockfile)
- **Objective it serves:** Keep APM dependencies current while detecting drift and risk deliberately.
- **Inspected APM CLI version:** v0.23.1 (official docs last updated 2026-06-30; v0.23 is the "lifecycle
  hooks" release). Feature/file/command names tagged `Implemented in APM by:` are conceptual hand-offs —
  the `apm-cli-explorer` confirms exact flags, precedence, prompts, and exit codes; the `code-verifier`
  runs them.
- **Frame note (which property this chapter feeds).** This chapter completes **reproducibility**. Chapter 6
  made a setup *frozen* — byte-for-byte restorable from the lockfile. Chapter 7 answers the obvious next
  worry: *if everything is pinned, how does anything ever move forward — safely?* The lifecycle loop is how
  a team keeps agent context **fresh without giving up frozen**: see what has drifted from upstream, change
  it on purpose, and verify the result is intact. It also touches **provenance/security** (the `apm audit`
  integrity check), previewing Chapter 8.
- **Prerequisite recap.** Chapter 2 warned that unpinned, moving refs are a liability; Chapter 6 delivered
  the lockfile, byte-for-byte restore, and `apm install --frozen` (the `npm ci` cousin). Chapter 7 layers a
  *maintenance* loop on top of that reproducible baseline. It is the agent-context equivalent of ordinary
  application-dependency upkeep.
- **Terminology note (avoid a name clash).** APM's docs use the word *lifecycle* two ways. The broad sense
  (the `concepts/lifecycle/` page) is the whole `init → install → compile → run → audit` flow. This chapter
  uses the narrower, everyday sense: the **maintenance triad** the consumer overview files under
  *"lifecycle automation (`update`, `outdated`, `audit`)"* — the deliberate upkeep motions that sit *outside*
  the daily four-command loop from Chapter 5
  ([Use APM packages](https://microsoft.github.io/apm/consumer/)). The author should make that scope
  explicit so readers don't conflate "the lifecycle" with "these three commands."
- **One flag to bust up front: `apm audit` is *not* `npm audit`.** It has **no CVE database** and reports no
  "known vulnerabilities." It is an integrity/safety check — hidden-Unicode scanning plus lockfile/drift
  consistency — not a vulnerability feed
  ([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)). This is the single most important
  misconception the chapter must prevent, and it recurs in Concept 2.

---

## Concepts covered

1. **Reproducibility must not become stagnation** — a frozen setup still needs a deliberate maintenance
   loop: *see what is stale → change it on purpose → check it is safe*. The agent-context analogue of
   routine dependency upkeep.
2. **The three lifecycle verbs** — `apm outdated` (report drift from upstream; **read-only**), `apm update`
   (the **explicit change**: re-resolve refs, rewrite the lockfile, behind a consent gate), and `apm audit`
   (the **integrity/safety** check: hidden-Unicode + lockfile/drift consistency — **not** a CVE feed).
3. **Refresh known deps vs. casually accepting drift** — `apm install` *restores* locked bytes; `apm update`
   is the *deliberate act* of moving; unpinned or moving refs drift **silently** until you update. Ties back
   to Chapter 2's unpinned warning and Chapter 6's `--frozen`.
4. **Ownership and cadence** — who owns the update rhythm, and the **lockfile diff as the review artifact**
   that makes an agent-context change reviewable like any dependency bump.

---

## Concept 1 — Reproducibility must not become stagnation

**Definition.** A lifecycle loop is the deliberate maintenance rhythm that keeps a *pinned* project current
without surrendering its pinning. In APM it is a three-beat motion layered on the reproducible baseline:
**inspect** what has moved upstream (`apm outdated`), **change** on purpose (`apm update`), then **verify**
integrity (`apm audit`). The consumer overview draws the boundary explicitly — the everyday four-command
loop is one thing, and *"everything else is either lifecycle automation (`update`, `outdated`, `audit`) or a
workflow extension"* ([Use APM packages](https://microsoft.github.io/apm/consumer/)). The broader lifecycle
concept page frames the cadence: you use *"`install` and `run` daily, `audit` in CI, and `init` and
`compile` rarely,"* with audit looping *"back to install (fix drift)"*
([Lifecycle](https://microsoft.github.io/apm/concepts/lifecycle/)).

**The problem it solves.** Chapter 6 solved "works on my machine" by freezing the dependency graph — but a
frozen graph, left alone, quietly rots. Upstream skills gain fixes, prompts get sharper, instructions track
new conventions; a project pinned six months ago is reproducible *and stale*. The failure mode inverts:
instead of silent drift you get silent staleness. Reproducibility is a floor, not a ceiling. The lifecycle
loop is what lets a team move off an old-but-known-good pin **on purpose and in the open**, rather than
either (a) never updating, or (b) chasing `main` and reintroducing the drift APM exists to kill.

**Key distinctions.**
- *Frozen vs. stale.* Chapter 6's `--frozen` guarantees a restore matches the lockfile; it says nothing
  about whether the lockfile is *current*. "Reproducible" and "up to date" are independent properties — the
  lifecycle loop is how you improve the second without losing the first.
- *Restore is not maintenance.* Bare `apm install` reproduces; it never bumps versions
  ([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)). Maintenance is a
  separate, consent-gated act (Concept 2). Conflating them is the error Concept 3 dismantles.
- *Lifecycle automation vs. the daily loop.* `outdated`/`update`/`audit` are real and important but
  *deliberate* — periodic upkeep, not everyday motions. The docs and this book both file them outside the
  four-command habit ([Use APM packages](https://microsoft.github.io/apm/consumer/)).

**Common misconception.** *"Once it's locked, I'm done — pinning is the whole story."* Pinning is the
*baseline*, not the finish line. A lockfile that is never revisited becomes a liability of a different kind:
outdated guidance, unpatched upstream content, and a growing gap from the sources of truth. Maintenance is
part of reproducibility, not a betrayal of it.

**Meridian beat (for the author).** Frame the chapter as the team's *first birthday* with a locked setup.
`meridian-checkout` has been reproducible for a quarter (Chapter 6), and it shows: the fraud-review skill
they pinned has three upstream releases they've never seen. Rather than let the pin rot or blindly track a
branch, the staff engineer institutes a **monthly agent-context refresh** — the loop this chapter teaches.

**Implemented in APM by:** the *"lifecycle automation"* triad `apm outdated` → `apm update` → `apm audit`,
sitting on top of the `apm.lock.yaml` baseline from Chapter 6. (Scope and grouping confirmed by the
explorer against v0.23.1.)

---

## Concept 2 — The three lifecycle verbs

**Definition.** APM splits maintenance into three single-purpose commands so that *reporting*, *changing*,
and *verifying* never blur together.

- **`apm outdated` — report drift from upstream (read-only).** It *"reads `apm.lock.yaml` and queries each
  remote to detect staleness"* and is explicitly *"read-only: this command does not modify `apm.lock.yaml`
  or touch `apm_modules/`"* ([apm outdated](https://microsoft.github.io/apm/reference/cli/outdated/)). It
  labels each dependency `up-to-date`, `outdated`, or `unknown`, and — being a report — *"finding outdated
  deps is not an error and does not change the exit code"* (exit `0` even with stale deps; exit `1` only when
  there is no lockfile) ([apm outdated](https://microsoft.github.io/apm/reference/cli/outdated/)).
- **`apm update` — the explicit change.** It *"re-resolves every dependency in your project's `apm.yml`
  against the newest version or Git ref allowed by its constraint, prints a structured plan — added,
  updated, removed, unchanged — and prompts before touching anything"*
  ([apm update](https://microsoft.github.io/apm/reference/cli/update/)). This is *"the command that actually
  changes versions in your project"* ([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)):
  it rewrites `apm.lock.yaml` (and, for revision pins, `apm.yml`) and redeploys.
- **`apm audit` — the integrity/safety check.** It is *"the explicit security and integrity tool,"* running
  a **content scan** (hidden Unicode in deployed prompt/instruction/skill/rules files) plus an
  **install-replay drift** check, with a machine-readable **CI gate** mode (`--ci`) for lockfile-consistency
  checks ([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)). Crucially, this protection
  *"already runs automatically in `apm install`"* — `apm audit` is the *on-demand* re-verification, not a
  gate you must remember to call to be safe ([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)).

**The problem it solves.** Bundling "what's new?", "change it," and "is it intact?" into one command is how
package managers historically made updates scary — you never knew what a single verb would touch. APM's
three verbs make each step *observable and reversible on its own*: you can see the drift without changing
anything, preview and consent to a change, and verify integrity independently. Reporting, mutation, and
verification are kept apart on purpose.

**Key distinctions.**
- *Read-only vs. mutating vs. verifying.* `outdated` never writes; `update` is the only one of the three
  that rewrites the lockfile/manifest and redeploys; `audit` inspects and (only with an explicit `--strip`)
  remediates. Three verbs, three blast radii.
- *`apm update` is consent-gated.* The prompt *"defaults to No,"* and *"in non-interactive contexts (CI,
  piped stdin) you must pass `--yes` to proceed"*; decline and *"APM exits cleanly: no manifest rewrite, no
  lockfile write, no filesystem changes"* ([apm update](https://microsoft.github.io/apm/reference/cli/update/)).
  `--dry-run` *"computes and prints the plan … but never writes and never asks"* — the safe preview
  ([apm update](https://microsoft.github.io/apm/reference/cli/update/)).
- *`apm update` ≠ `apm self-update`.* `apm update` refreshes **project dependencies**; upgrading the **CLI
  binary** is a different command, `apm self-update`
  ([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)). (Historical note the
  author can drop in a sidebar: `apm update` *used* to be the self-updater and was repurposed; a deprecation
  shim forwards for one release — ([apm update](https://microsoft.github.io/apm/reference/cli/update/)).)
- **`apm audit` is not `npm audit`.** It ships **no CVE/vulnerability database** and reports no "known
  advisories." Its checks are *content integrity* (hidden Unicode — zero-width, bidi overrides, tag
  characters) and *lockfile/drift consistency* (the `--ci` baseline: lockfile presence, ref consistency,
  deployed-files presence, no orphaned packages, content integrity via per-file SHA-256, and so on)
  ([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)). The only path to
  vulnerability-style analysis is opt-in **experimental external scanners** (e.g. SkillSpector / SARIF
  ingestion), which underlines that APM itself is not a CVE feed
  ([apm audit](https://microsoft.github.io/apm/reference/cli/audit/)).
- *Where CI fits (kept light here).* `outdated` deliberately does **not** gate CI — the docs say to *"wire
  `apm audit` into CI instead if you want gating"*
  ([apm outdated](https://microsoft.github.io/apm/reference/cli/outdated/)). Name `apm audit --ci` as the
  gate and stop there; the fleet-scale CI story is Chapter 11.

**Common misconception.** *"`apm audit` scans my agent packages for known CVEs like `npm audit` does."* No —
there is no vulnerability database behind it. It checks for **invisible/hidden-Unicode content** and
**lockfile/deploy drift**; a clean `apm audit` means "no hidden characters and nothing has drifted from the
lockfile," **not** "no known vulnerabilities." Treating it as a CVE gate would give a false sense of
coverage.

**Meridian beat (for the author).** Walk the monthly refresh through all three verbs in order: the staff
engineer runs `apm outdated` and sees the pinned fraud-review skill flagged `outdated` (a newer tag exists);
runs `apm update --dry-run` to read the plan, then `apm update` (or `--yes` in the scheduled job) to move it
and rewrite `apm.lock.yaml`; finishes with `apm audit` to confirm no hidden Unicode slipped in and nothing
drifted. Report → change → verify, made concrete.

**Implemented in APM by:** `apm outdated` (read-only staleness report; `up-to-date`/`outdated`/`unknown`;
exit `0` when stale, `1` when no lockfile); `apm update` `[--dry-run]` `[--yes]` (re-resolve to newest
allowed ref; structured added/updated/removed/unchanged plan; consent gate defaulting to No; rewrites
lockfile/manifest); `apm audit` `[--ci]` `[--strip]` (hidden-Unicode content scan + install-replay drift;
`--ci` lockfile-consistency gate; **no CVE database**). Distinct from `apm self-update` (CLI binary).
(Exact flags, plan sections, prompt text, and the `--ci` check list confirmed by the explorer.)

---

## Concept 3 — Refresh known deps vs. casually accepting drift

**Definition.** APM draws a hard line between **reproducing** what is already pinned and **moving** to
something newer. Plain `apm install` is a *sync*: *"with no flags, `apm install` reproduces exactly the
versions pinned in `apm.lock.yaml`"* and *"never silently bumps versions"*
([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)). Moving is a separate,
deliberate operation — `apm update` — and APM even nudges toward it without ever doing it for you: when the
lockfile is already satisfied, install prints *"`[i] Run 'apm update' to check for newer versions.`"* —
*"that is the nudge: install never silently bumps versions"*
([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)).

**The problem it solves.** The whole point of a lockfile is defeated if any routine command can quietly
change what you're running. By making `install` a pure restore and `update` the only mutation, APM ensures
that a version change is always a *chosen, visible* event — never a side effect of onboarding, CI, or a
teammate's clone. This is the discipline that keeps "reproducible" true in practice, not just on paper.

**Key distinctions.**
- *Restore (`apm install`) vs. refresh (`apm update`).* Restore replays the pinned set; refresh re-resolves
  to the newest allowed ref and re-locks. *"Reproduce the locked versions exactly → `apm install`; Bump deps
  and rewrite the lockfile → `apm update`"*
  ([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)).
- *Silent drift is a property of the ref, not the command.* A tag or full SHA is immutable; a **branch
  moves**. *"Branches move; tags and SHAs do not. For reproducibility, prefer tags or SHAs,"* and a
  branch-pinned dep *"will resolve to a new SHA on the next `apm update`"*
  ([Manage dependencies](https://microsoft.github.io/apm/consumer/manage-dependencies/)). The lockfile still
  pins a concrete commit either way — so two clones match today — but a moving ref means *tomorrow's*
  `apm update` legitimately changes it. This is exactly the unpinned hazard Chapter 2 flagged, now shown in
  its lifecycle consequence.
- *`--frozen` is the anti-drift guardrail (from Chapter 6).* `apm install --frozen` is the lockfile-only,
  fail-on-drift install for CI, and it is *"mutually exclusive with `--update`: one trusts the lockfile, the
  other rewrites it"* ([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)).
  Naming both here crystallizes the split: `--frozen` enforces "don't move"; `update` performs "move on
  purpose."
- *`--force` is not an update.* A common trap: *"`apm install --force` does not refresh remote refs. It only
  bypasses the security gate for an already-resolved set. If you want new commit SHAs, run `apm update`"*
  ([Update and refresh](https://microsoft.github.io/apm/consumer/update-and-refresh/)). "Force" changes
  *whether a scan blocks you*, not *which version you get*.

**Common misconception.** *"Re-running `apm install` (or adding `--force`) will pull the latest versions."*
Neither does. Bare install restores the pinned set and only *nudges* you toward `apm update`; `--force`
bypasses the security gate for the already-resolved set. Upgrading is always an explicit `apm update`.

**Meridian beat (for the author).** Use the refresh to *retire a moving ref*. During review the team notices
the public review-and-refactor skill is still pinned to `#main` (a leftover from Chapter 5's convenience
install) — the very thing that will keep silently re-resolving on every `apm update`. The optional manifest
refinement is to replace the branch with a verified tag or full SHA, converting a silently-drifting
dependency into a deliberately-versioned one. (Pin the exact ref only once the `code-verifier` confirms a
real tag/SHA.)

**Implemented in APM by:** bare `apm install` (restore/sync; the *"Run 'apm update' …"* nudge; never bumps);
`apm install --frozen` (fail-on-drift, mutually exclusive with `--update` — Chapter 6); `apm update` (the
only version-moving verb); ref choice in `apm.yml` (immutable tag/SHA vs. moving branch) as the true lever
on drift. (Nudge text, `--frozen`/`--update` exclusivity, and `--force` semantics confirmed by the
explorer.)

---

## Concept 4 — Ownership and cadence (the lockfile diff as the review artifact)

**Definition.** Because `apm update` is deliberate and consent-gated, a version bump becomes a **reviewable
change**: it lands as a diff to `apm.yml` (when refs or revision pins change) and to `apm.lock.yaml` (always
— new resolved commits, content hashes, and per-file hashes). The lockfile is the artifact reviewers read:
it is plain YAML you can *"use … to answer 'what version am I actually running?' without trusting the
manifest, which may have floating refs"*
([Manage dependencies](https://microsoft.github.io/apm/consumer/manage-dependencies/)). APM even frames the
review mental model directly: for SHA-pinned deps, *"think of `apm update` as Dependabot-style review for AI
packages: the manifest stays pinned to a commit, while the comment shows the release tag"*
([Manage dependencies](https://microsoft.github.io/apm/consumer/manage-dependencies/)).

**The problem it solves.** Maintenance that nobody owns doesn't happen — and updates that land without review
reintroduce risk. Two questions decide whether the lifecycle loop actually protects a team: *who runs it, and
how often?* and *how does a reviewer judge the change?* APM answers the second structurally (the lockfile
diff), which lets an organization answer the first as policy: assign a cadence and an owner, and route every
refresh through a pull request where the diff tells the story.

**Key distinctions.**
- *Manifest diff vs. lockfile diff.* The `apm.yml` diff shows *intent* (which refs/constraints changed); the
  `apm.lock.yaml` diff shows *effect* (which exact commits and content hashes changed). Reviewers should read
  both — intent explains *why*, the lockfile proves *what*
  ([Manage dependencies](https://microsoft.github.io/apm/consumer/manage-dependencies/)). This is the same
  two-file review the book has built toward since Chapter 4.
- *Do not hand-edit the lockfile.* It is a generated artifact — *"regenerated on every install; any manual
  change is overwritten or … will trip `apm audit`"*
  ([Manage dependencies](https://microsoft.github.io/apm/consumer/manage-dependencies/)). The review target
  is the *generated* diff from a real `apm update`, never a hand-tweak.
- *Cadence is a choice, not a default.* APM supplies the tools (`outdated` to surface staleness, `update` to
  act, `audit` to verify) but does not impose a schedule. The team decides the rhythm — the monthly refresh
  is Meridian's answer, not a product setting.
- *Ownership is an org decision (leader track).* The mapping of *who* owns the cadence — application team,
  platform team, or security enablement — is the leader-facing question, expanded below.

**Common misconception.** *"An agent-context update is invisible / not really reviewable."* The opposite is
true by construction: every deliberate `apm update` produces a concrete `apm.lock.yaml` diff (resolved
commits + content hashes) that a reviewer can inspect exactly like an application-dependency bump. The change
is as visible as the team's PR discipline makes it.

**Meridian beat (for the author).** Land the chapter's headline artifact: the staff engineer's monthly
refresh becomes a **pull request** where reviewers inspect *both* the `apm.yml` change (the fraud-review
skill moved to a newer tag) *and* the `apm.lock.yaml` diff (new resolved commit + content hash), with the
`apm audit` result attached as evidence the update is intact. The refresh is a normal, reviewable code change
— not a background mystery.

**For engineering leaders (callout seed).** Lifecycle work needs an **owner and a cadence**. Decide whether
the application team, the platform team, or security enablement owns update timing, and how stale agent
dependencies get reported (e.g., a scheduled `apm outdated` surfacing drift). The payoff is auditability: the
`apm.lock.yaml` diff answers *"what changed in our agent context, when, and who approved it?"* in the same
review surface as application dependencies — and `apm audit` (later `apm audit --ci`, Chapter 11) gives a
machine-checkable integrity signal without becoming a CVE feed it isn't.

**Implemented in APM by:** the reviewable `apm.yml` + `apm.lock.yaml` diffs produced by a deliberate
`apm update`; the lockfile's resolved-commit / content-hash / per-file-hash records as the review substance;
the "generated, never hand-edited" rule enforced by `apm audit`; `apm outdated` as the drift-reporting input
to a chosen cadence. (Diff contents, lockfile fields, and audit's hand-edit detection confirmed by the
explorer against v0.23.1.)

---

## Sources

Official APM documentation — CLI reference (behavior of the three verbs):
- apm outdated (read-only staleness report; `up-to-date`/`outdated`/`unknown` status; exit `0` when stale
  and `1` when no lockfile; *"wire `apm audit` into CI instead if you want gating"*) —
  <https://microsoft.github.io/apm/reference/cli/outdated/>
- apm update (re-resolve to newest allowed ref; structured added/updated/removed/unchanged plan; consent
  gate defaults to No, `--yes` for non-interactive, `--dry-run` never writes; revision-pin SHA→tag rewrite;
  back-compat with the former self-updater) — <https://microsoft.github.io/apm/reference/cli/update/>
- apm audit (two modes — content scan for hidden Unicode + install-replay drift, and `--ci` lockfile
  consistency; protection already runs inside `apm install`; **no CVE database**; experimental external
  scanners) — <https://microsoft.github.io/apm/reference/cli/audit/>

Official APM documentation — consumer ramp (framing + when-to-use-which):
- Use APM packages / consumer overview (*"lifecycle automation (`update`, `outdated`, `audit`)"* as distinct
  from the daily four-command loop) — <https://microsoft.github.io/apm/consumer/>
- Update and refresh (`apm install` is a sync that *"never silently bumps versions"*; the *"Run 'apm update'
  …"* nudge; the when-to-use-which table; `--frozen` mutually exclusive with `--update`; `--force` doesn't
  refresh refs; `apm update` ≠ `apm self-update`) —
  <https://microsoft.github.io/apm/consumer/update-and-refresh/>
- Manage dependencies (the lockfile as the *"what am I actually running?"* review artifact; commit-it /
  don't-hand-edit / inspect-freely; *"Dependabot-style review for AI packages"*; branches move, tags/SHAs
  don't) — <https://microsoft.github.io/apm/consumer/manage-dependencies/>
- Drift and secure by default (what runs on every install; on-demand `apm audit`; drift kinds
  unintegrated/modified/orphaned; hidden-Unicode scan scope) —
  <https://microsoft.github.io/apm/consumer/drift-and-secure-by-default/>

Official APM documentation — concepts (cadence framing):
- Lifecycle (the broad `init → install → compile → run → audit` flow; *"`install` and `run` daily, `audit`
  in CI"*; audit loops back to install to fix drift) —
  <https://microsoft.github.io/apm/concepts/lifecycle/>

---

## Artifact path

`content/research/07-lifecycle-theory.md`
