from modules.error.custom_errors import AppError
from modules.worker.types import WorkerErrorCode


class WorkflowIdNotFoundError(AppError):
    def __init__(self, workflow_id: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKFLOW_WITH_ID_NOT_FOUND,
            http_status_code=404,
            message=f"Could not find a workflow with id: {workflow_id}. Please verify and try again.",
        )


class WorkflowNameNotFoundError(AppError):
    def __init__(self, workflow_name: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKFLOW_WITH_NAME_NOT_FOUND,
            http_status_code=404,
            message=f"Could not find a workflow with name: {workflow_name}. Please verify and try again.",
        )


class WorkflowStartError(AppError):
    def __init__(self, workflow_name: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKFLOW_START_ERROR,
            http_status_code=500,
            message=f"Could not start workflow with name: {workflow_name}. Please verify and try again.",
        )
