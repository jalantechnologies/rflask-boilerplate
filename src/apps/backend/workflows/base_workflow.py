from abc import ABC, abstractmethod
from typing import Any

from modules.workflow.types import WorkflowPriority


class BaseWorkflow(ABC):
    """
    Base class for all Temporal workflows.
    """

    priority = WorkflowPriority.DEFAULT

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Subclasses must implement the run() method, which is the workflow's entry point.
        """
        pass
