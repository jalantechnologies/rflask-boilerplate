from logging.handlers import SysLogHandler
import logging 
from modules.logger.internal.base_logger import BaseLogger
from modules.config.config_service import ConfigService
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.content_encoding import ContentEncoding


class DatadogLogger(BaseLogger):
    def __init__(self):
        self.config = Configuration()
        self.config.api_key["apiKeyAuth"] = "YOUR_API_KEY"
        self.config.api_key["appKeyAuth"] = "YOUR_APPLICATION_KEY"

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)


    def critical(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = HTTPLog(message)
        response = apiInstance.submit_log(message)
        self.logger.critical(msg=body)

    def debug(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = HTTPLog(message)
        response = apiInstance.submit_log(message)
        self.logger.debug(msg=body)

    def error(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = HTTPLog(message)
        response = apiInstance.submit_log(message)
        self.logger.error(msg=body)

    def info(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = HTTPLog(message)
        response = apiInstance.submit_log(message)
        self.logger.info(msg=body)

    def warn(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = HTTPLog(message)
        response = apiInstance.submit_log(message)
        self.logger.warning(msg=body)