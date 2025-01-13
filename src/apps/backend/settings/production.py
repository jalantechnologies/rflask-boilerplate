from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionSettings:
    LOGGER_TRANSPORTS: tuple[str, str] = ("console", "papertrail")
    SMS_ENABLED: bool = True
    USE_PROXY: bool = True # Set as True if server is running behind proxy
