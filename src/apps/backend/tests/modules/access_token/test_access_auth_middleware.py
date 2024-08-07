import unittest
from unittest.mock import MagicMock, patch

from flask import request

from modules.access_token.errors import (
    AccessTokenInvalidError,
    AuthorizationHeaderNotFoundError,
    InvalidAuthorizationHeaderError,
    UnauthorizedAccessError,
)
from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from server import app


class TestAccessAuthMiddleware(unittest.TestCase):
    @patch("modules.access_token.access_token_service.AccessTokenService.verify_access_token")
    def test_missing_authorization_header(self, mock_verify_access_token):
        mock_next_func = MagicMock()

        with app.test_request_context():
            with self.assertRaises(AuthorizationHeaderNotFoundError):
                access_auth_middleware(mock_next_func)()

        mock_next_func.assert_not_called()

    @patch("modules.access_token.access_token_service.AccessTokenService.verify_access_token")
    def test_invalid_authorization_header(self, mock_verify_access_token):
        mock_next_func = MagicMock()

        with app.test_request_context():
            request.headers = {"Authorization": "JWT your_test_token"}
            with self.assertRaises(InvalidAuthorizationHeaderError):
                access_auth_middleware(mock_next_func)()

        mock_next_func.assert_not_called()

    @patch("modules.access_token.access_token_service.AccessTokenService.verify_access_token")
    def test_invalid_access_token(self, mock_verify_access_token):
        mock_next_func = MagicMock()
        mock_verify_access_token.side_effect = AccessTokenInvalidError("Invalid access token.")

        with app.test_request_context():
            request.headers = {"Authorization": "Bearer your_test_token"}
            with self.assertRaises(InvalidAuthorizationHeaderError):
                access_auth_middleware(mock_next_func)()

        mock_next_func.assert_not_called()

    @patch("modules.access_token.access_token_service.AccessTokenService.verify_access_token")
    def test_unauthorized_access(self, mock_verify_access_token):
        mock_verify_access_token.return_value = MagicMock(account_id="12345")

        @access_auth_middleware
        def test_view_func(account_id):
            return account_id

        with app.test_request_context(headers={"Authorization": "Bearer your_test_token"}):
            with self.assertRaises(UnauthorizedAccessError):
                test_view_func(account_id="67890")
