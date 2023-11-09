from modules.account.internal.account_util import AccountUtil
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.internal.store.account_model import AccountModel
from modules.account.types import AccountSearchParams, CreateAccountParams


class AccountReader:
  @staticmethod
  def get_account_by_username(*, username: str) -> AccountModel:
    account = AccountRepository.account_db.find_one({
      "username": username
    })
    if account is None:
      raise Exception("Username not found")

    return account

  @staticmethod
  def get_account_by_username_and_password(
    *, params: AccountSearchParams
  ) -> AccountModel:
    account = AccountReader.get_account_by_username(username=params.username)
    if not AccountUtil.compare_password(
      password=params.password,
      hashed_password=account.hashed_password
    ):
      raise Exception("User not found")

    return account

  @staticmethod
  def check_username_not_exist(*, params: CreateAccountParams) -> None:
    account = AccountRepository.account_db.find_one({
      "username": params.username,
      "active": True
    })

    if account:
      raise Exception("User exist")
