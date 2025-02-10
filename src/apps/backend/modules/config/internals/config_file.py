from __future__ import annotations

from typing import Any

from modules.config.internals.default_config import DefaultConfig
from modules.config.internals.app_env_config import AppEnvConfig
from modules.config.internals.custom_env_config import CustomEnvConfig
from modules.config.internals.config_utils import ConfigUtil

class ConfigFiles:

    def __init__(self) -> None:
        self.content: dict[str, Any] = {}

    def load(self) -> None:
        self.content = self._merge_configs()
        
    def get_content(self) -> dict[str, Any]:
        self.load()
        return self.content
    
    def _merge_configs(self) -> dict[str, Any]:
        default_content = DefaultConfig.load()
        app_env_content = AppEnvConfig.load()
        os_env_content = CustomEnvConfig.load()

        merged_content = ConfigUtil.deep_merge(default_content, app_env_content)
        return ConfigUtil.deep_merge(merged_content, os_env_content)
        