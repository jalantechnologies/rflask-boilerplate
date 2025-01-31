import os
from pathlib import Path
from typing import Any, Optional

import yaml


class ConfigParser:
    # Utility Methods
    @staticmethod
    def get_base_directory(current_file: str) -> Path:
        """
        Get the base directory of the project.
        """
        starting_index = current_file.find("app")
        base_directory = current_file[: starting_index + len("app")]
        return Path(base_directory)

    # Main Config Operations
    @staticmethod
    def read_config(filename: str, config_path: Path) -> dict[str, Any]:
        """
        Read the content of a YAML file.
        """
        file_path = config_path / filename
        yaml_content: dict[str, Any] = {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                yaml_content = yaml.safe_load(file)
        except FileNotFoundError:
            from modules.logger.logger import Logger

            Logger.error(message=f"Config file '{filename}' not found.")
        return yaml_content

    @staticmethod
    def deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """
        Deep merge two dictionaries.
        """
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                dict1[key] = ConfigParser.deep_merge(dict1[key], value)
            else:
                dict1[key] = value
        return dict1

    @staticmethod
    def initialize_config(config_path: Path) -> dict[str, Any]:
        """
        Initialize the configuration.

        The configuration is read from the default.yml file and the file corresponding to the APP_ENV environment
        variable. The configuration is then merged with the custom-environment-variables.yml file, which contains
        environment variable mappings. The environment variables are then replaced with their corresponding values.

        The final configuration is returned.
        """
        default_content = ConfigParser.read_config("default.yml", config_path)
        app_env = os.environ.get("APP_ENV", "development")
        app_env_content = ConfigParser.read_config(f"{app_env}.yml", config_path)
        config_dict = ConfigParser.deep_merge(default_content, app_env_content)

        custom_env_contents = ConfigParser.read_config("custom-environment-variables.yml", config_path)
        replaced_custom_env_contents = ConfigParser.replace_with_env_values(custom_env_contents)
        return ConfigParser.deep_merge(config_dict, replaced_custom_env_contents)

    # Data Processing Methods
    @staticmethod
    def replace_with_env_values(data: dict[str, Any]) -> dict[str, Any]:
        """
        Replace the values of the dictionary with the corresponding environment variables.

        The values of the dictionary are recursively processed. If a value is a dictionary, the process_dict_value
        method is called. If a value is a string, the process_str_value method is called.

        The keys that are not found in the environment variables are deleted from the dictionary.

        The processed dictionary is returned.
        """
        if not isinstance(data, dict):
            return data

        keys_to_delete: list = []

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = ConfigParser.process_dict_value(value)
            elif isinstance(value, str):
                ConfigParser.process_str_value(data, key, value, keys_to_delete)

        ConfigParser.delete_keys(data, keys_to_delete)
        return data

    @staticmethod
    def process_dict_value(value: dict[str, Any]) -> Any:
        """
        Process the values of a dictionary.

        If the dictionary contains the __name key, the value is cast into the corresponding __format and returned.

        Otherwise, the values of the dictionary are recursively replaced with the corresponding environment variables.
        """
        if "__name" in value:
            env_var_name = value["__name"]
            env_var_value = os.getenv(env_var_name)
            value_format = value.get("__format")
            return ConfigParser.parse_value(env_var_value, value_format) if value_format else env_var_value
        return ConfigParser.replace_with_env_values(value)

    @staticmethod
    def process_str_value(data: dict[str, Any], key: str, value: str, keys_to_delete: list) -> None:
        """
        Process the values of a string. If the string is an environment variable, the value is replaced
        with the corresponding environment variable. If the environment variable is not found, the key is
        added to the keys_to_delete list.
        """
        env_value = os.getenv(value)
        if env_value is None:
            keys_to_delete.append(key)
        else:
            data[key] = env_value

    @staticmethod
    def delete_keys(data: dict[str, Any], keys_to_delete: list) -> None:
        """
        Delete the keys from the dictionary.
        """
        for key in keys_to_delete:
            del data[key]

    # Parsing Methods
    @staticmethod
    def parse_value(value: Optional[str], value_format: str) -> int | float | bool | None:
        """
        Parse the value based on the value format.

        The value is parsed based on the value format. The supported formats are boolean and number.
        If the value format is not supported, a ValueError is raised.

        If the value cannot be parsed, a ValueError is raised.

        The parsed value is returned.
        """
        if value is None:
            return None

        parsers = {
            "boolean": lambda x: x.lower() in ["true", "1"],
            "number": lambda x: int(x) if x.isdigit() else float(x),
        }

        parser = parsers.get(value_format)
        if not parser:
            raise ValueError(f"Unsupported format: {value_format}")

        try:
            return parser(value)
        except Exception as e:
            raise ValueError(f"Error parsing value '{value}' as {value_format}: {e}") from e
