from flask import Blueprint

from modules.notification.rest_api.email_router import EmailRouter


class NotificationRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        notification_api_blueprint = Blueprint("notification", __name__)
        return EmailRouter.create_route(blueprint=notification_api_blueprint)
