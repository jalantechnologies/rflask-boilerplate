from unittest.mock import patch

from flask import request

from modules.access_token.types import AccessTokenPayload
from modules.account.account_service import AccountService
from modules.account.errors import AccountNotFoundError
from modules.account.types import AccountErrorCode, AccountSearchByIdParams, CreateAccountParams
from server import app
from tests.modules.account.base_test_account import BaseTestAccount


class TestAccountService(BaseTestAccount):
    def test_create_account(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                password="password", username="username", first_name="first_name", last_name="last_name"
            )
        )

        assert account.username == "username"
        assert account.first_name == "first_name"
        assert account.last_name == "last_name"

    @patch("modules.access_token.access_token_service.AccessTokenService.verify_access_token")
    def test_get_account_by_id(self, mock_verify_access_token) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        mock_verify_access_token.return_value = AccessTokenPayload(account_id=account.id)

        with app.test_request_context():
            request.headers = {"Authorization": "Bearer your_test_token"}
            get_account_by_id = AccountService.get_account_by_id(params=AccountSearchByIdParams(id=account.id))

        assert get_account_by_id.username == account.username
        assert get_account_by_id.first_name == account.first_name
        assert get_account_by_id.last_name == account.last_name

    @patch("modules.access_token.access_token_service.AccessTokenService.verify_access_token")
    def test_throw_exception_when_usernot_exist(self, mock_verify_access_token) -> None:
        try:
            mock_verify_access_token.return_value = AccessTokenPayload(account_id="5f7b1b7b4f3b9b1b3f3b9b1b")
            with app.test_request_context():
                request.headers = {"Authorization": "Bearer your_test_token"}
                AccountService.get_account_by_id(params=AccountSearchByIdParams(id="5f7b1b7b4f3b9b1b3f3b9b1b"))
        except AccountNotFoundError as exc:
            assert exc.code == AccountErrorCode.NOT_FOUND
