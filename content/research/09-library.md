# Chapter 9 library notes: Middleware and observability

Inspected version: `agent-framework==1.9.0` (`agent-framework-core==1.9.0`). Introspection used `dir(...)`, `inspect.signature`, docstrings/source, no-credential probes, and Microsoft Learn pages for middleware and observability; installed package behavior wins on conflicts.

## Agent middleware / `agent_framework.AgentMiddleware`, `agent_middleware`, `AgentContext`

Implements concept: Ch9 request/response middleware around agent runs; Ch2 pattern map: cross-cutting policy, logging, validation, retries, and short-circuiting.

Real signatures:

```python
AgentMiddleware()
async AgentMiddleware.process(context: AgentContext, call_next: Callable[[], Awaitable[None]]) -> None

agent_middleware(func: AgentMiddlewareCallable) -> AgentMiddlewareCallable

AgentContext(
    *,
    agent: SupportsAgentRun,
    messages: list[Message],
    session: AgentSession | None = None,
    tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None = None,
    options: Mapping[str, Any] | None = None,
    stream: bool = False,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    metadata: Mapping[str, Any] | None = None,
    result: AgentResponse | ResponseStream[AgentResponseUpdate, AgentResponse] | None = None,
    kwargs: Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Any] | None = None,
    function_invocation_kwargs: Mapping[str, Any] | None = None,
    stream_transform_hooks: Sequence[Callable[[AgentResponseUpdate], AgentResponseUpdate | Awaitable[AgentResponseUpdate]]] | None = None,
    stream_result_hooks: Sequence[Callable[[AgentResponse], AgentResponse | Awaitable[AgentResponse]]] | None = None,
    stream_cleanup_hooks: Sequence[Callable[[], Awaitable[None] | None]] | None = None,
) -> None

Agent(..., middleware: Sequence[MiddlewareTypes] | None = None)
Agent.run(..., middleware: Sequence[MiddlewareTypes] | None = None, ...)
```

Agent middleware is class-based (`AgentMiddleware.process`) or function-based (`@agent_middleware`). It receives a mutable `AgentContext`; call `await call_next()` to continue, inspect or replace `context.result` afterward, or set `context.result` and raise `MiddlewareTermination` to skip the remaining pipeline. Registration is either durable on `Agent(..., middleware=[...])` or per-call through `agent.run(..., middleware=[...])`; agent-level middleware wraps run-level middleware.

When to use: logging, guardrails, retries, redaction, response shaping, and per-run policy. When not to use: provider-specific request mutation is usually better as chat middleware, and tool-call argument validation is better as function middleware.

Minimal example: `backend/examples/ch09/middleware_demo.py`.

Inspected version: `agent-framework==1.9.0`.

## Chat middleware / `agent_framework.ChatMiddleware`, `chat_middleware`, `ChatContext`

Implements concept: Ch9 request/response middleware around model/chat-client calls; Ch2 pattern map: transport/provider instrumentation and prompt/request policy.

Real signatures:

```python
ChatMiddleware()
async ChatMiddleware.process(context: ChatContext, call_next: Callable[[], Awaitable[None]]) -> None

chat_middleware(func: ChatMiddlewareCallable) -> ChatMiddlewareCallable

ChatContext(
    client: SupportsChatGetResponse,
    messages: Sequence[Message],
    options: Mapping[str, Any] | None,
    stream: bool = False,
    metadata: Mapping[str, Any] | None = None,
    result: ChatResponse | ResponseStream[ChatResponseUpdate, ChatResponse] | None = None,
    kwargs: Mapping[str, Any] | None = None,
    function_invocation_kwargs: Mapping[str, Any] | None = None,
    stream_transform_hooks: Sequence[Callable[[ChatResponseUpdate], ChatResponseUpdate | Awaitable[ChatResponseUpdate]]] | None = None,
    stream_result_hooks: Sequence[Callable[[ChatResponse], ChatResponse | Awaitable[ChatResponse]]] | None = None,
    stream_cleanup_hooks: Sequence[Callable[[], Awaitable[None] | None]] | None = None,
) -> None

OpenAIChatClient(..., middleware: Sequence[ChatAndFunctionMiddlewareTypes] | None = None, ...)
OpenAIChatClient.get_response(..., middleware: Sequence[ChatAndFunctionMiddlewareTypes] | None = None, ...)
```

