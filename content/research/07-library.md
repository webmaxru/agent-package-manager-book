# Chapter 7 library notes: Handoff and group chat orchestration

Inspected version: `agent-framework==1.9.0` (`agent-framework-orchestrations==1.9.0`). Introspection used `agent_framework.orchestrations`, `agent_framework_orchestrations`, installed source, and Microsoft Learn orchestration docs; installed package names/signatures win on conflicts.

## Orchestration imports / `agent_framework.orchestrations` and `agent_framework_orchestrations`

Implements concept: Ch7 multi-agent orchestration package; Ch2 pattern map: sequential, concurrent, handoff, and group chat collaboration patterns.

Confirmed public names include:

```python
from agent_framework.orchestrations import (
    SequentialBuilder,
    ConcurrentBuilder,
    HandoffBuilder,
    GroupChatBuilder,
    GroupChatOrchestrator,
    AgentBasedGroupChatOrchestrator,
    BaseGroupChatOrchestrator,
    GroupChatState,
    GroupChatRequestMessage,
    GroupChatRequestSentEvent,
    GroupChatResponseReceivedEvent,
    AgentOrchestrationOutput,
    AgentRequestInfoResponse,
)
```

The import path `agent_framework.orchestrations` re-exports classes implemented in the installed `agent_framework_orchestrations` package. The older-looking C# doc name `AgentWorkflowBuilder` is not the Python 1.9.0 API; Python uses builder classes such as `SequentialBuilder`, `ConcurrentBuilder`, `HandoffBuilder`, and `GroupChatBuilder`.

When to use: import from `agent_framework.orchestrations` in application code. When not to use: avoid relying on private modules like `agent_framework_orchestrations._group_chat` except for source inspection.

Minimal example: `backend/examples/ch07/handoff_group_chat.py`.

Inspected version: `agent-framework==1.9.0`.

## `HandoffBuilder` / `agent_framework.orchestrations.HandoffBuilder`

Implements concept: Ch7 handoff orchestration; Ch2 pattern map: decentralized delegation where the active agent transfers task ownership to another specialist.

Real signatures:

```python
HandoffBuilder(
    *,
    name: str | None = None,
    participants: Sequence[Agent] | None = None,
    description: str | None = None,
    checkpoint_storage: CheckpointStorage | None = None,
    termination_condition: Callable[[list[Message]], bool | Awaitable[bool]] | None = None,
    output_from: Sequence[str | SupportsAgentRun | Executor] | Literal["all"] | None = UNSET,
    intermediate_output_from: Sequence[str | SupportsAgentRun | Executor] | Literal["all", "all_other"] | None = None,
) -> None

HandoffBuilder.participants(participants: Sequence[Agent]) -> HandoffBuilder
HandoffBuilder.add_handoff(source: Agent, targets: Sequence[Agent], *, description: str | None = None) -> HandoffBuilder
HandoffBuilder.with_start_agent(agent: Agent) -> HandoffBuilder
HandoffBuilder.with_autonomous_mode(*, agents: Sequence[Agent] | Sequence[str] | None = None, prompts: dict[str, str] | None = None, turn_limits: dict[str, int] | None = None) -> HandoffBuilder
HandoffBuilder.with_checkpointing(checkpoint_storage: CheckpointStorage) -> HandoffBuilder
HandoffBuilder.with_termination_condition(termination_condition) -> HandoffBuilder
HandoffBuilder.build() -> Workflow
```

Handoff builds a mesh-like workflow where each participating `Agent` receives injected handoff tools for allowed targets. The active agent can call a handoff tool to transfer control, and the target agent owns the next turn with full conversation context. Introspection of source found two important requirements: participants must be actual `agent_framework.Agent` instances, not arbitrary `SupportsAgentRun`, and they must be constructed with `require_per_service_call_history_persistence=True`.

When to use: support triage, expert routing, support queues, or specialist ownership transfer. When not to use: do not use handoff when a central moderator should choose each speaker; use group chat instead. Do not use non-`Agent` participants.

