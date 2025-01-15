from logging.handlers import SysLogHandler
import logging 
from modules.logger.internal.base_logger import BaseLogger
from modules.config.config_service import ConfigService
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from modules.logger.internal.loggerBody import loggerBody


class DatadogLogger(BaseLogger):
    def __init__(self):
        self.dgConfig = ConfigService.get_datadog_config()
        self.config = Configuration()
        self.config.api_key["apiKeyAuth"] = self.dgConfig[0]
        self.config.api_key["appKeyAuth"] = self.dgConfig[1]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        


    def critical(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = loggerBody.makeLog(message,self.dgConfig[2],"CRITICAL")
        response = apiInstance.submit_log(body)
        self.logger.critical(message)

    def debug(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = loggerBody.makeLog(message,self.dgConfig[2],"DEBUG")
        response = apiInstance.submit_log(body)
        self.logger.debug(message)

    def error(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = loggerBody.makeLog(message,self.dgConfig[2],"ERROR")
        response = apiInstance.submit_log(body)
        self.logger.error(message)

    def info(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = loggerBody.makeLog(message,self.dgConfig[2],"INFO")
        response = apiInstance.submit_log(body)
        self.logger.info(message)

    def warn(self, *, message: str) -> None:
        api_client = ApiClient(self.config)
        apiInstance = LogsApi(api_client)
        body = loggerBody.makeLog(message,self.dgConfig[2],"WARN")
        response = apiInstance.submit_log(body)
        self.logger.warning(message)