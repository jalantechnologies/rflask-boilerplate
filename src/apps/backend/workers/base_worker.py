from abc import ABC, abstractmethod
from typing import Any

from modules.application.types import WorkerPriority


class BaseWorker(ABC):
    """
    Base class for all Temporal workers.
    """

    priority: WorkerPriority = WorkerPriority.DEFAULT

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Subclasses must implement the run() method, which is the application's entry point.
        """
