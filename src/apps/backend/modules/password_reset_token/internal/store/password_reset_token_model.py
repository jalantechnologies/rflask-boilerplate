from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

class PasswordResetTokenModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    account: ObjectId | str
    expires_at: datetime
    token: str
    is_used: bool = False

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
