from bson.objectid import ObjectId

from modules.account.errors import AccountInvalidPasswordError, AccountNotFoundError, AccountWithUserNameExistsError
from modules.account.internal.account_util import AccountUtil
from modules.account.internal.store.account_model import AccountModel
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.types import Account, AccountSearchByIdParams, AccountSearchParams, CreateAccountParams


class AccountReader:
    @staticmethod
    def get_account_by_username(*, username: str) -> AccountModel:
        account = AccountRepository.collection().find_one({"username": username})
        if account is None:
            raise AccountNotFoundError(f"Account with username:: {username}, not found")

        return AccountModel(**account)

    @staticmethod
    def get_account_by_username_and_password(*, params: AccountSearchParams) -> Account:
        account = AccountReader.get_account_by_username(username=params.username)
        if not AccountUtil.compare_password(password=params.password, hashed_password=account.hashed_password):
            raise AccountInvalidPasswordError("Invalid password")

        return AccountUtil.convert_account_model_to_account(account_model=account)

    @staticmethod
    def get_account_by_id(*, params: AccountSearchByIdParams) -> Account:
        account = AccountRepository.collection().find_one({"_id": ObjectId(params.id), "active": True})
        if account is None:
            raise AccountNotFoundError(f"Account with id:: {params.id}, not found")

        return AccountUtil.convert_account_model_to_account(AccountModel(**account))

    @staticmethod
    def check_username_not_exist(*, params: CreateAccountParams) -> None:
        account = AccountRepository.collection().find_one({"username": params.username, "active": True})

        if account:
            raise AccountWithUserNameExistsError(f"Account already exist for username:: {params.username}")
