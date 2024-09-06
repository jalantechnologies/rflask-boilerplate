import json
from datetime import datetime, timedelta

import jwt

from modules.access_token.types import AccessTokenErrorCode
from modules.account.account_service import AccountService
from modules.account.types import AccountErrorCode, CreateAccountParams
from modules.config.config_service import ConfigService
from server import app
from tests.modules.account.base_test_account import BaseTestAccount

HEADERS = {"Content-Type": "application/json"}


class TestAccountApi(BaseTestAccount):
    def test_create_account(self) -> None:
        payload = json.dumps(
            {"first_name": "first_name", "last_name": "last_name", "password": "password", "username": "username"}
        )

        with app.test_client() as client:
            response = client.post("http://127.0.0.1:8080/api/accounts", headers=HEADERS, data=payload)
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
                headers=HEADERS,
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

    def test_get_account_by_username_and_password(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        with app.test_client() as client:
            access_token = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )
            response = client.get(
                f"http://127.0.0.1:8080/api/accounts/{account.id}",
                headers={"Authorization": f"Bearer {access_token.json.get('token')}"},
            )
            assert response.status_code == 200
            assert response.json
            assert response.json.get("id") == account.id
            assert response.json.get("username") == account.username
            assert response.json.get("first_name") == account.first_name
            assert response.json.get("last_name") == account.last_name

    def test_get_account_by_username_and_password_with_invalid_password(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        with app.test_client() as client:
            client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )
            response = client.get(
                f"http://127.0.0.1:8080/api/accounts/{account.id}", headers={"Authorization": f"Bearer invalid_token"}
            )

            assert response.status_code == 401
            assert response.json
            assert response.json.get("code") == AccessTokenErrorCode.ACCESS_TOKEN_INVALID

    def test_get_account_with_expired_access_token(self) -> None:
        account = AccountService.create_account(
            params=CreateAccountParams(
                first_name="first_name", last_name="last_name", password="password", username="username"
            )
        )

        # Create an expired token by setting the expiry to a date in the past using same method as in the
        # access token service
        jwt_signing_key = ConfigService.get_token_signing_key()
        jwt_expiry = timedelta(days=ConfigService.get_token_expiry_days() - 1)
        payload = {"account_id": account.id, "exp": (datetime.now() - jwt_expiry).timestamp()}
        expired_token = jwt.encode(payload, jwt_signing_key, algorithm="HS256")

        with app.test_client() as client:
            response = client.get(
                f"http://127.0.0.1:8080/api/accounts/{account.id}", headers={"Authorization": f"Bearer {expired_token}"}
            )

            assert response.status_code == 401
            assert "Access token has expired. Please login again." in response.json.get("message", "")
            assert response.json.get("code") == AccessTokenErrorCode.ACCESS_TOKEN_EXPIRED
