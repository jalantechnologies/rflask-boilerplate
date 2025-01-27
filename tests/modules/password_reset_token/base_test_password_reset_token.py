import unittest
from typing import Callable

from src.apps.backend.modules.account.internal.store.account_repository import AccountRepository
from src.apps.backend.modules.config.config_manager import ConfigManager
from src.apps.backend.modules.password_reset_token.internal.store.password_reset_token_repository import PasswordResetTokenRepository
from src.apps.backend.modules.password_reset_token.rest_api.password_reset_token_rest_api_server import PasswordResetTokenRestApiServer


class BaseTestPasswordResetToken(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        ConfigManager.mount_config()
        PasswordResetTokenRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        AccountRepository.collection().delete_many({})
        PasswordResetTokenRepository.collection().delete_many({})
