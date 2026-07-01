# Book Brief — The Missing Package Manager

*Working title: **The Missing Package Manager — Managing AI Agent Context with APM**.*

This is the **source of truth for scope, intent, and reader experience**. The `book-architect`
reads this first and designs the table of contents *within these constraints* — it does not invent
scope from scratch, and it does not water down the narrative devices below. Those devices are what
make this book worth reading instead of the docs; protect them. Edit this file to change what the
fleet builds.

## Subject
**Agent Package Manager (APM)** — an open-source dependency manager for AI agents. You declare the
skills, prompts, instructions, agents, plugins, and MCP servers your project needs in one
`apm.yml`; then any developer runs `apm install` and restores the *same* agent context across every
supported harness (GitHub Copilot, Claude Code, Cursor, OpenCode, Codex, Gemini, Windsurf, Kiro).

Taught as three files and one habit: `apm.yml` is the manifest, `apm.lock.yaml` is the lockfile
(exact versions + content hashes), `apm-policy.yml` is install-time governance, and `apm install`
is the restore. APM is pre-1.0 and ships often, so the book is **version-aware**: record the
inspected CLI version per chapter and cite the official docs for non-obvious claims.

## Goal
A **book** — a guided, progressive learning experience that blends **hands-on mastery** with
**conceptual framing**. A reader finishes able to author a manifest, install and restore
dependencies, reproduce a setup exactly, update and audit safely, write policy, package their own
reusable primitives, and explain where APM sits in a still-forming category. Not a reference
rewrite: a journey with a throughline, a running story, and a payoff.

## The reading experience (what makes this book engaging)
The book is built from three interlocking narrative devices, and **every chapter uses all three**.
This is the non-negotiable core of the reader experience.

**1. The spine — an analogy that lands in one sentence.**
*Agent context is where application code was before npm, pip, and Cargo:* scattered files, silent
drift, "works on my machine," weak provenance, painful onboarding. Each chapter takes one hard-won
lesson from the package-manager era and shows APM's answer. This makes lockfiles, hashes, audit, and
policy feel *inevitable* rather than arbitrary — the reader already knows in their gut why each
layer has to exist.

**2. The thread — one team you follow the whole way.**
A single running scenario appears in every chapter: **Meridian**, a mid-size fintech team of about
six developers on the `meridian-checkout` service, using Copilot, Claude Code, and Cursor. The book
opens on their drift (three copies of a review prompt, mismatched Cursor/Copilot rules, onboarding
by wiki-page-and-Slack-thread) and advances *one concrete beat per chapter* — a shared manifest, a
CI break that forces a lockfile, a sketchy transitive MCP server that gets blocked, a warn→block
policy pilot, publishing `meridian-standards`, then fleet rollout. Readers keep turning pages to
find out **what breaks next**. A shared running-example spec keeps every chapter's Meridian details
consistent and verifiable.

**3. The frame — four properties and a second reader.**
Everything ladders up to four properties the book names and returns to: **portability,
reproducibility, provenance/security, governance** — mapped onto APM's three promises (*portable by
manifest, secure by default, governed by policy*). And every chapter carries a short **"For
engineering leaders"** callout that translates the hands-on work into risk, ROI, onboarding, and
governance terms. One book, **two reading paths**: the developer body and the leader track.

**The operating rule every chapter answers, in order:**
1. **Why does this layer exist?** — the package-manager analogy plus the property it protects.
2. **What changes for Meridian?** — advance the story by exactly one beat, no side quests.
3. **What should a leader notice?** — a compact callout on risk, ROI, or governance.

## Learning arc (required)
Concept before command, always — every feature is introduced as the implementation of a property.
1. **Why agent context needs a package manager** — the drift and "works on my machine" pain; name
   the four properties and map them to APM's three promises.
2. **Package-manager lessons, made familiar** — manifests, lockfiles, pinning, registries, and
   provenance via npm/pip/Cargo analogies. Clear up the **name collision** early (Microsoft APM vs
   `orthogonalhq/apm`, `aipm`, Application Performance Monitoring, Atom Package Manager) so readers
   search for and install the right thing.
3. **The vocabulary** — skills, prompts, instructions, agents, plugins, MCP servers, and the
   standards underneath (AGENTS.md, SKILL.md, MCP) before any file is written.
4. **Portable by manifest** — `apm.yml`, dependency sources (any git server), pinning, `apm init`,
   `apm install`, `apm run`.
5. **Reproducible by lockfile** — `apm.lock.yaml`, exact versions, content hashes, `--frozen`
   restore; `apm outdated` / `apm update` / `apm audit` as *deliberate* change.
6. **Secure & governed** — install-time security (hidden-Unicode scanning, content-hash pinning,
   transitive MCP blocking), then `apm-policy.yml`, tighten-only enterprise → org → repo
   inheritance, and warn→block rollout.
