---
description: Content, style, structure, and citation conventions for APM book chapters.
applyTo: "content/**"
---

# Book Content Conventions

These rules apply to all book chapter content under `content/`. They keep chapters consistent,
accurate, and teachable across authors.

## Audience & voice
- Reader: a developer **new to Agent Package Manager** but comfortable with dependency managers
  (npm/pip) and agentic tooling.
- Voice: clear, direct, second-person ("you"). Explain *why* before *how*. No marketing fluff.

## Chapter structure (same skeleton every chapter)
1. **Objective** — one sentence: what the reader will be able to do afterward.
2. **Concept / theory** — the idea and the problem it solves (grounded in the theory brief).
3. **In APM** — the feature(s) that implement the concept, with the command/manifest and explanation.
4. **When to use / when not to** — guidance and common pitfalls.
5. **Worked example** — a minimal, verified `apm.yml` and/or `apm` command.
6. **Recap & next** — bullets + link to the next chapter / prerequisites.

## Concept ↔ tool linkage
- Every APM feature introduced **must** reference the concept it implements.
- No "orphan features": if a command or manifest key appears, the concept behind it was introduced
  first (here or earlier).

## Citations & accuracy
- Cite non-obvious claims with a source URL; prefer the **official APM docs** and the official repo.
- No unsourced statistics or unfalsifiable superlatives.
- Only use command/flag/manifest names that `apm-cli-explorer` verified and `code-verifier` ran.
- Record the **inspected `apm` CLI version** the chapter targets.

## Examples in content
- Every example must be **verified** (see `apm-examples.instructions.md`). Mark examples that require
  network access to a private source clearly.
- Caption each `apm.yml` / command block with what it demonstrates.

## HTML/markup
- Semantic, accessible HTML: real headings (`h1`–`h3`), landmarks, alt text, captioned `<pre><code>`.
- Keep **content decoupled from presentation** — no inline layout/styling that belongs to the shell
  (`frontend-builder` owns chrome, nav, and theming).
- Short paragraphs; prefer lists and tables for "when to use" comparisons.
