import json

from modules.account.account_service import AccountService
from modules.account.types import AccountErrorCode, CreateAccountParams
from server import app
from tests.modules.account.base_test_account import BaseTestAccount


class TestAccountApi(BaseTestAccount):
    def test_create_account(self) -> None:
        payload = json.dumps(
            {"first_name": "first_name", "last_name": "last_name", "password": "password", "username": "username"}
        )

        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts", headers={"Content-Type": "application/json"}, data=payload
            )
            assert response.status_code == 201
            assert response.json, f"No response from API with status code:: {response.status}"
            assert response.json.get("username") == "username"

    def test_create_account_with_existing_user(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )
        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/accounts",
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "first_name": "first_name",
                        "last_name": "last_name",
                        "password": "password",
                        "username": account.username,
                    }
                ),
            )
        assert response.status_code == 409
        assert response.json
        assert response.json.get("code") == AccountErrorCode.USERNAME_ALREADY_EXISTS
