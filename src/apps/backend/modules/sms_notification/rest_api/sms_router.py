from flask import Blueprint

from modules.sms_notification.rest_api.sms_view import SMSNotificationView


class SMSNotificationRouter:
    """Routes HTTP requests to the appropriate SMS notification view handlers"""

    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        """
        Registers SMS notification endpoints with the provided blueprint

        Args:
            blueprint: Flask blueprint to add routes to

        Returns:
            Updated blueprint with SMS notification routes
        """
        sms_view = SMSNotificationView.as_view("sms_view")
        blueprint.add_url_rule("/sms", view_func=sms_view, methods=["POST"])

        return blueprint
