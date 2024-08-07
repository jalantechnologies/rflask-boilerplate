from dataclasses import dataclass


@dataclass(frozen=True)
class AppEnv:
    DEVELOPMENT: str = "development"
    DOCKER_INSTANCE_TEST: str = "docker-test"
    DOCKER_INSTANCE_DEV: str = "docker-dev"
    PREVIEW: str = "preview"
    PRODUCTION: str = "production"
    TESTING: str = "testing"
