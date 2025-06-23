# src/apps/backend/modules/notification/rest_api/email_router.py
from flask import Blueprint

from modules.notification.rest_api.email_view import EmailView


class EmailRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        """
        Create email routes

        Routes:
        - POST /emails - Send emails (single/multiple recipients)
        """
        blueprint.add_url_rule("/emails", view_func=EmailView.as_view("email_view"), methods=["POST"])

        return blueprint
