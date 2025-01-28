from typing import TypeVar
from modules.common.types import ErrorCode
from modules.error.custom_errors import MissingKeyError
from modules.config.config import Config

T = TypeVar('T')

class ConfigService:

    @staticmethod
    def load_config() -> None:
        Config.load_config()

    @staticmethod
    def get_value(key: str) -> T: # type: ignore
        value = Config.get(key)
        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)
        return value # type: ignore

    @staticmethod
    def has_value(key: str) -> bool:
        return Config.has(key)
