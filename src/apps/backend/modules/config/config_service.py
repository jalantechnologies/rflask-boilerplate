from typing import Type, TypeVar, cast

from modules.common.types import ErrorCode
from modules.config.config import Config
from modules.error.custom_errors import MissingKeyError

T = TypeVar("T")


class ConfigService:

    @staticmethod
    def load_config() -> None:
        Config.load_config()

    @staticmethod
    def get_value(key: str, expected_type: Type[T]) -> T:
        value = Config.get(key)
        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)

        if isinstance(value, expected_type):
            return value

        try:
            return cast(T, expected_type(value))  # type: ignore [call-arg]

        except (ValueError, TypeError):
            raise TypeError(f"Cannot convert config value {value!r} to {expected_type}")

    @staticmethod
    def has_value(key: str) -> bool:
        return Config.has(key)
