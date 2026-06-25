---
description: Content, style, structure, and citation conventions for MAF playbook chapters.
applyTo: "content/**"
---

# Playbook Content Conventions

These rules apply to all playbook chapter content under `content/`. They keep chapters consistent,
accurate, and teachable across authors.

## Audience & voice
- Reader: a developer **new to the Microsoft Agent Framework** but comfortable with Python.
- Voice: clear, direct, second-person ("you"). Explain *why* before *how*. No marketing fluff.

## Chapter structure (same skeleton every chapter)
1. **Objective** — one sentence: what the reader will be able to do afterward.
2. **Concept / theory** — the idea and the problem it solves (grounded in the theory brief).
3. **In MAF** — the component(s) that implement the concept, with signatures and explanation.
4. **When to use / when not to** — guidance and common pitfalls.
5. **Worked example** — a minimal, verified, runnable snippet.
6. **Recap & next** — bullets + link to the next chapter / prerequisites.

## Theory ↔ library linkage
- Every MAF component introduced **must** reference the concept it implements.
- No "orphan APIs": if a component appears, the concept behind it was introduced first (here or earlier).

## Citations & accuracy
- Cite non-obvious claims with a source URL; prefer **Microsoft Learn** and the official repo.
- No unsourced statistics or unfalsifiable superlatives.
- Only use API names/signatures that `maf-library-explorer` verified and `code-verifier` ran.
- Record the **inspected `agent-framework` version** the chapter targets.

## Code in content
- Every snippet must be **verified** (see `maf-code-examples.instructions.md`). Mark
  credential-requiring examples clearly.
- Caption each code block with what it demonstrates.

## HTML/markup
- Semantic, accessible HTML: real headings (`h1`–`h3`), landmarks, alt text, captioned `<pre><code>`.
- Keep **content decoupled from presentation** — no inline layout/styling that belongs to the shell
  (`frontend-builder` owns chrome, nav, and theming).
- Short paragraphs; prefer lists and tables for "when to use" comparisons.
