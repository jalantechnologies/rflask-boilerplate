from modules.account.types import (
    CreateAccountByUsernameAndPasswordParams,
    AccountSearchByIdParams,
)
from modules.task.types import (
    CreateTaskParams,
    GetAllTaskParams,
    UpdateTaskParams,
    DeleteTaskParams
)
from modules.account.account_service import AccountService
from modules.access_token.types import AccessTokenPayload
from tests.modules.task.base_test_task import BaseTestTask
from modules.task.task_service import TaskService
from server import app


class TestTaskService(BaseTestTask):

    def test_create_task(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username6",
            )
        )
        with app.test_request_context():
            get_account_by_id = AccountService.get_account_by_id(
                params=AccountSearchByIdParams(id=account.id)
            )

            task = TaskService.create_task(
                params=CreateTaskParams(
                    account_id=get_account_by_id.id,
                    title="title",
                    description="description",
                )
            )
        assert task.id != None
        assert task.account_id == get_account_by_id.id
        assert task.description == "description"
        assert task.title == "title"

    def test_get_tasks(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username7",
            )
        )
        with app.test_request_context():
            get_account_by_id = AccountService.get_account_by_id(
                params=AccountSearchByIdParams(id=account.id)
            )
            task = TaskService.create_task(
                params=CreateTaskParams(
                    account_id=get_account_by_id.id,
                    title="title",
                    description="description",
                )
            )
            assert task != None
            task = TaskService.get_tasks_for_account(
                params=GetAllTaskParams(
                    account_id=get_account_by_id.id,
                )
            )
            assert isinstance(task, list)

    def test_update_task(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username8",
            )
        )
        with app.test_request_context():
            get_account_by_id = AccountService.get_account_by_id(
                params=AccountSearchByIdParams(id=account.id)
            )
            old_task = TaskService.create_task(
                params=CreateTaskParams(
                    account_id=get_account_by_id.id,
                    title="title",
                    description="description",
                )
            )
            assert old_task != None
            task = TaskService.update_task_for_account(
                params=UpdateTaskParams(
                    account_id=get_account_by_id.id,
                    task_id=old_task.id,
                    title="updated_title",
                    description="updated_description",
                )
            )
            assert task.id == old_task.id
            assert task.account_id == get_account_by_id.id
            assert task.description == "updated_description"
            assert task.title == "updated_title"

    def test_delete_task(self) -> None:
        account = AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name="first_name",
                last_name="last_name",
                password="password",
                username="username9",
            )
        )
        with app.test_request_context():
            get_account_by_id = AccountService.get_account_by_id(
                params=AccountSearchByIdParams(id=account.id)
            )
            task = TaskService.create_task(
                params=CreateTaskParams(
                    account_id=get_account_by_id.id,
                    title="title",
                    description="description",
                )
            )
            assert task != None
            delete_task_params = DeleteTaskParams(account_id=get_account_by_id.id, task_id=task.id)
            is_deleted = TaskService.delete_task_for_account(
                params=delete_task_params
            )
            assert is_deleted == True
