from logging.handlers import SysLogHandler
import logging 
from modules.logger.internal.base_logger import BaseLogger
from modules.config.config_service import ConfigService
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding


class DatadogLogger(BaseLogger):
    def __init__(self):
        self.config = Configuration()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)


    def critical(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        response = apiInstance.submit_log(message)
        self.logger.critical(msg=message)

    def debug(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        response = apiInstance.submit_log(message)
        self.logger.debug(msg=message)

    def error(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        response = apiInstance.submit_log(message)
        self.logger.error(msg=message)

    def info(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        response = apiInstance.submit_log(message)
        self.logger.info(msg=message)

    def warn(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        response = apiInstance.submit_log(message)
        self.logger.warning(msg=message)