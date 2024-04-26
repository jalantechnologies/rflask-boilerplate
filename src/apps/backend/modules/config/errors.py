from modules.error.custom_errors import AppError

class ConfigErrorCodes:
    MISSING = "CONFIG_ERR_O1"

class ConfigMissingError(AppError):
    code: ConfigErrorCodes
    
    def __init__(self, missing_key: str):
        super().__init__(f"Config key '{missing_key}' is missing")
        self.code = ConfigErrorCodes.MISSING
