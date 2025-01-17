from modules.error.custom_errors import AppError
from modules.openai.types import OpenAIErrorCode


class ErrorGettingChatCompletionResponse(AppError):
    def __init__(self) -> None:
        super().__init__(
            message="There was an error getting the chat completion response from OpenAI, please try again later.",
            code=OpenAIErrorCode.ERROR_GETTING_CHAT_COMPLETION_RESPONSE,
            http_status_code=500,
        )
