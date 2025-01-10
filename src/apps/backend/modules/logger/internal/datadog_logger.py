import datadog
import logging 
from modules.logger.internal.base_logger import BaseLogger
from modules.config.config_service import ConfigService

class DatadogLogger(BaseLogger):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logger_config = ConfigService.get_datadog_config()

    def critical(self, *, message: str) -> None:
        self.logger.critical(msg=message)

    def debug(self, *, message: str) -> None:
        self.logger.debug(msg=message)

    def error(self, *, message: str) -> None:
        self.logger.error(msg=message)

    def info(self, *, message: str) -> None:
        self.logger.info(msg=message)

    def warn(self, *, message: str) -> None:
        self.logger.warning(msg=message)