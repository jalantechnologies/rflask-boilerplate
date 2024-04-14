import json

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.account.types import AccountSearchByIdParams, CreateAccountParams
from modules.account.internal.account_writer import AccountWriter
from modules.account.internal.account_reader import AccountReader
from modules.account.types import Account


class AccountService:
  @staticmethod
  def create_account(*, params: CreateAccountParams) -> Account:
    account = AccountWriter.create_account(params=params)
    account_dict = json.loads(account.to_json())
    return Account(
      id=account_dict.get("id"),
      first_name=account_dict.get("first_name"),
      last_name=account_dict.get("last_name"),
      username=account_dict.get("username"),
    )

  @access_auth_middleware
  @staticmethod
  def get_account_by_id(*, params: AccountSearchByIdParams) -> Account:
    account = AccountReader.get_account_by_id(
      params=params
    )
    return Account(
      id=str(account.id),
      first_name=account.first_name,
      last_name=account.last_name,
      username=account.username,
    )
