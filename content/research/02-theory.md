# Chapter 2 theory brief: Agentic patterns and the MAF map

Artifact path: `content/research/02-theory.md`

## Concepts covered

- Single-agent with tools
- Sequential orchestration
- Concurrent / parallel orchestration
- Handoff / routing orchestration
- Group chat / collaborative orchestration
- Reflection / maker-checker loops
- Magentic / planner-style orchestration
- Workflows vs. autonomous orchestration
- Cross-cutting pattern support: streaming, checkpointing, human-in-the-loop, middleware, observability, declarative configuration, hosting
- How to choose a pattern

## Objective

Chapter 1 introduced the vocabulary: agent, tool, workflow, orchestration, and the distinction between model-driven agency and deterministic process control. Chapter 2 should use that vocabulary to give readers a mental map: start with the simplest pattern that solves the problem, then move toward workflows and multi-agent orchestration only when the task needs explicit sequencing, parallel specialization, dynamic routing, or collaboration. Microsoft Agent Framework (MAF) exposes this same progression as two main capability families: individual agents that process inputs and call tools, and graph-based workflows that connect agents and functions for multi-step tasks with routing, checkpointing, and human-in-the-loop support. Source: https://learn.microsoft.com/en-us/agent-framework/overview/

## Concept / theory

### Single-agent with tools

A single-agent pattern uses one LLM-backed agent with instructions, a model/chat client boundary, and a curated set of tools or knowledge sources. It solves the common case where one agent can handle varied requests in one domain, sometimes looping through model calls and tool invocations, without the coordination overhead of multiple agents. Microsoft Architecture Center calls this "often the right default for enterprise use cases" when dynamic tool use is needed but a single agent can still reliably solve the scenario. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **When to use:** Use when the task is open-ended or conversational, needs autonomous tool use and planning, and does not require multiple specialists or explicit process control. MAF's overview says agents are for open-ended or conversational tasks, autonomous tool use and planning, or a single LLM call with tools. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **When not to use / pitfalls:** Do not use an agent if a normal function can handle the task; MAF states, "If you can write a function to handle the task, do that instead of using an AI agent." Also avoid adding too many tools to one agent if tool overload, security boundaries, or prompt complexity make behavior unpredictable. Sources: https://learn.microsoft.com/en-us/agent-framework/overview/, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Agent + instructions + chat client boundary — Chapters 3-4; tools/function calling/MCP tools — Chapter 5; middleware and observability for guardrails around the agent — Chapter 9.

### Sequential orchestration

Sequential orchestration chains agents in a predefined order; each stage consumes the previous stage's output and adds a specialized transformation. It solves multi-step tasks with clear dependencies, such as draft -> review -> polish, where later work should not begin until earlier work completes. Microsoft Architecture Center notes that the next-agent choice is deterministic in this pattern, and MAF's orchestration docs describe sequential orchestration as agents organized in a pipeline. Sources: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns, https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/sequential

- **When to use:** Use for predictable, linear processes where each step depends on the previous step and quality improves through staged refinement. It is a good fit when business control, traceability, or validation between steps matters more than dynamic autonomy. Sources: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns, https://learn.microsoft.com/en-us/agent-framework/workflows/
- **When not to use / pitfalls:** Avoid it when stages can run independently in parallel, when a single agent can do the job, when accumulated errors would cascade, or when the flow needs backtracking or dynamic routing. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Workflows with executors and edges; sequential orchestration family — Chapter 6; streaming, checkpointing, and human-in-the-loop approval for long-running or sensitive sequences — Chapter 8.

### Concurrent / parallel orchestration

Concurrent orchestration sends the same task, or independent parts of a task, to multiple agents at the same time and then collects or aggregates the results. It solves problems where independent perspectives, ensemble reasoning, voting, or latency reduction are useful. Microsoft Architecture Center describes this as parallel, fan-out/fan-in, scatter-gather, or map-reduce, and MAF docs describe concurrent orchestration as multiple agents working on the same task in parallel with collected results. Sources: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns, https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/concurrent

- **When to use:** Use when agents do not depend on each other's intermediate outputs and the task benefits from specialized independent analysis, brainstorming, quorum/voting, or faster wall-clock time. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **When not to use / pitfalls:** Avoid it when the task requires strict order, cumulative context, shared mutable state, scarce model quota, or there is no clear aggregation/conflict-resolution strategy. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Workflows with parallel execution paths, concurrent orchestration, executors, edges, and aggregation — Chapter 6; streaming events and checkpointing for visibility and recovery — Chapter 8; observability for per-agent cost and latency tracking — Chapter 9.

### Handoff / routing orchestration

