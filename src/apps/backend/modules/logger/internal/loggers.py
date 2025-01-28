from typing import Any

from modules.config.config_service import ConfigService
from modules.logger.internal.console_logger import ConsoleLogger
from modules.logger.internal.types import LoggerTransports
from modules.logger.internal.datadog_logger import DatadogLogger


class Loggers:
    _loggers: list[Any] = []

    @staticmethod
    def initialize_loggers() -> None:
        logger_transports:list = ConfigService.get_value(key='logger.transports')
        for logger_transport in logger_transports:
            if logger_transport == LoggerTransports.CONSOLE:
                Loggers._loggers.append(Loggers.__get_console_logger())

            if logger_transport == LoggerTransports.DATADOG:
                Loggers._loggers.append(Loggers.__get_datadog_logger())


    @staticmethod
    def info(*, message: str) -> None:
        [logger.info(message=message) for logger in Loggers._loggers]

    @staticmethod
    def debug(*, message: str) -> None:
        [logger.debubg(message=message) for logger in Loggers._loggers]

    @staticmethod
    def error(*, message: str) -> None:
        [logger.error(message=message) for logger in Loggers._loggers]

    @staticmethod
    def warn(*, message: str) -> None:
        [logger.warn(message=message) for logger in Loggers._loggers]

    @staticmethod
    def critical(*, message: str) -> None:
        [logger.critical(message=message) for logger in Loggers._loggers]

    @staticmethod
    def __get_console_logger() -> ConsoleLogger:
        return ConsoleLogger()
    
    @staticmethod
    def __get_datadog_logger() -> DatadogLogger:
        return DatadogLogger()
