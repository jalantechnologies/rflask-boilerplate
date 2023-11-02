from modules.account.types import CreateAccountParams, AccountSearchParams
from modules.account.internal.account_writer import AccountWriter
from modules.account.internal.account_reader import AccountReader
from modules.account.types import Account, AccountInfo


class AccountService:
  @staticmethod
  def create_account(*, params: CreateAccountParams) -> AccountInfo:
    account = AccountWriter.create_account(params=params)
    return AccountInfo(
      id=account._id,
      username=account.username
    )

  @staticmethod
  def get_account_by_username_password(*, params: AccountSearchParams) -> Account:
    account = AccountReader.get_account_by_username_and_password(
      params=params
    )
    return Account(
      id=account._id,
      hashed_password=account.hashed_password,
      username=account.username
    )
