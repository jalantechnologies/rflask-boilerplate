from modules.openai.rest_api.openai_adapter import OpenAIAdapter


class OpenAIService:
    @staticmethod
    def get_chat_completion_response(prompt: str) -> str:
        return OpenAIAdapter.get_chat_completion_response(prompt)
