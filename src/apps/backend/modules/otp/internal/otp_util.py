import random
import string

from modules.otp.internal.store.otp_model import OtpModel
from modules.otp.types import Otp


class OtpUtil:
    @staticmethod
    def generate_otp(length: int) -> str:
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def convert_otp_model_to_otp(otp_model: OtpModel) -> Otp:
        return Otp(
            id=str(otp_model.id),
            otp_code=otp_model.otp_code,
            phone_number=otp_model.phone_number,
            status=otp_model.status,
        )
