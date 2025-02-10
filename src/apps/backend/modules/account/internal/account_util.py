from typing import Any
import bcrypt

from modules.account.types import Account, PhoneNumber


class AccountUtil:
    @staticmethod
    def hash_password(*, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()

    @staticmethod
    def compare_password(*, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def convert_account_bson_to_account(account_bson: dict[str,Any]) -> Account:
        phone_number_data = account_bson["phone_number"]
        phone_number = PhoneNumber(**phone_number_data) if phone_number_data else None
        return Account(
            id=str(account_bson['_id']),
            first_name=account_bson['first_name'],
            last_name=account_bson['last_name'],
            phone_number=phone_number,
            username=account_bson['username'],
            password=account_bson['hashed_password']
        )
