from dataclasses import dataclass


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    host: str
    app_name: str
    dd_log_level: str