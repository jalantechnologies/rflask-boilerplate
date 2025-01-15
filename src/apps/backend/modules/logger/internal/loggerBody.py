from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
import os 
from time import asctime

class loggerBody:
    @staticmethod
    def makeLog(message,app_name,level):
        env = os.environ.get("APP_ENV")
        body = HTTPLog[
            HTTPLogItem(
                env=env,
                dateTime="%(asctime)",
                time = asctime(),
                app_name = app_name,
                message = message,
                level = level
            )
        ]
        return body 