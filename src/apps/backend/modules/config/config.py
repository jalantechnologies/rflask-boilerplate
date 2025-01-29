import os
from pathlib import Path
from typing import Any, Optional

import yaml


def get_parent_directory(directory: str, levels: int) -> Path:
    parent_dir = Path(directory)
    for _ in range(levels):
        parent_dir = parent_dir.parent
    return parent_dir


class Config:
    config_dict: dict[str, Any]
    config_path: Path = get_parent_directory(__file__, 6) / "config"

    @staticmethod
    def read(filename: str) -> dict[str, Any]:
        file_path = Config.config_path / filename
        yaml_content: dict[str, Any] = {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                yaml_content = yaml.safe_load(file)
        except FileNotFoundError as e:
            print(e)
        return yaml_content

    @staticmethod
    def load_config() -> None:
        Config.intialize_config()
        Config.process_custom_environment_variables()
        print(yaml.dump(Config.config_dict))

    @staticmethod
    def intialize_config() -> None:
        default_content = Config.read("default.yml")
        app_env = os.environ.get("APP_ENV", "development")
        app_env_content = Config.read(f"{app_env}.yml")
        merge_content = Config.deep_merge(default_content, app_env_content)
        Config.config_dict = merge_content

    @staticmethod
    def parse_value(value: Optional[str], value_format: str) -> Any:
        """
        Parse the environment variable value based on the specified format.
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
            raise ValueError(
                f"Error parsing value '{value}' as {value_format}: {e}"
            ) from e

    @staticmethod
    def replace_with_env_values(data: dict[str, Any]) -> dict[str, Any]:
        """
        Recursively traverse a dictionary and replace values with the corresponding environment variable values
        if the value in the dictionary matches a key in the environment variables.
        """
        if not isinstance(data, dict):
            return data

        keys_to_delete: list = []  # Collect keys to delete

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = Config.process_dict_value(value)
            elif isinstance(value, str):
                Config.process_str_value(data, key, value, keys_to_delete)

        Config.delete_keys(data, keys_to_delete)
        return data

    @staticmethod
    def process_dict_value(value: dict[str, Any]) -> Any:
        """Process a dictionary value, replacing or recursively traversing it."""
        if "__name" in value:
            env_var_name = value["__name"]
            env_var_value = os.getenv(env_var_name)
            value_format = value.get("__format")
            return (
                Config.parse_value(env_var_value, value_format)
                if value_format
                else env_var_value
            )
        return Config.replace_with_env_values(value)

    @staticmethod
    def process_str_value(
        data: dict[str, Any], key: str, value: str, keys_to_delete: list
    ) -> None:
        """Process a string value, replacing it with an environment variable or marking for deletion."""
        env_value = os.getenv(value)
        if env_value is None:
            keys_to_delete.append(key)
        else:
            data[key] = env_value

    @staticmethod
    def delete_keys(data: dict[str, Any], keys_to_delete: list) -> None:
        """Delete keys marked for deletion."""
        for key in keys_to_delete:
            del data[key]

    @staticmethod
    def process_custom_environment_variables() -> None:
        """
        Reads keys from custom_env_contents, maps them to environment variables,
        and overrides them in the configuration if they exist.
        """
        custom_env_contents = Config.read("custom-environment-variables.yml")
        replaced_custom_env_contents = Config.replace_with_env_values(
            custom_env_contents
        )
        Config.deep_merge(Config.config_dict, replaced_custom_env_contents)

    @staticmethod
    def deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """
        Recursively merges dict2 into dict1. Values from dict2 will overwrite those in dict1.
        If a value is a nested dictionary, it will be merged as well.
        """
        for key, value in dict2.items():
            if (
                isinstance(value, dict)
                and key in dict1
                and isinstance(dict1[key], dict)
            ):
                # If both are dictionaries, merge them recursively
                dict1[key] = Config.deep_merge(dict1[key], value)
            else:
                # If not a dictionary, just overwrite or add the key-value pair
                dict1[key] = value
        return dict1

    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        keys = key.split(".")
        value = Config.config_dict
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    @staticmethod
    def has(key: str) -> bool:
        keys = key.split(".")
        value = Config.config_dict
        try:
            for k in keys:
                value = value[k]
            return True
        except (KeyError, TypeError):
            return False
