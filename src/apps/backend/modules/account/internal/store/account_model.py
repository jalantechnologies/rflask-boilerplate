from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from modules.account.types import PhoneNumber
class AccountModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    active: bool = True
    first_name: str = ""
    hashed_password: str = ""
    phone_number: Optional[PhoneNumber] = None
    last_name: str = ""
    username: str = ""
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_bson(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data

    @staticmethod
    def get_collection_name() -> str:
        return "accounts"
