from configparser import ConfigParser,NoOptionError,NoSectionError
import os
from typing import Type,TypeVar
from modules.error.custom_errors import MissingKeyError
from modules.common.types import ErrorCode
from modules.common.config_utils import ConfigUtils

T = TypeVar('T')

class ConfigService:
    _config = ConfigParser()
    config_path = ConfigUtils.get_parent_directory(__file__, 6) / "config"

    @staticmethod
    def load_config() -> None:
        app_env_config = ConfigService.initialize_config()
        os_env_config = ConfigService.load_environment_variables()
        ConfigService._config = ConfigService.merge_configs(app_env_config,os_env_config)
        ConfigService.log_config()
    
    @staticmethod
    def initialize_config() -> ConfigParser:
        config = ConfigParser()
        # To preserve the case of keys, we set `config.optionxform = str`.
        # Visit: https://github.com/python/mypy/issues/5062 for more information on the lint error.
        config.optionxform = str  # type: ignore
        default_config = ConfigService.config_path / "default.ini"
        config.read(default_config)
        app_env = os.environ.get("APP_ENV", "development")
        app_env_config = ConfigService.config_path / f"{app_env}.ini"
        config.read(app_env_config)
        return config
    
    @staticmethod
    def load_environment_variables() -> ConfigParser:
        custom_environment_file = ConfigService.config_path / "custom-environment-variables.ini"
        env_config = ConfigParser(allow_no_value=True)
        if not custom_environment_file.exists():
            return env_config
        # Preserve case sensitivity for keys
        env_config.optionxform = str  # type: ignore
        env_config.read(custom_environment_file)
        for section in env_config.sections():
            for key, _ in env_config.items(section):
                value = os.environ.get(key, "")
                env_config.set(section,key,value)
        return env_config

    @staticmethod
    def merge_configs(app_env_config:ConfigParser,os_env_config:ConfigParser)->ConfigParser:
        merge_config = app_env_config
        for section in os_env_config.sections():
            if section not in app_env_config.sections():
                merge_config.add_section(section)
            for key, value in os_env_config[section].items():
                if value == "":
                    if not merge_config.has_option(section,key):
                        merge_config.set(section,key,"")
                else:
                    merge_config.set(section,key,value)
        return merge_config

    @staticmethod
    def log_config() -> None:
        config_dict = {
            section: dict(ConfigService._config[section].items())
            for section in ConfigService._config.sections()
        }
        print("config:", config_dict)

    @staticmethod
    def get_value(key: str, section: str, expected_type: Type[T]) -> T:
        try:
            value = ConfigService._config.get(section, key)
            if expected_type == int:
                return int(value) if value != '' else None  # type: ignore
            elif expected_type == bool:
                return ConfigService._config.getboolean(section, key)  # type: ignore
            elif expected_type == float:
                return float(value) if value != '' else None  # type: ignore
            elif expected_type == str:
                return value  # type: ignore
            else:
                raise ValueError(f"Unsupported type {expected_type}")
        except (NoOptionError, NoSectionError) as exc:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY) from exc
        except ValueError as e:
            raise ValueError(f"Value for {key} in section {section} cannot be cast to {expected_type}: {e}") from e

    @staticmethod
    def has_value(key: str, section: str = "DEFAULT") -> bool:
        return ConfigService._config.has_option(section, key)
