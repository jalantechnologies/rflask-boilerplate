from dataclasses import dataclass
from datetime import datetime, timezone

from bson import ObjectId

from modules.common.base_model import BaseModel


@dataclass
class TaskModel(BaseModel):
    id: ObjectId
    title: str
    description: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    @classmethod
    def from_bson(cls, bson_data: dict) -> "TaskModel":
        return cls(
            id=bson_data.get("_id"),
            title=bson_data.get("title", ""),
            description=bson_data.get("description", ""),
            created_at=bson_data.get("created_at"),
            updated_at=bson_data.get("updated_at"),
        )

    @staticmethod
    def get_collection_name() -> str:
        return "tasks"
