import asyncio

from dotenv import load_dotenv
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

from modules.workflow.types import WorkflowPriority
from workflows.workflow_registry import WORKFLOW_MAP

with workflow.unsafe.imports_passed_through():
    from modules.config.config_manager import ConfigManager
    from modules.config.config_service import ConfigService
    from modules.logger.logger import Logger
    from modules.logger.logger_manager import LoggerManager


async def main() -> None:
    load_dotenv()

    # Mount configuration and logger
    ConfigManager.mount_config()
    LoggerManager.mount_logger()

    temporal_server = ConfigService.get_string("TEMPORAL_SERVER_ADDRESS")
    client = await Client.connect(temporal_server)

    # Create workers for each priority level
    workflows_default = [wf["class"] for wf in WORKFLOW_MAP.values() if wf["priority"] == WorkflowPriority.DEFAULT]
    workflows_critical = [wf["class"] for wf in WORKFLOW_MAP.values() if wf["priority"] == WorkflowPriority.CRITICAL]
    worker_default = Worker(client, task_queue=WorkflowPriority.DEFAULT.value, workflows=workflows_default)
    worker_critical = Worker(client, task_queue=WorkflowPriority.CRITICAL.value, workflows=workflows_critical)

    Logger.info(
        message=f"Starting workers on queues: Default='{WorkflowPriority.DEFAULT.value}', Critical='{WorkflowPriority.CRITICAL.value}'"
    )

    # Run both workers concurrently
    await asyncio.gather(worker_default.run(), worker_critical.run())


if __name__ == "__main__":
    asyncio.run(main())
