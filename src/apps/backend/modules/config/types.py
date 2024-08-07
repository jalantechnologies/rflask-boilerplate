from dataclasses import dataclass


@dataclass(frozen=True)
class PapertrailConfig:
    host: str
    port: int
