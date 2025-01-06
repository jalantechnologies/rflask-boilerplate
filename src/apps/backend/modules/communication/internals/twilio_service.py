from typing import Optional

from twilio.base.exceptions import TwilioException
from twilio.rest import Client

from modules.communication.errors import ServiceError
from modules.communication.internals.twilio_params import SMSParams
from modules.communication.types import SendSMSParams
from modules.config.config_service import ConfigService


class TwilioService:
    __client: Optional[Client] = None

    @staticmethod
    def send_sms(params: SendSMSParams) -> None:
        SMSParams.validate(params)

        try:
            client = TwilioService.get_client()

            # Send SMS
            client.messages.create(
                to=params.recipient_phone,
                messaging_service_sid=ConfigService.get_value(key="TWILIO_MESSAGING_SERVICE_SID",section="TWILIO",expected_type=str),
                body=params.message_body,
            )

        except TwilioException as err:
            raise ServiceError(err)

    @staticmethod
    def get_client() -> Client:
        if not TwilioService.__client:
            account_sid = ConfigService.get_value(key="TWILIO_ACCOUNT_SID",section="TWILIO",expected_type=str)
            auth_token = ConfigService.get_value(key="TWILIO_AUTH_TOKEN",section="TWILIO",expected_type=str)

            # Initialize the Twilio client
            TwilioService.__client = Client(account_sid, auth_token)

        return TwilioService.__client
