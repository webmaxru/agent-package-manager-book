# Playbook Brief — Microsoft Agent Framework

This is the **source of truth for scope and intent**. The `playbook-architect` reads this first and
designs the table of contents *within these constraints* (it does not invent scope from scratch).
Edit this file to change what the fleet builds.

## Subject
The **Microsoft Agent Framework (MAF)** — an open, multi-language framework for building
production-grade AI agents and multi-agent workflows.

## Goal
A **playbook**: a guided, progressive learning experience that takes a reader from *concepts* to
*confident use of the library components*.

## Learning arc (required)
1. **Start at high-level theory** — foundational concepts first: what an AI agent is, agentic
   patterns, why/when agents, the vocabulary the rest of the playbook builds on. Ground these in
   Microsoft Learn.
2. **Then go into the library components in detail** — walk through MAF's components, what each is
   for, how to use it, and when to use it, always linked back to the concept it implements.

## Depth
- **Mid-level.** Detailed and practical, with runnable examples — but **not super low-level**:
  no internals/source-code deep dives, no line-by-line framework plumbing. Focus on *using* the
  components well, not reimplementing them.
- Audience: developers comfortable with Python, new to MAF.

## Language focus
- **Python** (`agent-framework`) as the primary track. Mention .NET (`Microsoft.Agents.AI`)
  parity where relevant, but examples are Python.

## Topics to cover (the architect refines/orders these into chapters)
- Theory: what is an agent, agentic patterns, when to use agents, MAF's value proposition.
- Core: agents, chat clients, messages, tools / function calling, instructions.
- Middleware (request/response pipelines).
- Multi-agent orchestration & workflows: sequential, concurrent, handoff, group chat.
- Workflow features: streaming, checkpointing/durability, human-in-the-loop.
- Observability (OpenTelemetry).
- Declarative agents (YAML).
- Hosting/deployment overview (e.g. Foundry-hosted) — overview level.
- DevUI — brief.

## Explicitly out of scope
- Framework internals / low-level source walkthroughs.
- Exhaustive API reference (this is a playbook, not the docs).
- Building a production app end-to-end (focus is the components themselves).

## Output format
- An **interactive HTML page** with **subpages for chapters** (chapter navigation, in-page
  paragraph anchors, syntax-highlighted runnable examples).
- Owned by `frontend-builder`; content stays decoupled from presentation.

## Chapter count
- Let the `playbook-architect` decide, sized so each chapter fits one author's context budget.
  Roughly 8–12 chapters is a reasonable target; split anything too large.
