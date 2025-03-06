from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TaskSearchParams:
    title: str


@dataclass(frozen=True)
class TaskSearchByIdParams:
    id: str


@dataclass(frozen=True)
class CreateTaskParams:
    id: int
    title: str
    description: Optional[str]
    status: str


@dataclass(frozen=True)
class UpdateTaskParams:
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    description: Optional[str]
    status: str


@dataclass(frozen=True)
class TaskErrorCode:
    NOT_FOUND: str = "TASK_ERR_01"
    BAD_REQUEST: str = "TASK_ERR_02"
    ALREADY_EXISTS: str = "TASK_ERR_03"
