from typing import Generic,TypeVar
from modules.common.types import ErrorCode
from modules.error.custom_errors import MissingKeyError
from modules.config.config import Config

T = TypeVar('T')

class ConfigService(Generic[T]):
    @staticmethod
    def load_config() -> None:
        Config.load_config()

    @classmethod
    def get_value(cls,key: str) -> T:
        value = Config.get(key)
        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)
        return value  # type: ignore

    @staticmethod
    def has_value(key: str) -> bool:
        return Config.has(key)
