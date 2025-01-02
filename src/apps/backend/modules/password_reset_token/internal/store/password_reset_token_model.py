from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from modules.object_id.utils import object_id_validate

class PasswordResetTokenModel:
    def __init__(
        self,
        id: Optional[ObjectId | str] = None,
        account: Optional[ObjectId | str] = None,
        expires_at: datetime = datetime.now(),
        token: str = "",
        is_used: bool = False,
        **kwargs:Any
    ) -> None:
        self.id = object_id_validate(id) if id else kwargs.get("_id", None)
        self.account = object_id_validate(account) if account else kwargs.get("account", None)
        self.expires_at = expires_at
        self.token = token
        self.is_used = is_used

    @staticmethod
    def get_collection_name() -> str:
        return "password_reset_tokens"
