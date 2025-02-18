from dataclasses import dataclass


@dataclass(frozen=True)
class PreviewSettings:
    LOGGER_TRANSPORTS: tuple[str, str] = ("console", "datadog")
    SMS_ENABLED: bool = True
    IS_SERVER_RUNNING_BEHIND_PROXY: bool = True
    DEFAULT_OTP_ENABLED : bool = True
    DEFAULT_OTP : str = "6666"
