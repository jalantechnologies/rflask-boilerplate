from datetime import datetime
from typing import Optional
from bson import ObjectId
from dataclasses import dataclass
from modules.common.base_model import BaseModel


@dataclass
class PasswordResetTokenModel(BaseModel):
    
    account: ObjectId | str
    expires_at: datetime
    id: Optional[ObjectId | str]
    token: str
    
    is_used: bool = False

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
