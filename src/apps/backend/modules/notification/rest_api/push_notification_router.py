from flask import Blueprint

from modules.notification.rest_api.push_notification_view import PushNotificationView


class NotificationRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule(
            "/push-notification", view_func=PushNotificationView.as_view("push_notification_view"), methods=["POST"]
        )
        return blueprint
