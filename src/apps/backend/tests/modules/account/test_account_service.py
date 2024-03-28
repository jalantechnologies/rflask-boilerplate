from modules.account.account_service import AccountService
from modules.account.errors import AccountNotFoundError
from modules.account.types import AccountErrorCode, AccountSearchParams, CreateAccountParams 
from tests.modules.account.base_test_account import BaseTestAccount


class TestAccountService(BaseTestAccount):
  def test_create_account(self) -> None:
    account = AccountService.create_account(params = CreateAccountParams(
      password="password",
      username="username",
      first_name="first_name",
      last_name="last_name",
    ))

    assert account.username == "username"
    assert account.first_name == "first_name"
    assert account.last_name == "last_name"


  def test_get_account_by_username_password(self) -> None:
    account = AccountService.create_account(params = CreateAccountParams(
      first_name="first_name",
      last_name="last_name",
      password="password",
      username="username",
    ))

    fetched_account = AccountService.get_account_by_username_password(
      params = AccountSearchParams(
        password="password",
        username=account.username,
      )
    )

    assert fetched_account.username == account.username
    assert fetched_account.first_name == account.first_name
    assert fetched_account.last_name == account.last_name

  def test_throw_exception_when_usernot_exist(self) -> None:
    try:
      AccountService.get_account_by_username_password(params=AccountSearchParams(
        password="password",
        username="username",
      ))
    except AccountNotFoundError as exc:
      assert exc.code == AccountErrorCode.NOT_FOUND
