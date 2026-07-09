---
title: "The Undeclared Dependency"
subtitle: "Your AI agents drifted the moment you stopped looking. Here's the layer that was missing."
angle: "Developer efficiency"
audience: "Builders and practitioners of agentic systems"
word_count: 890
note: "Includes a runnable quick-start (installs a real skill via APM) and a closing APM-skill call to action; runs a little past the 500-800 target as a result."
source: 'Adapted from "The Missing Package Manager — Managing AI Agent Context with APM"'
---

# The Undeclared Dependency

*Every team building with AI coding agents is carrying a dependency it never declared. Here's what happens when you finally do.*

You know the feeling, because you've felt it before — in a different decade. A new engineer joins, and getting their environment right means a wiki page, a Slack thread, and copying files out of someone's home directory. Two developers swear they have the same setup, but their tools behave differently and nobody can say why.

Before npm, pip, and Cargo, that was simply how software felt. Dependencies lived wherever each developer happened to put them — a `lib/` folder copied between machines, a README that said "install these seven things first." It mostly worked, until it didn't. Package managers ended it by turning scattered files into a *declared* dependency: one manifest that names what you need, one lockfile that pins exactly what you got, one command that restores it anywhere.

The files that configure your AI coding agents are in that same pre-package-manager state right now.

## The context you never treated as code

Call it your *agent context*: the instructions and coding standards, the reusable prompts, the skills and agent personas, the plugins, the Model Context Protocol (MCP) server configurations. It shapes the code an agent writes, how it reviews a diff, and which external tools it can reach. That makes it a real project dependency — one of the highest-leverage ones you have, because it multiplies across every line the agent touches.

Yet most teams hand-maintain it as loose files scattered across per-tool directories and personal machines, with no declared source of truth. So it drifts. One tool's instructions say to use the `Money` value object; another still mentions raw decimals. Three copies of the same review prompt live in three home directories, each checking a *different* threat model. Neither is wrong. Neither is portable.

A shared README doesn't save you: documentation describes *intent* but never restores *state*, so the drift returns the moment someone edits a local file. This is "works on my machine," aimed squarely at your agents — and it's invisible, because nothing broke. The build is green. The agent just quietly got a little less consistent, or a little more dangerous, on one laptop.

## Three files and one habit

The fix is not a new methodology. It's the boring, proven shape that worked the first time. [Agent Package Manager (APM)](https://github.com/microsoft/apm), an open-source tool from Microsoft, borrows the manifest-plus-lockfile pattern and points it at agent context. There are three files and one habit:

- **`apm.yml`** — the manifest. The single human-authored source of truth, naming the primitives and MCP servers your project depends on, and which tools to target.
- **`apm.lock.yaml`** — the lockfile. Machine-generated, never hand-edited, pinning every dependency to an exact source ref *and* a content hash, so two developers install byte-identical context.
- **`apm-policy.yml`** — install-time governance, for when you're ready for it.
- **`apm install`** — the habit. The one command that reads the manifest and materializes the declared context into each tool's native location.

The move that makes it click is *materialization*. A manifest is a recipe, not a meal; `apm install` turns the declaration into the real files each tool reads natively — compiled into `.github/` for Copilot, `.claude/` for Claude Code, `.cursor/` for Cursor — then stays out of the way at runtime. Your three-harness maintenance burden becomes one.

## A 60-second quick start

Enough theory. Here is the entire loop against a real, public collection — [web-ai-agent-skills](https://github.com/webmaxru/web-ai-agent-skills#install-individual-skills), a maintained set of skills for the browser's built-in AI APIs. Every command below is in the [APM docs](https://microsoft.github.io/apm/):

```bash
# 1. Install the CLI (macOS/Linux; use the PowerShell one-liner on Windows)
curl -sSL https://aka.ms/apm-unix | sh

# 2. In your project, once:
apm init

# 3. Add a skill as a pinned dependency:
apm install webmaxru/web-ai-agent-skills/skills/prompt-api
```

That last line is the whole pitch. It resolves the skill straight from its git source, pins it in `apm.lock.yaml` by commit *and* content hash, and compiles it into the location your agents already read. Commit the two files, and the next developer who runs `apm install` gets byte-identical context. The Prompt API skill is a *declared dependency* now, not a snippet someone pasted from a stale gist — and swapping `prompt-api` for any other entry works the same way.

## What actually changes

Onboarding stops being a ritual and becomes `git clone` then `apm install` — the new hire's agent is configured identically to yours before their first coffee. Drift stops being something you find during a security review: the lockfile makes it impossible, reproducing known-good context down to the bytes. None of this makes your agents smarter. That's the point — it makes them *consistent*, the precondition for every other improvement, since you can't tune a context you can't reproduce.

The uncomfortable part is that we already learned this lesson once. Agent context deserves the same declaration and review discipline you already demand of `package.json` or `requirements.txt`. The tools exist. The only question is how long you keep paying the drift tax before you declare the dependency you already have.

And if authoring that first manifest feels like one more chore, there is a fitting last move: let an agent do it. The [Agent Package Manager skill](https://github.com/webmaxru/ai-native-dev#agent-package-manager) teaches your coding agent to run `apm init`, add and pin dependencies, validate the manifest, and manage the lockfile — installed, of course, exactly like any other skill:

```bash
apm install webmaxru/ai-native-dev/skills/agent-package-manager
```

Which is the whole idea coming full circle: the package manager for agent context, installed and operated by the agent itself.

---

*Adapted from ["The Missing Package Manager"](https://apm.isainative.dev/), an interactive book on Agent Package Manager built by an agent team using the methodology it teaches. Learn more: [APM on GitHub](https://github.com/microsoft/apm) · [APM docs](https://microsoft.github.io/apm/) · [read the book](https://apm.isainative.dev/).*
