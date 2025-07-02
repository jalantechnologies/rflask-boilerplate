from typing import Optional

from modules.account.types import NotificationPreferences
from modules.notification.email_service import EmailService
from modules.notification.sms_service import SMSService
from modules.notification.types import SendEmailParams, SendSMSParams


class NotificationService:

    @staticmethod
    def send_email(*, params: SendEmailParams) -> None:
        return EmailService.send_email(params=params)

    @staticmethod
    def send_email_with_preferences(
        *, params: SendEmailParams, preferences: Optional[NotificationPreferences] = None
    ) -> None:
        return EmailService.send_email_with_preferences(params=params, preferences=preferences)

    @staticmethod
    def send_sms(*, params: SendSMSParams) -> None:
        return SMSService.send_sms(params=params)

    @staticmethod
    def send_sms_with_preferences(
        *, params: SendSMSParams, preferences: Optional[NotificationPreferences] = None
    ) -> None:
        return SMSService.send_sms_with_preferences(params=params, preferences=preferences)
