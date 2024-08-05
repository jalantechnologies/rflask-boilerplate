from typing import Callable
import unittest

from modules.account.internal.store.account_repository import AccountRepository
from modules.access_token.rest_api.access_token_rest_api_server import AccessTokenRestApiServer


class BaseTestAccessToken(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        AccessTokenRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        AccountRepository.collection().delete_many({})
