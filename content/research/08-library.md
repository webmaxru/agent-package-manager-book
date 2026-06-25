# Chapter 8 library notes: Streaming, checkpointing, and human-in-the-loop

Inspected version: `agent-framework==1.9.0` (`agent-framework-core==1.9.0`). Introspection used `inspect.signature`, installed source, local no-credential probes, and Microsoft Learn pages for events, checkpoints, and HITL; installed package behavior wins on conflicts.

## Workflow streaming: `Workflow.run(..., stream=True)`, `ResponseStream`, and `WorkflowEvent`

Implements concept: Ch8 event streaming and progress observation; Ch2 pattern map: observable orchestration and incremental UI updates.

Real signatures:

```python
Workflow.run(message=None, *, stream: bool = False, responses=None, checkpoint_id=None, checkpoint_storage=None, include_status_events=False, function_invocation_kwargs=None, client_kwargs=None) -> ResponseStream[WorkflowEvent, WorkflowRunResult] | Awaitable[WorkflowRunResult]

ResponseStream(stream: AsyncIterable[UpdateT] | Awaitable[AsyncIterable[UpdateT]], *, finalizer=None, transform_hooks=None, cleanup_hooks=None, result_hooks=None) -> None
ResponseStream.get_final_response() -> FinalT

WorkflowEvent(
    type: WorkflowEventType,
    data: DataT | None = None,
    *,
    origin: WorkflowEventSource | None = None,
    state: WorkflowRunState | None = None,
    details: WorkflowErrorDetails | None = None,
    executor_id: str | None = None,
    request_id: str | None = None,
    source_executor_id: str | None = None,
    request_type: type[Any] | None = None,
    response_type: type[Any] | None = None,
    iteration: int | None = None,
) -> None
```

With `stream=True`, workflow execution is consumed using `async for event in workflow.run(..., stream=True)`. Event types confirmed in docs/source include `started`, `status`, `output`, `intermediate`, `failed`, `error`, `warning`, `executor_invoked`, `executor_completed`, `executor_failed`, deprecated `data`, `superstep_started`, `superstep_completed`, and `request_info`. `WorkflowEvent` also has factory methods such as `started`, `status`, `executor_invoked`, `executor_completed`, `superstep_started`, `superstep_completed`, `request_info`, `warning`, and `error`.

When to use: terminal progress UIs, long-running jobs, human approval loops, and debugging. When not to use: use non-streaming `await workflow.run(...)` for simple batch calls where only final outputs matter.

Minimal example: `backend/examples/ch08/stream_checkpoint_hitl.py`.

Inspected version: `agent-framework==1.9.0`.

## Agent streaming: `Agent.run(..., stream=True)`, `AgentResponseUpdate`, and agent events in workflows

Implements concept: Ch8 token/update streaming from LLM-backed agents; Ch2 pattern map: streaming agent response surfaces inside orchestrations.

Real signatures:

```python
Agent.run(messages=None, *, stream: bool = False, session=None, middleware=None, tools=None, options=None, compaction_strategy=None, tokenizer=None, function_invocation_kwargs=None, client_kwargs=None) -> Awaitable[AgentResponse[Any]] | ResponseStream[AgentResponseUpdate, AgentResponse[Any]]

AgentResponseUpdate(*, contents=None, role=None, author_name=None, agent_id=None, response_id=None, message_id=None, created_at=None, finish_reason=None, continuation_token=None, additional_properties=None, raw_representation=None) -> None
```

There is no separate `run_stream` method in 1.9.0. Agent streaming uses `run(..., stream=True)` and returns `ResponseStream`. Inside workflow orchestrations, `AgentExecutor` and group/handoff builders surface agent output through workflow `output` events containing `AgentResponseUpdate` chunks while streaming and `AgentResponse` values at completion.

When to use: chat UIs and multi-agent traces where users should see incremental model output. When not to use: avoid streaming in tests that only assert final values unless you need event-level behavior.

Minimal example: no live LLM streaming is executed because there is no API key; workflow streaming is verified in `backend/examples/ch08/stream_checkpoint_hitl.py`, and fake-agent orchestration is in `backend/examples/ch07/handoff_group_chat.py`.

Inspected version: `agent-framework==1.9.0`.

## Checkpoint storage / `agent_framework.CheckpointStorage`, `InMemoryCheckpointStorage`, `FileCheckpointStorage`, `WorkflowCheckpoint`

Implements concept: Ch8 durability, pause/resume, and superstep-boundary recovery; Ch2 pattern map: durable workflow execution.

Real signatures:

```python
CheckpointStorage  # Protocol
async CheckpointStorage.save(checkpoint: WorkflowCheckpoint) -> CheckpointID
async CheckpointStorage.load(checkpoint_id: CheckpointID) -> WorkflowCheckpoint
async CheckpointStorage.list_checkpoints(*, workflow_name: str) -> list[WorkflowCheckpoint]
async CheckpointStorage.list_checkpoint_ids(*, workflow_name: str) -> list[CheckpointID]
async CheckpointStorage.get_latest(*, workflow_name: str) -> WorkflowCheckpoint | None
async CheckpointStorage.delete(checkpoint_id: CheckpointID) -> bool

InMemoryCheckpointStorage() -> None
FileCheckpointStorage(storage_path: str | Path, *, allowed_checkpoint_types: list[str] | None = None) -> None

WorkflowCheckpoint(
    workflow_name: str,
    graph_signature_hash: str,
    checkpoint_id: CheckpointID = factory,
    previous_checkpoint_id: CheckpointID | None = None,
    timestamp: str = factory,
    messages: dict[str, list[WorkflowMessage]] = factory,
    state: dict[str, Any] = factory,
    pending_request_info_events: dict[str, WorkflowEvent[Any]] = factory,
    iteration_count: int = 0,
    metadata: dict[str, Any] = factory,
    version: str = "1.0",
) -> None
```

