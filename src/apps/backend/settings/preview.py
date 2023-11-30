from dataclasses import dataclass


@dataclass(frozen=True)
class PreviewSettings:
	LOGGER_TRANSPORTS: tuple[str] = ("console", "papertrail")
