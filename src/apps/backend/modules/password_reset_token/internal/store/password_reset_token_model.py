from bson import ObjectId
from datetime import datetime
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field, validator, ConfigDict

def object_id_validate(v: ObjectId | str) -> ObjectId:
    if isinstance(v, str):
        if not ObjectId.is_valid(v):
            raise ValueError(f'{v} is not a valid ObjectId')
        return ObjectId(v)
    elif isinstance(v, ObjectId):
        return v


PyObjectId = Annotated[ObjectId | str, validator('object_id_validate')]


class PasswordResetTokenModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(None, alias="_id")
    account: PyObjectId
    expires_at: datetime 
    token: str
    is_used: bool = False

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
