from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TaskSearchParams:
    title: str


@dataclass(frozen=True)
class CreateTaskParams:
    title: str
    description: Optional[str]


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class TaskErrorCode:
    NOT_FOUND = "TASK_NOT_FOUND"
    BAD_REQUEST = "TASK_BAD_REQUEST"
    ALREADY_EXISTS = "TASK_ALREADY_EXISTS"
    CREATION_ERROR = "TASK_CREATION_ERROR"
    SERVICE_ERROR = "TASK_SERVICE_ERROR"
    DATABASE_ERROR = "TASK_DATABASE_ERROR"
    CONVERSION_ERROR = "TASK_CONVERSION_ERROR"
