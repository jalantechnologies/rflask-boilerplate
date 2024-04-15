import json
from tests.modules.access_token.base_test_access_token import BaseTestAccessToken
from modules.account.types import CreateAccountParams
from modules.account.account_service import AccountService
from server import app

API_URL = "http://127.0.0.1:8080/api/access-tokens"
HEADERS = {'Content-Type': 'application/json'}

class TestAccessTokenApi(BaseTestAccessToken):
    def test_get_access_token(self) -> None:
        account = AccountService.create_account(params=CreateAccountParams(
            first_name="first_name",
            last_name="last_name",
            password="password",
            username="username",
        ))
        
        with app.test_client() as client:
            response = client.post(
                API_URL,
                headers=HEADERS,
                data=json.dumps({
                    "username": account.username,
                    "password": "password",
                }),
            )
            assert response.status_code == 201
            assert response.json
            assert response.json.get("token")
            assert response.json.get("account_id") == account.id
            assert response.json.get("expires_at")
    
    def test_get_access_token_with_invalid_password(self) -> None:
        account = AccountService.create_account(params=CreateAccountParams(
            first_name="first_name",
            last_name="last_name",
            password="password",
            username="username",
        ))
        
        with app.test_client() as client:
            response = client.post(
                API_URL,
                headers=HEADERS,
                data=json.dumps({
                    "username": account.username,
                    "password": "invalid_password",
                }),   
            )
            assert response.status_code == 400
            assert response.json
            assert response.json.get("code") == "ACCOUNT_ERR_02"
            
    def test_get_access_token_with_invalid_username(self) -> None:
        with app.test_client() as client:
            response = client.post(
                API_URL,
                headers=HEADERS,
                data=json.dumps({
                    "username": "invalid_username",
                    "password": "password",
                }),
            )
            assert response.status_code == 400
            assert response.json
            assert response.json.get("code") == "ACCOUNT_ERR_02"
    
    def test_get_access_token_with_invalid_username_and_password(self) -> None:
        with app.test_client() as client:
            response = client.post(
                API_URL,
                headers=HEADERS,
                data=json.dumps({
                    "username": "invalid_username",
                    "password": "invalid_password",
                }),
            )
            assert response.status_code == 400
            assert response.json
            assert response.json.get("code") == "ACCOUNT_ERR_02"
