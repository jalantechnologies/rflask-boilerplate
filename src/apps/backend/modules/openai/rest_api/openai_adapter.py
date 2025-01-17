import requests
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.openai.errors import ErrorGettingChatCompletionResponse


class OpenAIAdapter:
    API_URL = "https://api.openai.com/v1/chat/completions"
    API_KEY = ConfigService.get_openai_api_key()
    MODEL = "gpt-4o-mini"

    @staticmethod
    def get_chat_completion_response(prompt: str) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {OpenAIAdapter.API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": OpenAIAdapter.MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
            response = requests.post(OpenAIAdapter.API_URL, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as error:
            Logger.error(f"Error getting chat completion response from OpenAI: {error}")
            raise ErrorGettingChatCompletionResponse() from error
