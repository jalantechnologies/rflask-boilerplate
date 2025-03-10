from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId


@dataclass
class CommentModel:
    id: Optional[str] = None
    task_id: str = field(default_factory=str)
    user_id: str = field(default_factory=str)
    content: str = field(default_factory=str)
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    @classmethod
    def from_bson(cls, bson_data: dict):
        return cls(
            id=str(bson_data["_id"]),
            task_id=str(bson_data["task_id"]),
            user_id=str(bson_data["user_id"]),
            content=bson_data["content"],
            created_at=bson_data["created_at"],
            updated_at=bson_data["updated_at"],
        )

    def to_bson(self) -> dict:
        return {
            "_id": ObjectId(self.id) if self.id else ObjectId(),
            "task_id": ObjectId(self.task_id),
            "user_id": ObjectId(self.user_id),
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
