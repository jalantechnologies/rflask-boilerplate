import requests

from modules.application.types import BaseWorker
from modules.logger.logger import Logger


class HealthCheckWorker(BaseWorker):
    async def run(self) -> None:
        try:
            res = requests.get("http://localhost:8080/api/")

            if res.status_code == 200:
                Logger.info(message="Backend is healthy")

            else:
                Logger.error(message="Backend is unhealthy")

        except Exception as e:
            Logger.error(message=f"Backend is unhealthy: {e}")
