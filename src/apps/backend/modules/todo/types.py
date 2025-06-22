# modules/todo/types.py

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional


@dataclass
class Todo:
    description: Optional[str]
    due_date: Optional[datetime]
    id: str
    status: str
    title: str
    type: Optional[str] = None


@dataclass(kw_only=True)
class CreateTodoParams:
    description: Optional[str]
    due_date: Optional[datetime] = None
    status: str = "todo"
    title: str
    type: Optional[Literal["Personal", "Official", "Hobby"]] = None


@dataclass(kw_only=True)
class UpdateTodoParams:
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    title: Optional[str] = None
