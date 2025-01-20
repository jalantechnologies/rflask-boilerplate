from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TodosSearchByUsernameParams:
    username: str


@dataclass(frozen=True)
class TodoSearchByIdParams:
    todo_id: str


@dataclass(frozen=True)
class CreateTodoParams:
    username: str
    title: str
    description: str
    t_type: str
    due_date: datetime


@dataclass(frozen=True)
class Todo:
    id: str
    username: str
    title: str
    description: str
    t_type: str
    completed: bool
    due_date: datetime


@dataclass(frozen=True)
class TodoErrorCode:
    NOT_FOUND: str = "TODO_ERR_01"
    BAD_REQUEST: str = "TODO_ERR_02"
