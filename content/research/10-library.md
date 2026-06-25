# Chapter 10 library notes: Declarative agents, hosting, and DevUI

Inspected versions: `agent-framework==1.9.0`, `agent-framework-core==1.9.0`, `agent-framework-declarative==1.0.0rc2`, `agent-framework-devui==1.0.0b260528`, `agent-framework-foundry==1.8.2`, and `agent-framework-a2a==1.0.0b260604`. Introspection used `dir(...)`, `inspect.signature`, docstrings/source, local no-credential probes, and Microsoft Learn pages; installed package behavior wins on conflicts.

## Declarative agent loader / `agent_framework_declarative.AgentFactory`

Implements concept: Ch10 YAML-defined agents; Ch2 pattern map: configuration-first agent definitions separated from imperative host code.

Real signatures:

```python
AgentFactory(
    *,
    client: SupportsChatGetResponse | None = None,
    bindings: Mapping[str, Any] | None = None,
    connections: Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Any] | None = None,
    additional_mappings: Mapping[str, ProviderTypeMapping] | None = None,
    default_provider: str = "Foundry",
    safe_mode: bool = True,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
) -> None

AgentFactory.create_agent_from_yaml(yaml_str: str) -> Agent
AgentFactory.create_agent_from_yaml_path(yaml_path: str | Path) -> Agent
AgentFactory.create_agent_from_dict(agent_def: dict[str, Any]) -> Agent
AgentFactory.create_agent_from_yaml_async(yaml_str: str) -> Agent
AgentFactory.create_agent_from_yaml_path_async(yaml_path: str | Path) -> Agent
AgentFactory.create_agent_from_dict_async(agent_def: dict[str, Any]) -> Agent
```

`AgentFactory` is the real installed loader/factory for YAML `PromptAgent` definitions. It is available from both `agent_framework_declarative` and the alias `agent_framework.declarative`. A minimal YAML shape confirmed locally is `kind: Prompt`, `name`, `description`, `instructions`, and optional `model.options`; a preconfigured `client=` lets the agent be constructed and even run locally without credentials. If no client is supplied, the factory expects a `model` block and provider mapping, defaulting to Foundry.

When to use: user-editable agent specs, team-shared prompt/config assets, and tests that need to load the same YAML the host uses. When not to use: highly dynamic agent construction or trusted Python-only composition may be clearer as code; keep `safe_mode=True` for untrusted YAML.

Minimal example: `backend/examples/ch10/declarative_loader.py` with YAML at `backend/examples/ch10/local_prompt_agent.yaml`.

Inspected version: `agent-framework-declarative==1.0.0rc2` with core `agent-framework==1.9.0`.

## Declarative workflow loader / `agent_framework_declarative.WorkflowFactory`

Implements concept: Ch10 declarative orchestration/hosting boundary; Ch2 pattern map: workflow graph as configuration.

Real signatures:

```python
WorkflowFactory(
    *,
    agent_factory: AgentFactory | None = None,
    agents: Mapping[str, SupportsAgentRun | AgentExecutor] | None = None,
    bindings: Mapping[str, Any] | None = None,
    env_file: str | None = None,
    checkpoint_storage: CheckpointStorage | None = None,
    max_iterations: int | None = None,
    http_request_handler: HttpRequestHandler | None = None,
    mcp_tool_handler: MCPToolHandler | None = None,
    configuration: Mapping[str, str] | None = None,
    restrict_env_to_configuration: bool = True,
) -> None

WorkflowFactory.create_workflow_from_yaml(yaml_content: str, base_path: Path | None = None) -> Workflow
WorkflowFactory.create_workflow_from_yaml_path(yaml_path: str | Path) -> Workflow
WorkflowFactory.create_workflow_from_definition(workflow_def: dict[str, Any], base_path: Path | None = None) -> Workflow
WorkflowFactory.register_agent(name: str, agent: SupportsAgentRun | AgentExecutor) -> WorkflowFactory
WorkflowFactory.register_tool(name: str, func: Any) -> WorkflowFactory
WorkflowFactory.register_binding(name: str, func: Any) -> WorkflowFactory
```

`WorkflowFactory` parses declarative workflow YAML into core `Workflow` objects. It accepts prebuilt agents/tools/bindings, optional checkpoint storage, and explicit handlers for HTTP and MCP actions. The docstring highlights security-sensitive defaults: `configuration` is the controlled source for Power Fx `Env` values, and `restrict_env_to_configuration=True` prevents broad process-environment exposure.

