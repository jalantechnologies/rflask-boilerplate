from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class TaskModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    title: str
    account: ObjectId | str = Field(None, alias="account")
    description: str
    active: bool = True
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_bson(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data

    @staticmethod
    def get_collection_name() -> str:
        return "tasks"
