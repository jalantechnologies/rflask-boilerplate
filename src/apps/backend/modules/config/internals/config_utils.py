import os
from pathlib import Path
from typing import Any

import yaml


class ConfigUtil:

    @staticmethod
    def deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                dict1[key] = ConfigUtil.deep_merge(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    @staticmethod
    def read_yml_from_config_dir(filename: str) -> dict[str, Any]:
        config_path = ConfigUtil._get_base_config_directory(__file__)
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
        starting_index = current_file.find("src")
        if starting_index == -1:
            # Raised when 'src' is not in the project_path
            raise ValueError(f"'src' not found in current_file path: {current_file}")

        base_directory = current_file[: starting_index]
        config_directory = os.path.join(base_directory, "config")
        config_path = Path(config_directory)

        if not config_path.exists() or not config_path.is_dir():
            # Raised when config dir is not created
            raise FileNotFoundError(f"Config directory does not exist: {config_directory}")

        return config_path
