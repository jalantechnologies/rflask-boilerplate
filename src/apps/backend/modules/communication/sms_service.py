from modules.communication.internals.twilio_service import TwilioService
from modules.communication.types import SendSMSParams
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger


class SMSService:
    @staticmethod
    def send_sms(*, params: SendSMSParams) -> None:
        is_sms_enabled = ConfigService.get_bool("SMS_ENABLED")

        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send message - {params.message_body}")
            return

        TwilioService.send_sms(params=params)
