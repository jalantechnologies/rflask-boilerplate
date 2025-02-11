from __future__ import annotations

from typing import Any

from modules.config.internals.default_config import DefaultConfig
from modules.config.internals.app_env_config import AppEnvConfig
from modules.config.internals.custom_env_config import CustomEnvConfig
from modules.config.internals.config_utils import ConfigUtil


class ConfigFiles:
    content: dict[str, Any] = {}

    @staticmethod
    def load() -> None:
        ConfigFiles.content = ConfigFiles._merge_configs()

    @staticmethod
    def get_config_contents() -> dict[str, Any]:
        return ConfigFiles.content

    @staticmethod
    def _merge_configs() -> dict[str, Any]:
        default_content = DefaultConfig.load()
        app_env_content = AppEnvConfig.load()
        os_env_content = CustomEnvConfig.load()

        merged_content = ConfigUtil.deep_merge(default_content, app_env_content)
        return ConfigUtil.deep_merge(merged_content, os_env_content)
