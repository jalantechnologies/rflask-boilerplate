from modules.config.types import PapertrailConfig
from modules.common.dict_util import DictUtil
from modules.config.config_manager import ConfigManager


class ConfigService:
  @staticmethod
  def get_db_uri() -> str:
    mongo_client = DictUtil.required_get_dict(input_dict=ConfigManager.config, key='mongoDb')
    return DictUtil.required_get_str(input_dict=mongo_client, key='uri')

  @staticmethod
  def get_logger_transports() -> list[str]:
    logger_config = DictUtil.required_get_dict(input_dict=ConfigManager.config, key='logger')
    return DictUtil.required_get_list(input_dict=logger_config, key='transports')

  @staticmethod
  def get_papertrail_config() -> PapertrailConfig:
    papertrail_dict = DictUtil.required_get_dict(input_dict=ConfigManager.config, key='papertrail')
    return PapertrailConfig(
      host=DictUtil.required_get_str(input_dict=papertrail_dict, key='host'),
      port=DictUtil.required_get_int(input_dict=papertrail_dict, key='port')
    )
