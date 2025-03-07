from modules.application.types import BaseWorker, WorkerPriority
from modules.application.worker_registry import register_worker
from modules.logger.logger import Logger


@register_worker
class MockDefaultWorker(BaseWorker):
    """
    A simple mock worker to demonstrate the default-priority application.
    """

    async def run(self, message: str) -> None:
        Logger.info(message=f"Message from TestDefaultWorker: {message}")


@register_worker
class MockCriticalWorker(BaseWorker):
    """
    A simple mock worker to demonstrate a critical-priority application.
    """

    priority: WorkerPriority = WorkerPriority.CRITICAL

    async def run(self, x: int, y: int) -> None:
        Logger.info(message=f"Message from TestCriticalWorker: {x + y}")
