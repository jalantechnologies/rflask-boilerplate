from typing import Any

from modules.config.internals.config_utils import ConfigUtil


class DefaultConfig:

    filename: str = "default.yml"

    @staticmethod
    def load() -> dict[str, Any]:
        return ConfigUtil.read_yml_from_config_dir(DefaultConfig.filename)
