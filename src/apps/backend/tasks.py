from celery import Celery
from dotenv import load_dotenv

from modules.config.config_manager import ConfigManager
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.logger.logger_manager import LoggerManager

load_dotenv()

# Mount deps
ConfigManager.mount_config()
LoggerManager.mount_logger()

celery = Celery(
    ConfigService.get_string("APP_NAME"),
    broker=ConfigService.get_string("CELERY_BROKER_URL"),
    backend=ConfigService.get_string("CELERY_BACKEND_URL"),
)


@celery.task
def example_task(x: int, y: int) -> int:
    Logger.info(message=f"Executing {example_task.__name__} with x={x}, y={y}")
    return x + y
