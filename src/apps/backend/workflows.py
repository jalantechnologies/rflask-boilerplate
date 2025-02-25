import asyncio
from datetime import timedelta

from dotenv import load_dotenv
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from modules.config.config_manager import ConfigManager
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.logger.logger_manager import LoggerManager

WORKFLOW_MAP = {"add": "AddWorkflow"}


@activity.defn
async def add_activity(x: int, y: int) -> int:
    return x + y


@workflow.defn
class AddWorkflow:
    @workflow.run
    async def run(self, x: int, y: int) -> int:
        # Call the activity with a timeout.
        result = await workflow.execute_activity(
            activity=add_activity, args=(x, y), start_to_close_timeout=timedelta(seconds=10)
        )
        return result


async def main() -> None:
    load_dotenv()

    # Mount deps
    ConfigManager.mount_config()
    LoggerManager.mount_logger()

    client = await Client.connect(ConfigService.get_string("TEMPORAL_SERVER_ADDRESS"))
    task_queue = ConfigService.get_string("TEMPORAL_TASK_QUEUE")
    worker = Worker(client, task_queue=task_queue, workflows=[AddWorkflow], activities=[add_activity])
    Logger.info(message=f"Worker started. Listening on task queue '{task_queue}'...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
