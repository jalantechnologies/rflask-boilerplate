from modules.config.config_service import ConfigService
from modules.logger.internal.logger_enum import Levels
import logging

class LogLevel:
    @staticmethod
    def get_level() -> int:
        ddconfig = ConfigService.get_datadog_config()
        datadog_level = ddconfig.datadog_log_level.lower()
        for level in Levels:
            if datadog_level.lower()==level.name:
                return level.value
        return logging.DEBUG