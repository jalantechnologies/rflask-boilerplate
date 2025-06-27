# modules/todo/types.py

from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional


@dataclass(frozen=True, kw_only=True)
class Todo:
    description: Optional[str]
    due_date: Optional[date]
    id: str
    status: str
    title: str
    type: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class CreateTodoParams:
    description: Optional[str]
    due_date: Optional[date] = None
    status: str = "todo"
    title: str
    type: Optional[Literal["Personal", "Official", "Hobby"]] = None


@dataclass(frozen=True, kw_only=True)
class UpdateTodoParams:
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    title: Optional[str] = None
