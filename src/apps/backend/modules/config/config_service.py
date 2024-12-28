import configparser
import os
from pathlib import Path
from modules.error.custom_errors import MissingKeyError
from modules.common.types import ErrorCode

def get_parent_directory(directory: str, levels: int) -> Path:
    parent_dir = Path(directory)
    for _ in range(levels):
        parent_dir = parent_dir.parent
    return parent_dir

class ConfigService:
    _config: configparser.ConfigParser = configparser.ConfigParser()
    config_path = get_parent_directory(__file__, 6) / "config"

    @staticmethod
    def load_config()->None:
        config = configparser.ConfigParser()
        config.optionxform = str # type: ignore
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
    def __ensure_all_sections_exist(config: configparser.ConfigParser,
                                    default_config_path: Path)->None:
        default_config = configparser.ConfigParser()
        default_config.read(default_config_path)

        for section in default_config.sections():
            if section not in config:
                config.add_section(section)

    @staticmethod
    def __load_environment_variables(config: configparser.ConfigParser)->None:
        env_config = configparser.ConfigParser()
        env_config.optionxform = str # type: ignore
        custom_env_file = ConfigService.config_path / "custom-environment-variables.ini"

        if custom_env_file.exists():
            env_config.read(custom_env_file)

        for section in env_config.sections():
            if section not in config:
                config.add_section(section)
            for key, value in env_config[section].items():
                print("key",key)
                env_var_value = os.environ.get(key)
                if env_var_value is not None:
                    config[section][key] = env_var_value
                elif not config.has_option(section, key):
                    config[section][key] = ""
    
    @staticmethod
    def get_value(*, key: str, section: str = 'DEFAULT') -> str:
        try:
            value = ConfigService._config.get(section, key)
            return value 
        except (configparser.NoOptionError, configparser.NoSectionError) as exc:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY) from exc

    @staticmethod
    def has_value(*, key: str, section: str = 'DEFAULT') -> bool:
        if ConfigService._config.has_option(section, key):
            value = ConfigService._config.get(section, key)
            return bool(value)
        return False
    