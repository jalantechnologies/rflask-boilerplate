from bson.objectid import ObjectId

from modules.authentication.errors import PasswordResetTokenNotFoundError
from modules.authentication.internals.password_reset_token.password_reset_token_util import PasswordResetTokenUtil
from modules.authentication.internals.password_reset_token.store.password_reset_token_repository import (
    PasswordResetTokenRepository,
)
from modules.authentication.types import PasswordResetToken


class PasswordResetTokenReader:
    @staticmethod
    def get_password_reset_token_by_account_id(account_id: str) -> PasswordResetToken:
        cursor = (
            PasswordResetTokenRepository.collection().find({"account": ObjectId(account_id)}).sort("expires_at", -1)
        )

        try:
            token_data = next(cursor)
        except StopIteration:
            raise PasswordResetTokenNotFoundError()

        return PasswordResetToken(
            id=str(token_data.get("_id")),
            is_expired=PasswordResetTokenUtil.is_token_expired(token_data.get("expires_at")),
            account=token_data.get("account"),
            token=token_data.get("token"),
            expires_at=token_data.get("expires_at"),
            is_used=token_data.get("is_used"),
        )
