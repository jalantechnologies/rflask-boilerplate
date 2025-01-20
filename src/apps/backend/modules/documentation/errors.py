from modules.documentation.types import DocumentationErrorCode
from modules.error.custom_errors import AppError


class DocumentationGenerationError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            message="Documentation generation failed with error: " + message,
            code=DocumentationErrorCode.ERROR_GENERATING_DOCUMENTATION,
            http_status_code=500,
        )


class ErrorReadingFile(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code=DocumentationErrorCode.ERROR_READING_FILE, http_status_code=500)
