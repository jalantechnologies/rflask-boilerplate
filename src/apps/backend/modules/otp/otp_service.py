from modules.communication.sms_service import SMSService
from modules.communication.types import SendSMSParams
from modules.otp.internal.otp_writer import OtpWriter
from modules.otp.types import CreateOtpParams, Otp, VerifyOtpParams


class OtpService:
    @staticmethod
    def create_otp(*, params: CreateOtpParams) -> Otp:
        otp = OtpWriter.create_new_otp(params=params)

        send_sms_params = SendSMSParams(
            message_body=f"{otp.otp_code} is your One Time Password (OTP) for verification.",
            recipient_phone=params.phone_number,
        )
        SMSService.send_sms(params=send_sms_params)

        return otp

    @staticmethod
    def verify_otp(*, params: VerifyOtpParams) -> Otp:
        return OtpWriter.verify_otp(params=params)
