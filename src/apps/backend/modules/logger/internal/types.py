from dataclasses import dataclass


@dataclass(frozen=True)
class LoggerTransports:
    CONSOLE: str = "console"
    PAPERTRAIL: str = "papertrail"
