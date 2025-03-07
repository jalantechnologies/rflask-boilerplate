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


@dataclass(frozen=True)
class WorkerErrorCode:
    WORKER_CLIENT_CONNECTION_ERROR: str = "WORKER_ERR_01"
    WORKER_CLASS_INVALID: str = "WORKER_ERR_02"
    WORKER_WITH_ID_NOT_FOUND: str = "WORKER_ERR_03"
    WORKER_START_ERROR: str = "WORKER_ERR_04"
    WORKER_ALREADY_COMPLETED: str = "WORKER_ERR_05"
    WORKER_ALREADY_CANCELLED: str = "WORKER_ERR_06"
    WORKER_ALREADY_TERMINATED: str = "WORKER_ERR_07"
