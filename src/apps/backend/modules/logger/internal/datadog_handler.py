import os
from logging import StreamHandler
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.models import HTTPLog, HTTPLogItem
from modules.config.config_service import ConfigService
from logging import LogRecord


class DatadogHandler(StreamHandler):
    def __init__(self, ddsource: str) -> None:
        StreamHandler.__init__(self)
        self.ddsource = ddsource

    def emit(self, record: LogRecord) -> None:
        msg = self.format(record)
        datadog_api_key = ConfigService.get_value(key="API_KEY", section="DATADOG")
        datadog_host = ConfigService.get_value(key="SITE_NAME", section="DATADOG")
        data_app_name = ConfigService.get_value(key="APP_NAME", section="DATADOG")
        config = Configuration()
        config.api_key["apiKeyAuth"] = datadog_api_key
        config.server_variables["site"] = datadog_host
        config.debug = True
        with ApiClient(config) as api_client:
            api_instance = LogsApi(api_client)
            body = HTTPLog(
                [
                    HTTPLogItem(
                        ddsource=self.ddsource,
                        ddtags=f"env : {os.environ.get('APP_NAME')}",
                        hostname="",
                        message=msg,
                        service=data_app_name,
                    )
                ]
            )

            api_instance.submit_log(body)
