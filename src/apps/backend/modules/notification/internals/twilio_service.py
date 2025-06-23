from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional

from twilio.base.exceptions import TwilioException
from twilio.rest import Client

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.errors import ServiceError
from modules.notification.internals.twilio_params import SMSParams
from modules.notification.types import BulkSMSParams, PersonalizedSMSParams, SendSMSParams, SMSResponse

_TWILIO_ACCOUNT_SID_KEY = "twilio.account_sid"
_TWILIO_AUTH_TOKEN_KEY = "twilio.auth_token"
_TWILIO_MESSAGING_SERVICE_SID_KEY = "twilio.messaging_service_sid"


class TwilioService:
    __client: Optional[Client] = None
    MAX_CONCURRENT_REQUESTS = 10

    @staticmethod
    def send_sms(params: SendSMSParams) -> SMSResponse:
        SMSParams.validate(params)

        try:
            client = TwilioService.get_client()
            messaging_service_sid = ConfigService[str].get_value(key=_TWILIO_MESSAGING_SERVICE_SID_KEY)

            message_obj = client.messages.create(
                to=str(params.recipient_phone), messaging_service_sid=messaging_service_sid, body=params.message_body
            )

            Logger.info(message=f"SMS sent successfully to {params.recipient_phone}. Message SID: {message_obj.sid}")

            return SMSResponse(success=True, sent_count=1, failed_count=0, message_ids=[str(message_obj.sid)])

        except TwilioException as err:
            Logger.error(message=f"Twilio error sending SMS: {str(err)}")
            return SMSResponse(success=False, sent_count=0, failed_count=1, errors=[str(err)])
        except Exception as err:
            Logger.error(message=f"Unexpected error sending SMS: {str(err)}")
            raise ServiceError(err)

    @staticmethod
    def send_bulk_sms(params: BulkSMSParams) -> SMSResponse:
        for phone in params.recipient_phones:
            single_params = SendSMSParams(message_body=params.message_body, recipient_phone=phone)
            SMSParams.validate(single_params)

        message_ids = []
        errors = []
        sent_count = 0
        failed_count = 0

        try:
            client = TwilioService.get_client()
            messaging_service_sid = ConfigService[str].get_value(key=_TWILIO_MESSAGING_SERVICE_SID_KEY)

            with ThreadPoolExecutor(max_workers=TwilioService.MAX_CONCURRENT_REQUESTS) as executor:
                future_to_phone = {
                    executor.submit(
                        TwilioService._send_single_message,
                        client,
                        str(phone),
                        params.message_body,
                        messaging_service_sid,
                    ): phone
                    for phone in params.recipient_phones
                }

                for future in as_completed(future_to_phone):
                    phone = future_to_phone[future]
                    try:
                        message_sid = future.result()
                        if message_sid:
                            message_ids.append(message_sid)
                            sent_count += 1
                            Logger.info(message=f"SMS sent successfully to {phone}. Message SID: {message_sid}")
                        else:
                            failed_count += 1
                            errors.append(f"Failed to send SMS to {phone}")
                    except Exception as exc:
                        failed_count += 1
                        error_msg = f"Failed to send SMS to {phone}: {str(exc)}"
                        errors.append(error_msg)
                        Logger.error(message=error_msg)

            success = sent_count > 0
            Logger.info(message=f"Bulk SMS completed. Sent: {sent_count}, Failed: {failed_count}")

            return SMSResponse(
                success=success,
                sent_count=sent_count,
                failed_count=failed_count,
                message_ids=message_ids,
                errors=errors,
            )

        except Exception as err:
            Logger.error(message=f"Unexpected error in bulk SMS: {str(err)}")
            raise ServiceError(err)

    @staticmethod
    def send_personalized_sms(params: PersonalizedSMSParams) -> SMSResponse:
        message_ids = []
        errors = []
        sent_count = 0
        failed_count = 0

        try:
            client = TwilioService.get_client()
            messaging_service_sid = ConfigService[str].get_value(key=_TWILIO_MESSAGING_SERVICE_SID_KEY)

            for recipient_data in params.recipients_data:
                try:
                    phone = recipient_data.get("phone")
                    template_data = recipient_data.get("template_data", {})

                    if not phone:
                        failed_count += 1
                        errors.append("Phone number is required for each recipient")
                        continue

                    personalized_message = TwilioService._replace_template_placeholders(
                        params.message_template, template_data
                    )

                    single_params = SendSMSParams(message_body=personalized_message, recipient_phone=phone)
                    SMSParams.validate(single_params)

                    message_obj = client.messages.create(
                        to=str(phone), messaging_service_sid=messaging_service_sid, body=personalized_message
                    )

                    message_ids.append(str(message_obj.sid))
                    sent_count += 1
                    Logger.info(message=f"Personalized SMS sent to {phone}. Message SID: {message_obj.sid}")

                except Exception as exc:
                    failed_count += 1
                    error_msg = f"Failed to send personalized SMS to {phone}: {str(exc)}"
                    errors.append(error_msg)
                    Logger.error(message=error_msg)

            success = sent_count > 0
            Logger.info(message=f"Personalized SMS completed. Sent: {sent_count}, Failed: {failed_count}")

            return SMSResponse(
                success=success,
                sent_count=sent_count,
                failed_count=failed_count,
                message_ids=message_ids,
                errors=errors,
            )

        except Exception as err:
            Logger.error(message=f"Unexpected error in personalized SMS: {str(err)}")
            raise ServiceError(err)

    @staticmethod
    def _send_single_message(
        client: Client, phone: str, message_body: str, messaging_service_sid: str
    ) -> Optional[str]:
        try:
            message_obj = client.messages.create(
                to=phone, messaging_service_sid=messaging_service_sid, body=message_body
            )
            return str(message_obj.sid) if message_obj.sid else None
        except Exception as e:
            Logger.error(message=f"Error sending SMS to {phone}: {str(e)}")
            return None

    @staticmethod
    def _replace_template_placeholders(template: str, data: Dict[str, Any]) -> str:
        try:
            return template.format(**data)
        except KeyError as e:
            Logger.warn(message=f"Template placeholder not found in data: {e}")
            return template
        except Exception as e:
            Logger.error(message=f"Error replacing template placeholders: {e}")
            return template

    @staticmethod
    def get_client() -> Client:
        if not TwilioService.__client:
            account_sid = ConfigService[str].get_value(key=_TWILIO_ACCOUNT_SID_KEY)
            auth_token = ConfigService[str].get_value(key=_TWILIO_AUTH_TOKEN_KEY)

            TwilioService.__client = Client(account_sid, auth_token)

        return TwilioService.__client
