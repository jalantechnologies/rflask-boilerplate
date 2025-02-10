import os
from typing import Any, Optional
from modules.config.internals.config_utils import ConfigUtil

class CustomEnvConfig:
    
    filename:str = "custom-environment-variables.yml"
    
    @staticmethod
    def load() -> dict[str,Any]:
        custom_env_config = ConfigUtil.read_yml_from_config_dir("custom-environment-variables.yml")
        return CustomEnvConfig._inject_environment_variables(custom_env_config)

    @staticmethod
    def _inject_environment_variables(data: dict[str, Any]) -> dict[str, Any]:
        
        if not isinstance(data, dict):
            return data

        keys_to_delete: list = []

        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = CustomEnvConfig._search_and_replace_dict_value_with_env(value)
            elif isinstance(value, str):
                CustomEnvConfig._search_and_replace_str_value_with_env(data, key, value, keys_to_delete)

        for key in keys_to_delete:
            del data[key]

        return data

    @staticmethod
    def _search_and_replace_dict_value_with_env(value: dict[str, Any]) -> Any:
        if "__name" in value:
            env_var_name = value["__name"]
            env_var_value = os.getenv(env_var_name)
            value_format = value.get("__format")
            return CustomEnvConfig._parse_value(env_var_value, value_format) if value_format else env_var_value
        return CustomEnvConfig._inject_environment_variables(value)

    @staticmethod
    def _search_and_replace_str_value_with_env(data: dict[str, Any], key: str, value: str, keys_to_delete: list) -> None:
        env_value = os.getenv(value)
        if env_value is None:
            keys_to_delete.append(key)
        else:
            data[key] = env_value

    @staticmethod
    def _parse_value(value: Optional[str], value_format: str) -> int | float | bool | None:
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
