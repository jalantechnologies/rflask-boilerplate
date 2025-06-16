from flask import Blueprint

from modules.email_notification.rest_api.email_view import EmailView


class EmailRouter:
    """Routes HTTP requests to the appropriate email view handlers"""

    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        """
        Registers email notification endpoints with the provided blueprint

        Args:
            blueprint: Flask blueprint to add routes to

        Returns:
            Updated blueprint with email routes
        """
        email_view = EmailView.as_view("email_view")
        blueprint.add_url_rule("/emails", view_func=email_view, methods=["POST"])

        template_email_view = EmailView.as_view("template_email_view")
        blueprint.add_url_rule("/emails/template", view_func=template_email_view, methods=["POST"])

        return blueprint
