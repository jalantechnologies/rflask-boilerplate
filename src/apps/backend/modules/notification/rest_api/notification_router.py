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
        notification_view = NotificationView.as_view("notification_view")
        blueprint.add_url_rule("/notifications", view_func=notification_view, methods=["POST"])

        multiple_notification_view = NotificationView.as_view("multiple_notification_view")
        blueprint.add_url_rule("/notifications/multiple", view_func=multiple_notification_view, methods=["POST"])

        return blueprint
