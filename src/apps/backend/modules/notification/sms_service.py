from typing import List

from modules.account.types import PhoneNumber
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.internals.twilio_service import TwilioService
from modules.notification.types import BulkSMSParams, PersonalizedSMSParams, SendSMSParams, SMSResponse


class SMSService:
    @staticmethod
    def send_sms(*, params: SendSMSParams) -> SMSResponse:
        is_sms_enabled = ConfigService[bool].get_value(key="sms.enabled")
        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send message - {params.message_body}")
            return SMSResponse(success=False, sent_count=0, failed_count=1, errors=["SMS service is disabled"])

        return TwilioService.send_sms(params=params)

    @staticmethod
    def send_bulk_sms(*, params: BulkSMSParams) -> SMSResponse:
        is_sms_enabled = ConfigService[bool].get_value(key="sms.enabled")
        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send bulk message - {params.message_body}")
            return SMSResponse(
                success=False,
                sent_count=0,
                failed_count=len(params.recipient_phones),
                errors=["SMS service is disabled"],
            )

        return TwilioService.send_bulk_sms(params=params)

    @staticmethod
    def send_personalized_sms(*, params: PersonalizedSMSParams) -> SMSResponse:
        is_sms_enabled = ConfigService[bool].get_value(key="sms.enabled")
        if not is_sms_enabled:
            Logger.warn(message=f"SMS is disabled. Could not send personalized messages")
            return SMSResponse(
                success=False,
                sent_count=0,
                failed_count=len(params.recipients_data),
                errors=["SMS service is disabled"],
            )

        return TwilioService.send_personalized_sms(params=params)

    @staticmethod
    def send_simple_sms(*, phone_numbers: List[str] | str, message: str) -> SMSResponse:
        try:
            if isinstance(phone_numbers, str):
                phone_numbers = [phone_numbers]

            recipient_phones = []
            for phone in phone_numbers:
                phone = phone.strip()

                if phone.startswith("+"):
                    from phonenumbers import NumberParseException
                    from phonenumbers import parse as parse_phone

                    try:
                        parsed = parse_phone(phone, None)
                        country_code = f"+{parsed.country_code}"
                        national_number = str(parsed.national_number)
                        recipient_phones.append(PhoneNumber(country_code=country_code, phone_number=national_number))
                    except NumberParseException:
                        if phone.startswith("+91"):
                            recipient_phones.append(PhoneNumber(country_code="+91", phone_number=phone[3:]))
                        elif phone.startswith("+1"):
                            recipient_phones.append(PhoneNumber(country_code="+1", phone_number=phone[2:]))
                        elif phone.startswith("+44"):
                            recipient_phones.append(PhoneNumber(country_code="+44", phone_number=phone[3:]))
                        else:
                            recipient_phones.append(PhoneNumber(country_code=phone[:3], phone_number=phone[3:]))
                else:
                    recipient_phones.append(PhoneNumber(country_code="+1", phone_number=phone))

            if len(recipient_phones) == 1:
                params = SendSMSParams(message_body=message, recipient_phone=recipient_phones[0])
                return SMSService.send_sms(params=params)
            else:
                params = BulkSMSParams(message_body=message, recipient_phones=recipient_phones)
                return SMSService.send_bulk_sms(params=params)

        except Exception as e:
            Logger.error(message=f"Error in send_simple_sms: {str(e)}")
            return SMSResponse(
                success=False,
                sent_count=0,
                failed_count=len(phone_numbers) if isinstance(phone_numbers, list) else 1,
                errors=[str(e)],
            )
