from typing import Generic, Optional, cast

from modules.common.types import ErrorCode
from modules.config.internals.config_manager import ConfigManager
from modules.config.types import T
from modules.error.custom_errors import MissingKeyError


class ConfigService(Generic[T]):
    @staticmethod
    def load_config() -> None:
        """
        Load the configuration files
        """
        ConfigManager.load_config()

    @classmethod
    def get_value(cls, key: str, default: Optional[T] = None) -> T:
        """
        Get the value of the key from the configuration
        """
        value: Optional[T] = ConfigManager.get(key, default=default)
        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)
        return cast(T, value)

    @staticmethod
    def has_value(key: str) -> bool:
        """
        Check if the key exists in the configuration
        """
        return ConfigManager.has(key)
