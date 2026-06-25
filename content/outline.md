# Microsoft Agent Framework Playbook Outline

This outline follows `content/playbook-brief.md`: theory first, Python-primary MAF component coverage, mid-level practical depth, no framework internals, and content decoupled from the interactive HTML presentation.

## Chapter table

| # | Chapter | Objective | MAF components | Depends on |
|---:|---|---|---|---|
| 1 | What is an agent? | Define AI agents, distinguish them from chatbots and workflows, and learn the vocabulary used by the rest of the playbook. | — | — |
| 2 | Agentic patterns and the MAF map | Connect common agentic patterns to MAF's component families before introducing APIs. | — | 01-what-is-an-agent |
| 3 | Agents and instructions | Create a Python MAF agent with a clear role, instructions, and model client boundary. | Agent; instructions; agent identity/name; run invocation | 01-what-is-an-agent; 02-agentic-patterns-and-maf-map |
| 4 | Chat clients, messages, and conversations | Understand how MAF separates agent behavior from provider chat clients, messages, and conversation state. | ChatClient; FoundryChatClient; providers; messages; conversations; multi-turn state | 01-what-is-an-agent; 02-agentic-patterns-and-maf-map; 03-agents-and-instructions |
| 5 | Tools and function calling | Add safe, well-scoped tools so an agent can act beyond text generation. | tools; function calling; tool schemas; agent skills | 02-agentic-patterns-and-maf-map; 03-agents-and-instructions; 04-chat-clients-messages-and-conversations |
| 6 | Workflows for sequential and concurrent orchestration | Model repeatable multi-step agent systems with workflow executors, edges, and sequential or concurrent paths. | workflows; WorkflowBuilder; executors; edges; sequential orchestration; concurrent orchestration | 02-agentic-patterns-and-maf-map; 03-agents-and-instructions; 05-tools-and-function-calling |
| 7 | Handoff and group chat orchestration | Choose handoff and group collaboration patterns when one agent is not enough. | handoff orchestration; group chat; multi-agent collaboration; routing | 02-agentic-patterns-and-maf-map; 03-agents-and-instructions; 06-workflows-sequential-and-concurrent |
| 8 | Streaming, checkpointing, and human-in-the-loop | Make longer-running agent workflows observable, resumable, and controllable by people. | streaming; checkpointing; durability; human-in-the-loop; workflow events | 04-chat-clients-messages-and-conversations; 06-workflows-sequential-and-concurrent; 07-handoff-and-group-chat |
| 9 | Middleware and observability | Add cross-cutting behavior and OpenTelemetry traces without burying operational concerns inside agent logic. | middleware; request/response pipeline; exception handling; OpenTelemetry; tracing | 03-agents-and-instructions; 04-chat-clients-messages-and-conversations; 05-tools-and-function-calling; 06-workflows-sequential-and-concurrent |
| 10 | Declarative agents, hosting, and DevUI | Understand how MAF projects move from local authored components toward YAML configuration, hosted execution, and interactive debugging. | declarative agents; YAML configuration; Foundry-hosted agents; hosting overview; A2A integration; DevUI | 03-agents-and-instructions; 05-tools-and-function-calling; 06-workflows-sequential-and-concurrent; 08-streaming-checkpointing-and-human-in-the-loop; 09-middleware-and-observability |

## Navigation model

- `content/toc.yml` is the machine-readable source of truth for chapter navigation.
- The frontend should render top-level chapter subpages from `chapters[*].slug`.
- Within each subpage, render ordered section anchors from `chapters[*].sections`.
- Cross-references should link from every `In MAF` section back to the earliest chapter that introduced the underlying theory in `depends_on`.

## Per-chapter section breakdown

### 1. What is an agent?

- Objective
- Concept/Theory
  - Agent definition, autonomy boundaries, goals, actions, observations, memory/context, and feedback loops.
  - Difference between single prompt, chatbot, workflow, and agent.
- When to use / pitfalls
  - Use agents for goal-directed, tool-using, iterative work; avoid them for deterministic transformations.
  - Pitfalls: anthropomorphism, uncontrolled autonomy, unclear success criteria.
- Recap & next

### 2. Agentic patterns and the MAF map

- Objective
- Concept/Theory
  - Patterns: tool use, planning, reflection, routing, orchestration, collaboration, and human approval.
  - MAF value proposition: production-grade agents and multi-agent workflows across Python and .NET.
- When to use / pitfalls
  - Choose the simplest pattern that matches the task risk, latency, and governance needs.
  - Pitfalls: over-orchestration, premature multi-agent design, hiding policy in prompts.
- Recap & next

### 3. Agents and instructions

- Objective
- Concept/Theory
  - Agent role, instruction hierarchy, task boundary, model boundary, and invocation lifecycle.
- In MAF
  - Python `Agent`, `instructions`, agent name/identity, run invocation, and .NET parity notes.
- When to use / pitfalls
  - Use an agent wrapper when behavior and model access need a stable boundary.
  - Pitfalls: vague instructions, provider assumptions inside business behavior, overly broad roles.
- Worked example
  - A minimal Python agent that answers within a role and demonstrates the client/agent boundary.
- Recap & next

### 4. Chat clients, messages, and conversations

- Objective
- Concept/Theory
  - Provider abstraction, message history, multi-turn context, and conversation state.
- In MAF
  - `ChatClient` concepts, `FoundryChatClient`, provider setup, message/conversation handling, multi-turn state.
- When to use / pitfalls
  - Use chat clients to isolate provider choice from agent behavior.
  - Pitfalls: leaking credentials into examples, confusing provider state with app state, unbounded history.
