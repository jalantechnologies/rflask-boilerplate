from dataclasses import dataclass


@dataclass(frozen=True)
class TestingSettings:
    MONGODB_URI: str = "mongodb://localhost:27017/frm-boilerplate-test"


@dataclass(frozen=True)
class DockerInstanceTestingSettings:
    MONGODB_URI: str = "mongodb://db:27017/frm-boilerplate-test"
