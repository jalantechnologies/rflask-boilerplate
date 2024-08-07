from functools import wraps
from typing import Any, Callable

from flask import request

from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.errors import (
    AccessTokenInvalidError,
    AuthorizationHeaderNotFoundError,
    InvalidAuthorizationHeaderError,
    UnauthorizedAccessError,
)


def access_auth_middleware(next_func: Callable) -> Callable:
    @wraps(next_func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise AuthorizationHeaderNotFoundError("Authorization header is missing.")

        auth_scheme, auth_token = auth_header.split(" ")
        if auth_scheme != "Bearer" or not auth_token:
            raise InvalidAuthorizationHeaderError("Invalid authorization header.")

        try:
            auth_payload = AccessTokenService.verify_access_token(token=auth_token)
        except AccessTokenInvalidError:
            raise InvalidAuthorizationHeaderError("Invalid authorization header.")

        if "account_id" in kwargs and auth_payload.account_id != kwargs["account_id"]:
            raise UnauthorizedAccessError("Unauthorized access.")

        setattr(request, "account_id", auth_payload.account_id)  # Set account_id attribute on request
        return next_func(*args, **kwargs)

    return wrapper
