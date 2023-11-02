from modules.common.dict_util import DictUtil
from modules.config.config_manager import ConfigManager


class ConfigService:
  @staticmethod
  def get_db_uri() -> str:
    mongo_client = DictUtil.required_get_dict(input_dict=ConfigManager.config, key='mongoDb')
    return DictUtil.required_get_str(input_dict=mongo_client, key='uri')

  @staticmethod
  def get_db_name() -> str:
    mongo_client = DictUtil.required_get_dict(input_dict=ConfigManager.config, key='mongoDb')
    return DictUtil.required_get_str(input_dict=mongo_client, key='dbName')

  @staticmethod
  def get_logger_transports() -> list[str]:
    logger_config = DictUtil.required_get_dict(input_dict=ConfigManager.config, key='logger')
    return DictUtil.required_get_list(input_dict=logger_config, key='transports')