Minimal example: `backend/examples/ch07/handoff_group_chat.py` builds and runs a no-credential handoff workflow with fake chat clients and a one-response termination condition.

Inspected version: `agent-framework==1.9.0`.

## `GroupChatBuilder` / `agent_framework.orchestrations.GroupChatBuilder`

Implements concept: Ch7 group chat orchestration; Ch2 pattern map: centrally coordinated multi-agent collaboration and iterative refinement.

Real signatures:

```python
GroupChatBuilder(
    *,
    participants: Sequence[SupportsAgentRun | Executor] | None = None,
    participant_factories: Sequence[Callable[[], SupportsAgentRun | Executor]] | None = None,
    orchestrator_agent: Agent | Callable[[], Agent] | None = None,
    orchestrator: BaseGroupChatOrchestrator | Callable[[], BaseGroupChatOrchestrator] | None = None,
    selection_func: GroupChatSelectionFunction | None = None,
    orchestrator_name: str | None = None,
    termination_condition: Callable[[list[Message]], bool | Awaitable[bool]] | None = None,
    max_rounds: int | None = None,
    checkpoint_storage: CheckpointStorage | None = None,
    output_from: Sequence[str | SupportsAgentRun | Executor] | Literal["all"] | None = UNSET,
    intermediate_output_from: Sequence[...] | Literal["all", "all_other"] | None = None,
) -> None

GroupChatBuilder.with_max_rounds(max_rounds: int | None) -> GroupChatBuilder
GroupChatBuilder.with_termination_condition(termination_condition) -> GroupChatBuilder
GroupChatBuilder.with_checkpointing(checkpoint_storage: CheckpointStorage) -> GroupChatBuilder
GroupChatBuilder.with_request_info(*, agents: Sequence[str | SupportsAgentRun] | None = None) -> GroupChatBuilder
GroupChatBuilder.build() -> Workflow
```

Group chat constructs a star topology: participants sit around a central orchestrator. Speaker selection can be a deterministic `selection_func`, an `orchestrator_agent`, or a custom `BaseGroupChatOrchestrator`. Unlike handoff, group chat supports `SupportsAgentRun` and `Executor` participants.

When to use: brainstorming, review loops, debate, or coordinated multi-agent collaboration where all participants share context. When not to use: avoid it when a single specialist should own the task after routing; handoff is simpler.

Minimal example: `backend/examples/ch07/handoff_group_chat.py` runs a deterministic two-round group chat with fake chat clients.

Inspected version: `agent-framework==1.9.0`.

## `GroupChatState`, `GroupChatSelectionFunction`, and events / `agent_framework.orchestrations`

Implements concept: Ch7 turn-taking and observability; Ch2 pattern map: moderated group conversation.

Real signatures:

```python
GroupChatState(current_round: int, participants: OrderedDict[str, str], conversation: list[Message]) -> None
GroupChatSelectionFunction = Callable[[GroupChatState], Awaitable[str] | str]
GroupChatRequestMessage(additional_instruction: str | None = None, metadata: dict[str, Any] | None = None) -> None
GroupChatRequestSentEvent(round_index: int, participant_name: str) -> None
GroupChatResponseReceivedEvent(round_index: int, participant_name: str) -> None
```

A selection function receives `GroupChatState` and returns the next participant name. The built-in group chat emits custom `WorkflowEvent(type="group_chat", data=...)` payloads such as `GroupChatRequestSentEvent` and `GroupChatResponseReceivedEvent`, in addition to normal executor and output events.

When to use: implement predictable turn order, custom speaker policies, or trace UI for group chat. When not to use: if the model should decide the next speaker, prefer `orchestrator_agent` and `AgentBasedGroupChatOrchestrator`.

Minimal example: `backend/examples/ch07/handoff_group_chat.py` uses `GroupChatState` for round-robin selection.

