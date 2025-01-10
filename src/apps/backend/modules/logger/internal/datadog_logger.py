import datadog
from modules.logger.internal.base_logger import BaseLogger
from modules.config.config_service import ConfigService

class DatadogLogger(BaseLogger):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
