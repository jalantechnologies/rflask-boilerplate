from abc import ABC, abstractmethod

from modules.workflow.types import WorkflowPriority


class BaseWorkflow(ABC):
    """
    Base class for all Temporal workflows.
    """

    priority = WorkflowPriority.DEFAULT

    @abstractmethod
    async def run(self, *args, **kwargs):
        """
        Subclasses must implement the run() method, which is the workflow's entry point.
        """
        pass
