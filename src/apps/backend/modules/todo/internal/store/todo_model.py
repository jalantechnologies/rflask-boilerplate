# modules/todo/internal/store/todo_model.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bson import ObjectId

from modules.application.base_model import BaseModel


@dataclass
class TodoModel(BaseModel):
    id: Optional[ObjectId | str]
    title: str
    description: Optional[str]
    status: str
    due_date: Optional[datetime]
    account_id: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    type: Optional[str] = None

    @classmethod
    def from_bson(cls, bson_data: dict) -> "TodoModel":
        return cls(
            id=bson_data.get("_id"),
            title=bson_data.get("title", ""),
            description=bson_data.get("description"),
            status=bson_data.get("status", "todo"),
            due_date=bson_data.get("due_date"),
            account_id=bson_data.get("account_id", ""),
            created_at=bson_data.get("created_at"),
            updated_at=bson_data.get("updated_at"),
        )

    @staticmethod
    def get_collection_name() -> str:
        return "todos"
