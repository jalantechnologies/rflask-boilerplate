from typing import Optional

from twilio.base.exceptions import TwilioException
from twilio.rest import Client

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.sms_notification.errors import ServiceError, ValidationError
from modules.sms_notification.types import SendSMSParams, SMSResponse


class TwilioService:
    """Service for interacting with the Twilio API for SMS functionality"""

    __client: Optional[Client] = None

    @staticmethod
    def send_sms(params: SendSMSParams) -> SMSResponse:
        """
        Send an SMS using Twilio

        Args:
            params: Parameters for sending the SMS

        Returns:
            SMSResponse object with success status and message details

        Raises:
            ValidationError: If params validation fails
            ServiceError: If Twilio API call fails
        """
        try:
            TwilioService._validate_params(params)

            client = TwilioService.get_client()

            formatted_phone = f"{params.recipient_phone.country_code}{params.recipient_phone.phone_number}"

            message = client.messages.create(
                to=formatted_phone,
                messaging_service_sid=ConfigService[str].get_value(key="twilio.messaging_service_sid"),
                body=params.message_body,
            )

            Logger.info(message=f"SMS sent successfully to {formatted_phone}, SID: {message.sid}")

            return SMSResponse(
                success=True,
                message_sid=message.sid,
                details={"to": formatted_phone, "status": message.status, "date_created": str(message.date_created)},
            )

        except TwilioException as err:
            Logger.error(message=f"Twilio error: {str(err)}")
            raise ServiceError(err)
        except Exception as err:
            Logger.error(message=f"Unexpected error in Twilio service: {str(err)}")
            raise ServiceError(err)

    @staticmethod
    def get_client() -> Client:
        """
        Get or initialize the Twilio client

        Returns:
            Initialized Twilio client
        """
        if not TwilioService.__client:
            account_sid = ConfigService[str].get_value(key="twilio.account_sid")
            auth_token = ConfigService[str].get_value(key="twilio.auth_token")

            if not account_sid or not auth_token:
                raise ServiceError("Twilio credentials not configured properly")

            TwilioService.__client = Client(account_sid, auth_token)

        return TwilioService.__client

    @staticmethod
    def _validate_params(params: SendSMSParams) -> None:
        """
        Validate SMS parameters

        Args:
            params: Parameters to validate

        Raises:
            ValidationError: If validation fails
        """
        if not params.recipient_phone:
            raise ValidationError("Recipient phone number is required")

        if not params.recipient_phone.country_code:
            raise ValidationError("Country code is required")

        if not params.recipient_phone.phone_number:
            raise ValidationError("Phone number is required")

        if not params.message_body:
            raise ValidationError("Message body is required")

        if len(params.message_body) > 1600:
            raise ValidationError("Message body exceeds maximum length (1600 characters)")
