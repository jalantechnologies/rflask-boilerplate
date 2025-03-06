from abc import ABC, abstractmethod
from typing import Any

from modules.worker.types import WorkerPriority


class BaseWorker(ABC):
    """
    Base class for all Temporal workers.
    """

    priority: WorkerPriority = WorkerPriority.DEFAULT

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Subclasses must implement the run() method, which is the worker's entry point.
        """
