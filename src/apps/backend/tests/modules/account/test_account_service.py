from modules.account.account_service import AccountService
from modules.account.errors import AccountNotFoundError
from modules.account.types import AccountErrorCode, AccountSearchParams, CreateAccountParams 
from tests.modules.account.base_test_account import BaseTestAccount


class TestAccountService(BaseTestAccount):
  def test_create_account(self) -> None:
    account = AccountService.create_account(params = CreateAccountParams(
      password="password",
      username="username",
    ))

    assert account.username == "username"
    assert account.hashed_password is not None, "Unable to set hashed password while creating account"
    assert account.hashed_password != "password"


  def test_get_account_by_username_password(self) -> None:
    account = AccountService.create_account(params = CreateAccountParams(
      password="password",
      username="username",
    ))

    fetched_account = AccountService.get_account_by_username_password(
      params = AccountSearchParams(
        password="password",
        username=account.username,
      )
    )

    assert fetched_account.hashed_password == account.hashed_password

  def test_throw_exception_when_usernot_exist(self) -> None:
    try:
      AccountService.get_account_by_username_password(params=AccountSearchParams(
        password="password",
        username="username",
      ))
    except AccountNotFoundError as exc:
      assert exc.code == AccountErrorCode.NOT_FOUND
