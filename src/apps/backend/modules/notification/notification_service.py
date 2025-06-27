from typing import Optional

from modules.account.account_service import AccountService
from modules.account.types import AccountSearchByIdParams
from modules.logger.logger import Logger
from modules.notification.email_service import EmailService
from modules.notification.sms_service import SMSService
from modules.notification.types import SendEmailParams, SendSMSParams


class NotificationService:

    @staticmethod
    def send_email(*, params: SendEmailParams, account_id: Optional[str] = None) -> None:
        if account_id:
            try:
                account = AccountService.get_account_by_id(params=AccountSearchByIdParams(id=account_id))
                if not account.notification_preferences or not account.notification_preferences.email_enabled:
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
                account = AccountService.get_account_by_id(params=AccountSearchByIdParams(id=account_id))
                if not account.notification_preferences or not account.notification_preferences.sms_enabled:
                    Logger.info(
                        message=f"SMS notification skipped: disabled by user preferences for account {account_id}"
                    )
                    return
            except Exception as e:
                Logger.error(message=f"Error checking notification preferences: {str(e)}")

        return SMSService.send_sms(params=params)

    @staticmethod
    def send_push_notification(*, message: str, account_id: str) -> None:
        """
        Placeholder for push notification functionality.
        Will be implemented in the future.
        """
        try:
            account = AccountService.get_account_by_id(params=AccountSearchByIdParams(id=account_id))
            if not account.notification_preferences or not account.notification_preferences.push_enabled:
                Logger.info(message=f"Push notification skipped: disabled by user preferences for account {account_id}")
                return

            Logger.info(message=f"Push notification would be sent to account {account_id}: {message}")
        except Exception as e:
            Logger.error(message=f"Error sending push notification: {str(e)}")
