from typing import Any, Optional, cast

from modules.config.internals.config_files_loader import ConfigFilesLoader
from modules.config.types import T
from modules.config.types import Config

class ConfigManager:

    CONFIG_KEY_SEPARATOR: str = "."

    def __init__(self) -> None:
        self.config_store: Config = ConfigFilesLoader.load()

    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        value = self._traverse_config(key)
        return value if value is not None else default

    def has(self, key: str) -> bool:
        return self._traverse_config(key) is not None

    def _traverse_config(self, key: str) -> Optional[T]:
        value = self.config_store
        for k in key.split(self.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return None  # Indicates key was not found
            value = value[k]
        return cast(T,value)
