from modules.communication.internals.sendgrid_service import SendGridService
from modules.communication.types import SendEmailParams


class EmailService:
    def send_email(self, params: SendEmailParams) -> None:
        return SendGridService.send_email(params)
