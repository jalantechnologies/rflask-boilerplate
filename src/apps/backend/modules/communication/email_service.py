from modules.communication.internals.sendgrid_service import SendGridService
from modules.communication.types import SendEmailParams


class EmailService:
    @staticmethod
    def send_email(*, params: SendEmailParams) -> None:
        return SendGridService.send_email(params)
