from dataclasses import dataclass
from typing import TypeVar, Union

T = TypeVar("T", bound=int | str | bool | list | dict)


class Config(dict):
    def __setitem__(self, key: str, value: Union[int, str, bool, float, list, dict, None, "Config"]) -> None:
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, got {type(key).__name__}")
        if not isinstance(value, (str, bool, int, float, list, dict, type(None), Config)):
            raise TypeError(f"Value must be str, bool, int, float, list, dict, or None, got {type(value).__name__}")
        super().__setitem__(key, value)
