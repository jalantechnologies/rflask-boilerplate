from modules.communication.types import CommunicationErrorCode, ValidationFailure
from modules.error.custom_errors import AppError


class ValidationError(AppError):
    code: CommunicationErrorCode
    failures: list[ValidationFailure]
    
    def __init__(self, msg: str, failures: list[ValidationFailure] = None) -> None:
        if failures is None:
            failures = []
        self.code = CommunicationErrorCode.VALIDATION_ERROR
        super().__init__(
            message=msg,
            code=self.code,
        )
        self.failures = failures
        self.https_code = 400
    
class ServiceError(AppError):
    code: CommunicationErrorCode
    
    def __init__(self, err: Exception):
        super().__init__(
            err.args[0],
        )
        self.code = CommunicationErrorCode.SERVICE_ERROR
        self.stack = err.stack
        self.http_status_code = 503
