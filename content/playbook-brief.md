# Book Brief — Agent Package Manager

This is the **source of truth for scope and intent**. The `book-architect` reads this first and
designs the table of contents *within these constraints* (it does not invent scope from scratch).
Edit this file to change what the fleet builds.

## Subject
**Agent Package Manager (APM)** — an open-source dependency manager for AI agents. You declare the
skills, prompts, instructions, plugins, and MCP servers your project needs in one `apm.yml`, then
any developer runs `apm install` and gets the same agent context across every supported harness
(GitHub Copilot, Claude Code, Cursor, OpenCode, Codex, Gemini, Windsurf, Kiro).

## Goal
A **book**: a guided, progressive learning experience that takes a reader from *concepts* to
*confident daily use of the tool* — authoring a manifest, installing packages, reproducing a setup,
and governing it at scale.

## Learning arc (required)
1. **Start at high-level concepts** — foundational ideas first: why agent context needs a package
   manager, portability across harnesses, reproducibility, supply-chain security, and the
   vocabulary the rest of the book builds on. Ground these in the APM docs.
2. **Then go into the tool in detail** — walk through APM's features (the `apm.yml` manifest, the
   lockfile, primitives, the CLI commands, policy/governance), what each is for, how to use it, and
   when to use it, always linked back to the concept it implements.

## Depth
- **Mid-level.** Detailed and practical, with runnable examples — but **not super low-level**:
  no internals/source-code deep dives of the CLI, no byte-level lockfile plumbing. Focus on *using*
  APM well.
- Audience: developers comfortable with dependency managers (npm/pip) and agentic tooling, new to APM.

## Primary surface
- **The `apm` CLI and `apm.yml`** as the primary track. Show cross-harness parity where relevant
  (Copilot, Claude Code, Cursor, Codex, Gemini, Windsurf, Kiro, OpenCode), but examples center on
  the manifest and the command surface.

## Topics to cover (the architect refines/orders these into chapters)
- Concepts: why a package manager for agents, primitives (skills/prompts/instructions/plugins/MCP),
  harnesses, portability, reproducibility, the value proposition.
- The manifest: `apm.yml` structure, dependency sources (any git server), version pinning.
- Installing & restoring: `apm init`, `apm install`, `apm run <script>`.
- The lockfile: `apm.lock.yaml`, exact versions, content hashes, byte-for-byte reproducibility.
- Security by default: hidden-Unicode scanning, content-hash pinning, transitive MCP blocking.
- Governance: `apm-policy.yml`, install-time enforcement, tighten-only enterprise → org → repo.
- Lifecycle: `apm update`, `apm outdated`, `apm audit`.
- Ramps: consumer, producer (authoring/publishing packages), enterprise (fleet-scale policy/CI).

## Explicitly out of scope
- CLI internals / low-level source walkthroughs.
- Exhaustive flag reference (this is a book, not the man page).
- Deep dives into any single harness's runtime behavior (that is the harness's domain, not APM's).

## Output format
- An **interactive HTML page** with **subpages for chapters** (chapter navigation, in-page
  paragraph anchors, syntax-highlighted runnable examples).
- Owned by `frontend-builder`; content stays decoupled from presentation.

## Chapter count
- Let the `book-architect` decide, sized so each chapter fits one author's context budget.
  Roughly 8–12 chapters is a reasonable target; split anything too large.
