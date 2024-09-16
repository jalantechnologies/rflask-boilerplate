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
                messaging_service_sid=ConfigService.get_twilio_config(key="messaging_service_sid"),
                body=params.message_body,
            )

        except TwilioException as err:
            raise ServiceError(err)

    @staticmethod
    def get_client() -> Client:
        if not TwilioService.__client:
            account_sid = ConfigService.get_twilio_config(key="account_sid")
            auth_token = ConfigService.get_twilio_config(key="auth_token")

            # Initialize the Twilio client
            TwilioService.__client = Client(account_sid, auth_token)

        return TwilioService.__client
