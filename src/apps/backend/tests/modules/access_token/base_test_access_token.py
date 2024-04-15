from typing import Callable
import unittest

from modules.account.internal.store.account_repository import AccountRepository
from modules.access_token.access_token_service_manager import AccessTokenServiceManager


class BaseTestAccessToken(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        AccessTokenServiceManager.create_rest_api_server()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        AccountRepository.account_db.delete_many({})
