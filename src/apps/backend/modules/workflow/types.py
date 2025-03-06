from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type


@dataclass(frozen=True)
class SearchWorkflowByIdParams:
    id: str
    runs_limit: Optional[int] = None


@dataclass(frozen=True)
class QueueWorkflowParams:
    cls: Type
    arguments: list
    cron_schedule: str


@dataclass(frozen=True)
class WorkflowErrorCode:
    WORKFLOW_CLIENT_CONNECTION_ERROR: str = "WORKER_ERR_01"
    WORKFLOW_NOT_REGISTERED: str = "WORKER_ERR_02"
    WORKFLOW_WITH_ID_NOT_FOUND: str = "WORKER_ERR_03"
    WORKFLOW_START_ERROR: str = "WORKER_ERR_04"
    WORKFLOW_ALREADY_COMPLETED: str = "WORKER_ERR_05"
    WORKFLOW_ALREADY_CANCELLED: str = "WORKER_ERR_06"
    WORKFLOW_ALREADY_TERMINATED: str = "WORKER_ERR_07"


class WorkflowPriority(Enum):
    DEFAULT = "DEFAULT"
    CRITICAL = "CRITICAL"
