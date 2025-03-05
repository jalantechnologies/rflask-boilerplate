from modules.error.custom_errors import AppError
from modules.workflow.types import WorkflowErrorCode


class WorkflowClientConnectionError(AppError):
    def __init__(self, server_address: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_CLIENT_CONNECTION_ERROR,
            http_status_code=500,
            message=f"Failed to connect to Temporal server. "
            f"Verify that the temporal server is running at {server_address} and try again.",
        )


class WorkflowIdNotFoundError(AppError):
    def __init__(self, workflow_id: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_WITH_ID_NOT_FOUND,
            http_status_code=404,
            message=f"Could not find a workflow with id: {workflow_id}. Please verify and try again.",
        )


class WorkflowNameNotFoundError(AppError):
    def __init__(self, workflow_name: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_WITH_NAME_NOT_FOUND,
            http_status_code=404,
            message=f"Could not find a workflow with name: {workflow_name}. Please verify and try again.",
        )


class WorkflowStartError(AppError):
    def __init__(self, workflow_name: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_START_ERROR,
            http_status_code=500,
            message=f"Could not start workflow with name: {workflow_name}. Please verify and try again.",
        )


class WorkflowAlreadyCompletedError(AppError):
    def __init__(self, workflow_id: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_ALREADY_COMPLETED,
            http_status_code=400,
            message=f"Workflow with id: {workflow_id} has already completed. Please verify and try again.",
        )


class WorkflowAlreadyCancelledError(AppError):
    def __init__(self, workflow_id: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_ALREADY_CANCELLED,
            http_status_code=400,
            message=f"Workflow with id: {workflow_id} has already been cancelled. Please verify and try again.",
        )


class WorkflowAlreadyTerminatedError(AppError):
    def __init__(self, workflow_id: str) -> None:
        super().__init__(
            code=WorkflowErrorCode.WORKFLOW_ALREADY_TERMINATED,
            http_status_code=400,
            message=f"Workflow with id: {workflow_id} has already been terminated. Please verify and try again.",
        )
