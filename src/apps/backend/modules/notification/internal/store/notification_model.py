from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from bson import ObjectId


@dataclass
class NotificationModel:
    user_id: str
    payload: dict
    type: str
    channels: List[str]
    schedule_at: Optional[str] = None
    id: ObjectId
    active: bool = True
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def to_bson(self):
        return self.__dict__

    @staticmethod
    def get_collection_name() -> str:
        return "notifications"
