from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentSettings:
    LOGGER_TRANSPORTS: tuple[str] = ("console",)
    MONGODB_URI: str = "mongodb://localhost:27017/frm-boilerplate-dev"
    SMS_ENABLED: bool = False
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True


@dataclass(frozen=True)
class DockerInstanceDevelopmentSettings:
    LOGGER_TRANSPORTS: tuple[str] = ("console",)
    MONGODB_URI: str = "mongodb://db:27017/frm-boilerplate-dev"
    SMS_ENABLED: bool = False
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True
