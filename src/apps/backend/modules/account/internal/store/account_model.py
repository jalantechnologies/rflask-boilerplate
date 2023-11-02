from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class AccountModel(BaseModel):
  _id: Optional[str] = None
  active: bool = True
  username: str
  hashed_password: str
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  def to_json(self) -> str:
    return self.model_dump_json()

  def to_bson(self) -> dict[str, Any]:
    data = self.model_dump(exclude_none=True)
    if data["_id"] is None:
      data.pop("_id")
    return data

  @staticmethod
  def get_collection_name() -> str:
    return "accounts"