Handoff orchestration lets one active agent transfer control of a task or conversation to another specialist when context shows that another agent is better suited. It solves dynamic triage problems where the right specialist, or the sequence of specialists, is not fully known at the start. MAF docs describe handoff as agents transferring control based on context or user request, implemented as a mesh topology without a central orchestrator; Microsoft Architecture Center also frames it as routing, triage, transfer, dispatch, or delegation. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **When to use:** Use when expertise requirements emerge during processing, when only one specialist should own the task at a time, or when a conversation may need escalation to another AI or human participant. Sources: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns, https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff
- **When not to use / pitfalls:** Avoid it when routing is deterministic from the initial input, when parallel work is required, or when infinite handoff loops and bouncing between agents are hard to prevent. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Handoff orchestration and routing component family — Chapter 7; human-in-the-loop escalation, tool approval, and checkpointing for durable handoff workflows — Chapter 8; observability of handoff paths — Chapter 9.

### Group chat / collaborative orchestration

Group chat orchestration coordinates multiple agents in a shared conversation thread so they can iteratively refine, debate, validate, or synthesize a result. It solves problems that benefit from collaboration rather than a fixed pipeline: brainstorming, consensus-building, multi-perspective analysis, and structured review. MAF docs describe group chat as a collaborative conversation coordinated by an orchestrator that determines speaker selection and conversation flow; Microsoft Architecture Center calls it roundtable, collaborative, multiagent debate, or council. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/group-chat, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **When to use:** Use when agents should see and react to a shared conversation history, when human oversight in the thread is valuable, or when iterative maker/checker-style review improves output quality. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/group-chat, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **When not to use / pitfalls:** Avoid it for simple delegation, deterministic workflows, low-latency requirements, or when the manager lacks an objective completion condition. Microsoft Architecture Center warns that managing conversation flow gets harder as more agents are added and suggests limiting group chat to three or fewer agents for control. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Group chat and multi-agent collaboration component family — Chapter 7; streaming conversation events and human participation — Chapter 8; middleware and telemetry around shared conversations — Chapter 9.

### Reflection / maker-checker loops

Reflection-style orchestration is a structured review loop: one agent produces an answer or artifact, and another evaluates it against acceptance criteria, sends feedback, and may force revision. Microsoft Architecture Center documents this as a maker-checker loop within group chat and notes the aliases evaluator-optimizer, generator-verifier, critic loop, and reflection loop. It solves quality-control problems where a second role can catch gaps, policy issues, or weak reasoning before the output is accepted. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **When to use:** Use when there are clear acceptance criteria and revision is valuable, such as editorial review, compliance checks, or "draft and critique" workflows. Set an iteration cap and fallback behavior because Microsoft guidance warns these loops need maximum iteration limits to avoid infinite refinement. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **When not to use / pitfalls:** Avoid it when criteria are too vague for a checker to make consistent pass/fail decisions, or when added turns cost more latency and tokens than the task justifies. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Group chat orchestration with roles and termination conditions — Chapter 7; streaming/HITL for review visibility and escalation — Chapter 8; observability for iteration counts and failure loops — Chapter 9.

### Magentic / planner-style orchestration

Magentic orchestration is a planner-style multi-agent pattern for complex, open-ended work where the solution path is not known in advance. A manager agent coordinates specialized agents, tracks progress, adapts the plan, and selects who should act next based on evolving context and capabilities. MAF docs state that Magentic orchestration is based on AutoGen's Magentic-One and is suited to complex tasks requiring dynamic collaboration; Microsoft Architecture Center describes it as dynamic, task-ledger-based, or adaptive planning orchestration. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **When to use:** Use when the work requires a plan of approach, multiple specialized agents, tool-using agents that may change external systems, and potentially a human-reviewable task ledger. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **When not to use / pitfalls:** Avoid it when the solution path is deterministic, the task is low-complexity, the work is time-sensitive, or stalls/infinite loops are likely. MAF's Magentic page also cautions that Magentic has the same architecture as group chat with a powerful planning manager and recommends group chat when simpler coordination is enough. Sources: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns, https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic
- **Implemented in MAF by:** Magentic orchestration as an advanced multi-agent collaboration family — Chapter 7; plan review, streaming progress, checkpointing, and HITL — Chapter 8; observability and safeguards around long-running adaptive loops — Chapter 9.

### Workflows vs. autonomous orchestration

The key distinction from Chapter 1 carries forward: autonomous agent behavior is model-driven, while workflows define the process path more explicitly. MAF's workflow overview says an agent's steps are dynamic and determined by the LLM based on context and tools, while a workflow is a predefined sequence of operations that can include agents, human interactions, and integrations with an explicitly defined flow. Source: https://learn.microsoft.com/en-us/agent-framework/workflows/

- **When to use workflow control:** Use workflows when the process has well-defined steps, requires explicit execution order, or multiple agents/functions must coordinate; MAF's overview lists these as workflow use cases. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **When to use autonomous behavior:** Use a single agent or planner-style orchestration when the path genuinely depends on context that cannot be captured well as deterministic branches. The tradeoff is less predictability, so add iteration limits, validation, telemetry, and human checkpoints where needed. Sources: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns, https://learn.microsoft.com/en-us/agent-framework/overview/
- **Implemented in MAF by:** Workflows, executors, edges, workflow events, and graph-based orchestration — Chapter 6; handoff/group chat/magentic for less deterministic collaboration — Chapter 7; checkpointing/HITL — Chapter 8.

