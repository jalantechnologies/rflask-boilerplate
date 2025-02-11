from typing import Any, Optional

from modules.config.internals.config_file import ConfigFiles


class ConfigManager:

    CONFIG_KEY_SEPARATOR: str = "."

    def __init__(self) -> None:
        self.config_store: dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        value = self._traverse_config(key)
        return value if value is not None else default

    def has(self, key: str) -> bool:
        return self._traverse_config(key) is not None

    def load_config(self) -> None:
        ConfigFiles.load()
        self.config_store = ConfigFiles.get_config_contents()

    def _traverse_config(self, key: str) -> Optional[Any]:
        value = self.config_store
        for k in key.split(self.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return None  # Indicates key was not found
            value = value[k]
        return value
