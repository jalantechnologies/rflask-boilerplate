import unittest
from typing import Callable

from modules.config.config_manager import ConfigManager
from modules.logger.logger_manager import LoggerManager
from modules.workflow.rest_api.workflow_rest_api_server import WorkflowRestApiServer


class BaseTestWorkflow(unittest.TestCase):
    def setup_method(self, method: Callable) -> None:
        print(f"Executing:: {method.__name__}")
        ConfigManager.mount_config()
        LoggerManager.mount_logger()
        WorkflowRestApiServer.create()

    def teardown_method(self, method: Callable) -> None:
        print(f"Executed:: {method.__name__}")
