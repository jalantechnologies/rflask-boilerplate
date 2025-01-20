from flask import Blueprint

from modules.documentation.rest_api.documentation_router import DocumentationRouter


class DocumentationRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        documentation_api_blueprint = Blueprint("documentation", __name__)
        return DocumentationRouter.create_route(blueprint=documentation_api_blueprint)
