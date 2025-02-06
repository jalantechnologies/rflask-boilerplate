import json
from server import app
from modules.account.account_service import AccountService
from modules.account.types import CreateAccountByUsernameAndPasswordParams

TASK_URL = "http://127.0.0.1:8080/api/tasks"
HEADERS = {"Content-Type": "application/json"}
PAGE = 1
SIZE = 5
URL_WITH_PARAMS = f"{TASK_URL}?page={PAGE}&size={SIZE}"


class TestTaskApiWithAuth:
    def test_create_task(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username",
            )
        )

        with app.test_client() as client:
            access_token = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )
            token = access_token.json.get("token")
            assert token, "Access token is missing in the response"

            auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

            payload = json.dumps(
                {"title": "Test Task", "description": "Test Description"}
            )
            response = client.post(TASK_URL, headers=auth_headers, data=payload)

            assert (
                response.status_code == 201
            ), f"Unexpected status code: {response.status_code}"
            assert (
                response.json
            ), f"No response body with status code {response.status_code}"
            assert (
                response.json.get("title") == "Test Task"
            ), "Task title does not match"
            assert (
                response.json.get("description") == "Test Description"
            ), "Task description does not match"
            assert response.json.get("account_id") == account.id, "Account ID mismatch"

    def test_get_tasks(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username2",
            )
        )
        with app.test_client() as client:
            access_token = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )
            token = access_token.json.get("token")
            assert token, "Access token is missing in the response"

            auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

            response = client.get(TASK_URL, headers=auth_headers)

            assert (
                response.status_code == 200
            ), f"Unexpected status code: {response.status_code}"
            assert isinstance(response.json, list), "Response is not a list"

    def test_get_tasks_with_page_params(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username3",
            )
        )

        with app.test_client() as client:
            access_token = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )
            token = access_token.json.get("token")
            assert token, "Access token is missing in the response"

            auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

            response = client.get(URL_WITH_PARAMS, headers=auth_headers)

            assert (
                response.status_code == 200
            ), f"Unexpected status code: {response.status_code}"
            assert isinstance(response.json, list), "Response is not a list"

    def test_patch_task(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username4",
            )
        )

        with app.test_client() as client:
            access_token = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )
            token = access_token.json.get("token")
            assert token, "Access token is missing in the response"

            auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}

            payload = json.dumps(
                {"title": "Test Task", "description": "Test Description"}
            )
            response = client.post(TASK_URL, headers=auth_headers, data=payload)
            assert (
                response.status_code == 201
            ), f"Unexpected status code: {response.status_code}"
            task_id = response.json.get("id")
            assert task_id, "Task ID is missing after creating task"

            updated_payload = json.dumps(
                {"title": "Updated Task", "description": "Updated Description"}
            )
            patch_response = client.patch(
                f"{TASK_URL}/{task_id}", headers=auth_headers, data=updated_payload
            )

            assert (
                patch_response.status_code == 200
            ), f"Unexpected status code: {patch_response.status_code}"
            assert (
                patch_response.json.get("title") == "Updated Task"
            ), "Task title was not updated"
            assert (
                patch_response.json.get("description") == "Updated Description"
            ), "Task description was not updated"

    def test_delete_task(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username5",
            )
        )
        with app.test_client() as client:
            access_token = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": account.username, "password": "password"}),
            )

            token = access_token.json.get("token")
            assert token, "Access token is missing in the response"

            auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
            payload = json.dumps(
                {"title": "Test Task", "description": "Test Description"}
            )
            response = client.post(TASK_URL, headers=auth_headers, data=payload)
            assert (
                response.status_code == 201
            ), f"Unexpected status code: {response.status_code}"

            task_id = response.json.get("id")
            assert task_id, "Task ID is missing after creating task"

            delete_response = client.delete(
                f"{TASK_URL}/{task_id}", headers=auth_headers
            )
            assert (
                delete_response.status_code == 200
            ), f"Unexpected status code: {delete_response.status_code}"
            assert (
                delete_response.json.get("message") == "Task deleted successfully"
            ), "Task deletion failed"
