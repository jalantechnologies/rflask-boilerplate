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
    config: dict[str, Any]
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
        print(yaml.dump(Config.config))

    @staticmethod
    def intialize_config() -> None:
        default_content = Config.read("default.yml")
        app_env = os.environ.get("APP_ENV", "development")
        app_env_content = Config.read(f"{app_env}.yml")
        merge_content = Config.deep_merge(default_content, app_env_content)
        Config.config = merge_content

    @staticmethod
    def parse_value(value:Optional[str], value_format:str)-> Any:
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
            raise ValueError(f"Error parsing value '{value}' as {value_format}: {e}") from e


    @staticmethod
    def replace_with_env_values(data:dict[str,Any])-> dict[str,Any]:
        """
        Recursively traverse a dictionary and replace values with the corresponding environment variable values
        if the value in the dictionary matches a key in the environment variables.
        """
        if isinstance(data, dict):
            keys_to_delete = []  # Collect keys to delete
            for key, value in data.items():
                if isinstance(value, dict) and "__name" in value:
                    env_var_name = value["__name"]
                    env_var_value = os.getenv(env_var_name)
                    value_format = value.get("__format")

                    if value_format:
                        data[key] = Config.parse_value(env_var_value, value_format)
                    else:
                        data[key] = env_var_value
                elif isinstance(value, dict):  # If nested, call recursively
                    data[key] = Config.replace_with_env_values(value)
                elif isinstance(value, str):  # Replace if the value is an environment key
                    env_value = os.getenv(value)
                    if env_value is None:  # Mark key for deletion if env variable is not found
                        keys_to_delete.append(key)
                    else:
                        data[key] = env_value
            # Delete keys with None values after iteration
            for key in keys_to_delete:
                del data[key]
        return data

    @staticmethod
    def process_custom_environment_variables() -> None:
        """
        Reads keys from custom_env_contents, maps them to environment variables,
        and overrides them in the configuration if they exist.
        """
        custom_env_contents = Config.read("custom-environment-variables.yml")
        replaced_custom_env_contents = Config.replace_with_env_values(custom_env_contents)
        Config.deep_merge(Config.config, replaced_custom_env_contents)

    @staticmethod
    def deep_merge(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
        """
        Recursively merges dict2 into dict1. Values from dict2 will overwrite those in dict1.
        If a value is a nested dictionary, it will be merged as well.
        """
        for key, value in dict2.items():
            if isinstance(value, dict) and key in dict1 and isinstance(dict1[key], dict):
                # If both are dictionaries, merge them recursively
                dict1[key] = Config.deep_merge(dict1[key], value)
            else:
                # If not a dictionary, just overwrite or add the key-value pair
                dict1[key] = value
        return dict1

    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        keys = key.split(".")
        value = Config.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    @staticmethod
    def has(key: str) -> bool:
        keys = key.split(".")
        value = Config.config
        try:
            for k in keys:
                value = value[k]
            return True
        except (KeyError, TypeError):
            return False
