from dataclasses import dataclass

from modules.error.custom_errors import AppError


@dataclass(frozen=True)
class WorkerErrorCode:
    WORKER_CLIENT_CONNECTION_ERROR: str = "WORKER_ERR_01"
    WORKER_CLASS_INVALID: str = "WORKER_ERR_02"
    WORKER_WITH_ID_NOT_FOUND: str = "WORKER_ERR_03"
    WORKER_START_ERROR: str = "WORKER_ERR_04"
    WORKER_ALREADY_COMPLETED: str = "WORKER_ERR_05"
    WORKER_ALREADY_CANCELLED: str = "WORKER_ERR_06"
    WORKER_ALREADY_TERMINATED: str = "WORKER_ERR_07"


class WorkerClientConnectionError(AppError):
    def __init__(self, server_address: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKER_CLIENT_CONNECTION_ERROR,
            http_status_code=500,
            message=f"Failed to connect to Temporal server. "
            f"Verify that the temporal server is running at {server_address} and try again.",
        )


class WorkerIdNotFoundError(AppError):
    def __init__(self, worker_id: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKER_WITH_ID_NOT_FOUND,
            http_status_code=404,
            message=f"Worker with given id: {worker_id} not found. " f"Verify the ID of the worker and try again.",
        )


class WorkerStartError(AppError):
    def __init__(self, worker_name: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKER_START_ERROR,
            http_status_code=500,
            message=f"Could not start worker with name: {worker_name}. "
            f"Check temporal server logs for more information.",
        )


class WorkerAlreadyCompletedError(AppError):
    def __init__(self, worker_id: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKER_ALREADY_COMPLETED,
            http_status_code=400,
            message=f"Worker with id: {worker_id} has already completed running. "
            f"Verify the worker ID and try again.",
        )


class WorkerAlreadyCancelledError(AppError):
    def __init__(self, worker_id: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKER_ALREADY_CANCELLED,
            http_status_code=400,
            message=f"Worker with id: {worker_id} has already been cancelled." f"Verify the worker ID and try again.",
        )


class WorkerAlreadyTerminatedError(AppError):
    def __init__(self, worker_id: str) -> None:
        super().__init__(
            code=WorkerErrorCode.WORKER_ALREADY_TERMINATED,
            http_status_code=400,
            message=f"Worker with id: {worker_id} has already been terminated. " f"Verify the worker ID and try again.",
        )
