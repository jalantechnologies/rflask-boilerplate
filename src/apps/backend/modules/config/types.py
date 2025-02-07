from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T", bound=int | str | bool | list | dict)


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    app_name: str
    datadog_log_level: str
    host: str
