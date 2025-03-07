from modules.application.types import BaseWorker, WorkerPriority
from modules.logger.logger import Logger
from workers.worker_registry import register_worker


@register_worker
class TestDefaultWorker(BaseWorker):
    """
    A simple test application to demonstrate the default-priority application.
    """

    async def run(self, message: str) -> None:
        Logger.info(message=f"Message from TestDefaultWorker: {message}")


@register_worker
class TestCriticalWorker(BaseWorker):
    """
    A simple test application to demonstrate a critical-priority application.
    """

    priority: WorkerPriority = WorkerPriority.CRITICAL

    async def run(self, x: int, y: int) -> None:
        Logger.info(message=f"Message from TestCriticalWorker: {x + y}")
