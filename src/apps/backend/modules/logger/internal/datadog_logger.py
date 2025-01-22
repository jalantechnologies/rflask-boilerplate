import logging
from modules.logger.internal.base_logger import BaseLogger
from modules.config.config_service import ConfigService
from datadog_api_client import Configuration
from modules.logger.internal.DDHandler import DDHandler


class DatadogLogger(BaseLogger):
    def __init__(self):
        self.ddConfig = ConfigService.get_datadog_config()
        self.config = Configuration()
        self.config.api_key["apiKeyAuth"] = self.ddConfig.api_key
        if (self.ddConfig.application_key is not None):
            self.config.api_key["appKeyAuth"] = self.ddConfig.application_key
        self.app_name = self.ddConfig.app_name
        self.logger = logging.getLogger(__name__)
        self.format = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
        self.formatter = logging.Formatter(
            self.format,
        )
        self.logger.setLevel(logging.INFO)

    def critical(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler(self.config,self.app_name,'Log-source')
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.critical(message)

    def debug(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler(self.config,self.app_name,'Log-source')
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.debug(message)

    def error(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler(self.config,self.app_name,'Log-source')
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.error(message)

    def info(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler(self.config,self.app_name,'Log-source')
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.info(message)

    def warn(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler(self.config,self.app_name,'Log-source')
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.warning(message)
