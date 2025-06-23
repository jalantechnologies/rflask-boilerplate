from typing import List, Optional

from modules.application.errors import AppError
from modules.notification.types import CommunicationErrorCode, ValidationFailure


class ValidationError(AppError):
    failures: List[ValidationFailure]

    def __init__(self, msg: str, failures: Optional[List[ValidationFailure]] = None) -> None:
        if failures is None:
            failures = []
        self.code = CommunicationErrorCode.VALIDATION_ERROR
        super().__init__(message=msg, code=self.code)
        self.failures = failures
        self.http_code = 400


class ServiceError(AppError):

    def __init__(self, err: Exception) -> None:
        if hasattr(err, "args") and len(err.args) > 0:
            if len(err.args) == 1:
                message = str(err.args[0])
            else:
                message = " | ".join(str(arg) for arg in err.args)
        else:
            message = str(err)

        super().__init__(message=message, code=CommunicationErrorCode.SERVICE_ERROR)
        self.code = CommunicationErrorCode.SERVICE_ERROR
        self.stack = getattr(err, "stack", None)
        self.http_status_code = 503
