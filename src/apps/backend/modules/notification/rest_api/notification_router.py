from flask import Blueprint

from modules.notification.rest_api.notification_view import NotificationView


class NotificationRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/notifications", view_func=NotificationView.as_view("notification_view"))
        return blueprint
