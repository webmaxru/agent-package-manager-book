# Chapter 6 library notes: Workflows for sequential and concurrent orchestration

Inspected version: `agent-framework==1.9.0` (`agent-framework-core==1.9.0`, `agent-framework-orchestrations==1.9.0`). Introspection used `dir(agent_framework)`, `inspect.signature`, docstrings, installed package source under `.venv\Lib\site-packages`, and Microsoft Learn workflow pages; installed package names/signatures win on conflicts.

## `WorkflowBuilder` / `agent_framework.WorkflowBuilder`

Implements concept: Ch6 graph workflow builder; Ch2 pattern map: explicit sequential pipelines, fan-out/fan-in concurrent orchestration, and conditional routing.

Real signatures:

```python
WorkflowBuilder(
    max_iterations: int = 100,
    name: str | None = None,
    description: str | None = None,
    *,
    start_executor: Executor | SupportsAgentRun,
    checkpoint_storage: CheckpointStorage | None = None,
    output_from: list[Executor | SupportsAgentRun] | Literal["all"] | None = UNSET,
    intermediate_output_from: list[Executor | SupportsAgentRun] | Literal["all", "all_other"] | None = UNSET,
    output_executors: list[Executor | SupportsAgentRun] | None = UNSET,
) -> None

WorkflowBuilder.add_edge(source, target, condition=None) -> Self
WorkflowBuilder.add_chain(executors: Sequence[Executor | SupportsAgentRun]) -> Self
WorkflowBuilder.add_fan_out_edges(source, targets: Sequence[Executor | SupportsAgentRun]) -> Self
WorkflowBuilder.add_fan_in_edges(sources: Sequence[Executor | SupportsAgentRun], target) -> Self
WorkflowBuilder.add_switch_case_edge_group(source, cases: Sequence[Case | Default]) -> Self
WorkflowBuilder.add_multi_selection_edge_group(source, targets, selection_func) -> Self
WorkflowBuilder.build() -> Workflow
```

`WorkflowBuilder` creates a validated directed graph. It accepts either custom `Executor` instances or agents that implement the framework agent-run protocol; agents are wrapped internally as `AgentExecutor`. Terminal output is a build-time designation: use `output_from=[...]` for final outputs and `intermediate_output_from=[...]` for observational outputs.

When to use: fixed business processes, typed dataflow, deterministic fan-out/fan-in, and graph-level checkpointing. When not to use: simple one-shot agent calls or dynamic agent-driven control flow where handoff/group chat is a better fit.

Minimal example: `backend/examples/ch06/workflow_patterns.py`.

Inspected version: `agent-framework==1.9.0`.

## `Executor`, `@handler`, `@executor`, and `WorkflowContext` / `agent_framework`

Implements concept: Ch6 workflow node/executor; Ch2 pattern map: task decomposition units connected by routing edges.

Real signatures:

```python
Executor(id: str, *, type: str | None = None, type_: str | None = None, defer_discovery: bool = False, **_: Any) -> None

handler(func=None, *, input=None, output=None, workflow_output=None) -> Callable[..., Any]
executor(func=None, *, id=None, input=None, output=None, workflow_output=None) -> FunctionExecutor

async WorkflowContext.send_message(message: OutT, target_id: str | None = None) -> None
async WorkflowContext.yield_output(output: W_OutT) -> None
async WorkflowContext.add_event(event: WorkflowEvent[Any]) -> None
async WorkflowContext.request_info(request_data: object, response_type: type, *, request_id: str | None = None) -> None
```

Executors are async processing units. Class executors subclass `Executor` and decorate methods with `@handler`; standalone functions can be converted with `@executor`. Handlers must expose type information via annotations or explicit decorator parameters so the builder can validate edge compatibility. `WorkflowContext` methods are `async` in source and must be awaited, even though basic `inspect.signature` output only shows return annotations.

When to use: custom non-LLM logic, adapters, validators, aggregators, and workflow glue around agents. When not to use: do not put long, unrelated business processes into one executor if you need event visibility/checkpoint boundaries between steps.

Minimal example: `backend/examples/ch06/workflow_patterns.py`.

Inspected version: `agent-framework==1.9.0`.

## Edges: direct, fan-out, fan-in, switch/case / `agent_framework.Case`, `agent_framework.Default`

Implements concept: Ch6 orchestration control flow; Ch2 pattern map: chain, concurrent branches, barrier aggregation, and conditional branch.

