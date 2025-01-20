from dataclasses import dataclass


@dataclass
class OpenAIErrorCode:
    ERROR_GETTING_CHAT_COMPLETION_RESPONSE: str = "OPENAI_ERR_01"
