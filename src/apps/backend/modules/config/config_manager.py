import os
import yaml

from typing import Any

from modules.common.file_manager import FileManager


class ConfigManager:
  config: dict[str, Any]

  @staticmethod
  def mount_config() -> None:
    app_env = os.environ.get('APP_ENV')

    default_config_file = "../../../config/default.yml"
    with FileManager(default_config_file, 'r') as file:
      default_config = yaml.safe_load(file)

    config_file = f"../../../config/{app_env}.yml"
    with FileManager(config_file, 'r') as file:
      config = yaml.safe_load(file)

    ConfigManager.config = {**default_config, **config}
