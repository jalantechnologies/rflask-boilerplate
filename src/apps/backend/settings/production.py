from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionSettings:
	LOGGER_TRANSPORTS: tuple[str, str] = ("console", "papertrail")
	PAPERTRAIL_HOST: str = "logs6.papertrailapp.com"
	PAPERTRAIL_PORT: str = "12345"
	MONGODB_URI: str = "mongodb://db:27017/frm-boilerplate-dev"