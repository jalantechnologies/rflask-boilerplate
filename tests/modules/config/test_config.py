import os

from modules.config.types import PapertrailConfig
from modules.common.types import ErrorCode
from modules.config.config_service import ConfigService
from modules.error.custom_errors import MissingKeyError
from tests.modules.config.base_test_config import BaseTestConfig


class TestConfig(BaseTestConfig):
    def test_db_config_is_loaded(self) -> None:
        uri = ConfigService.get_value(key="mongodb.uri")
        assert uri.split(":")[0] == "mongodb"
        assert uri.split("/")[-1] == "frm-boilerplate-test"

    def test_logger_config_is_loaded(self) -> None:
        loggers = ConfigService.get_value(key="logger.transports")
        assert type(loggers) == list
        assert "console" in loggers

    def test_datadog_config_is_loaded(self) -> None:
        try:
            ConfigService.get_value(key="datadog.api_key")
        except MissingKeyError as exc:
            assert exc.code == ErrorCode.MISSING_KEY

        populated_env = os.environ.get("APP_ENV")
        assert populated_env == "testing" or populated_env == "docker-test"
