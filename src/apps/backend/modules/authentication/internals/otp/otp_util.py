import secrets
import string
from typing import Any

from modules.authentication.internals.otp.store.otp_model import OTPModel
from modules.authentication.types import OTP
from modules.config.config_service import ConfigService


class OTPUtil:
    @staticmethod
    def is_exempt_phone_number(phone_number: str) -> bool:
        exempt_phone_number = None
        if ConfigService[str].has_value(key="otp.exempt_phone_number"):
            exempt_phone_number = ConfigService[str].get_value(key="otp.exempt_phone_number")
            if exempt_phone_number and phone_number == exempt_phone_number:
                return True
        return False

    @staticmethod
    def generate_otp(length: int, phone_number: str) -> str:
        if OTPUtil.is_exempt_phone_number(phone_number):
            exempt_otp = ConfigService[str].get_value(key="otp.exempt_otp")
            return exempt_otp
        return "".join(secrets.choice(string.digits) for _ in range(length))

    @staticmethod
    def convert_otp_bson_to_otp(otp_bson: dict[str, Any]) -> OTP:
        validated_otp_data = OTPModel.from_bson(otp_bson)
        return OTP(
            id=str(validated_otp_data.id),
            otp_code=validated_otp_data.otp_code,
            phone_number=validated_otp_data.phone_number,
            status=validated_otp_data.status,
        )
