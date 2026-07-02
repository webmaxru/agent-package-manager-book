# Product

## Register

brand

## Users

**Primary — developers new to APM.** Engineers who are already fluent with dependency
managers (npm, pip, Cargo) and are working with agentic tooling (GitHub Copilot, Claude Code,
Cursor, and peers). They arrive to *learn APM by doing*: authoring an `apm.yml`, installing and
restoring agent context, reproducing a setup exactly, and auditing it safely. Their context is
focused reading with an editor open — they want runnable, copy-able examples and a throughline they
can follow chapter to chapter, not a reference to grep.

**Secondary — engineering leaders and decision-makers.** Managers and architects who need the
risk, ROI, onboarding, and governance story. They skim rather than read linearly, following the
per-chapter "For engineering leaders" callouts to decide whether and how to adopt APM across a
team or fleet.

One book, two reading paths: the developer body and the leader track share every page.

## Product Purpose

An interactive, multi-page HTML **book** that teaches **Agent Package Manager (APM)** — an
open-source dependency manager for AI agent context. It is a guided, progressive learning
experience that blends hands-on mastery with conceptual framing, moving concept-before-command from
"why does agent context need a package manager?" down into the real tool: the `apm.yml` manifest,
the `apm.lock.yaml` lockfile, `apm-policy.yml` governance, and the `apm` CLI.

Success is a reader who finishes able to author a manifest, install and restore dependencies,
reproduce a setup byte-for-byte, update and audit safely, write policy, package their own reusable
primitives, and explain where APM sits in a still-forming category. It is not a reference rewrite —
it is a journey with a spine (the package-manager analogy), a thread (the **Meridian** team's
running story), and a frame (four properties: portability, reproducibility, security, governance).

The book is itself produced by the agentic methodology it teaches: a fleet of specialized Copilot
primitives collaborating in waves. That makes the project its own proof.

## Brand Personality

**Grounded, precise, trustworthy.** The voice is clear, direct, and second-person — it explains
*why* before *how* and never reaches for "revolutionary" or "game-changing." Non-obvious claims are
cited to the official APM docs; every example is verified against the installed CLI. Confidence
comes from correctness, not volume.

The identity is **manifest-native**: the book presents itself as a pinned, versioned dependency you
can trust. It carries a deliberate **dual voice** — an *indigo* human/manifest voice (what you
declare and intend) and an *amber* machine/lockfile voice (what the tool resolves and stamps). The
emotional goal is the quiet reassurance of a green CI check: this is settled, reproducible, and
safe to build on.

## Anti-references

- **Generic AI-docs template sameness — the primary thing to avoid.** Docusaurus / Mintlify /
  GitBook out-of-the-box: left-sidebar + prose + default sans, indistinguishable from every other
  generated documentation site. If a reader could mistake this for a template, it has failed.
- **Hyped SaaS landing page** — gradient hero, big-number vanity metrics, buzzword stacks,
  "revolutionary" copy. The subject sells itself on rigor, not adjectives.
- **Dense man-page / API reference dump** — exhaustive flag tables and no narrative. This is a
  book, not the CLI's `--help`.
- **Corporate enterprise whitepaper** — stocky, safe, forgettable, stock-photo neutrality.

## Design Principles

1. **Concept before command.** Every APM feature is introduced as the implementation of a concept
   the reader already understands — one of the four properties, anchored to a package-manager
   lesson. No feature appears orphaned from the reason it exists.
2. **Ground truth over training memory.** Content is grounded in the real, installed `apm` CLI and
   the official docs — never in what a model "remembers." Command names, flags, and schemas are
   verified, and the inspected CLI version is recorded because APM is pre-1.0 and moves fast.
3. **Executable proof.** Every `apm.yml` and CLI example is real and validated: it resolves, its
   schema checks out, and it is marked clearly when it needs network or private access. Show, don't
   assert.
4. **Two reading paths, one book.** The developer body and the "For engineering leaders" track
   coexist on every page with distinct, consistent treatment — a leader can skim one path and a
   developer the other without either feeling bolted on.
5. **Practice what you preach.** The book is built by the fleet-of-primitives methodology it
   teaches, and the interface should feel like the artifact APM produces — reproducible, pinned,
   trustworthy — not like a page about that idea.

## Accessibility & Inclusion

Target **WCAG 2.2 AA**. Body text meets ≥4.5:1 contrast (large text ≥3:1); the muted and code
"ink" tokens are held to that bar, not lightened for elegance. Semantic HTML throughout — real
heading hierarchy, landmarks, skip links, captioned code blocks, and meaningful alt text. Full
keyboard operability with visible `:focus-visible` outlines. Light and dark themes both honor the
contrast bar. Every animation has a `prefers-reduced-motion: reduce` alternative (crossfade or
instant). Color is never the sole carrier of meaning — the four-property cues pair color with a
label.