When to use: declarative workflows with registered tools/agents, checkpointable action graphs, and host-specific policy around HTTP/MCP. When not to use: simple one-off workflows may be clearer with `WorkflowBuilder`.

Minimal example: documented here only; Wave 3 executable example focuses on declarative agent loading in `backend/examples/ch10/declarative_loader.py`.

Inspected version: `agent-framework-declarative==1.0.0rc2`.

## DevUI / `agent_framework_devui.serve` and `DevServer`

Implements concept: Ch10 local development host and visual debugger; Ch2 pattern map: test harness and OpenAI-compatible local endpoint.

Real signatures:

```python
serve(
    entities: list[Any] | None = None,
    entities_dir: str | None = None,
    port: int = 8080,
    host: str = "127.0.0.1",
    auto_open: bool = False,
    cors_origins: list[str] | None = None,
    ui_enabled: bool = True,
    instrumentation_enabled: bool = False,
    mode: str = "developer",
    auth_enabled: bool = True,
    auth_token: str | None = None,
) -> None

DevServer(
    entities_dir: str | None = None,
    port: int = 8080,
    host: str = "127.0.0.1",
    cors_origins: list[str] | None = None,
    ui_enabled: bool = True,
    mode: str = "developer",
    auth_enabled: bool = True,
    auth_token: str | None = None,
) -> None
```

The real DevUI launch entry point is `agent_framework_devui.serve` (also documented as `agent_framework.devui.serve` in Learn for the umbrella package). `serve(...)` constructs a `DevServer`, optionally registers in-memory entities, then starts `uvicorn`; Wave 3 examples intentionally do not call it. Learn describes DevUI as a sample development app, not production hosting, with a web UI, OpenAI-compatible API, directory discovery, and tracing view. Directory discovery requires each entity folder's `__init__.py` to export `agent` or `workflow`.

When to use: local manual testing, visual debugging, sample-gallery exploration, and OpenAI-compatible smoke tests. When not to use: production hosting or unattended services; use a real hosting adapter and auth/policy instead.

Minimal example: `backend/examples/ch10/devui_hosting_structure.py` imports and constructs only; it does not start a server.

Inspected version: `agent-framework-devui==1.0.0b260528`.

## Azure Functions hosting / `agent_framework.azure.AgentFunctionApp`

Implements concept: Ch10 serverless hosting adapter for agents/workflows; Ch2 pattern map: protocol/runtime adapter around framework agents.

Real signatures:

```python
AgentFunctionApp(
    agents: list[SupportsAgentRun] | None = None,
    workflow: Workflow | None = None,
    http_auth_level: func.AuthLevel = AuthLevel.FUNCTION,
    enable_health_check: bool = True,
    enable_http_endpoints: bool = True,
    max_poll_retries: int = 30,
    poll_interval_seconds: float = 1.0,
    enable_mcp_tool_trigger: bool = False,
    default_callback: AgentResponseCallbackProtocol | None = None,
)

AgentFunctionApp.add_agent(agent: SupportsAgentRun, callback: AgentResponseCallbackProtocol | None = None, enable_http_endpoint: bool | None = None, enable_mcp_tool_trigger: bool | None = None) -> None
```

`agent_framework.azure` exposes hosting and Azure integration classes including `AgentFunctionApp`, `DurableAIAgent`, `DurableAIAgentClient`, `DurableAIAgentWorker`, `CosmosHistoryProvider`, and `AzureAISearchContextProvider`. Microsoft Learn's Python hosting page shows `AgentFunctionApp` as the Azure Functions entry point and `FoundryChatClient` as a common hosted model client.

When to use: Azure Functions deployment, health endpoints, HTTP agent endpoints, durable agent orchestration, and optional MCP tool triggers. When not to use: local visual debugging (DevUI is easier) or non-Azure hosting.

Minimal example: `backend/examples/ch10/devui_hosting_structure.py` constructs `AgentFunctionApp(agents=[])` without starting an Azure Functions host.

Inspected version: core `agent-framework==1.9.0`.

## Foundry clients and hosted agents / `agent_framework.foundry`

Implements concept: Ch10 Microsoft Foundry-backed model and hosted-agent integration; Ch2 pattern map: managed runtime/provider adapter.

Real signatures:

