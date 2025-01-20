import json
import os

from modules.documentation.errors import DocumentationGenerationError
from modules.documentation.internal.constant import DOCUMENTATION_GENERATION_PROMPT
from modules.documentation.internal.document_generator_util import DocumentGeneratorUtil
from modules.documentation.types import (
    GetRoutesWithViewDetailsResponse,
    HttpRouteWithRootFolderPath,
    MarkdownDocumentation,
)
from modules.logger.logger import Logger
from modules.openai.openai_service import OpenAIService
from typing import List


class DocumentationService:
    flask_routes_list: List[HttpRouteWithRootFolderPath] = []

    @staticmethod
    def get_documentation() -> MarkdownDocumentation:
        # is_documentation_enabled = ConfigService.get_value("documentation.enabled")
        is_documentation_enabled = True

        if not is_documentation_enabled:
            return MarkdownDocumentation(markdown_documentation="")

        routes = DocumentGeneratorUtil.get_routes_with_view_details(
            params=GetRoutesWithViewDetailsResponse(flask_routes_list=DocumentationService.flask_routes_list)
        )

        prompt = f"{DOCUMENTATION_GENERATION_PROMPT}\n{json.dumps(routes, indent=2)}"

        try:
            markdown_documentation = OpenAIService.get_chat_completion_response(prompt)
        except Exception as e:
            error_message = f"Error fetching documentation from OpenAIService: {e}"
            Logger.error(error_message)
            raise DocumentationGenerationError(message=error_message)
            markdown_documentation = ""

        return MarkdownDocumentation(markdown_documentation=markdown_documentation)

    @staticmethod
    def generate_api_documentation() -> MarkdownDocumentation:
        documentation = DocumentationService.get_documentation()

        try:
            assets_path = os.path.join(os.getcwd(), "dist", "assets", "documentation")

            os.makedirs(assets_path, exist_ok=True)

            with open(os.path.join(assets_path, "index.json"), "w", encoding="utf8") as file:
                json.dump(documentation, file, indent=2)
        except Exception as error:
            Logger.error("Error generating and injecting documentation:", str(error))

        return documentation
