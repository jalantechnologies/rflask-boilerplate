from flask import Blueprint

from modules.notification.rest_api.notification_view import NotificationView


class NotificationRouter:
    """Routes HTTP requests to the appropriate notification view handlers"""

    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        """
        Registers notification endpoints with the provided blueprint

        Args:
            blueprint: Flask blueprint to register routes with

        Returns:
            The updated blueprint with notification routes
        """
        blueprint.add_url_rule("/notifications", view_func=NotificationView.as_view("notification_view"))
        return blueprint
