"""Chapter 6: graph workflows with sequential, fan-out/fan-in, and conditional edges.

Runs without model credentials.
"""

import asyncio

from agent_framework import Case, Default, Executor, WorkflowBuilder, WorkflowContext, handler


class UpperCase(Executor):
    def __init__(self) -> None:
        super().__init__(id="upper")

    @handler(input=str, output=str)
    async def handle(self, text: str, ctx: WorkflowContext[str, str]) -> None:
        await ctx.send_message(text.upper())


class AddSuffix(Executor):
    def __init__(self, id: str, suffix: str) -> None:
        self.suffix = suffix
        super().__init__(id=id)

    @handler(input=str, output=str)
    async def handle(self, text: str, ctx: WorkflowContext[str, str]) -> None:
        await ctx.send_message(f"{text}{self.suffix}")


class FinalSuffix(Executor):
    def __init__(self) -> None:
        self.suffix = "!"
        super().__init__(id="exclaim")

    @handler(input=str, workflow_output=str)
    async def handle(self, text: str, ctx: WorkflowContext[None, str]) -> None:
        await ctx.yield_output(f"{text}{self.suffix}")


class JoinResults(Executor):
    def __init__(self) -> None:
        super().__init__(id="join")

    @handler(input=list[str], workflow_output=str)
    async def handle(self, results: list[str], ctx: WorkflowContext[None, str]) -> None:
        await ctx.yield_output(" | ".join(sorted(results)))


class Classifier(Executor):
    def __init__(self) -> None:
        super().__init__(id="classifier")

    @handler(input=str, output=str)
    async def handle(self, text: str, ctx: WorkflowContext[str, str]) -> None:
        await ctx.send_message(text)


class Label(Executor):
    def __init__(self, id: str, label: str) -> None:
        self.label = label
        super().__init__(id=id)

    @handler(input=str, workflow_output=str)
    async def handle(self, text: str, ctx: WorkflowContext[None, str]) -> None:
        await ctx.yield_output(f"{self.label}: {text}")


async def sequential_demo() -> None:
    upper = UpperCase()
    exclaim = FinalSuffix()
    workflow = WorkflowBuilder(start_executor=upper, output_from=[exclaim]).add_edge(upper, exclaim).build()
    result = await workflow.run("hello")
    print("sequential:", result.get_outputs())


async def fan_out_fan_in_demo() -> None:
    upper = UpperCase()
    a = AddSuffix("branch_a", " from A")
    b = AddSuffix("branch_b", " from B")
    join = JoinResults()
    workflow = (
        WorkflowBuilder(start_executor=upper, output_from=[join])
        .add_fan_out_edges(upper, [a, b])
        .add_fan_in_edges([a, b], join)
        .build()
    )
    result = await workflow.run("parallel")
    print("fan_out_fan_in:", result.get_outputs())


async def conditional_demo() -> None:
    classifier = Classifier()
    urgent = Label("urgent", "urgent")
    normal = Label("normal", "normal")
    workflow = (
        WorkflowBuilder(start_executor=classifier, output_from=[urgent, normal])
        .add_switch_case_edge_group(
            classifier,
            [
                Case(lambda text: "!" in text, urgent),
                Default(normal),
            ],
        )
        .build()
    )
    result = await workflow.run("ship it!")
    print("conditional:", result.get_outputs())


async def main() -> None:
    await sequential_demo()
    await fan_out_fan_in_demo()
    await conditional_demo()


if __name__ == "__main__":
    asyncio.run(main())
