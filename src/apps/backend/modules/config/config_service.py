import configparser
import os
from typing import Any
from modules.config.errors import ConfigMissingError
from pathlib import Path
  
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
        default_config_path = ConfigService.config_path / "default.ini"
        app_env = os.environ.get('APP_ENV', "development")
        env_config_path = ConfigService.config_path / f"{app_env}.ini"

        config.read([default_config_path, env_config_path])
        ConfigService.__load_environment_variables(config=config)

        ConfigService._config = config
    
    def __load_environment_variables(config: configparser.ConfigParser):
        env_config = configparser.ConfigParser()
        env_config.read(ConfigService.config_path / "custom-environment-variables.ini")
        for section in env_config.sections():
            for key, value in env_config[section].items():
                env_var = os.environ.get(value)
                if env_var is not None:
                    if section not in config:
                        config[section] = {}
                    config[section][key] = env_var
                
    @staticmethod
    def get_value(key: str, section: str = 'DEFAULT') -> Any:
        try:
            return ConfigService._config.get(section, key)
        except (configparser.NoOptionError, configparser.NoSectionError):
            raise ConfigMissingError(key)
          
    @staticmethod
    def has_value(key: str, section: str = 'DEFAULT') -> bool:
        return ConfigService._config.has_option(section, key)
