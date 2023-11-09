import os
import yaml

from typing import Any

from modules.common.file_manager import FileManager


class ConfigManager:
  config: dict[str, Any] = {}

  @staticmethod
  def mount_config() -> None:
    ConfigManager.__load_secrets_map()
    ConfigManager.__load_default_config()
    ConfigManager.__load_env_config()

  @staticmethod
  def __load_default_config() -> None:
    try:
      default_config_file = "../../../config/default.yml"
      with FileManager(default_config_file, 'r') as file:
        default_config = yaml.safe_load(file)
        ConfigManager.config = {**ConfigManager.config, **default_config}
    except FileNotFoundError:
      ...

  @staticmethod
  def __load_env_config() -> None:
    try:
      app_env = os.environ.get('APP_ENV')
      env_config_file = f"../../../config/{app_env}.yml"
      with FileManager(env_config_file, 'r') as file:
        env_config = yaml.safe_load(file)
        ConfigManager.config = {**ConfigManager.config, **env_config}
    except FileNotFoundError:
      ...

  @staticmethod
  def __load_secrets_map() -> None:
    try:
      secrets_config_file = "../../../config/custom-environment-variables.yml"
      secrets_config_mp: dict[str, Any]
      with FileManager(secrets_config_file, 'r') as file:
        secrets_config_mp = yaml.safe_load(file)
        ConfigManager.__load_secrets_value_from_os_envs(secrets_config_mp)
        ConfigManager.config = {**ConfigManager.config, **secrets_config_mp}
    except FileNotFoundError:
      ...

  @staticmethod
  def __load_secrets_value_from_os_envs(secrets_config_mp: dict[str, Any]) -> None:
    for key, value in secrets_config_mp.items():
      if isinstance(value, str):
        secrets_config_mp[key] = os.environ.get(secrets_config_mp[key])

      if isinstance(value, dict):
        ConfigManager.__load_secrets_value_from_os_envs(value)
