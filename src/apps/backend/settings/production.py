from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionSettings:
    LOGGER_TRANSPORTS: tuple[str, str] = ("console", "papertrail")
