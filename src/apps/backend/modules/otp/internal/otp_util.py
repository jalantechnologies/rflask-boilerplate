import random
import string
from typing import Any

from modules.otp.internal.store.otp_model import OtpModel
from modules.config.config_service import ConfigService
from modules.otp.types import Otp


class OtpUtil:
    @staticmethod
    def is_exempt_phone_number(phone_number: str) -> bool:
        exempt_phone_number = None
        if ConfigService.has_exempt_phone_number():
            exempt_phone_number = ConfigService.get_otp_config("exempt_phone_number")
            if exempt_phone_number and phone_number == exempt_phone_number:
                return True
        return False

    @staticmethod
    def generate_otp(length: int, phone_number: str) -> str:
        if OtpUtil.is_exempt_phone_number(phone_number):
            return ConfigService.get_otp_config("exempt_otp")
        if OtpUtil.is_default_otp_enabled():
            return ConfigService.get_default_otp()
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def convert_otp_bson_to_otp(otp_bson: dict[str, Any]) -> Otp:
        validated_otp_data = OtpModel.from_bson(otp_bson)
        return Otp(
            id=str(validated_otp_data.id),
            otp_code=validated_otp_data.otp_code,
            phone_number=validated_otp_data.phone_number,
            status=validated_otp_data.status,
        )

    @staticmethod
    def is_default_otp_enabled() -> bool:
        if ConfigService.has_key("DEFAULT_OTP_ENABLED"):
            return ConfigService.get_default_otp_enabled()
        return False
