"""No-network middleware demo for Agent Framework 1.9.0."""

import asyncio

from agent_framework import Agent, ChatResponse, Content, Message, MiddlewareTermination
from agent_framework import agent_middleware, chat_middleware
from agent_framework.openai import OpenAIChatClient


@agent_middleware
async def log_agent_run(context, call_next):
    print(f"agent middleware saw {len(context.messages)} message(s)")
    context.metadata["chapter"] = "09"
    await call_next()
    print(f"agent middleware result: {context.result.text}")


@chat_middleware
async def local_chat_response(context, call_next):
    print("chat middleware short-circuited request")
    context.result = ChatResponse(
        messages=Message(role="assistant", contents=[Content.from_text("local chat response")]),
        model="middleware-local",
    )
    raise MiddlewareTermination(result=context.result)


async def main() -> None:
    # The OpenAI client is never called because chat middleware terminates the
    # pipeline with a local ChatResponse before network I/O.
    client = OpenAIChatClient(model="not-called", api_key="placeholder")
    agent = Agent(client=client, name="middleware-demo", middleware=[log_agent_run, local_chat_response])
    response = await agent.run("hello from ch09")
    print(f"final: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
