from datetime import datetime, timedelta

import jwt

from modules.access_token.errors import AccessTokenExpiredError, AccessTokenInvalidError
from modules.access_token.types import AccessToken, AccessTokenPayload, CreateAccessTokenParams
from modules.account.internal.account_reader import AccountReader
from modules.account.types import Account, AccountSearchParams
from modules.config.config_service import ConfigService


class AccessTokenService:
    @staticmethod
    def create_access_token(*, params: CreateAccessTokenParams) -> AccessToken:
        account = AccountReader.get_account_by_username_and_password(
            params=AccountSearchParams(username=params.username, password=params.password)
        )

        return AccessTokenService.__generate_access_token(account=account)

    @staticmethod
    def __generate_access_token(*, account: Account) -> AccessToken:
        jwt_signing_key = ConfigService.get_token_signing_key()
        jwt_expiry = timedelta(days=ConfigService.get_token_expiry_days())
        payload = {"account_id": account.id, "exp": (datetime.now() + jwt_expiry).timestamp()}
        jwt_token = jwt.encode(payload, jwt_signing_key, algorithm="HS256")
        access_token = AccessToken(token=jwt_token, account_id=account.id, expires_at=str(payload["exp"]))

        return access_token

    @staticmethod
    def verify_access_token(*, token: str) -> AccessTokenPayload:

        jwt_signing_key = ConfigService.get_token_signing_key()

        try:
            verified_token = jwt.decode(token, jwt_signing_key, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            raise AccessTokenInvalidError("Invalid access token")

        if verified_token.get("exp") * 1000 < datetime.now().timestamp() * 1000:
            raise AccessTokenExpiredError(message="Access token has expired. Please login again.")

        return AccessTokenPayload(account_id=verified_token.get("account_id"))
