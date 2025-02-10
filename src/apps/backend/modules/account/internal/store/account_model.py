from datetime import datetime
from typing import Optional
from bson import ObjectId
from dataclasses import dataclass
from modules.account.types import PhoneNumber
from modules.common.base_model import BaseModel


@dataclass
class AccountModel(BaseModel):
    
    first_name: str
    hashed_password: str
    id: Optional[ObjectId | str]
    last_name: str
    phone_number: Optional[PhoneNumber]
    username: str
    
    active: bool = True
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    @staticmethod
    def get_collection_name() -> str:
        return "accounts"
