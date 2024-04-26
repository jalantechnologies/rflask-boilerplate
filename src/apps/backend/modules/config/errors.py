from modules.error.custom_errors import MissingKeyError
from modules.common.types import ErrorCode

class ConfigMissingError(MissingKeyError):
    code: ErrorCode
    
    def __init__(self, missing_key: str):
        self.code = ErrorCode.MISSING_KEY
        self.https_code = 401
        super().__init__(missing_key=missing_key, error_code=self.code)
