from typing import Any, Optional

from modules.config.internals.config_file import ConfigFiles


class ConfigManager:

    CONFIG_KEY_SEPARATOR: str = "."

    def __init__(self) -> None:
        self.config_store: dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Retrieve a configuration value using dot-separated keys.
        """
        value = self.config_store
        for k in key.split(self.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return default
            value = value[k]
        return value

    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        """
        value = self.config_store
        for k in key.split(self.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return False
            value = value[k]
        return True

    def load_config(self) -> None:
        self.config_store = ConfigFiles().get_content()
        print(self.config_store)

