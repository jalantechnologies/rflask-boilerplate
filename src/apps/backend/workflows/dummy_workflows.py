from workflows.workflow_registry import register_temporal_workflow


@register_temporal_workflow()
class TestDefaultWorkflow:
    """
    A simple test workflow to demonstrate the Temporal workflow decorator.

    This workflow adds two numbers together.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y


@register_temporal_workflow(priority="critical")
class TestCriticalWorkflow:
    """
    A simple test workflow to demonstrate the Temporal workflow decorator.

    This workflow adds two numbers together.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y
