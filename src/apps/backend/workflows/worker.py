import asyncio

from dotenv import load_dotenv
from temporalio import workflow
from temporalio.client import Client
from temporalio.service import RetryConfig
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

    server_address = ConfigService.get_string("TEMPORAL_SERVER_ADDRESS")

    try:
        client = await Client.connect(server_address, retry_config=RetryConfig(max_retries=3))
    except RuntimeError:
        Logger.error(message=f"Failed to connect to Temporal server at {server_address}. Exiting...")
        return

    worker_coros = []

    # Iterate over each priority level defined in WorkflowPriority enum
    for priority in WorkflowPriority:
        # Filter workflows for the current priority
        workflows_for_priority = [_cls for _cls, _priority in WORKFLOW_MAP.items() if _priority == priority]

        # Only create a worker if there are workflows for that priority
        if workflows_for_priority:
            task_queue = priority.value
            Logger.info(
                message=f"Starting worker on queue '{task_queue}' for priority '{priority.name}' "
                f"with {len(workflows_for_priority)} workflow(s)."
            )
            worker = Worker(client, task_queue=task_queue, workflows=workflows_for_priority)
            worker_coros.append(worker.run())

    if worker_coros:
        await asyncio.gather(*worker_coros)
    else:
        Logger.error(message="No workflows registered for any priority.")


if __name__ == "__main__":
    asyncio.run(main())
