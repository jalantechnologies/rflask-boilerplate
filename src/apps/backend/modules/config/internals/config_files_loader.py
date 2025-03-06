from typing import Any

from modules.config.internals.config_files.default_config_file import DefaultConfig
from modules.config.internals.config_files.app_env_config_file import AppEnvConfig
from modules.config.internals.config_files.custom_env_config_file import CustomEnvConfig
from modules.config.internals.config_utils import ConfigUtil
from modules.config.types import Config

class ConfigFilesLoader:

    @staticmethod
    def load() -> Config:
        return ConfigFilesLoader._load_and_merge_configs()


    @staticmethod
    def _load_and_merge_configs() -> Config:
        default_content = DefaultConfig.load()
        app_env_content = AppEnvConfig.load()
        os_env_content = CustomEnvConfig.load()

        merged_content = ConfigUtil.deep_merge(default_content, app_env_content)
        return ConfigUtil.deep_merge(merged_content, os_env_content)
