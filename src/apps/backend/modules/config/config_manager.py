import os
import yaml

from typing import Any

from modules.common.file_manager import FileManager


class ConfigManager:
  config: dict[str, Any] = {}
  config_path = "../../../config"

  @staticmethod
  def mount_config() -> None:
    ConfigManager.__load_custom_env_config()
    ConfigManager.__load_default_config()
    ConfigManager.__load_env_config()

  @staticmethod
  def __load_default_config() -> None:
    default_config_file = f"{ConfigManager.config_path}/default.yml"
    with FileManager(default_config_file, 'r') as file:
      default_config = yaml.safe_load(file)
      ConfigManager.config = {**ConfigManager.config, **default_config}

  @staticmethod
  def __load_env_config() -> None:
    filename = ConfigManager._get_filename_by_config_env()
    env_config_file = f"{ConfigManager.config_path}/{filename}.yml"
    with FileManager(env_config_file, 'r') as file:
      env_config = yaml.safe_load(file)
      ConfigManager.config = {**ConfigManager.config, **env_config}

  @staticmethod
  def __load_custom_env_config() -> None:
    secrets_config_file = f"{ConfigManager.config_path}/custom-environment-variables.yml"
    secrets_config_mp: dict[str, Any]
    with FileManager(secrets_config_file, 'r') as file:
      secrets_config_mp = yaml.safe_load(file)
      ConfigManager.__load_secrets_value_from_os_envs(secrets_config_mp)
      ConfigManager.config = {**ConfigManager.config, **secrets_config_mp}

  @staticmethod
  def __load_secrets_value_from_os_envs(secrets_config_mp: dict[str, Any]) -> None:
    for key, value in secrets_config_mp.items():
      if isinstance(value, str):
        secrets_config_mp[key] = os.environ.get(secrets_config_mp[key])

      if isinstance(value, dict):
        ConfigManager.__load_secrets_value_from_os_envs(value)

  @staticmethod
  def _get_filename_by_config_env() -> str:
    # if not NODE_ENV selected, default env will be development
    node_env = os.environ.get("NODE_ENV") if os.environ.get("NODE_ENV") is not None else os.environ.get("NODE_CONFIG_ENV")
    if node_env is None:
      node_env = "development"
    assert node_env is not None, "Invalid env, unable to populate config"
    node_env_instance = os.environ.get("NODE_APP_INSTANCE")
    return node_env if node_env_instance is None else f"{node_env}-{node_env_instance}"
