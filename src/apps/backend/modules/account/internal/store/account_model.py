from bson import ObjectId
from datetime import datetime
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import AfterValidator


def object_id_validate(v: ObjectId | str) -> ObjectId | str:
  assert ObjectId.is_valid(v), f'{v} is not a valid ObjectId'
  if isinstance(v, str):
    return ObjectId(v)
  return str(v)


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
