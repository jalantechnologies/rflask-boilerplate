from datetime import datetime
from typing import Annotated, Optional

from bson import ObjectId
from pydantic import AfterValidator, BaseModel, ConfigDict, Field
from modules.common.validation_utils import ValidationUtils

PyObjectId = Annotated[ObjectId | str, AfterValidator(ValidationUtils.object_id_validate)]


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
