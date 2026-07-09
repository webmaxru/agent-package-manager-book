---
title: "The Undeclared Dependency"
subtitle: "Your AI agents drifted the moment you stopped looking. Here's the layer that was missing."
angle: "Developer efficiency"
audience: "Builders and practitioners of agentic systems"
word_count: 776
source: 'Adapted from "The Missing Package Manager — Managing AI Agent Context with APM"'
---

# The Undeclared Dependency

*Every team building with AI coding agents is carrying a dependency it never declared. Here's what happens when you finally do.*

You know the feeling, because you've felt it before — in a different decade. A new engineer joins, and getting their environment right means a wiki page, a Slack thread, and someone copying files out of their home directory. Two developers swear they have the same setup, but their tools behave differently and nobody can say why. Preparing for a review, you go looking for the canonical configuration and find four versions of it, none authoritative.

Before npm, pip, and Cargo, that was simply how software felt. Dependencies lived wherever each developer happened to put them — a `lib/` folder copied between machines, a README that said "install these seven things first." It mostly worked, until it didn't. Package managers ended it by turning scattered files into a *declared* dependency: one manifest that names what you need, one lockfile that pins exactly what you got, one command that restores it anywhere.

The files that configure your AI coding agents are in that same pre-package-manager state right now.

## The context you never treated as code

Call it your *agent context*: the instructions and coding standards, the reusable prompts, the skills and agent personas, the plugins, the Model Context Protocol (MCP) server configurations. This is not decoration. It shapes the code an agent writes, how it reviews a diff, and which external tools it is allowed to reach. That makes it a real project dependency — arguably one of the highest-leverage ones you have, because it multiplies across every line the agent touches.

Yet most teams hand-maintain it as loose files scattered across per-tool directories and personal machines, with no single declared source of truth. So it drifts. One tool's instructions say to use the `Money` value object; another still mentions raw decimals. Three copies of the same review prompt live in three home directories, each checking a *different* threat model. The rules for one harness emphasize idempotency; the rules for another emphasize accessibility. Neither is wrong. Neither is portable.

A shared README doesn't save you, because documentation describes *intent* but never restores *state*. The drift returns the moment someone edits a local file. This is "works on my machine," aimed squarely at your agents — and it's invisible, because nothing broke. The build is green. The agent just quietly got a little less consistent, or a little more dangerous, on one person's laptop.

## Three files and one habit

The fix is not a new methodology. It's the boring, proven shape that worked the first time. Agent Package Manager (APM), an open-source tool from Microsoft, borrows the manifest-plus-lockfile pattern and points it at agent context. There are three files and one habit:

- **`apm.yml`** — the manifest. The single human-authored source of truth, naming the primitives and MCP servers your project depends on, and which tools to target.
- **`apm.lock.yaml`** — the lockfile. Machine-generated, never hand-edited, pinning every dependency to an exact source ref *and* a content hash, so two developers install byte-identical context.
- **`apm-policy.yml`** — install-time governance, for when you're ready for it.
- **`apm install`** — the habit. The one command that reads the manifest and materializes the declared context into each tool's native location.

The move that makes it click is *materialization*. A manifest is a recipe, not a meal; `apm install` is what turns the declaration into real files that Copilot, Claude Code, Cursor, Codex, Gemini, and the rest each read natively. One declared source, compiled into `.github/`, `.claude/`, `.cursor/` — then APM stays out of the way at runtime. Your three-harness maintenance burden becomes one.

## What actually changes

Onboarding stops being a ritual and becomes `git clone` then `apm install`. The new hire's agent is configured identically to yours before their first coffee. Drift stops being something you discover during a security review and becomes something the lockfile makes impossible: a later install reproduces the previously known-good context exactly, down to the bytes.

None of this makes your agents smarter. That's the point. It makes them *consistent* — and consistency is the precondition for every other improvement you want to make. You can't tune a context you can't reproduce, and you can't share an improvement that lives in one person's home directory.

The uncomfortable part is that we already learned this lesson once. Agent context deserves the same declaration and review discipline you already demand of `package.json` or `requirements.txt`. The tools to give it that discipline now exist. The only question is how long you keep paying the drift tax before you declare the dependency you already have.

---

*Adapted from "The Missing Package Manager," an interactive book on Agent Package Manager built by an agent team using the methodology it teaches. APM docs: [microsoft.github.io/apm](https://microsoft.github.io/apm/).*
