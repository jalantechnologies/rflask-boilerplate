import unittest
from typing import Callable

from modules.config.config_manager import ConfigManager


class BaseTestConfig(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        ConfigManager.mount_config()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
