from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class TodoModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    account_id: str = ""
    title: str = ""
    description: str = ""
    t_type: str = ""
    due_date: Optional[datetime] = None
    completed: bool = False
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_bson(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data

    @staticmethod
    def get_collection_name() -> str:
        return "todos"
