from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from bson import ObjectId
from modules.account.types import PhoneNumber


class OtpModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[ObjectId | str] = Field(None, alias="_id")
    active: bool = True
    otp_code: str
    phone_number: PhoneNumber
    status: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    def to_json(self) -> str:
        return self.model_dump_json()

    def to_bson(self) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        return data

    @staticmethod
    def get_collection_name() -> str:
        return "otps"
