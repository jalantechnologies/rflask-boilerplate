from typing import Generic, Optional, cast

from modules.common.types import ErrorCode
from modules.config.internals.config_manager import ConfigManager
from modules.config.types import T
from modules.error.custom_errors import MissingKeyError


class ConfigService(Generic[T]):
    config_manager: ConfigManager = ConfigManager()

    @classmethod
    def get_value(cls, key: str, default: Optional[T] = None) -> T:
        value: Optional[T] = cls.config_manager.get(key, default=default)
        if value is None:
            # Raised when key is not found in config store
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)
        return cast(T, value)

    @classmethod
    def has_value(cls, key: str) -> bool:
        return cls.config_manager.has(key)