```python
FoundryChatClient(
    *,
    project_endpoint: str | None = None,
    project_client: AIProjectClient | None = None,
    model: str | None = None,
    credential: AzureCredentialTypes | AzureTokenProvider | None = None,
    allow_preview: bool | None = None,
    default_headers: Mapping[str, str] | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
    instruction_role: str | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    additional_properties: dict[str, Any] | None = None,
    middleware: Sequence[ChatAndFunctionMiddlewareTypes] | None = None,
    function_invocation_configuration: FunctionInvocationConfiguration | None = None,
) -> None

FoundryAgent(
    *,
    project_endpoint: str | None = None,
    agent_name: str | None = None,
    agent_version: str | None = None,
    credential: AzureCredentialTypes | None = None,
    project_client: AIProjectClient | None = None,
    allow_preview: bool | None = None,
    default_headers: Mapping[str, str] | None = None,
    tools: FunctionTool | Callable[..., Any] | Sequence[FunctionTool | Callable[..., Any]] | None = None,
    context_providers: Sequence[ContextProvider] | None = None,
    middleware: Sequence[MiddlewareTypes] | None = None,
    client_type: type[RawFoundryAgentChatClient] | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
    id: str | None = None,
    name: str | None = None,
    description: str | None = None,
    instructions: str | None = None,
    default_options: FoundryAgentOptionsT | Mapping[str, Any] | None = None,
    require_per_service_call_history_persistence: bool = False,
    function_invocation_configuration: FunctionInvocationConfiguration | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    additional_properties: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> None
```

`agent_framework.foundry` and `agent_framework_foundry` export `FoundryChatClient`, `FoundryAgent`, raw variants, embedding clients, eval helpers, and `to_prompt_agent`. `FoundryAgent` connects to an existing PromptAgent or HostedAgent in Foundry and adds full middleware/telemetry; `RawFoundryAgent` is the lower-level variant without those layers. `FoundryChatClient` is the model/chat client used for Foundry project deployments.

When to use: Azure AI Foundry projects, managed PromptAgent/HostedAgent connections, Foundry tracing, and production model clients. When not to use: no-credential local examples or offline tests; use a fake `SupportsChatGetResponse` client.

Minimal example: `backend/examples/ch10/devui_hosting_structure.py` verifies imports and skips live construction unless environment variables are present.

Inspected version: `agent-framework-foundry==1.8.2`.

## A2A integration / `agent_framework_a2a.A2AAgent`, `A2AExecutor`

Implements concept: Ch10 Agent-to-Agent protocol interoperability and remote agent hosting/client boundaries.

Real signatures:

```python
A2AAgent(
    *,
    name: str | None = None,
    id: str | None = None,
    description: str | None = None,
    agent_card: AgentCard | None = None,
    url: str | None = None,
    client: Client | None = None,
    http_client: httpx.AsyncClient | None = None,
    auth_interceptor: AuthInterceptor | None = None,
    timeout: float | httpx.Timeout | None = None,
    supported_protocol_bindings: list[Literal["JSONRPC", "GRPC", "HTTP+JSON"] | str] | None = None,
    **kwargs: Any,
) -> None

A2AAgent.run(
    messages: AgentRunInputs | None = None,
    *,
    stream: bool = False,
    session: AgentSession | None = None,
    function_invocation_kwargs: Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Any] | None = None,
    continuation_token: A2AContinuationToken | None = None,
    background: bool = False,
    **kwargs: Any,
) -> Awaitable[AgentResponse[Any]] | ResponseStream[AgentResponseUpdate, AgentResponse[Any]]

A2AExecutor(agent: SupportsAgentRun, stream: bool = False, run_kwargs: Mapping[str, Any] | None = None)
A2AAgentSession(*, context_id: str | None = None, task_id: str | None = None, task_state: TaskState | None = None) -> None
```

The installed A2A surface is `agent_framework_a2a` plus aliases under `agent_framework.a2a`. `A2AAgent` is a client-side wrapper for a remote A2A-compliant agent, converting Agent Framework messages to A2A protocol messages and responses back to `AgentResponse`. `A2AExecutor` bridges a local `SupportsAgentRun` agent/workflow to A2A server infrastructure. Learn frames A2A as standardized discovery through agent cards, message communication, long-running tasks, and cross-framework interoperability.

When to use: multi-agent systems where agents may be remote or built with different frameworks. When not to use: in-process agent composition, where `Agent.as_tool`, workflows, or group chat/handoff orchestrations are simpler.

Minimal example: `backend/examples/ch10/devui_hosting_structure.py` verifies imports and prints skip messages for live A2A client construction.

Inspected version: `agent-framework-a2a==1.0.0b260604`.
