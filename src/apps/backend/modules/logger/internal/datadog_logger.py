import logging
from modules.logger.internal.base_logger import BaseLogger
from modules.logger.internal.DDHandler import DDHandler


class DatadogLogger(BaseLogger):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.format = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
        self.formatter = logging.Formatter(
            self.format,
        )
        self.logger.setLevel(logging.DEBUG)

    def critical(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler('flask')
        handler.setLevel(logging.CRITICAL)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.critical(message)

    def debug(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler('flask')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.debug(message)

    def error(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler('flask')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.error(message)

    def info(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler('flask')
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.info(message)

    def warn(self, *, message: str) -> None:
        logger = logging.getLogger(__name__)
        handler = DDHandler('flask')
        handler.setLevel(logging.WARNING)
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        self.logger.warning(message)
