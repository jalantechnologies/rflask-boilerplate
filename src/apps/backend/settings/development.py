from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentSettings:
    LOGGER_TRANSPORTS: tuple[str] = ("console",)
    MONGODB_URI: str = "mongodb://localhost:27017/frm-boilerplate-dev"
    SMS_ENABLED: bool = False
    USE_PROXY: bool = False # Set as True if server is running behind proxy


@dataclass(frozen=True)
class DockerInstanceDevelopmentSettings:
    LOGGER_TRANSPORTS: tuple[str] = ("console",)
    MONGODB_URI: str = "mongodb://db:27017/frm-boilerplate-dev"
    SMS_ENABLED: bool = False
    USE_PROXY: bool = False # Set as True if server is running behind proxy
