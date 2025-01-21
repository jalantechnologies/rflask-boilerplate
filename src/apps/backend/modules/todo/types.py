from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TodosSearchByAccountIdParams:
    account_id: str
    limit: Optional[int] = 0


@dataclass(frozen=True)
class TodoSearchByIdParams:
    todo_id: str


@dataclass(frozen=True)
class CreateTodoParams:
    account_id: str
    title: str
    description: str
    t_type: str
    due_date: datetime


@dataclass(frozen=True)
class Todo:
    id: str
    account_id: str
    title: str
    description: str
    type: str
    dueDate: datetime
    completed: bool
    completedDate: Optional[datetime] = None


@dataclass(frozen=True)
class TodoErrorCode:
    NOT_FOUND: str = "TODO_ERR_01"
    BAD_REQUEST: str = "TODO_ERR_02"
