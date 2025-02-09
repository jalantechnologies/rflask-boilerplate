from dataclasses import asdict
from typing import Optional

from bson.objectid import ObjectId

from modules.account.errors import (
    AccountInvalidPasswordError,
    AccountNotFoundError,
    AccountWithPhoneNumberExistsError,
    AccountWithUserNameExistsError,
)
from modules.account.internal.account_util import AccountUtil
from modules.account.internal.store.account_model import AccountModel
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.types import (
    Account,
    AccountWithPassword,
    AccountSearchByIdParams,
    AccountSearchParams,
    CreateAccountByUsernameAndPasswordParams,
    PhoneNumber,
)


class AccountReader:
    @staticmethod
    def get_account_by_username(*, username: str) -> AccountWithPassword:
        account_bson = AccountRepository.collection().find_one({"username": username})
        if account_bson is None:
            raise AccountNotFoundError(f"Account with username:: {username}, not found")
        account_model = AccountModel.from_bson(account_bson)
        return AccountUtil.convert_account_model_to_account_password(account_model)

    @staticmethod
    def get_account_by_username_and_password(*, params: AccountSearchParams) -> Account:
        account_bson = AccountRepository.collection().find_one({"username": params.username})
        if account_bson is None:
            raise AccountNotFoundError(f"Account with username:: {params.username}, not found")
        account_model = AccountModel.from_bson(account_bson)
        if not AccountUtil.compare_password(password=params.password, hashed_password=account_model.hashed_password):
            raise AccountInvalidPasswordError("Invalid password")
        return AccountUtil.convert_account_model_to_account(account_model)

    @staticmethod
    def get_account_by_id(*, params: AccountSearchByIdParams) -> Account:
        account_bson = AccountRepository.collection().find_one({"_id": ObjectId(params.id), "active": True})
        if account_bson is None:
            raise AccountNotFoundError(f"Account with id:: {params.id}, not found")
        account_model = AccountModel.from_bson(account_bson)
        return AccountUtil.convert_account_model_to_account(account_model)

    @staticmethod
    def check_username_not_exist(*, params: CreateAccountByUsernameAndPasswordParams) -> None:
        account_bson = AccountRepository.collection().find_one({"username": params.username, "active": True})

        if account_bson:
            raise AccountWithUserNameExistsError(f"Account already exist for username:: {params.username}")

    @staticmethod
    def get_account_by_phone_number_optional(*, phone_number: PhoneNumber) -> Optional[Account]:
        phone_number_dict = asdict(phone_number)
        account_bson = AccountRepository.collection().find_one({"phone_number": phone_number_dict})
        if account_bson is None:
            return None
        account_model = AccountModel.from_bson(account_bson)
        return AccountUtil.convert_account_model_to_account(account_model)

    @staticmethod
    def get_account_by_phone_number(*, phone_number: PhoneNumber) -> Account:
        account = AccountReader.get_account_by_phone_number_optional(phone_number=phone_number)
        if account is None:
            raise AccountNotFoundError(f"Account with phone number:: {phone_number}, not found")

        return account

    @staticmethod
    def check_phone_number_not_exist(*, phone_number: PhoneNumber) -> None:
        phone_number_dict = asdict(phone_number)
        account_bson = AccountRepository.collection().find_one({"phone_number": phone_number_dict, "active": True})

        if account_bson:
            raise AccountWithPhoneNumberExistsError(f"Account already exist for phone number:: {phone_number}")