Real signatures:

```python
Case(condition: Callable[[Any], bool], target: Executor | SupportsAgentRun) -> None
Default(target: Executor | SupportsAgentRun) -> None
WorkflowBuilder.add_edge(source, target, condition: Callable[[Any], bool | Awaitable[bool]] | None = None) -> Self
WorkflowBuilder.add_fan_out_edges(source, targets) -> Self
WorkflowBuilder.add_fan_in_edges(sources, target) -> Self
WorkflowBuilder.add_switch_case_edge_group(source, cases: Sequence[Case | Default]) -> Self
```

A direct edge routes every compatible message to one target. Fan-out sends one source message to multiple targets that run in the next superstep. Fan-in is a barrier edge group: the target runs only after all source executors complete and receives `list[T]`, so the target handler must declare `input=list[T]`. Switch/case groups require exactly one `Default` case in 1.9.0.

When to use: use edges when routing is known at design time. When not to use: avoid switch/case for open-ended LLM routing; handoff or group chat may be clearer.

Minimal example: `backend/examples/ch06/workflow_patterns.py`.

Inspected version: `agent-framework==1.9.0`.

## `Workflow` and `WorkflowRunResult` / `agent_framework.Workflow`, `agent_framework.WorkflowRunResult`

Implements concept: Ch6 workflow runtime and result collection; Ch2 pattern map: deterministic superstep execution.

Real signatures:

```python
Workflow.run(
    message: Any | None = None,
    *,
    stream: bool = False,
    responses: Mapping[str, Any] | None = None,
    checkpoint_id: str | None = None,
    checkpoint_storage: CheckpointStorage | None = None,
    include_status_events: bool = False,
    function_invocation_kwargs: Mapping[str, Mapping[str, Any]] | Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Mapping[str, Any]] | Mapping[str, Any] | None = None,
) -> ResponseStream[WorkflowEvent, WorkflowRunResult] | Awaitable[WorkflowRunResult]

WorkflowRunResult(events: list[WorkflowEvent[Any]], status_events: list[WorkflowEvent[Any]] | None = None) -> None
WorkflowRunResult.get_outputs() -> list[Any]
WorkflowRunResult.get_intermediate_outputs() -> list[Any]
WorkflowRunResult.get_request_info_events() -> list[WorkflowEvent[Any]]
WorkflowRunResult.get_final_state() -> WorkflowRunState
Workflow.as_agent(name: str | None = None, *, description: str | None = None, context_providers=None, **kwargs) -> WorkflowAgent
```

`Workflow.run()` is non-streaming by default and returns a list-like `WorkflowRunResult`; with `stream=True`, it returns a `ResponseStream` of `WorkflowEvent` objects. The runtime uses a Pregel-like superstep model: all ready executors in a superstep run, then a synchronization barrier occurs before the next superstep.

When to use: use non-streaming for batch-style workflows and streaming for UI/progress/HITL. When not to use: do not expect a chained branch to advance past a superstep barrier while a sibling branch is still running.

Minimal example: `backend/examples/ch06/workflow_patterns.py`.

Inspected version: `agent-framework==1.9.0`.

## `AgentExecutor`, `AgentExecutorRequest`, `AgentExecutorResponse` / `agent_framework`

Implements concept: Ch6 agent-as-workflow-node; Ch2 pattern map: hybrid workflows that combine deterministic steps with LLM agents.

Real signatures:

```python
AgentExecutor(
    agent: SupportsAgentRun,
    *,
    session: AgentSession | None = None,
    id: str | None = None,
    context_mode: Literal["full", "last_agent", "custom"] | None = None,
    context_filter: Callable[[list[Message]], list[Message]] | None = None,
)
AgentExecutorRequest(messages: list[Message], should_respond: bool = True) -> None
AgentExecutorResponse(executor_id: str, agent_response: AgentResponse, full_conversation: list[Message]) -> None
```

`AgentExecutor` adapts an agent to workflow message handling. It can pass full conversation context, the last agent response, or custom-filtered messages, and emits `AgentExecutorResponse` for downstream orchestration components.

When to use: use when an agent is one step in a larger workflow. When not to use: direct `Agent.run()` is simpler for a single agent without graph routing.

Minimal example: agent-backed orchestration is demonstrated without live credentials in `backend/examples/ch07/handoff_group_chat.py` using a fake chat client.

Inspected version: `agent-framework==1.9.0`.
