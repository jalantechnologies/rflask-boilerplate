# tests/modules/todo/test_todo_api.py

import json
from datetime import date

from modules.account.account_service import AccountService
from modules.account.types import CreateAccountByUsernameAndPasswordParams
from server import app

from tests.modules.todo.base_test_todo import BaseTestTodo

TODO_URL = "http://127.0.0.1:8080/api/todos"
HEADERS = {"Content-Type": "application/json"}


class TestTodoApi(BaseTestTodo):
    def test_create_todo(self):
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                username="todo_user", password="secure", first_name="F", last_name="L"
            )
        )

        token = self._get_access_token(username="todo_user", password="secure")

        payload = {
            "title": "Write tests",
            "description": "Add tests for todo APIs",
            "status": "todo",
            "due_date": date.today().isoformat(),
        }

        with app.test_client() as client:
            res = client.post(
                TODO_URL,
                headers={**HEADERS, "Authorization": f"Bearer {token}"},
                data=json.dumps(payload),
            )
            assert res.status_code == 201
            assert res.json.get("title") == "Write tests"
            assert res.json.get("status") == "todo"
            assert res.json.get("description") == "Add tests for todo APIs"

    def test_get_todos(self):
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                username="todo_user2", password="secure", first_name="F", last_name="L"
            )
        )

        token = self._get_access_token(username="todo_user2", password="secure")

        payload = {"title": "Task1", "status": "todo", "description": None}

        with app.test_client() as client:
            client.post(
                TODO_URL,
                headers={**HEADERS, "Authorization": f"Bearer {token}"},
                data=json.dumps(payload),
            )

            response = client.get(
                TODO_URL, headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert isinstance(response.json, list)
            assert any(todo["title"] == "Task1" for todo in response.json)

    def _get_access_token(self, username: str, password: str) -> str:
        with app.test_client() as client:
            response = client.post(
                "http://127.0.0.1:8080/api/access-tokens",
                headers=HEADERS,
                data=json.dumps({"username": username, "password": password}),
            )
            return response.json.get("token")
