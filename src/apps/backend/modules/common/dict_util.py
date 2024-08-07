from typing import Any, Type, TypeVar

from modules.common.types import ErrorCode
from modules.error.custom_errors import MissingKeyError, ValueTypeMismatchError

T = TypeVar("T")


class DictUtil:
    @staticmethod
    def required_get_str(*, input_dict: dict[str, Any], key: str) -> str:
        return DictUtil._required_get(input_dict=input_dict, key=key, value_type=str)

    @staticmethod
    def required_get_list(*, input_dict: dict[str, Any], key: str) -> list:
        return DictUtil._required_get(input_dict=input_dict, key=key, value_type=list)

    @staticmethod
    def required_get_tuple(*, input_dict: dict[str, Any], key: str) -> tuple:
        return DictUtil._required_get(input_dict=input_dict, key=key, value_type=tuple)

    @staticmethod
    def required_get_dict(*, input_dict: dict[str, Any], key: str) -> dict:
        return DictUtil._required_get(input_dict=input_dict, key=key, value_type=dict)

    @staticmethod
    def required_get_int(*, input_dict: dict[str, Any], key: str) -> int:
        return DictUtil._required_get(input_dict=input_dict, key=key, value_type=int)

    @staticmethod
    def required_get_bool(*, input_dict: dict[str, Any], key: str) -> bool:
        return DictUtil._required_get(input_dict=input_dict, key=key, value_type=bool)

    @staticmethod
    def _required_get(*, input_dict: dict[str, Any], key: str, value_type: Type[T]) -> T:
        value = input_dict.get(key)

        if value is None:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)

        if not isinstance(value, value_type):
            raise ValueTypeMismatchError(
                actual_value_type=value.__class__.__name__,
                expected_value_type=value_type.__class__.__name__,
                key=key,
                error_code=ErrorCode.VALUE_TYPE_MISMATCH,
            )

        return value
