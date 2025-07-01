from datetime import datetime

from pymongo import ReturnDocument

from modules.account.internal.account_reader import AccountReader
from modules.account.internal.account_writer import AccountWriter
from modules.account.internal.store.account_notification_preferences_model import AccountNotificationPreferencesModel
from modules.account.internal.store.account_notification_preferences_repository import (
    AccountNotificationPreferencesRepository,
)
from modules.account.types import (
    Account,
    AccountSearchByIdParams,
    AccountSearchParams,
    CreateAccountByPhoneNumberParams,
    CreateAccountByUsernameAndPasswordParams,
    NotificationPreferences,
    PhoneNumber,
    ResetPasswordParams,
    UpdateNotificationPreferencesParams,
)
from modules.authentication.authentication_service import AuthenticationService
from modules.authentication.types import CreateOTPParams


class AccountService:
    @staticmethod
    def create_account_by_username_and_password(*, params: CreateAccountByUsernameAndPasswordParams) -> Account:
        account = AccountWriter.create_account_by_username_and_password(params=params)
        default_prefs = AccountNotificationPreferencesModel(account_id=account.id, id=None).to_bson()
        AccountNotificationPreferencesRepository.collection().insert_one(default_prefs)

        return account

    @staticmethod
    def get_account_by_phone_number(*, phone_number: PhoneNumber) -> Account:
        return AccountReader.get_account_by_phone_number(phone_number=phone_number)

    @staticmethod
    def get_or_create_account_by_phone_number(*, params: CreateAccountByPhoneNumberParams) -> Account:
        account = AccountReader.get_account_by_phone_number_optional(phone_number=params.phone_number)

        if account is None:
            account = AccountWriter.create_account_by_phone_number(params=params)

            default_prefs = AccountNotificationPreferencesModel(account_id=account.id, id=None).to_bson()
            AccountNotificationPreferencesRepository.collection().insert_one(default_prefs)

        create_otp_params = CreateOTPParams(phone_number=params.phone_number)
        AuthenticationService.create_otp(params=create_otp_params)

        return account

    @staticmethod
    def reset_account_password(*, params: ResetPasswordParams) -> Account:
        account = AccountReader.get_account_by_id(params=AccountSearchByIdParams(id=params.account_id))

        password_reset_token = AuthenticationService.verify_password_reset_token(
            account_id=account.id, token=params.token
        )

        updated_account = AccountWriter.update_password_by_account_id(
            account_id=params.account_id, password=params.new_password
        )

        AuthenticationService.set_password_reset_token_as_used_by_id(password_reset_token_id=password_reset_token.id)

        return updated_account

    @staticmethod
    def get_account_by_id(*, params: AccountSearchByIdParams) -> Account:
        return AccountReader.get_account_by_id(params=params)

    @staticmethod
    def get_account_by_username(*, username: str) -> Account:
        return AccountReader.get_account_by_username(username=username)

    @staticmethod
    def get_account_by_username_and_password(*, params: AccountSearchParams) -> Account:
        return AccountReader.get_account_by_username_and_password(params=params)

    @staticmethod
    def get_notification_preferences(*, account_id: str) -> NotificationPreferences:
        preferences = AccountNotificationPreferencesRepository.collection().find_one({"account_id": account_id})

        if not preferences:
            default_prefs = AccountNotificationPreferencesModel(account_id=account_id, id=None).to_bson()

            result = AccountNotificationPreferencesRepository.collection().insert_one(default_prefs)
            preferences = AccountNotificationPreferencesRepository.collection().find_one({"_id": result.inserted_id})

        return NotificationPreferences(
            email_enabled=preferences.get("email_enabled", True),
            sms_enabled=preferences.get("sms_enabled", True),
            push_enabled=preferences.get("push_enabled", True),
        )

    @staticmethod
    def update_notification_preferences(*, params: UpdateNotificationPreferencesParams) -> NotificationPreferences:
        AccountReader.get_account_by_id(params=AccountSearchByIdParams(id=params.account_id))

        notification_preferences = {
            "email_enabled": params.email_enabled,
            "push_enabled": params.push_enabled,
            "sms_enabled": params.sms_enabled,
            "updated_at": datetime.now(),
        }

        result = AccountNotificationPreferencesRepository.collection().find_one_and_update(
            {"account_id": params.account_id},
            {"$set": notification_preferences},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        return NotificationPreferences(
            email_enabled=result.get("email_enabled", True),
            sms_enabled=result.get("sms_enabled", True),
            push_enabled=result.get("push_enabled", True),
        )
