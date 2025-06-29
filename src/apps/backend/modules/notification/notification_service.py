from typing import Optional

from modules.account.account_service import AccountService
from modules.account.types import AccountSearchByIdParams
from modules.logger.logger import Logger
from modules.notification.email_service import EmailService
from modules.notification.push_notification_service import PushNotificationService
from modules.notification.sms_service import SMSService
from modules.notification.types import PushNotificationParams, SendEmailParams, SendSMSParams


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
    def send_push_notification(*, params: PushNotificationParams, account_id: Optional[str] = None) -> Optional[str]:
        """
        Send a push notification using Firebase Cloud Messaging.

        Args:
            params: PushNotificationParams with notification details
            account_id: Optional account ID to check notification preferences

        Returns:
            str: The message ID from FCM or None if sending failed or skipped
        """
        if account_id:
            try:
                account = AccountService.get_account_by_id(params=AccountSearchByIdParams(id=account_id))
                if not account.notification_preferences or not account.notification_preferences.push_enabled:
                    Logger.info(
                        message=f"Push notification skipped: disabled by user preferences for account {account_id}"
                    )
                    return None
            except Exception as e:
                Logger.error(message=f"Error checking notification preferences: {str(e)}")

        return PushNotificationService.send_push_notification(params=params)
