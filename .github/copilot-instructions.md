# Microsoft Agent Framework — Interactive Playbook

This repository builds an **interactive HTML playbook** that teaches the
[Microsoft Agent Framework (MAF)](https://learn.microsoft.com/en-us/agent-framework/). The playbook
starts from **high-level agentic concepts** (grounded in Microsoft Learn) and descends into the
**MAF library components**, linking each component back to the concept it implements. The backend
imports the real `agent-framework` packages so the framework is studied empirically, not described
from memory.

The book is itself produced with the **agentic methodology it teaches**: a team of specialized
Copilot primitives (custom agents + skills + instructions) collaborate in waves of
draft → verify → review → integrate.

## The primitives (the "team")

### Custom agents — `.github/agents/`
| Agent | Responsibility |
|-------|----------------|
| `playbook-architect` | Designs TOC, chapter specs, navigation, and the wave plan |
| `theory-researcher` | Cited concept briefs from Microsoft docs (theory sections) |
| `maf-library-explorer` | Installs & introspects `agent-framework`; component notes + examples |
| `chapter-author` | Weaves theory + library into chapter content |
| `code-verifier` | Runs every code example; reports PASS/FAIL |
| `chapter-reviewer` | Reviews chapters; ACCEPT/REVISE + ranked findings |
| `frontend-builder` | Builds the interactive HTML shell and wires content in |

### Skills — `.github/skills/`
- `playbook-orchestration` — the wave-based workflow coordinating the whole team.
- `maf-environment-setup` — reproducible Python env + `agent-framework` install/introspection.

### Instructions — `.github/instructions/`
- `playbook-content.instructions.md` — content/style/structure/citation rules (`content/**`).
- `maf-code-examples.instructions.md` — MAF Python example conventions (`**/*.py`).

### Prompts — `.github/prompts/`
- `new-chapter.prompt.md` — kick off one chapter end-to-end through the team.

## How they work together
See `.github/skills/playbook-orchestration/SKILL.md`. In short:
`architect` sets the outline → `frontend-builder` scaffolds the shell → per chapter,
`theory-researcher` + `maf-library-explorer` research in parallel → `chapter-author` drafts →
`code-verifier` proves the examples → `chapter-reviewer` gates quality → `frontend-builder`
integrates. Work proceeds in waves (pilot chapter first), with a checkpoint commit per chapter.

## Project conventions
- **Theory before API.** Every component is anchored to a concept introduced first.
- **Verify before ship.** A chapter is done only when its examples PASS (or are clearly marked
  `SKIPPED-needs-creds`) and the reviewer returns ACCEPT.
- **No secrets in code.** Provider keys live in a gitignored `.env`; examples mock live calls.
- **Version-aware.** Record the inspected `agent-framework` version in research/verification artifacts.
- **Content ⟂ presentation.** Authors write content; `frontend-builder` owns chrome/nav/theming.

## MAF reference (verified)
- PyPI: `agent-framework` (full) · `agent-framework-core` · `agent-framework-foundry` ·
  `agent-framework-copilotstudio` (`--pre`). .NET: `Microsoft.Agents.AI`.
- Docs: https://learn.microsoft.com/en-us/agent-framework/
- Repo & samples: https://github.com/microsoft/agent-framework
  (`01-get-started`, `02-agents`, `03-workflows`, `04-hosting`)
