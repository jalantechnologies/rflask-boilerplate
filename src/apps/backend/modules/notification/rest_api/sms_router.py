from flask import Blueprint

from modules.notification.rest_api.sms_view import SMSView


class SMSRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/sms", view_func=SMSView.as_view("sms_view"), methods=["POST"])

        return blueprint
