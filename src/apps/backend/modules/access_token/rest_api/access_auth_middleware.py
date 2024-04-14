from modules.access_token.access_token_service import AccessTokenService
from modules.access_token.errors import AccessTokenInvalidError, AuthorizationHeaderNotFoundError, InvalidAuthorizationHeaderError, UnauthorizedAccessError
from flask import request
from functools import wraps

def access_auth_middleware(next_func):
    @wraps(next_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthorizationHeaderNotFoundError()

        auth_scheme, auth_token = auth_header.split(' ')
        if auth_scheme != 'Bearer' or not auth_token:
            raise InvalidAuthorizationHeaderError()

        try:
            auth_payload = AccessTokenService.verify_access_token(token=auth_token)
        except AccessTokenInvalidError:
            raise InvalidAuthorizationHeaderError()

        if 'account_id' in kwargs and auth_payload.get('account_id') != kwargs['account_id']:
            raise UnauthorizedAccessError()

        request.account_id = auth_payload.get('account_id')
        return next_func(*args, **kwargs)

    return wrapper
