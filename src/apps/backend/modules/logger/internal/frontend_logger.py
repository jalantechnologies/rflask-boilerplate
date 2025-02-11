import logging

from modules.logger.internal.datadog_handler import DatadogHandler


class FrontendLogger:
    def __init__(self, error_name: str, error_message: str, error_info: str):
        self.error_name = error_name
        self.error_message = error_message
        self.error_info = error_info
        self.logger = logging.getLogger(__name__)
        self.handler = DatadogHandler("react")
        self.logger.addHandler(self.handler)
        self.log_format = "%(asctime)s - " + f"{self.error_name} - {self.error_message} - {self.error_info}"
        self.send_logs()

    def send_logs(self) -> None:
        self.logger.error(self.log_format)
