import os

from tests.modules.config.base_test_config import BaseTestConfig

from modules.common.types import ErrorCode
from modules.config.config_service import ConfigService
from modules.config.types import PapertrailConfig
from modules.error.custom_errors import MissingKeyError


class TestConfig(BaseTestConfig):
    def test_db_config_is_loaded(self) -> None:
        uri = ConfigService.get_value(key="mongodb.uri", expected_type=str)
        assert uri.split(":")[0] == "mongodb"
        assert uri.split("/")[-1] == "frm-boilerplate-test"

    def test_logger_config_is_loaded(self) -> None:
        loggers = ConfigService.get_value(key="logger.transports", expected_type=list)
        assert type(loggers) == list
        assert "console" in loggers

    def test_papertrail_config_is_loaded(self) -> None:
        try:
            PapertrailConfig(
                host=ConfigService.get_value(key="papertrail.host", expected_type=str),
                port=ConfigService.get_value(key="papertrail.port", expected_type=int),
            )
        except MissingKeyError as exc:
            assert exc.code == ErrorCode.MISSING_KEY

        populated_env = os.environ.get("APP_ENV")
        assert populated_env == "testing" or populated_env == "docker-test"
