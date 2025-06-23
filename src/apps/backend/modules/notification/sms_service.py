from typing import List

from modules.account.types import PhoneNumber
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.internals.twilio_service import TwilioService
from modules.notification.types import BulkSMSParams, PersonalizedSMSParams, SendSMSParams, SMSResponse

_SMS_ENABLED_KEY = "sms.enabled"

_SMS_DISABLED_ERROR = "SMS service is disabled"

_DEFAULT_COUNTRY_CODE = "+1"
_COUNTRY_CODE_MAPPINGS = {"+91": 3, "+1": 2, "+44": 3}  # India  # US/Canada  # UK


class SMSService:
    @staticmethod
    def send_sms(*, params: SendSMSParams) -> SMSResponse:
        is_sms_enabled = ConfigService[bool].get_value(key=_SMS_ENABLED_KEY)
        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send message - {params.message_body}")
            return SMSResponse(success=False, sent_count=0, failed_count=1, errors=[_SMS_DISABLED_ERROR])

        return TwilioService.send_sms(params)

    @staticmethod
    def send_bulk_sms(*, params: BulkSMSParams) -> SMSResponse:
        is_sms_enabled = ConfigService[bool].get_value(key=_SMS_ENABLED_KEY)
        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send bulk message - {params.message_body}")
            return SMSResponse(
                success=False, sent_count=0, failed_count=len(params.recipient_phones), errors=[_SMS_DISABLED_ERROR]
            )

        return TwilioService.send_bulk_sms(params)

    @staticmethod
    def send_personalized_sms(*, params: PersonalizedSMSParams) -> SMSResponse:
        is_sms_enabled = ConfigService[bool].get_value(key=_SMS_ENABLED_KEY)
        if not is_sms_enabled:
            Logger.warn(message="SMS is disabled. Could not send personalized messages")
            return SMSResponse(
                success=False, sent_count=0, failed_count=len(params.recipients_data), errors=[_SMS_DISABLED_ERROR]
            )

        return TwilioService.send_personalized_sms(params)

    @staticmethod
    def send_simple_sms(*, phone_numbers: List[str] | str, message: str) -> SMSResponse:
        try:
            normalized_phones = SMSService._normalize_phone_input(phone_numbers)

            recipient_phones = SMSService._parse_phone_numbers(normalized_phones)

            return SMSService._send_based_on_recipient_count(recipient_phones, message)

        except Exception as e:
            Logger.error(message=f"Error in send_simple_sms: {str(e)}")
            recipient_count = len(phone_numbers) if isinstance(phone_numbers, list) else 1
            return SMSResponse(success=False, sent_count=0, failed_count=recipient_count, errors=[str(e)])

    @staticmethod
    def _normalize_phone_input(phone_numbers: List[str] | str) -> List[str]:
        if isinstance(phone_numbers, str):
            return [phone_numbers]
        return phone_numbers

    @staticmethod
    def _parse_phone_numbers(phone_numbers: List[str]) -> List[PhoneNumber]:
        recipient_phones = []

        for phone in phone_numbers:
            phone = phone.strip()
            parsed_phone = SMSService._parse_single_phone_number(phone)
            recipient_phones.append(parsed_phone)

        return recipient_phones

    @staticmethod
    def _parse_single_phone_number(phone: str) -> PhoneNumber:
        if phone.startswith("+"):
            return SMSService._parse_international_phone(phone)
        else:
            return PhoneNumber(country_code=_DEFAULT_COUNTRY_CODE, phone_number=phone)

    @staticmethod
    def _parse_international_phone(phone: str) -> PhoneNumber:
        try:
            from phonenumbers import NumberParseException
            from phonenumbers import parse as parse_phone

            parsed = parse_phone(phone, None)
            country_code = f"+{parsed.country_code}"
            national_number = str(parsed.national_number)
            return PhoneNumber(country_code=country_code, phone_number=national_number)

        except NumberParseException:
            return SMSService._manual_parse_phone(phone)

    @staticmethod
    def _manual_parse_phone(phone: str) -> PhoneNumber:
        for country_code, digit_count in _COUNTRY_CODE_MAPPINGS.items():
            if phone.startswith(country_code):
                return PhoneNumber(country_code=country_code, phone_number=phone[digit_count:])

        return PhoneNumber(country_code=phone[:3], phone_number=phone[3:])

    @staticmethod
    def _send_based_on_recipient_count(recipient_phones: List[PhoneNumber], message: str) -> SMSResponse:
        if len(recipient_phones) == 1:
            single_params = SendSMSParams(message_body=message, recipient_phone=recipient_phones[0])
            return SMSService.send_sms(params=single_params)
        else:
            bulk_params = BulkSMSParams(message_body=message, recipient_phones=recipient_phones)
            return SMSService.send_bulk_sms(params=bulk_params)
