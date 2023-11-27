import os

from modules.common.types import ErrorCode
from modules.config.config_manager import ConfigManager
from modules.config.config_service import ConfigService
from modules.config.types import PapertrailConfig
from modules.error.custom_errors import MissingKeyError

from tests.modules.config.base_test_config import BaseTestConfig


class TestConfig(BaseTestConfig):
  def test_db_config_is_loaded(self) -> None:
    uri = ConfigService.get_db_uri()
    assert uri.split(":")[0] == "mongodb"
    assert uri.split("/")[-1] == "frm-boilerplate-test"

  def test_logger_config_is_loaded(self) -> None:
    loggers = ConfigService.get_logger_transports()
    assert type(loggers) == list
    assert "console" in loggers

  def test_papertrail_config_is_loaded(self) -> None:
    try:
      ConfigService.get_papertrail_config()
    except MissingKeyError as exc:
      assert exc.code == ErrorCode.MISSING_KEY

    populated_env = os.environ["NODE_ENV"]
    os.environ["NODE_ENV"] = "production"
    os.environ["PAPERTRAIL_HOST"] = "PAPERTRAIL_HOST"
    os.environ["PAPERTRAIL_PORT"] = "32"
    ConfigManager.mount_config()
    papertrail_config = ConfigService.get_papertrail_config()
    assert papertrail_config == PapertrailConfig(
      host="PAPERTRAIL_HOST",
      port=32
    )

    # reset manipulated os envs
    del os.environ["PAPERTRAIL_HOST"]
    del os.environ["PAPERTRAIL_PORT"]
    os.environ["NODE_ENV"] = populated_env
