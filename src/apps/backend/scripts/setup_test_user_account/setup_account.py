"""
Generic test user setup script.
- Creates a test user on app startup if enabled in config (dev/preview only).
- Idempotent: does nothing if user already exists.
- Uses only generic fields (username, password, full_name).
"""
from modules.account.account_service import AccountService
from modules.account.errors import AccountWithUserNameExistsError, AccountWithUsernameNotFoundError
from modules.account.types import CreateAccountByUsernameAndPasswordParams
from modules.config.config_service import ConfigService

def setup_test_user_account() -> None:
    # Check config flag to enable test user creation (should be true only in dev/preview)
    create_test_user_account = ConfigService[bool].get_value(key="accounts.create_test_user_account", default=False)
    if not create_test_user_account:
        return
    test_account_username = ConfigService[str].get_value(key="accounts.test_user.username")
    try:
        # If user already exists, do nothing
        AccountService.get_account_by_username(username=test_account_username)
        return
    except AccountWithUsernameNotFoundError:
        pass  # User does not exist, proceed to create

    test_account_password = ConfigService[str].get_value(key="accounts.test_user.password")
    test_account_full_name = ConfigService[str].get_value(key="accounts.test_user.full_name")
    # Split full_name into first and last name if possible
    name_parts = test_account_full_name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    try:
        AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                first_name=first_name,
                last_name=last_name,
                password=test_account_password,
                username=test_account_username,
            )
        )
    except AccountWithUserNameExistsError:
        pass  # Already exists, nothing to do 