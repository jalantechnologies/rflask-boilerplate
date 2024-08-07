from typing import List, Optional

from modules.communication.types import CommunicationErrorCode, ValidationFailure
from modules.error.custom_errors import AppError


class ValidationError(AppError):
    failures: List[ValidationFailure]

    def __init__(self, msg: str, failures: Optional[List[ValidationFailure]] = None) -> None:
        if failures is None:
            failures = []
        self.code = CommunicationErrorCode.VALIDATION_ERROR
        super().__init__(message=msg, code=self.code)
        self.failures = failures
        self.https_code = 400


class ServiceError(AppError):

    def __init__(self, err: Exception) -> None:
        super().__init__(message=err.args[0], code=CommunicationErrorCode.SERVICE_ERROR)
        self.code = CommunicationErrorCode.SERVICE_ERROR
        self.stack = getattr(err, "stack", None)
        self.http_status_code = 503
