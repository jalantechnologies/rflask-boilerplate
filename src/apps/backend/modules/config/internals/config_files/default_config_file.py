from typing import Any

from modules.config.internals.config_utils import ConfigUtil
from modules.config.types import Config

class DefaultConfig:

    FILENAME: str = "default.yml"

    @staticmethod
    def load() -> Config:
        default_config_dict = ConfigUtil.read_yml_from_config_dir(DefaultConfig.FILENAME)
        return Config(default_config_dict)
