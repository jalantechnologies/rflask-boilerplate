import os
from typing import Any
from modules.config.internals.config_utils import ConfigUtil


class AppEnvConfig:

    filename: str

    @staticmethod
    def load() -> dict[str, Any]:
        app_env = os.environ.get("APP_ENV", "development")
        AppEnvConfig.filename = f"{app_env}.yml"
        return ConfigUtil.read_yml_from_config_dir(AppEnvConfig.filename)
