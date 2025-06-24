# src/apps/backend/modules/notification/rest_api/fcm_router.py
from flask import Blueprint

from modules.notification.rest_api.fcm_view import FCMView


class FCMRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        # Route for single token notification
        blueprint.add_url_rule("/notification/token", view_func=FCMView.as_view("fcm_token_view"), methods=["POST"])

        # Route for multiple tokens notification
        blueprint.add_url_rule("/notification/tokens", view_func=FCMView.as_view("fcm_tokens_view"), methods=["POST"])

        # Route for sending to all users
        blueprint.add_url_rule("/notification/all", view_func=FCMView.as_view("fcm_all_view"), methods=["POST"])

        return blueprint
