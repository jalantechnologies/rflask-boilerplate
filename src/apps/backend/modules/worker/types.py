from dataclasses import dataclass
from typing import Optional

from celery import Task


@dataclass(frozen=True)
class SearchTaskByIdParams:
    id: str


@dataclass(frozen=True)
class SearchTaskByNameParams:
    name: str


@dataclass(frozen=True)
class QueueTaskParams:
    task: Task
    task_params: Optional[dict] = None


@dataclass(frozen=True)
class WorkerErrorCode:
    TASK_WITH_NAME_NOT_FOUND: str = "WORKER_ERR_01"
    TASK_WITH_ID_NOT_FOUND: str = "WORKER_ERR_02"
