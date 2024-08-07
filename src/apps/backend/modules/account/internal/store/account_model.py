from datetime import datetime
from typing import Annotated, Any, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import AfterValidator

from modules.object_id.utils import object_id_validate

PyObjectId = Annotated[ObjectId | str, AfterValidator(object_id_validate)]


class AccountModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(None, alias="_id")
    active: bool = True
    first_name: str
    hashed_password: str
    last_name: str
    username: str
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
