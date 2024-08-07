from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.account.internal.account_reader import AccountReader
from modules.account.internal.account_writer import AccountWriter
from modules.account.types import Account, AccountSearchByIdParams, CreateAccountParams, ResetPasswordParams
from modules.password_reset_token.password_reset_token_service import PasswordResetTokenService


class AccountService:
    @staticmethod
    def create_account(*, params: CreateAccountParams) -> Account:
        return AccountWriter.create_account(params=params)

    @staticmethod
    def reset_account_password(*, params: ResetPasswordParams) -> Account:

        account = AccountReader.get_account_by_id(params=AccountSearchByIdParams(id=params.account_id))

        password_reset_token = PasswordResetTokenService.verify_password_reset_token(
            account_id=account.id, token=params.token
        )

        updated_account = AccountWriter.update_password_by_account_id(
            account_id=params.account_id, password=params.new_password
        )

        PasswordResetTokenService.set_password_reset_token_as_used_by_id(
            password_reset_token_id=password_reset_token.id
        )

        return updated_account

    @access_auth_middleware
    @staticmethod
    def get_account_by_id(*, params: AccountSearchByIdParams) -> Account:
        return AccountReader.get_account_by_id(params=params)
