import os
from typing import Any
from modules.config.types import Config
from modules.config.internals.config_utils import ConfigUtil


class AppEnvConfig:

    FILENAME: str

    @staticmethod
    def load() -> Config:
        app_env = os.environ.get("APP_ENV", "development")
        AppEnvConfig.FILENAME = f"{app_env}.yml"
        app_env_dict = ConfigUtil.read_yml_from_config_dir(AppEnvConfig.FILENAME)
        return Config(app_env_dict)
