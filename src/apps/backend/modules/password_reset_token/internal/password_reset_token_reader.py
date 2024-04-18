from bson.objectid import ObjectId

from modules.password_reset_token.errors import PasswordResetTokenNotFoundError
from modules.password_reset_token.internal.store.password_reset_token_repository import PasswordResetTokenRepository
from modules.password_reset_token.types import PasswordResetToken
from modules.password_reset_token.internal.password_reset_token_util import PasswordResetTokenUtil

class PasswordResetTokenReader:
    @staticmethod
    def get_password_reset_token_by_account_id(account_id: str) -> PasswordResetToken:
        cursor = PasswordResetTokenRepository.password_reset_token_db.find(
            {"account": ObjectId(account_id)}
        ).sort("created_at", -1)

        try:
            token_data = next(cursor)
        except StopIteration:
            raise PasswordResetTokenNotFoundError(account_id)

        return PasswordResetToken(
            id=str(token_data.get("_id")),
            is_expired=PasswordResetTokenUtil.is_token_expired(token_data.get("expires_at")),
            account=token_data.get("account"),
            token=token_data.get("token"),
            expires_at=token_data.get("expires_at"),
            is_used=token_data.get("is_used"),
        )