Inspected version: `agent-framework==1.9.0`.

## `GroupChatOrchestrator`, `AgentBasedGroupChatOrchestrator`, and `BaseGroupChatOrchestrator`

Implements concept: Ch7 centralized group coordinator; Ch2 pattern map: moderator/orchestrator agent.

Real signatures:

```python
BaseGroupChatOrchestrator(
    id: str,
    participant_registry: ParticipantRegistry,
    *,
    name: str | None = None,
    max_rounds: int | None = None,
    termination_condition: Callable[[list[Message]], bool | Awaitable[bool]] | None = None,
) -> None

GroupChatOrchestrator(
    id: str,
    participant_registry: ParticipantRegistry,
    selection_func: GroupChatSelectionFunction,
    *,
    name: str | None = None,
    max_rounds: int | None = None,
    termination_condition: TerminationCondition | None = None,
) -> None

AgentBasedGroupChatOrchestrator(
    agent: Agent,
    participant_registry: ParticipantRegistry,
    *,
    max_rounds: int | None = None,
    termination_condition: TerminationCondition | None = None,
    retry_attempts: int | None = None,
    session: AgentSession | None = None,
) -> None
```

`GroupChatBuilder` normally creates these for you. `GroupChatOrchestrator` uses a Python selection function; `AgentBasedGroupChatOrchestrator` uses an `Agent` to decide whether to terminate and who should speak next, returning an `AgentOrchestrationOutput` model.

When to use: subclass or provide a custom orchestrator only for specialized turn-taking. When not to use: use `GroupChatBuilder(selection_func=...)` for normal deterministic selection.

Minimal example: `backend/examples/ch07/handoff_group_chat.py` uses the builder path rather than direct orchestrator construction.

Inspected version: `agent-framework==1.9.0`.

## `SequentialBuilder` and `ConcurrentBuilder` / `agent_framework.orchestrations`

Implements concept: Ch7/Ch6 packaged orchestration helpers; Ch2 pattern map: multi-agent sequential pipeline and parallel ensemble.

Real signatures:

```python
SequentialBuilder(
    *,
    participants: Sequence[SupportsAgentRun | Executor],
    checkpoint_storage: CheckpointStorage | None = None,
    chain_only_agent_responses: bool = False,
    output_from: Sequence[str | SupportsAgentRun | Executor] | Literal["all"] | None = UNSET,
    intermediate_output_from: Sequence[str | SupportsAgentRun | Executor] | Literal["all", "all_other"] | None = None,
) -> None
SequentialBuilder.with_request_info(*, agents: Sequence[str | SupportsAgentRun] | None = None) -> SequentialBuilder
SequentialBuilder.build() -> Workflow

ConcurrentBuilder(...same participant/checkpoint/output shape...) -> None
ConcurrentBuilder.with_aggregator(aggregator: Executor | Callable[[list[AgentExecutorResponse]], Any] | Callable[[list[AgentExecutorResponse], WorkflowContext], Any]) -> ConcurrentBuilder
ConcurrentBuilder.with_request_info(*, agents: Sequence[str | SupportsAgentRun] | None = None) -> ConcurrentBuilder
ConcurrentBuilder.build() -> Workflow
```

These are higher-level builders for common multi-agent patterns. Sequential chains participants in order; `chain_only_agent_responses=True` limits downstream agent context to previous responses instead of the full conversation. Concurrent fans the same task to all participants and aggregates their `AgentExecutorResponse` values.

When to use: use these instead of hand-built graphs for standard agent pipelines or ensemble calls. When not to use: use raw `WorkflowBuilder` when you need custom non-agent routing, conditional edges, or fan-in semantics beyond the packaged builders.

Minimal example: Ch6 raw workflow equivalent is `backend/examples/ch06/workflow_patterns.py`; Ch7 focuses on handoff/group chat in `backend/examples/ch07/handoff_group_chat.py`.

Inspected version: `agent-framework==1.9.0`.
