from modules.common.dict_util import DictUtil
from modules.config.config_manager import ConfigManager
from modules.config.types import PapertrailConfig


class ConfigService:
    @staticmethod
    def get_string(key: str) -> str:
        return DictUtil.required_get_str(input_dict=ConfigManager.config, key=key)

    @staticmethod
    def get_bool(key: str) -> bool:
        return DictUtil.required_get_bool(input_dict=ConfigManager.config, key=key)

    @staticmethod
    def get_db_uri() -> str:
        return DictUtil.required_get_str(input_dict=ConfigManager.config, key="MONGODB_URI")

    @staticmethod
    def get_logger_transports() -> tuple:
        return DictUtil.required_get_tuple(input_dict=ConfigManager.config, key="LOGGER_TRANSPORTS")

    @staticmethod
    def get_papertrail_config() -> PapertrailConfig:
        return PapertrailConfig(
            host=DictUtil.required_get_str(input_dict=ConfigManager.config, key="PAPERTRAIL_HOST"),
            port=int(DictUtil.required_get_str(input_dict=ConfigManager.config, key="PAPERTRAIL_PORT")),
        )

    @staticmethod
    def get_accounts_config() -> dict:
        return DictUtil.required_get_dict(input_dict=ConfigManager.config, key="ACCOUNTS")

    @staticmethod
    def get_token_signing_key() -> str:
        return DictUtil.required_get_str(input_dict=ConfigService.get_accounts_config(), key="token_signing_key")

    @staticmethod
    def get_token_expiry_days() -> int:
        return DictUtil.required_get_int(input_dict=ConfigService.get_accounts_config(), key="token_expiry_days")

    @staticmethod
    def get_web_app_host() -> str:
        return DictUtil.required_get_str(input_dict=ConfigManager.config, key="WEB_APP_HOST")

    @staticmethod
    def get_sendgrid_api_key() -> str:
        return str(DictUtil.required_get_dict(input_dict=ConfigManager.config, key="SENDGRID")["api_key"])

    @staticmethod
    def get_mailer_config(key: str) -> str:
        return str(DictUtil.required_get_dict(input_dict=ConfigManager.config, key="MAILER")[key])

    @staticmethod
    def get_password_reset_token() -> dict:
        return DictUtil.required_get_dict(input_dict=ConfigManager.config, key="PASSWORD_RESET_TOKEN")