- Worked example
  - A multi-turn Python conversation showing state carried explicitly and provider details isolated.
- Recap & next

### 5. Tools and function calling

- Objective
- Concept/Theory
  - Tool affordances, function schemas, grounding, side effects, and safety boundaries.
- In MAF
  - Tool registration, function calling flow, tool schemas, and agent skills where appropriate.
- When to use / pitfalls
  - Use tools when the agent needs verified data or controlled action.
  - Pitfalls: unsafe side effects, oversized tools, ambiguous parameters, missing failure behavior.
- Worked example
  - A Python agent with one deterministic local tool and mocked external effects.
- Recap & next

### 6. Workflows for sequential and concurrent orchestration

- Objective
- Concept/Theory
  - Graph-based orchestration, executors, edges, sequential pipelines, fan-out/fan-in, and deterministic control.
- In MAF
  - Workflows, `WorkflowBuilder`, executors, edges, sequential orchestration, concurrent orchestration.
- When to use / pitfalls
  - Use workflows when explicit coordination is more reliable than one autonomous loop.
  - Pitfalls: encoding simple logic as complex graphs, missing error paths, uncontrolled concurrency.
- Worked example
  - A Python workflow with sequential steps and a small concurrent branch.
- Recap & next

### 7. Handoff and group chat orchestration

- Objective
- Concept/Theory
  - Specialist agents, routing, handoff, group collaboration, turn-taking, and shared context.
- In MAF
  - Handoff orchestration, group chat patterns, routing, multi-agent collaboration.
- When to use / pitfalls
  - Use handoff when ownership moves between specialists; use group chat when deliberation helps.
  - Pitfalls: duplicated roles, circular handoffs, unclear stop conditions, noisy group dynamics.
- Worked example
  - A compact specialist-agent scenario using handoff or group collaboration with mocked model calls.
- Recap & next

### 8. Streaming, checkpointing, and human-in-the-loop

- Objective
- Concept/Theory
  - Long-running work, incremental feedback, resumability, durability, approval gates, and intervention points.
- In MAF
  - Streaming outputs/events, checkpointing, durable workflow concepts, human-in-the-loop controls.
- When to use / pitfalls
  - Use these features for long-running, user-visible, interruptible, or high-risk workflows.
  - Pitfalls: streaming without useful UX, checkpoints without stable state shape, approval gates too late.
- Worked example
  - A workflow that streams progress, records a checkpoint, and pauses at a human approval boundary.
- Recap & next

### 9. Middleware and observability

- Objective
- Concept/Theory
  - Cross-cutting concerns, pipeline behavior, instrumentation, traces, metrics, and debuggability.
- In MAF
  - Middleware, request/response pipeline hooks, exception handling, OpenTelemetry tracing.
- When to use / pitfalls
  - Use middleware for reusable policy, logging, telemetry, retries, and guardrails.
  - Pitfalls: business logic hidden in middleware, swallowed exceptions, high-cardinality telemetry.
- Worked example
  - Add lightweight tracing/logging middleware around a previously built agent or workflow.
- Recap & next

### 10. Declarative agents, hosting, and DevUI

- Objective
- Concept/Theory
  - Configuration as contract, local-to-hosted lifecycle, deployment surface, interoperability, and debugging loops.
- In MAF
  - Declarative agents/YAML, Foundry-hosted overview, A2A integration overview, DevUI.
- When to use / pitfalls
  - Use declarative and hosted options when teams need repeatability, governance, or environment promotion.
  - Pitfalls: treating YAML as a prose dump, overpromising hosting depth, skipping local verification.
- Worked example
  - A small YAML/config-oriented walkthrough and a DevUI/hosting orientation, not a full production deployment.
- Recap & next

## Wave plan

Each chapter follows the dispatch path: `theory-researcher` and `maf-library-explorer` research in parallel, then `chapter-author`, `code-verifier`, `chapter-reviewer`, and `frontend-builder`. Pure-theory chapters skip library exploration unless the author needs source mapping context.

### Wave 0 — pilot pipeline validation

| Chapter | Dispatch target agents |
|---|---|
| 01-what-is-an-agent | theory-researcher → chapter-author → chapter-reviewer → frontend-builder |

Goal: validate research, authoring, review, and HTML integration on one pure-theory chapter before API-heavy work.

### Wave 1 — high-source core chapters

| Chapter | Dispatch target agents |
|---|---|
| 02-agentic-patterns-and-maf-map | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |
| 03-agents-and-instructions | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |
| 04-chat-clients-messages-and-conversations | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |
| 05-tools-and-function-calling | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |

Goal: cover agents, chat clients, messages/conversations, and tools/function calling while source material is abundant.

### Wave 2 — hardest orchestration and workflow chapters

| Chapter | Dispatch target agents |
|---|---|
| 06-workflows-sequential-and-concurrent | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |
| 07-handoff-and-group-chat | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |
| 08-streaming-checkpointing-and-human-in-the-loop | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |

Goal: handle multi-agent orchestration, sequential/concurrent workflows, handoff/group chat, streaming, checkpointing, and human-in-the-loop with tighter review.

### Wave 3 — integration and cross-cutting chapters

| Chapter | Dispatch target agents |
|---|---|
| 09-middleware-and-observability | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |
| 10-declarative-hosting-and-devui | theory-researcher → maf-library-explorer → chapter-author → code-verifier → chapter-reviewer → frontend-builder |

Goal: add middleware, OpenTelemetry observability, declarative YAML agents, hosting overview, A2A, and DevUI after the core concepts are in place.
