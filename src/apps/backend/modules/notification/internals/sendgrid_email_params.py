# src/apps/backend/modules/notification/internals/sendgrid_email_params.py
import re
from typing import List

from modules.notification.errors import ValidationError
from modules.notification.types import BulkEmailParams, SendEmailParams, ValidationFailure


class EmailParams:
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    max_recipients = 1000  # SendGrid limit

    @staticmethod
    def validate(params: SendEmailParams) -> None:
        """Validate SendEmailParams with reduced cognitive complexity"""
        failures: List[ValidationFailure] = []

        # Validate recipients
        failures.extend(EmailParams._validate_recipients(params.recipients))

        # Validate sender
        failures.extend(EmailParams._validate_sender(params.sender))

        # Validate email content
        failures.extend(EmailParams._validate_email_content(params))

        if failures:
            raise ValidationError("Email cannot be sent, please check the params validity.", failures)

    @staticmethod
    def validate_bulk_email(params: BulkEmailParams) -> None:
        """Validate BulkEmailParams with reduced cognitive complexity"""
        failures: List[ValidationFailure] = []

        # Validate recipients
        failures.extend(EmailParams._validate_recipients(params.recipients))

        # Validate sender
        failures.extend(EmailParams._validate_sender(params.sender))

        # Validate template requirements for bulk emails
        failures.extend(EmailParams._validate_bulk_template(params))

        # Validate personalizations
        failures.extend(EmailParams._validate_personalizations(params))

        if failures:
            raise ValidationError("Bulk email cannot be sent, please check the params validity.", failures)

    @staticmethod
    def _validate_recipients(recipients) -> List[ValidationFailure]:
        """Validate recipients list and individual email formats"""
        failures = []

        if not recipients or len(recipients) == 0:
            failures.append(ValidationFailure(field="recipients", message="At least one recipient is required."))
            return failures

        if len(recipients) > EmailParams.max_recipients:
            failures.append(
                ValidationFailure(
                    field="recipients", message=f"Maximum {EmailParams.max_recipients} recipients allowed per email."
                )
            )
            return failures

        # Validate each recipient email format
        for i, recipient in enumerate(recipients):
            if not EmailParams.is_email_valid(recipient.email):
                failures.append(
                    ValidationFailure(
                        field=f"recipients[{i}].email", message=f"Invalid email format: {recipient.email}"
                    )
                )

        return failures

    @staticmethod
    def _validate_sender(sender) -> List[ValidationFailure]:
        """Validate sender email and name"""
        failures = []

        if not EmailParams.is_email_valid(sender.email):
            failures.append(
                ValidationFailure(
                    field="sender.email", message="Please specify valid sender email in format you@example.com."
                )
            )

        if not sender.name:
            failures.append(ValidationFailure(field="sender.name", message="Please specify a non-empty sender name."))

        return failures

    @staticmethod
    def _validate_email_content(params: SendEmailParams) -> List[ValidationFailure]:
        """Validate email content requirements (template vs direct content)"""
        failures = []

        if params.template_id:
            failures.extend(EmailParams._validate_template_id(params.template_id))
        else:
            failures.extend(EmailParams._validate_direct_content(params))

        return failures

    @staticmethod
    def _validate_template_id(template_id: str) -> List[ValidationFailure]:
        """Validate template ID format"""
        failures = []

        if not isinstance(template_id, str) or len(template_id.strip()) == 0:
            failures.append(ValidationFailure(field="template_id", message="Template ID must be a non-empty string."))

        return failures

    @staticmethod
    def _validate_direct_content(params: SendEmailParams) -> List[ValidationFailure]:
        """Validate direct content email requirements"""
        failures = []

        if not params.subject:
            failures.append(ValidationFailure(field="subject", message="Subject is required for non-template emails."))

        if not params.html_content and not params.text_content:
            failures.append(
                ValidationFailure(
                    field="content", message="Either html_content or text_content is required for non-template emails."
                )
            )

        return failures

    @staticmethod
    def _validate_bulk_template(params: BulkEmailParams) -> List[ValidationFailure]:
        """Validate template requirements for bulk emails"""
        failures = []

        if not params.template_id or len(params.template_id.strip()) == 0:
            failures.append(ValidationFailure(field="template_id", message="Template ID is required for bulk emails."))

        return failures

    @staticmethod
    def _validate_personalizations(params: BulkEmailParams) -> List[ValidationFailure]:
        """Validate personalizations if provided"""
        failures = []

        if params.personalizations is None:
            return failures

        if len(params.personalizations) != len(params.recipients):
            failures.append(
                ValidationFailure(
                    field="personalizations", message="Number of personalizations must match number of recipients."
                )
            )

        return failures

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """Validate email format using regex"""
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailParams.email_regex, email.lower()))
