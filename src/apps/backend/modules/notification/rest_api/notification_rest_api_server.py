# src/apps/backend/modules/notification/rest_api/notification_rest_api_server.py
from flask import Blueprint

from modules.notification.rest_api.email_router import EmailRouter


class NotificationRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        """
        Create notification API blueprint with all notification-related routes
        """
        notification_api_blueprint = Blueprint("notification", __name__)
        return EmailRouter.create_route(blueprint=notification_api_blueprint)
