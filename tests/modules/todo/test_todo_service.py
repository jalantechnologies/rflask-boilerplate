# tests/modules/todo/test_todo_service.py

from datetime import datetime

from modules.account.account_service import AccountService
from modules.account.types import CreateAccountByUsernameAndPasswordParams
from modules.todo.internal.todo_reader import TodoReader
from modules.todo.internal.todo_writer import TodoWriter
from modules.todo.types import CreateTodoParams, UpdateTodoParams

from tests.modules.todo.base_test_todo import BaseTestTodo


class TestTodoService(BaseTestTodo):
    def test_create_and_get_todo_for_user(self):
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                username="user", password="pass", first_name="fname", last_name="lname"
            )
        )

        created_todo = TodoWriter.create_todo(
            account_id=account.id,
            params=CreateTodoParams(
                title="Test Task",
                description="Description here",
                status="todo",
                due_date=datetime.now(),
            ),
        )

        todos = TodoReader.get_todos_for_user(account_id=account.id)
        assert len(todos) == 1
        assert todos[0].title == "Test Task"
        assert todos[0].description == "Description here"
        assert todos[0].status == "todo"

    def test_update_existing_todo(self):
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                username="user", password="pass", first_name="fname", last_name="lname"
            )
        )

        todo = TodoWriter.create_todo(
            account_id=account.id,
            params=CreateTodoParams(title="Old Title", status="todo", description=None),
        )

        updated = TodoWriter.update_todo(
            todo_id=todo.id,
            params=UpdateTodoParams(
                title="New Title", description="Updated Desc", status="done"
            ),
        )

        assert updated.title == "New Title"
        assert updated.description == "Updated Desc"
        assert updated.status == "done"

    def test_delete_todo(self):
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                username="user", password="pass", first_name="fname", last_name="lname"
            )
        )

        todo = TodoWriter.create_todo(
            account_id=account.id,
            params=CreateTodoParams(
                title="To Be Deleted", status="todo", description=None
            ),
        )

        TodoWriter.delete_todo(todo_id=todo.id)

        todos = TodoReader.get_todos_for_user(account_id=account.id)
        assert len(todos) == 0
