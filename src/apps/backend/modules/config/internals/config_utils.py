import os
from pathlib import Path
from typing import Any

import yaml

from modules.config.types import Config

class ConfigUtil:
    DIR_LEVELS_FROM_BASE_DIR_TO_CONFIG_UTILS:int = 6
    CURRENT_FILE:str = __file__
    
    @staticmethod
    def deep_merge(config1: "Config", config2: "Config") -> "Config":
        for key, value in config2.items():
            if isinstance(value, dict) and key in config1 and isinstance(config1[key], dict):
                config1[key] = ConfigUtil.deep_merge(Config(config1[key]), Config(value))
            else:
                config1[key] = value
        return config1

    @staticmethod
    def read_yml_from_config_dir(filename: str) -> dict[str, Any]:
        config_path = ConfigUtil._get_base_config_directory(ConfigUtil.CURRENT_FILE)
        file_path = config_path / filename  # Path lib's join operator
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = yaml.safe_load(file) or {}
        except FileNotFoundError:
            # Raised when filename is not found in config dir
            raise FileNotFoundError(f"Config file '{filename}' not found in {config_path}")
        return content

    @staticmethod
    def _get_base_config_directory(current_file: str) -> Path:
        base_directory = Path(current_file).resolve().parents[ConfigUtil.DIR_LEVELS_FROM_BASE_DIR_TO_CONFIG_UTILS]
        config_directory = base_directory / "config" # Path lib's join operator

        if not config_directory.exists() or not config_directory.is_dir():
            raise FileNotFoundError(f"Config directory does not exist: {config_directory}")

        return config_directory
