from dataclasses import dataclass


@dataclass(frozen=True)
class DevelopmentSettings:
    LOGGER_TRANSPORTS: tuple[str] = ("console",)
    MONGODB_URI: str = "mongodb://localhost:27017/frm-boilerplate-dev"
    TEMPORAL_SERVER_ADDRESS: str = "localhost:7233"
    TEMPORAL_TASK_QUEUE: str = "frm-boilerplate-dev-queue"
    SMS_ENABLED: bool = False
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True


@dataclass(frozen=True)
class DockerInstanceDevelopmentSettings:
    LOGGER_TRANSPORTS: tuple[str] = ("console",)
    MONGODB_URI: str = "mongodb://app-db:27017/frm-boilerplate-dev"
    TEMPORAL_SERVER_ADDRESS: str = "temporal:7233"
    TEMPORAL_TASK_QUEUE: str = "frm-boilerplate-dev-queue"
    SMS_ENABLED: bool = False
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True
