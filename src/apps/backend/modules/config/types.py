from dataclasses import dataclass


@dataclass(frozen=True)
class PapertrailConfig:
    host: str
    port: int


@dataclass(frozen=True)
class DatadogConfig:
    api_key: str
    application_key: str