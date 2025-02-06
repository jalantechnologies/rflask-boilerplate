from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Task:
    id: str
    account_id: str
    title: str
    description: str


@dataclass(frozen=True)
class GetAllTaskParams:
    account_id: str
    page: Optional[int] = 1
    size: Optional[int] = None


@dataclass(frozen=True)
class GetTaskParams:
    account_id: str
    task_id: str


@dataclass(frozen=True)
class PaginationParams:
    page: int
    size: int


@dataclass(frozen=True)
class CreateTaskParams:
    account_id: str
    description: str
    title: str


@dataclass(frozen=True)
class UpdateTaskParams:
    account_id: str
    description: str
    task_id: str
    title: str


@dataclass(frozen=True)
class DeleteTaskParams:
    account_id: str
    task_id: str

@dataclass(frozen=True)
class TaskErrorCode:
    NOT_FOUND: str = "TASK_ERR_01"
    BAD_REQUEST: str = "TASK_ERR_04"
