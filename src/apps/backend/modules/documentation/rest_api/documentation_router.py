from flask import Blueprint

from modules.documentation.rest_api.documentation_view import DocumentationView


class DocumentationRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> None:
        blueprint.add_url_rule(
            "/get-documentation", view_func=DocumentationView.as_view("documentation_view"), methods=["GET"]
        )
        return blueprint
