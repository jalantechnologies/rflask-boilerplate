import configparser
import os
from typing import Type,TypeVar,Any
from modules.error.custom_errors import MissingKeyError
from modules.common.types import ErrorCode
from modules.common.config_utils import ConfigUtils

T = TypeVar('T')

class ConfigService:
    _config: configparser.ConfigParser = configparser.ConfigParser()
    config_path = ConfigUtils.get_parent_directory(__file__, 6) / "config"

    @staticmethod
    def load_config() -> None:
        config = configparser.ConfigParser()
        # ConfigParser converts all keys to lowercase by default.
        # To preserve the case of keys, we set `config.optionxform = str`.
        # The following line will always throw a lint error, hence the `# type: ignore`.
        # Visit: https://github.com/python/mypy/issues/5062 for more information on the lint error.
        config.optionxform = str  # type: ignore
        default_config = ConfigService.config_path / "default.ini"
        app_env = os.environ.get("APP_ENV", "development")
        app_env_config = ConfigService.config_path / f"{app_env}.ini"
        config.read([default_config, app_env_config])
        ConfigService.__load_environment_variables(config=config)
        ConfigService._config = config
        config_dict = {
            section: {key: value for key, value in ConfigService._config[section].items()}
            for section in ConfigService._config.sections()
        }
        print("config:", config_dict)

    @staticmethod
    def __load_environment_variables(config: configparser.ConfigParser) -> None:
        """This function reads the custom_environment_file for keys
        and retrieves associated values from the project environment"""
        custom_environment_file = ConfigService.config_path / "custom-environment-variables.ini"
        if not custom_environment_file.exists():
            return

        env_config = configparser.ConfigParser()
        env_config.optionxform = str  # type: ignore
        env_config.read(custom_environment_file)

        for section in env_config.sections():
            if section not in config:
                config.add_section(section)
            for key, _ in env_config[section].items():
                env_var_value = os.environ.get(key)
                if env_var_value is not None:
                    config[section][key] = env_var_value
                elif not config.has_option(section, key):
                    config[section][key] = ""

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
        except (configparser.NoOptionError, configparser.NoSectionError) as exc:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY) from exc
        except ValueError as e:
            raise ValueError(f"Value for {key} in section {section} cannot be cast to {expected_type}: {e}") from e

    @staticmethod
    def has_value(key: str, section: str = "DEFAULT") -> bool:
        return ConfigService._config.has_option(section, key)