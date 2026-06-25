"""Chapter 7: handoff and group chat orchestration without live LLM credentials."""

import asyncio
from collections.abc import Sequence
from typing import Any

from agent_framework import Agent, ChatResponse, Message
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState, HandoffBuilder


class FakeChatClient:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    async def get_response(self, messages: Sequence[Message], **_: Any) -> ChatResponse[str]:
        last = messages[-1].text if messages else ""
        return ChatResponse(messages=Message("assistant", [f"{self.prefix}: {last}"]))


def fake_agent(name: str, description: str) -> Agent:
    return Agent(
        FakeChatClient(name),
        name=name,
        description=description,
        instructions=f"You are {name}.",
        require_per_service_call_history_persistence=True,
    )


async def handoff_demo() -> None:
    triage = fake_agent("triage", "Routes requests to specialists")
    billing = fake_agent("billing", "Handles billing requests")
    workflow = (
        HandoffBuilder(
            participants=[triage, billing],
            termination_condition=lambda messages: sum(1 for m in messages if m.role == "assistant") >= 1,
        )
        .add_handoff(triage, [billing], description="Billing issue")
        .add_handoff(billing, [triage], description="Return to triage")
        .with_start_agent(triage)
        .build()
    )
    result = await workflow.run("I need help with an invoice")
    print("handoff_outputs:", [output.text for output in result.get_outputs()])


async def group_chat_demo() -> None:
    writer = fake_agent("writer", "Drafts copy")
    reviewer = fake_agent("reviewer", "Reviews copy")

    def select_next(state: GroupChatState) -> str:
        names = list(state.participants.keys())
        return names[state.current_round % len(names)]

    workflow = GroupChatBuilder(participants=[writer, reviewer], selection_func=select_next, max_rounds=2).build()
    result = await workflow.run("Create a short product slogan")
    print("group_chat_outputs:", [getattr(output, "text", output) for output in result.get_outputs()])


async def main() -> None:
    await handoff_demo()
    await group_chat_demo()


if __name__ == "__main__":
    asyncio.run(main())
