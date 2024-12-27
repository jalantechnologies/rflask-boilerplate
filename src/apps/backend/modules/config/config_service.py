import configparser
import os
from typing import Any
from pathlib import Path
from modules.error.custom_errors import MissingKeyError
from modules.common.types import ErrorCode
import json


def get_parent_directory(directory: str, levels: int) -> Path:
    parent_dir = Path(directory)
    for _ in range(levels):
        parent_dir = parent_dir.parent
    return parent_dir

class ConfigService:
    _config = None
    config_path = get_parent_directory(__file__, 6) / "config"

    @staticmethod
    def load_config():
        config = configparser.ConfigParser()
        default_config = ConfigService.config_path / "default.ini"
        app_env = os.environ.get('APP_ENV', "development")
        app_env_config = ConfigService.config_path / f"{app_env}.ini"
        config.read([default_config, app_env_config])
        ConfigService.__ensure_all_sections_exist(config, default_config)
        ConfigService.__load_environment_variables(config=config)
        ConfigService._config = config
        config_dict = {
            section: {
                key: value
                for key, value in ConfigService._config[section].items()
            }
            for section in ConfigService._config.sections()
        }
        print("config:", config_dict)

    @staticmethod
    def __ensure_all_sections_exist(config: configparser.ConfigParser, default_config_path: Path):
        default_config = configparser.ConfigParser()
        default_config.read(default_config_path)

        for section in default_config.sections():
            if section not in config:
                config.add_section(section)

    @staticmethod
    def __load_environment_variables(config: configparser.ConfigParser):
        env_config = configparser.ConfigParser()
        custom_env_file = ConfigService.config_path / "custom-environment-variables.ini"
        
        if custom_env_file.exists():
            env_config.read(custom_env_file)
            config.read(custom_env_file)

        for section in env_config.sections():
            if section not in config:
                config.add_section(section)
            for key, value in env_config[section].items():
                env_var = os.environ.get(value)
                if env_var is not None:
                    config[section][key] = env_var

    @staticmethod
    def get_value(*, key: str, section: str = 'DEFAULT') -> Any:
        try:
            value = ConfigService._config.get(section, key, fallback=None)
            return value if value else None
        except (configparser.NoOptionError, configparser.NoSectionError):
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY)

    @staticmethod
    def has_value(*, key: str, section: str = 'DEFAULT') -> bool:
        if ConfigService._config.has_option(section, key):
            value = ConfigService._config.get(section, key, fallback=None)
            return bool(value)  
        return False