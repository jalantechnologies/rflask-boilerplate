import random
import string
from typing import Any

from modules.config.config_service import ConfigService
from modules.otp.types import Otp


class OtpUtil:
    @staticmethod
    def is_default_phone_number(phone_number: str) -> bool:
        default_phone_number = None
        if ConfigService.has_default_phone_number():
            default_phone_number = ConfigService.get_otp_config("default_phone_number")
            if default_phone_number and phone_number == default_phone_number:
                return True
        return False

    @staticmethod
    def generate_otp(length: int, phone_number: str) -> str:
        if OtpUtil.is_default_phone_number(phone_number):
            return ConfigService.get_otp_config("default_otp")
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def convert_otp_bson_to_otp(otp_bson: dict[str, Any]) -> Otp:
        return Otp(
            id=str(otp_bson['_id']),
            otp_code=otp_bson['otp_code'],
            phone_number=otp_bson['phone_number'],
            status=otp_bson['status'],
        )
