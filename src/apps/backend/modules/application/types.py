from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Type

from temporalio.client import WorkflowExecutionStatus


class WorkerPriority(Enum):
    DEFAULT = "DEFAULT"
    CRITICAL = "CRITICAL"


class BaseWorker(ABC):
    """
    Base class for all Temporal workers.
    """

    priority: WorkerPriority = WorkerPriority.DEFAULT

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any) -> None:
        """
        Subclasses must implement the run() method, which is the application's entry point.
        """


@dataclass(frozen=True)
class RegisteredWorker:
    cls: Type[BaseWorker]
    priority: WorkerPriority


@dataclass(frozen=True)
class Worker:
    id: str
    status: Optional[WorkflowExecutionStatus]
    start_time: datetime
    close_time: Optional[datetime]
    task_queue: str
    worker_type: str