Chat middleware wraps `get_response` on clients that include the `ChatMiddlewareLayer` (confirmed with `OpenAIChatClient`). It can be registered on the chat client, per `get_response(...)`, or on an `Agent` using a middleware list; the agent passes chat/function middleware down to capable clients. This is the right layer for raw message/options inspection, request substitution, telemetry correlation, or local short-circuiting before a network call.

When to use: request logging, system-message injection, model-call caching, prompt filtering, provider retries, and no-network test fakes. When not to use: whole-agent behavior that should include tools/session state belongs in agent middleware.

Minimal example: `backend/examples/ch09/middleware_demo.py`.

Inspected version: `agent-framework==1.9.0`.

## Function middleware / `agent_framework.FunctionMiddleware`, `function_middleware`, `FunctionInvocationContext`

Implements concept: Ch9 middleware around tool/function invocation; Ch2 pattern map: side-effect guardrails, audit, and validation.

Real signatures:

```python
FunctionMiddleware()
async FunctionMiddleware.process(context: FunctionInvocationContext, call_next: Callable[[], Awaitable[None]]) -> None

function_middleware(func: FunctionMiddlewareCallable) -> FunctionMiddlewareCallable

FunctionInvocationContext(
    function: FunctionTool,
    arguments: BaseModel | Mapping[str, Any],
    session: AgentSession | None = None,
    metadata: Mapping[str, Any] | None = None,
    result: Any = None,
    kwargs: Mapping[str, Any] | None = None,
    tools: list[ToolTypes] | None = None,
) -> None
```

Function middleware intercepts the framework's tool/function invocation loop. It can inspect the selected `FunctionTool`, validate `context.arguments`, call `await call_next()` to execute the tool, then transform or cache `context.result`; raising `MiddlewareTermination` from this pipeline propagates as a function-loop termination signal rather than being suppressed.

When to use: tool authorization, argument allowlists, idempotency, caching, audit trails, and masking tool outputs. When not to use: do not use it for model request mutation or whole-agent retry policies.

Minimal example: not separately executed in Wave 3; the registered type and context were introspected, and agent/chat middleware are verified in `backend/examples/ch09/middleware_demo.py`.

Inspected version: `agent-framework==1.9.0`.

## Middleware control flow and exceptions / `MiddlewareTermination`, `MiddlewareException`, type aliases

Implements concept: Ch9 exception handling and early termination.

Real signatures:

```python
MiddlewareTermination(message: str = "Middleware terminated execution.", *, result: Any = None) -> None
MiddlewareException(message: str, inner_exception: Exception | None = None, log_level: Literal[0,10,20,30,40,50] | None = 10, *args: Any, **kwargs: Any)

AgentMiddlewareTypes = AgentMiddleware | Callable[[AgentContext, Callable[[], Awaitable[None]]], Awaitable[None]]
ChatMiddlewareTypes = ChatMiddleware | Callable[[ChatContext, Callable[[], Awaitable[None]]], Awaitable[None]]
FunctionMiddlewareTypes = FunctionMiddleware | Callable[[FunctionInvocationContext, Callable[[], Awaitable[None]]], Awaitable[None]]
MiddlewareTypes = AgentMiddlewareTypes | ChatMiddlewareTypes | FunctionMiddlewareTypes
```

`MiddlewareTermination` is a control-flow exception. Agent and chat pipelines suppress it after the middleware has set `context.result`; function middleware lets it propagate to signal tool-loop termination. Invalid or ambiguous middleware registration is wrapped as `MiddlewareException`. Ordinary exceptions raised before/after `call_next()` propagate to the caller unless the middleware catches them and sets a fallback result.

