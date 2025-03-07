import logging

from modules.logger.internal.base_logger import BaseLogger
from modules.logger.internal.datadog_handler import DatadogHandler
from modules.logger.internal.datadog_handler_level import LogLevel


class DatadogLogger(BaseLogger):
    def __init__(self) -> None:
        self.level = LogLevel.get_level()
        self.logger = logging.getLogger(__name__)
        self.format = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
        self.formatter = logging.Formatter(self.format)
        self.logger.setLevel(LogLevel.get_level())
        self.handler = DatadogHandler("flask")
        self.handler.setLevel(LogLevel.get_level())
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def critical(self, *, message: str) -> None:
        self.handler.setLevel(logging.CRITICAL)
        self.logger.critical(message)

    def debug(self, *, message: str) -> None:
        self.handler.setLevel(logging.DEBUG)
        self.logger.debug(message)

    def error(self, *, message: str) -> None:
        self.handler.setLevel(logging.ERROR)
        self.logger.error(message)

    def info(self, *, message: str) -> None:
        self.handler.setLevel(logging.INFO)
        self.logger.info(message)

    def warn(self, *, message: str) -> None:
        self.handler.setLevel(logging.WARNING)
        self.logger.warning(message)
