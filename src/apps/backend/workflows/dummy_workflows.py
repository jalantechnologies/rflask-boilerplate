from modules.workflow.types import WorkflowPriority
from workflows.base_workflow import BaseWorkflow
from workflows.workflow_registry import register_workflow


@register_workflow
class TestDefaultWorkflow(BaseWorkflow):
    """
    A simple test workflow to demonstrate the default-priority worker.
    """

    async def run(self, x: int, y: int) -> int:
        return x + y


@register_workflow
class TestCriticalWorkflow(BaseWorkflow):
    """
    A simple test workflow to demonstrate a critical-priority worker.
    """

    priority: WorkflowPriority = WorkflowPriority.CRITICAL

    async def run(self, x: int, y: int) -> int:
        return x + y