Checkpointing is enabled by passing storage to `WorkflowBuilder(..., checkpoint_storage=...)` or to `workflow.run(..., checkpoint_storage=...)`. Checkpoints are created at superstep boundaries and capture pending messages, shared state, executor state, iteration count, and pending request-info events. `InMemoryCheckpointStorage` is for tests/demos; `FileCheckpointStorage` persists locally and should be treated as trusted private storage because non-JSON values may require pickle serialization.

When to use: long-running workflows, HITL pauses, recovery, auditability, and local durable demos. When not to use: do not load file checkpoints from untrusted or tampered storage.

Minimal example: `backend/examples/ch08/stream_checkpoint_hitl.py` uses `InMemoryCheckpointStorage` and lists saved checkpoints.

Inspected version: `agent-framework==1.9.0`.

## Checkpoint resume and executor state hooks / `Workflow.run(checkpoint_id=...)`, `Executor.on_checkpoint_save`, `Executor.on_checkpoint_restore`

Implements concept: Ch8 resume/rehydration; Ch2 pattern map: resumable orchestration state.

Real signatures:

```python
Workflow.run(..., checkpoint_id: str | None = None, checkpoint_storage: CheckpointStorage | None = None, stream: bool = False) -> ...
async Executor.on_checkpoint_save() -> dict[str, Any]
async Executor.on_checkpoint_restore(state: dict[str, Any]) -> None
```

To resume, load or list checkpoints from storage, then call `workflow.run(checkpoint_id=saved.checkpoint_id, stream=True)` on the same workflow or pass both `checkpoint_id` and `checkpoint_storage` to a newly built compatible workflow. Executors that maintain internal mutable fields should override the async checkpoint hooks to save and restore their own state.

When to use: stateful executors, workflows that must survive process restarts, and HITL workflows that pause at request boundaries. When not to use: stateless one-shot workflows usually do not need custom hooks.

Minimal example: `backend/examples/ch08/stream_checkpoint_hitl.py` demonstrates checkpoint creation; resume API is documented in this note but not forced in the snippet because the example completes after responding.

Inspected version: `agent-framework==1.9.0`.

## Human-in-the-loop request/response / `WorkflowContext.request_info` and `@response_handler`

Implements concept: Ch8 human-in-the-loop and external asynchronous input; Ch2 pattern map: approval gate and pending request/resume.

Real signatures:

```python
async WorkflowContext.request_info(request_data: object, response_type: type, *, request_id: str | None = None) -> None

response_handler(
    func=None,
    *,
    request: type | UnionType | str | None = None,
    response: type | UnionType | str | None = None,
    output: type | UnionType | str | None = None,
    workflow_output: type | UnionType | str | None = None,
) -> Callable[..., Any]

Workflow.run(..., responses: Mapping[str, Any] | None = None) -> ...
```

An executor calls `await ctx.request_info(request_data=..., response_type=...)`; the workflow emits `WorkflowEvent(type="request_info")` with `event.request_id`, `event.data`, source executor id, request type, and response type. The external caller collects responses in a `{request_id: response}` mapping and calls `workflow.run(responses=responses)`; the framework routes each response to the matching `@response_handler` method.

When to use: human approvals, external forms, async API callbacks, or any workflow pause that needs caller input. When not to use: simple synchronous decisions can be handled inside an executor without request/response.

Minimal example: `backend/examples/ch08/stream_checkpoint_hitl.py` collects a request event and resumes with an approval response.

Inspected version: `agent-framework==1.9.0`.

## Tool approval as HITL / `ToolApprovalMiddleware` and approval response helpers

Implements concept: Ch8 human approval for agent tool calls; Ch2 pattern map: approval gate around side-effecting tools.

Real signatures:

```python
ToolApprovalMiddleware(*args, **kwargs)
create_always_approve_tool_response(request: Content, *, reason: str | None = None) -> Content
create_always_approve_tool_with_arguments_response(request: Content, *, reason: str | None = None) -> Content
```

Tool approval APIs are present under the top-level package and `_harness._tool_approval`, but docstrings mark the middleware and related state/rule types as experimental. In workflow orchestrations, approval-required tools surface through the same `request_info` event path, typically carrying `Content(type="function_approval_request")` and expecting an approval response content.

When to use: side-effecting tools such as deploy, purchase, refund, or data deletion. When not to use: do not depend on experimental approval middleware without version pinning and tests.

Minimal example: `backend/examples/ch08/stream_checkpoint_hitl.py` demonstrates the stable generic request/response mechanism rather than experimental tool approval middleware.

Inspected version: `agent-framework==1.9.0`.
