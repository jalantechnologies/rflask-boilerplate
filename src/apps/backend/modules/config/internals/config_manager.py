from pathlib import Path
from typing import Any, Optional, cast

from modules.config.internals.config_parser import ConfigParser
from modules.config.types import T


class ConfigManager:
    CONFIG_STORE: dict[str, Any] = {}
    CONFIG_PATH: Path
    CONFIG_KEY_SEPARATOR: str = "."

    @staticmethod
    def load_config() -> None:
        """
        Load the configuration files and store them in the CONFIG_STORE variable.
        """
        ConfigManager.CONFIG_PATH = ConfigParser.get_base_directory(__file__) / "config"
        ConfigManager.CONFIG_STORE = ConfigParser.initialize_config(ConfigManager.CONFIG_PATH)

    @staticmethod
    def get(key: str, default: Optional[T] = None) -> Optional[T]:
        """
        Get the value of the key from the configuration store.
        """
        value = ConfigManager.CONFIG_STORE
        for k in key.split(ConfigManager.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return default
            value = value[k]
        return cast(Optional[T], value)

    @staticmethod
    def has(key: str) -> bool:
        """
        Check if the key exists in the configuration store.
        """
        value = ConfigManager.CONFIG_STORE
        for k in key.split(ConfigManager.CONFIG_KEY_SEPARATOR):
            if not isinstance(value, dict) or k not in value:
                return False
            value = value[k]
        return True
