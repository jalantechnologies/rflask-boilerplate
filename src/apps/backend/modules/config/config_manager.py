import os

from dataclasses import asdict
from typing import Any

from settings import (
  DefaultSettings,
  DevelopmentSettings,
  DockerInstanceDevelopmentSettings,
  DockerInstanceTestingSettings,
  OSSettings,
  PreviewSettings,
  ProductionSettings,
  TestingSettings,
)

from settings.types import AppEnv

class ConfigManager:
  config: dict[str, Any] = {}

  @staticmethod
  def mount_config() -> None:
    ConfigManager.config = {**ConfigManager.config, **asdict(DefaultSettings())}
    ConfigManager.config = {**ConfigManager.config, **asdict(ConfigManager._load_app_env_settings())}
    not_nullable_os_envs = {k:v for k, v in asdict(OSSettings()).items() if v is not None}
    ConfigManager.config = {**ConfigManager.config, **not_nullable_os_envs}

  @staticmethod
  def _load_app_env_settings() -> dict[str, Any]:
    app_env = os.environ.get('APP_ENV', "development")
    settings_mp = {
      AppEnv.DEVELOPMENT: DevelopmentSettings,
      AppEnv.DOCKER_INSTANCE_DEV: DockerInstanceDevelopmentSettings,
      AppEnv.DOCKER_INSTANCE_TEST: DockerInstanceTestingSettings,
      AppEnv.PRODUCTION: ProductionSettings,
      AppEnv.PREVIEW: PreviewSettings,
      AppEnv.TESTING: TestingSettings,
    }

    return settings_mp.get(app_env)()
