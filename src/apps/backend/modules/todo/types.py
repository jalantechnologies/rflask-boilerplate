# modules/todo/types.py

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional


@dataclass
class Todo:
    id: str
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[datetime]
    type: Optional[str] = None


@dataclass
class CreateTodoParams:
    title: str
    description: Optional[str]
    status: str = "todo"
    due_date: Optional[datetime] = None
    type: Optional[Literal["Personal", "Official", "Hobby"]] = None


@dataclass
class UpdateTodoParams:
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