### Cross-cutting pattern support

Long-running or sensitive orchestration needs operational support independent of the chosen pattern. MAF workflows list checkpointing, events, external integration, human-in-the-loop scenarios, streaming and non-streaming modes, and multi-agent orchestration among workflow capabilities; the GitHub README also highlights checkpointing, streaming, human-in-the-loop, observability, governance, declarative agents, hosting, and DevUI as production-oriented capabilities. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/, https://github.com/microsoft/agent-framework

- **When to use:** Add streaming when users/operators need progress visibility, checkpointing when work must resume after interruption, HITL/tool approval when actions are sensitive, middleware when cross-cutting behavior should not be buried in agent instructions, and observability when you need to diagnose cost, latency, failures, or handoff paths. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/, https://learn.microsoft.com/en-us/agent-framework/workflows/workflows, https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- **When not to use / pitfalls:** Avoid treating these operational features as afterthoughts; Microsoft Architecture Center warns multi-agent systems multiply distributed-system concerns such as failures, latency, context growth, security boundaries, cost, and observability needs. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Streaming, checkpointing, durability, workflow events, and human-in-the-loop — Chapter 8; middleware, request/response pipeline, exception handling, OpenTelemetry tracing — Chapter 9; declarative agents, YAML configuration, Foundry-hosted agents, A2A integration, hosting, and DevUI — Chapter 10.

## How to choose a pattern

1. **Start below agents if possible.** If a deterministic function or direct model call solves the task, use that; Microsoft explicitly recommends the lowest level of complexity that reliably meets requirements. Sources: https://learn.microsoft.com/en-us/agent-framework/overview/, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
2. **Default to one agent with tools for one domain.** A single agent is easier to test and debug than a multi-agent system while still supporting dynamic tool use. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
3. **Choose sequential when dependency order is real.** Use it for predictable stage gates; do not use it when stages are naturally parallel or when dynamic routing is required. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
4. **Choose concurrent when independence is real.** Use it for independent perspectives or lower latency; avoid it without conflict resolution, quota headroom, and clear aggregation. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
5. **Choose handoff when ownership should move.** Use it when the right specialist emerges during conversation; avoid it for simple deterministic classification or if handoff loops are likely. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
6. **Choose group chat or reflection when collaboration is the point.** Use it for debate, consensus, maker-checker validation, and human-visible review; avoid it when a fixed pipeline is enough. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
7. **Choose Magentic only for open-ended planning.** It is the highest-complexity pattern here: useful for dynamic plan building, but slower and more failure-prone when the task is simple or deterministic. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
8. **Add operational overlays deliberately.** Streaming, checkpointing, HITL, middleware, telemetry, declarative configuration, and hosting are not separate problem-solving patterns; they make whichever pattern you choose safer, observable, resumable, and deployable. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/, https://github.com/microsoft/agent-framework

## Pitfalls of over-orchestrating

- **Adding agents without meaningful specialization.** Microsoft Architecture Center lists adding agents that do not provide meaningful specialization as a common antipattern. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Using nondeterminism where deterministic control is needed.** The same guidance warns against using deterministic patterns for inherently nondeterministic workflows and nondeterministic patterns for inherently deterministic workflows. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Ignoring coordination overhead.** Multi-agent orchestration adds latency, cost, coordination overhead, and failure modes; justify it only when a single agent cannot reliably handle the task because of prompt complexity, tool overload, security requirements, specialization, or parallelism. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Letting context grow unchecked.** Microsoft guidance notes that context windows can grow rapidly across transitions and recommends compaction such as summarization or selective pruning. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Treating the framework as the safety boundary.** MAF provides building blocks, but Microsoft states builders remain responsible for reviewing, testing, and implementing responsible AI, quality, reliability, security, and trustworthiness mitigations for their use case. Source: https://learn.microsoft.com/en-us/agent-framework/overview/

## Recap & next

The MAF map is a progression from simple to coordinated: one agent with tools, deterministic workflows for sequence or parallelism, dynamic handoff when ownership moves, group collaboration when agents need to discuss, and Magentic planning when the path is unknown. The next chapters should introduce these component families in the same order: agents and instructions (Ch3), chat clients and conversations (Ch4), tools (Ch5), workflows for sequential/concurrent orchestration (Ch6), handoff/group chat/Magentic collaboration (Ch7), operational controls (Ch8-9), and declarative/hosting concerns (Ch10).

## Sources

- https://learn.microsoft.com/en-us/agent-framework/
- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/agent-framework/agents/
- https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- https://learn.microsoft.com/en-us/agent-framework/workflows/
- https://learn.microsoft.com/en-us/agent-framework/workflows/workflows
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/sequential
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/concurrent
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/group-chat
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- https://github.com/microsoft/agent-framework
