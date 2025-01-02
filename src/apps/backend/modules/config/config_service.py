import configparser
import os
from modules.error.custom_errors import MissingKeyError
from modules.common.types import ErrorCode
from modules.common.config_utils import ConfigUtils

class ConfigService:
    _config: configparser.ConfigParser = configparser.ConfigParser()
    config_path = ConfigUtils.get_parent_directory(__file__, 6) / "config"

    @staticmethod
    def load_config()->None:
        config = configparser.ConfigParser()
        config.optionxform = str # type: ignore
        default_config = ConfigService.config_path / "default.ini"
        app_env = os.environ.get('APP_ENV', "development")
        app_env_config = ConfigService.config_path / f"{app_env}.ini"
        config.read([default_config, app_env_config])
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
    def __load_environment_variables(config: configparser.ConfigParser)->None:
        custom_environment_file = ConfigService.config_path / "custom-environment-variables.ini"
        if not custom_environment_file.exists():
            return
        
        env_config = configparser.ConfigParser()
        env_config.optionxform = str # type: ignore
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
    def get_string(*, key: str, section: str = 'DEFAULT') -> str:
        try:
            value = ConfigService._config.get(section, key)
            return value 
        except (configparser.NoOptionError, configparser.NoSectionError) as exc:
            raise MissingKeyError(missing_key=key, error_code=ErrorCode.MISSING_KEY) from exc

    @staticmethod
    def get_int(*, key: str, section: str = 'DEFAULT') -> int:
        value = 0
        try:
            value = ConfigService._config.getint(section,key)
        except ValueError as e:
            print(f"Error setting JWT expiry: {e}")
        
        return value
        
        

    @staticmethod
    def get_boolean(*, key: str, section: str = 'DEFAULT') -> bool:
        value = False
        try:
            value = ConfigService._config.getboolean(section,key)
        except ValueError as e:
            print(f"Error setting JWT expiry: {e}")
        return value
    
    @staticmethod
    def has_value(*, key: str, section: str = 'DEFAULT') -> bool:
        if ConfigService._config.has_option(section, key):
            value = ConfigService._config.get(section, key)
            return bool(value)
        return False
    