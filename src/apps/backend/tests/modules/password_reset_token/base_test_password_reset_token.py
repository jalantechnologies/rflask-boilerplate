from typing import Callable
import unittest
from unittest import mock

import faker
from modules.account.internal.store.account_repository import AccountRepository
from modules.config.config_manager import ConfigManager
from modules.password_reset_token.internal.store.password_reset_token_repository import PasswordResetTokenRepository
from modules.password_reset_token.password_reset_token_service_manager import PasswordResetTokenServiceManager


class BaseTestPasswordResetToken(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        self.faker = faker.Faker()
        ConfigManager.mount_config()
        PasswordResetTokenServiceManager.create_rest_api_server()
    
    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        AccountRepository.account_db.delete_many({})
        PasswordResetTokenRepository.password_reset_token_db.delete_many({})
