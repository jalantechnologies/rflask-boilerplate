# src/apps/backend/modules/notification/rest_api/notification_rest_api_server.py
from flask import Blueprint

from modules.notification.rest_api.email_router import EmailRouter
from modules.notification.rest_api.fcm_router import FCMRouter
from modules.notification.rest_api.sms_router import SMSRouter


class NotificationRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        notification_api_blueprint = Blueprint("notification", __name__)

        EmailRouter.create_route(blueprint=notification_api_blueprint)

        SMSRouter.create_route(blueprint=notification_api_blueprint)

        FCMRouter.create_route(blueprint=notification_api_blueprint)

        return notification_api_blueprint
