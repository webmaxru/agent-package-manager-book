"""Load a declarative YAML agent without credentials or network."""

import asyncio
import sys
from pathlib import Path

# Importing agent_framework_declarative pulls in powerfx, which prints a Unicode
# checkmark at import time. Force UTF-8 stdout so this works on Windows consoles
# (cp1252) too, where it would otherwise raise UnicodeEncodeError.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from agent_framework import ChatResponse, Content, Message
from agent_framework_declarative import AgentFactory


class LocalChatClient:
    async def get_response(self, messages, *, stream=False, options=None, middleware=None, **kwargs):
        return ChatResponse(
            messages=Message(role="assistant", contents=[Content.from_text("loaded declarative agent locally")]),
            model="local-no-network",
        )


async def main() -> None:
    yaml_path = Path(__file__).with_name("local_prompt_agent.yaml")
    factory = AgentFactory(client=LocalChatClient())
    agent = factory.create_agent_from_yaml_path(yaml_path)
    response = await agent.run("confirm load")
    print(f"loaded: {agent.name}")
    print(f"description: {agent.description}")
    print(f"response: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
