from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.sms_notification.internal.twilio_service import TwilioService
from modules.sms_notification.types import SendSMSParams, SMSResponse


class SMSNotificationService:
    """
    Service for sending SMS notifications using Twilio

    This service provides a layer of abstraction over the Twilio service,
    allowing for configuration options like enabling/disabling SMS functionality
    and potentially supporting multiple SMS providers in the future.
    """

    @staticmethod
    def send_sms(*, params: SendSMSParams) -> SMSResponse:
        """
        Send an SMS notification

        Args:
            params: Parameters for sending the SMS

        Returns:
            SMSResponse object with success status and message details
        """
        is_sms_enabled = ConfigService[bool].get_value(key="sms.enabled", default=False)

        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send message to {params.recipient_phone}")
            return SMSResponse(success=False, error_message="SMS functionality is disabled", details={"disabled": True})

        return TwilioService.send_sms(params)