7. **Produce & share** — extract local conventions into reusable packages; `apm pack`; distribution.
8. **Scale & position** — CI gating (`apm audit --ci`), registry proxy / air-gapped, adoption and
   ROI, and an honest landscape map ending on the open questions on the path to v1.0.

## Depth
- **Mid-level and practical.** Runnable `apm.yml` and CLI examples throughout — but **not**
  super low-level: no CLI source internals, no byte-level lockfile plumbing, no exhaustive flag
  reference. The goal is *using APM well*.
- **Version-aware.** Record the inspected `apm` CLI version and re-verify command behavior before an
  example is marked verified. Mark network/private-source examples clearly (`SKIPPED-needs-network`).
- **Grounded, not hyped.** Clear, direct, second-person; explain *why* before *how*. No
  "revolutionary" or "game-changing" language; cite non-obvious claims to the official APM docs first.

## Audience
- **Primary: developers** comfortable with dependency managers (npm/pip/Cargo) and agentic tooling,
  new to APM.
- **Secondary: engineering leaders / decision-makers** who need the risk, ROI, and governance story
  — served by the per-chapter leader callout, not by a separate track.

## Primary surface
- **The `apm` CLI and `apm.yml` manifest** are the primary track; **`apm.lock.yaml`** is the
  reproducibility surface and **`apm-policy.yml`** is the governance surface. Show cross-harness
  parity where it matters (Copilot, Claude Code, Cursor, Codex, Gemini, Windsurf, Kiro, OpenCode),
  but do not deep-dive any single harness's runtime — that is the harness's domain, not APM's.

## Topics to cover (the architect refines/orders these into chapters)
- Concepts: why a package manager for agents; the four properties; primitives
  (skills/prompts/instructions/agents/plugins/MCP); harnesses; the npm/pip/Cargo analogy; the
  name-collision explainer.
- The manifest: `apm.yml` structure, dependency sources (any git server), version pinning, scripts,
  harness targets.
- Installing & restoring: `apm init`, `apm install [pkg]`, `apm run <script>`.
- The lockfile: `apm.lock.yaml`, exact versions, content hashes, byte-for-byte reproducibility,
  `--frozen`.
- Security by default: hidden-Unicode scanning, content-hash pinning, transitive MCP blocking, trust
  boundaries.
- Governance: `apm-policy.yml`, install-time enforcement, tighten-only enterprise → org → repo,
  warn→block pilots.
- Lifecycle: `apm update`, `apm outdated`, `apm audit`.
- Ramps: consumer, producer (authoring/publishing packages, `apm pack`), enterprise (fleet-scale
  policy, `apm audit --ci`, registry proxy, adoption/ROI).
- Landscape & future: SKILL.md / OpenAPM, `gh skill`, `vercel-labs/skills`, competitors, the
  registry gap, and the path to v1.0 — as positioning, not a market report.

## Explicitly out of scope
- CLI internals / low-level source walkthroughs.
- Exhaustive flag reference (this is a book, not the man page).
- Deep dives into any single harness's runtime behavior (that is the harness's domain, not APM's).
- A full agentic-SDLC methodology treatise — the book teaches the APM dependency layer and points
  elsewhere for methodology.
- Live publishing with real credentials; no secrets in examples.

## The interactive book (output & reader experience)
An **interactive HTML book** with **subpages for chapters**. `frontend-builder` owns the chrome and
content stays decoupled from presentation — but the shell must *actively support* the reading
experience above, not just render text:
- **Navigable spine:** persistent part/chapter navigation with reading progress and clear
  prev/next and prerequisite links, so the learning path is always visible.
- **On-this-page anchors:** in-page section anchors and a mini-TOC for the standard chapter skeleton
  (Objective · Concept · In APM · When to use / pitfalls · Worked example · Recap & next).
- **Runnable, readable examples:** syntax-highlighted, **captioned**, copy-able `apm.yml` and CLI
  blocks, each stamped with the verified CLI version and marked if it needs network or private access.
- **A visible leader track:** the "For engineering leaders" callout gets a distinct, consistent
  treatment (an aside or collapsible) so a leader can skim one path and a developer the other.
- **A visible Meridian thread:** a recurring marker for the running story so readers can follow
  "what the team did next" across chapters.
- **Concept↔command cues:** each feature visibly linked to the property it implements — no orphan
  features.
- **Memorable sidebars:** the name-collision disambiguation and "when to use / when not"
  comparisons as scannable callouts and tables, not buried prose.
- Accessible, semantic HTML throughout (real headings, landmarks, alt text, captioned code).

## Chapter structure & count
- **Every chapter uses the same skeleton:** Objective · Concept/Theory · In APM · When to use /
  pitfalls · Worked example · Recap & next — plus one **"For engineering leaders"** callout.
- **Recommended arc: ~12 chapters in 6 parts**, following the learning arc above (Why → Portable →
  Reproducible → Secure & governed → Producing & sharing → At scale & ahead). The `book-architect`
  may resize or split chapters so each fits one author's context budget, but should preserve the
  six-part progression and the three narrative devices.
