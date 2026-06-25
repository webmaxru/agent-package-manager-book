"""Chapter 8: streaming events, checkpoint storage, and HITL request/response."""

import asyncio
from dataclasses import dataclass

from agent_framework import (
    Executor,
    InMemoryCheckpointStorage,
    WorkflowBuilder,
    WorkflowContext,
    handler,
    response_handler,
)


@dataclass
class ApprovalRequest:
    item: str


class ApprovalExecutor(Executor):
    def __init__(self) -> None:
        super().__init__(id="approval")

    @handler(input=str)
    async def start(self, item: str, ctx: WorkflowContext[ApprovalRequest, str]) -> None:
        await ctx.request_info(ApprovalRequest(item), response_type=bool)

    @response_handler(request=ApprovalRequest, response=bool, workflow_output=str)
    async def on_response(self, request: ApprovalRequest, approved: bool, ctx: WorkflowContext[None, str]) -> None:
        verdict = "approved" if approved else "rejected"
        await ctx.yield_output(f"{request.item}: {verdict}")


async def main() -> None:
    checkpoint_storage = InMemoryCheckpointStorage()
    approval = ApprovalExecutor()
    workflow = WorkflowBuilder(
        name="approval_workflow",
        start_executor=approval,
        checkpoint_storage=checkpoint_storage,
        output_from=[approval],
    ).build()

    responses: dict[str, bool] = {}
    async for event in workflow.run("deploy production", stream=True):
        if event.type == "request_info":
            print(f"stream_request: {event.request_id} -> {event.data}")
            responses[event.request_id] = True
        elif event.type in {"started", "status", "superstep_completed"}:
            print(f"stream_event: {event.type}")

    checkpoints = await checkpoint_storage.list_checkpoints(workflow_name=workflow.name)
    print("checkpoint_count:", len(checkpoints))

    result = await workflow.run(responses=responses)
    print("final_outputs:", result.get_outputs())


if __name__ == "__main__":
    asyncio.run(main())
