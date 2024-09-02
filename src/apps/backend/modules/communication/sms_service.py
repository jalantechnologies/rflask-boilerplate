from dataclasses import asdict
from modules.account.types import PhoneNumber
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.communication.internals.twilio_service import TwilioService
from modules.communication.types import SendSMSParams


class SMSService:
    @staticmethod
    def send_sms(*, params: SendSMSParams) -> None:
        is_sms_enabled = ConfigService.get_bool("SMS_ENABLED")
        
        if (not is_sms_enabled):
            Logger.warn(message=f"SMS is disabled. Could not send message - {params.message_body}")
            return
        
        send_sms_params = SendSMSParams(
            message_body=params.message_body,
            recipient_phone=PhoneNumber(**asdict(params)['recipient_phone'])
        )
        TwilioService.send_sms(params=send_sms_params)
