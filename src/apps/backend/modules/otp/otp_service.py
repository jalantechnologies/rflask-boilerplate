from dataclasses import asdict

from modules.account.types import PhoneNumber
from modules.communication.sms_service import SMSService
from modules.communication.types import SendSMSParams
from modules.otp.internal.otp_util import OTPUtil
from modules.otp.internal.otp_writer import OTPWriter
from modules.otp.types import CreateOTPParams, OTP, VerifyOTPParams


class OTPService:
    @staticmethod
    def create_otp(*, params: CreateOTPParams) -> OTP:
        recipient_phone_number = PhoneNumber(**asdict(params)["phone_number"])
        otp = OTPWriter.create_new_otp(params=params)

        send_sms_params = SendSMSParams(
            message_body=f"{otp.otp_code} is your One Time Password (OTP) for verification.",
            recipient_phone=recipient_phone_number,
        )
        if not OTPUtil.is_default_phone_number(phone_number=recipient_phone_number.phone_number):
            SMSService.send_sms(params=send_sms_params)

        return otp

    @staticmethod
    def verify_otp(*, params: VerifyOTPParams) -> OTP:
        return OTPWriter.verify_otp(params=params)
