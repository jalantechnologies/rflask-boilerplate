import os
from logging import StreamHandler
from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api import logs_api
from datadog_api_client.v2.models import HTTPLog,HTTPLogItem
from logging import LogRecord

class DDHandler(StreamHandler):
    def __init__(self,configuration: Configuration,service_name: str,ddsource: str) -> None:
        StreamHandler.__init__(self)
        self.config = configuration
        self.service_name = service_name
        self.ddsource = ddsource
    
    def emit(self,record: LogRecord) -> None:
        msg = self.format(record)

        api_client = ApiClient(self.config)
        api_instance = logs_api.LogsApi(api_client)
        body = HTTPLog(
            [
                HTTPLogItem(
                    ddsource = self.ddsource,
                    ddtags = f"env : {os.environ.get('APP_NAME')}",
                    message = msg,
                    service = self.service_name
                )
            ]
        )

        api_instance.submit_log(body)