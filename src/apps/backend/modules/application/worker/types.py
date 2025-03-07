from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional, Type

if TYPE_CHECKING:
    from workers.base_worker import BaseWorker


@dataclass(frozen=True)
class SearchWorkerByIdParams:
    id: str
    runs_limit: Optional[int] = None


@dataclass(frozen=True)
class RunWorkerImmediatelyParams:
    cls: Type["BaseWorker"]
    arguments: list


@dataclass(frozen=True)
class RunWorkerAsCronParams:
    cls: Type["BaseWorker"]
    arguments: list
    cron_schedule: str  # Example: "/10 * * * *" (every 10 minutes)


@dataclass(frozen=True)
class WorkerErrorCode:
    WORKER_CLIENT_CONNECTION_ERROR: str = "WORKER_ERR_01"
    WORKER_CLASS_INVALID: str = "WORKER_ERR_02"
    WORKER_CLASS_NOT_REGISTERED: str = "WORKER_ERR_03"
    WORKER_WITH_ID_NOT_FOUND: str = "WORKER_ERR_04"
    WORKER_START_ERROR: str = "WORKER_ERR_05"
    WORKER_ALREADY_COMPLETED: str = "WORKER_ERR_06"
    WORKER_ALREADY_CANCELLED: str = "WORKER_ERR_07"
    WORKER_ALREADY_TERMINATED: str = "WORKER_ERR_08"


class WorkerPriority(Enum):
    DEFAULT = "DEFAULT"
    CRITICAL = "CRITICAL"
