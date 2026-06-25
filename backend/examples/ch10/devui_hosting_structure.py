"""Import-only DevUI, hosting, Foundry, and A2A structure probe."""

import os

from agent_framework.azure import AgentFunctionApp
from agent_framework.foundry import FoundryAgent, FoundryChatClient
from agent_framework_a2a import A2AAgent, A2AExecutor
from agent_framework_devui import DevServer, serve


def main() -> None:
    server = DevServer(port=8765, auth_enabled=False)
    function_app = AgentFunctionApp(agents=[])

    print(f"devui entry point: {serve.__module__}.serve")
    print(f"dev server constructed: {type(server).__name__} (not started)")
    print(f"azure functions app constructed: {type(function_app).__name__}")
    print(f"foundry imports: {FoundryAgent.__name__}, {FoundryChatClient.__name__}")
    print(f"a2a imports: {A2AAgent.__name__}, {A2AExecutor.__name__}")

    if not os.getenv("FOUNDRY_PROJECT_ENDPOINT"):
        print("skipping Foundry live construction: FOUNDRY_PROJECT_ENDPOINT not set")
    if not os.getenv("A2A_AGENT_URL"):
        print("skipping A2A live client construction: A2A_AGENT_URL not set")
    print("server launch skipped intentionally; call serve(...) only in an app entry point")


if __name__ == "__main__":
    main()
