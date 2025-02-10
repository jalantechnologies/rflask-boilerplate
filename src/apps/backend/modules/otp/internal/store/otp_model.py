from datetime import datetime
from typing import Optional
from bson import ObjectId
from modules.account.types import PhoneNumber
from dataclasses import dataclass
from modules.common.base_model import BaseModel


@dataclass
class OtpModel(BaseModel):
    active: bool
    id: Optional[ObjectId | str]
    otp_code: str
    phone_number: PhoneNumber
    status: str
    
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    @staticmethod
    def get_collection_name() -> str:
        return "otps"
