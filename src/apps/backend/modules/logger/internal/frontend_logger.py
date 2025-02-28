import logging

from modules.logger.internal.datadog_handler import DatadogHandler


class FrontendLogger:
    def __init__(self, error: dict) -> None:
        self.error = error
        self.send_logs()

    def dtype(self) -> bool:
        if type(self.error) == dict:
            return True
        else:
            return False

    def send_logs(self) -> None:
        logger = logging.getLogger(__name__)
        error_details = [self.error["error-name"], self.error["error-message"], self.error["error-info"]]
        message = " - ".join(error_details)
        format = "%(asctime)s - " + message
        formatter = logging.Formatter(format)
        handler = DatadogHandler("react")
        handler.setFormatter(self.formatter)
        logger.addHandler(self.handler)
        logger.error(message)
