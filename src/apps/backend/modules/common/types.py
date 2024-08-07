from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorCode:
    MISSING_KEY: str = "KEY_ERR_404"
    VALUE_TYPE_MISMATCH: str = "INVALID_VALUE_TYPE_400"
