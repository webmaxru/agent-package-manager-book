# Agent Package Manager — Interactive Book

This repository builds an **interactive HTML book** that teaches the
[Agent Package Manager (APM)](https://microsoft.github.io/apm/). The book starts from
**high-level concepts** (dependency management for AI agents, portability across harnesses,
reproducibility, supply-chain security, and governance) and descends into the **APM features** —
the `apm.yml` manifest, the lockfile, primitives, the CLI, and policy — linking each feature back
to the concept it implements. The backend installs the real `apm` CLI so the tool is studied
empirically, not described from memory.

The book is itself produced with the **agentic methodology it teaches**: a team of specialized
Copilot primitives (custom agents + skills + instructions) collaborate in waves of
draft → verify → review → integrate.

## The primitives (the "team")

### Custom agents — `.github/agents/`
| Agent | Responsibility |
|-------|----------------|
| `book-architect` | Designs TOC, chapter specs, navigation, and the wave plan |
| `theory-researcher` | Cited concept briefs from APM docs (theory sections) |
| `apm-cli-explorer` | Installs & introspects the `apm` CLI + manifest/lockfile/policy schemas |
| `chapter-author` | Weaves theory + CLI reference into chapter content |
| `code-verifier` | Runs every `apm` example / validates every manifest; reports PASS/FAIL |
| `chapter-reviewer` | Reviews chapters; ACCEPT/REVISE + ranked findings |
| `frontend-builder` | Builds the interactive HTML shell and wires content in |

### Skills — `.github/skills/`
- `book-orchestration` — the wave-based workflow coordinating the whole team.
- `apm-environment-setup` — reproducible install of the `apm` CLI + a sample repo for introspection.

### Instructions — `.github/instructions/`
- `book-content.instructions.md` — content/style/structure/citation rules (`content/**`).
- `apm-examples.instructions.md` — APM manifest/command example conventions (`**/apm*.yml`).

### Prompts — `.github/prompts/`
- `new-chapter.prompt.md` — kick off one chapter end-to-end through the team.

## How they work together
See `.github/skills/book-orchestration/SKILL.md`. In short:
`architect` sets the outline → `frontend-builder` scaffolds the shell → per chapter,
`theory-researcher` + `apm-cli-explorer` research in parallel → `chapter-author` drafts →
`code-verifier` proves the examples → `chapter-reviewer` gates quality → `frontend-builder`
integrates. Work proceeds in waves (pilot chapter first), with a checkpoint commit per chapter.

## Project conventions
- **Concept before command.** Every feature is anchored to a concept introduced first.
- **Verify before ship.** A chapter is done only when its examples PASS (or are clearly marked
  `SKIPPED-needs-network`) and the reviewer returns ACCEPT.
- **No secrets in code.** Host/registry tokens live in a gitignored `.env`; examples avoid live pushes.
- **Version-aware.** Record the inspected `apm` CLI version in research/verification artifacts.
- **Content ⟂ presentation.** Authors write content; `frontend-builder` owns chrome/nav/theming.

## APM reference (verified)
- CLI install: `curl -sSL https://aka.ms/apm-unix | sh` (Unix) · `irm https://aka.ms/apm-windows | iex` (Windows).
- Core commands: `apm init` · `apm install [<pkg>]` · `apm run <script>` · `apm update` ·
  `apm outdated` · `apm audit`.
- Files: `apm.yml` (manifest) · `apm.lock.yaml` (lockfile: exact versions + content hashes) ·
  `apm-policy.yml` (governance, enforced at install time incl. transitive MCP).
- Primitives declared in `apm.yml`: skills, prompts, instructions, plugins, MCP servers.
  Sources: any git server (GitHub, GitLab, Azure DevOps, Bitbucket, Gitea) with version pinning.
- Built on AGENTS.md, Agent Skills, MCP. Ramps: consumer · producer · enterprise.
- Docs: https://microsoft.github.io/apm/
- Repo & samples: https://github.com/microsoft/apm (try `apm install microsoft/apm-sample-package`)
