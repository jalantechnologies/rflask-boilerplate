from typing import Optional

from modules.account.account_service import AccountService
from modules.logger.logger import Logger
from modules.notification.email_service import EmailService
from modules.notification.sms_service import SMSService
from modules.notification.types import SendEmailParams, SendSMSParams


class NotificationService:

    @staticmethod
    def send_email(*, params: SendEmailParams, account_id: Optional[str] = None) -> None:
        if account_id:
            try:
                preferences = AccountService.get_notification_preferences(account_id=account_id)
                if not preferences.email_enabled:
                    Logger.info(
                        message=f"Email notification skipped: disabled by user preferences for account {account_id}"
                    )
                    return
            except Exception as e:
                Logger.error(message=f"Error checking notification preferences: {str(e)}")

        return EmailService.send_email(params=params)

    @staticmethod
    def send_sms(*, params: SendSMSParams, account_id: Optional[str] = None) -> None:
        if account_id:
            try:
                preferences = AccountService.get_notification_preferences(account_id=account_id)
                if not preferences.sms_enabled:
                    Logger.info(
                        message=f"SMS notification skipped: disabled by user preferences for account {account_id}"
                    )
                    return
            except Exception as e:
                Logger.error(message=f"Error checking notification preferences: {str(e)}")

        return SMSService.send_sms(params=params)
