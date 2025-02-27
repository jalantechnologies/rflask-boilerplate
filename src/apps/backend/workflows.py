import asyncio
from typing import Callable, Type

from dotenv import load_dotenv
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

with workflow.unsafe.imports_passed_through():
    from modules.config.config_manager import ConfigManager
    from modules.config.config_service import ConfigService
    from modules.logger.logger import Logger
    from modules.logger.logger_manager import LoggerManager

# Global registry for workflows
WORKFLOW_MAP = {}


def register_temporal_workflow() -> Callable:
    """
    Decorator to register a Temporal workflow with additional metadata.
    """

    def decorator(cls: Type) -> Callable:
        cls = workflow.defn(cls)  # Wrap the class as a Temporal workflow.

        # Register the workflow in the global map.
        WORKFLOW_MAP[cls.__name__] = cls

        return cls

    return decorator


# Just for demonstration; in practice this would be done inside a module
@register_temporal_workflow()
class AddWorkflow:
    @workflow.run
    async def run(self, x: int, y: int) -> int:
        return x + y


# Just for demonstration; in practice this would be done inside a module
@register_temporal_workflow()
class BuildUserFeedWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> dict:
        # Add logic as needed
        return {"user_id": user_id, "feed": []}


async def main() -> None:
    load_dotenv()

    # Mount configuration and logger
    ConfigManager.mount_config()
    LoggerManager.mount_logger()

    temporal_server = ConfigService.get_string("TEMPORAL_SERVER_ADDRESS")
    client = await Client.connect(temporal_server)

    default_queue = ConfigService.get_string("TEMPORAL_DEFAULT_TASK_QUEUE")
    high_priority_queue = ConfigService.get_string("TEMPORAL_HIGH_PRIORITY_TASK_QUEUE")

    Logger.info(message=f"Starting workers on queues: Default='{default_queue}', Priority='{high_priority_queue}'")

    # Create two worker instances, one for each queue
    worker_default = Worker(client, task_queue=default_queue, workflows=list(WORKFLOW_MAP.values()))
    worker_high_priority = Worker(client, task_queue=high_priority_queue, workflows=list(WORKFLOW_MAP.values()))

    # Run both workers concurrently
    await asyncio.gather(worker_default.run(), worker_high_priority.run())


if __name__ == "__main__":
    asyncio.run(main())
