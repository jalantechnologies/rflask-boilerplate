import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class OSSettings:
    INSPECTLET_KEY: Optional[str] = os.environ.get("INSPECTLET_KEY")
    MONGODB_URI: Optional[str] = os.environ.get("MONGODB_URI")
    PAPERTRAIL_HOST: Optional[str] = os.environ.get("PAPERTRAIL_HOST")
    PAPERTRAIL_PORT: Optional[str] = os.environ.get("PAPERTRAIL_PORT")
    SENDGRID: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {"api_key": os.environ.get("SENDGRID_API_KEY")}
    )
    MAILER: Optional[dict[str, Optional[str]]] = field(
        default_factory=lambda: {
            "default_email": os.environ.get("DEFAULT_EMAIL"),
            "default_email_name": os.environ.get("DEFAULT_EMAIL_NAME"),
            "forgot_password_mail_template_id": os.environ.get("FORGOT_PASSWORD_MAIL_TEMPLATE_ID"),
        }
    )
    WEB_APP_HOST: Optional[str] = os.environ.get("WEB_APP_HOST")
