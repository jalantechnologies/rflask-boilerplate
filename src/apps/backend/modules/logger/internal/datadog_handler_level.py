from modules.config.config_service import ConfigService
from modules.logger.internal.logger_enum import Levels
import logging

class LogLevel:
    @staticmethod
    def get_level() -> int:
        ddconfig_level = ConfigService.get_value(key="LOG_LEVEL", section="DATADOG")
        datadog_level = ddconfig_level.lower()
        for level in Levels:
            if datadog_level.lower()==level.name:
                return level.value
        return logging.DEBUG