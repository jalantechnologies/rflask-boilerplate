from dataclasses import dataclass


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    application_key: str
    app_name: str