When to use: use `MiddlewareTermination` for deliberate short-circuiting and ordinary exceptions for real failures. When not to use: do not use `MiddlewareTermination` without setting an appropriate `context.result` for agent/chat pipelines.

Minimal example: `backend/examples/ch09/middleware_demo.py`.

Inspected version: `agent-framework==1.9.0`.

## Observability setup / `agent_framework.observability.configure_otel_providers`

Implements concept: Ch9 OpenTelemetry traces/logs/metrics setup; Ch2 pattern map: observable agent runtime and distributed tracing.

Real signatures:

```python
configure_otel_providers(
    *,
    enable_sensitive_data: bool | None = None,
    enable_console_exporters: bool | None = None,
    exporters: list[LogRecordExporter | SpanExporter | MetricExporter] | None = None,
    views: list[View] | None = None,
    vs_code_extension_port: int | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
) -> None

enable_instrumentation(*, enable_sensitive_data: bool | None = None, force: bool = False) -> None
disable_instrumentation() -> None
enable_sensitive_telemetry(*, force: bool = False) -> None
get_tracer(instrumenting_module_name: str = "agent_framework", instrumenting_library_version: str = "1.9.0", schema_url: str | None = None, attributes: dict[str, Any] | None = None) -> trace.Tracer
get_meter(name: str = "agent_framework", version: str = "1.9.0", schema_url: str | None = None, attributes: dict[str, Any] | None = None) -> metrics.Meter
```

The installed package does not expose `setup_observability` or `configure_tracing`; the real setup function is `agent_framework.observability.configure_otel_providers`. It configures OpenTelemetry providers/exporters from arguments and standard `OTEL_EXPORTER_OTLP_*` environment variables, plus Agent Framework flags such as `ENABLE_CONSOLE_EXPORTERS`, `ENABLE_SENSITIVE_DATA`, and `VS_CODE_EXTENSION_PORT`. In the installed 1.9.0 process, `OBSERVABILITY_SETTINGS.enable_instrumentation` defaulted to `True` and sensitive data defaulted to `False`, even though one Learn page still describes env-based enablement; package behavior wins.

When to use: call once at application startup before agent/workflow calls, or use `enable_instrumentation()` after a third-party OTel setup such as Azure Monitor or Langfuse. When not to use: do not call `configure_otel_providers()` repeatedly in the same process, and do not enable sensitive telemetry in production.

Minimal example: `backend/examples/ch09/observability_setup.py`.

Inspected version: `agent-framework==1.9.0`.

## Telemetry layers / `AgentTelemetryLayer`, `ChatTelemetryLayer`, `EmbeddingTelemetryLayer`

Implements concept: Ch9 automatic spans on agent, chat, and embedding calls.

Real signatures:

```python
AgentTelemetryLayer(*args: Any, otel_agent_provider_name: str | None = None, otel_provider_name: str | None = None, **kwargs: Any) -> None
ChatTelemetryLayer(*args: Any, otel_provider_name: str | None = None, **kwargs: Any) -> None
EmbeddingTelemetryLayer(*args: Any, otel_provider_name: str | None = None, **kwargs: Any) -> None
workflow_tracer() -> Tracer
create_mcp_client_span(method_name: str, target: str | None = None, attributes: dict[str, Any] | None = None) -> Generator[trace.Span, Any, Any]
```

These mixin layers are used by framework agents/clients to emit GenAI-convention OpenTelemetry spans. Learn notes that workflows also emit spans such as `workflow.build`, `workflow.run`, `executor.process ...`, `edge_group.process ...`, and `message.send`. MCP client spans are supported through `create_mcp_client_span`, and Learn documents automatic trace propagation to client-opened MCP sessions.

When to use: rely on built-in telemetry layers in concrete framework clients/agents and add custom spans with `get_tracer()` for app-specific work. When not to use: application code normally should not subclass these layers unless building a provider adapter.

Minimal example: `backend/examples/ch09/observability_setup.py`.

Inspected version: `agent-framework==1.9.0`.
