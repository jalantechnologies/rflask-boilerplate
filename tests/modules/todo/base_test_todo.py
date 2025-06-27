# tests/modules/todo/base_test_todo.py

import unittest
from typing import Callable

from modules.account.internal.store.account_repository import AccountRepository
from modules.authentication.internals.otp.store.otp_repository import OTPRepository
from modules.config.config_service import ConfigService
from modules.logger.logger_manager import LoggerManager
from modules.todo.internal.store.todo_repository import TodoRepository
from modules.todo.rest_api.todo_rest_api_server import TodoRestApiServer


class BaseTestTodo(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        LoggerManager.mount_logger()
        TodoRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
        TodoRepository.collection().delete_many({})
        OTPRepository.collection().delete_many({})
        AccountRepository.collection().delete_many({})
