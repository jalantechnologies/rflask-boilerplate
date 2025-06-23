from typing import List

from phonenumbers import NumberParseException, is_valid_number, parse

from modules.notification.errors import ValidationError
from modules.notification.types import BulkSMSParams, PersonalizedSMSParams, SendSMSParams, ValidationFailure


class SMSParams:
    MAX_RECIPIENTS = 1000
    MAX_MESSAGE_LENGTH = 1600

    @staticmethod
    def validate(params: SendSMSParams) -> None:
        failures: List[ValidationFailure] = []

        failures.extend(SMSParams._validate_phone_number(params.recipient_phone, "recipient_phone"))

        failures.extend(SMSParams._validate_message_body(params.message_body))

        if failures:
            raise ValidationError("SMS cannot be sent, please check the params validity.", failures)

    @staticmethod
    def validate_bulk_sms(params: BulkSMSParams) -> None:
        failures: List[ValidationFailure] = []

        failures.extend(SMSParams._validate_bulk_recipients(params.recipient_phones))

        failures.extend(SMSParams._validate_message_body(params.message_body))

        if failures:
            raise ValidationError("Bulk SMS cannot be sent, please check the params validity.", failures)

    @staticmethod
    def validate_personalized_sms(params: PersonalizedSMSParams) -> None:
        failures: List[ValidationFailure] = []

        failures.extend(SMSParams._validate_personalized_recipients(params.recipients_data))

        failures.extend(SMSParams._validate_message_template(params.message_template))

        if failures:
            raise ValidationError("Personalized SMS cannot be sent, please check the params validity.", failures)

    @staticmethod
    def _validate_phone_number(phone_number, field_name: str) -> List[ValidationFailure]:
        failures = []

        try:
            parsed_number = parse(str(phone_number))
            is_phone_valid = is_valid_number(parsed_number)
        except NumberParseException:
            is_phone_valid = False

        if not is_phone_valid:
            failures.append(
                ValidationFailure(
                    field=field_name, message="Please specify a valid phone number in format +12124567890."
                )
            )

        return failures

    @staticmethod
    def _validate_bulk_recipients(recipient_phones) -> List[ValidationFailure]:
        failures = []

        if not recipient_phones or len(recipient_phones) == 0:
            failures.append(
                ValidationFailure(field="recipient_phones", message="At least one recipient phone number is required.")
            )
            return failures

        if len(recipient_phones) > SMSParams.MAX_RECIPIENTS:
            failures.append(
                ValidationFailure(
                    field="recipient_phones",
                    message=f"Maximum {SMSParams.MAX_RECIPIENTS} recipients allowed per bulk SMS.",
                )
            )

        for i, phone in enumerate(recipient_phones):
            phone_failures = SMSParams._validate_phone_number(phone, f"recipient_phones[{i}]")
            failures.extend(phone_failures)

        return failures

    @staticmethod
    def _validate_personalized_recipients(recipients_data) -> List[ValidationFailure]:
        failures = []

        if not recipients_data or len(recipients_data) == 0:
            failures.append(ValidationFailure(field="recipients_data", message="At least one recipient is required."))
            return failures

        if len(recipients_data) > SMSParams.MAX_RECIPIENTS:
            failures.append(
                ValidationFailure(
                    field="recipients_data",
                    message=f"Maximum {SMSParams.MAX_RECIPIENTS} recipients allowed per personalized SMS.",
                )
            )

        for i, recipient in enumerate(recipients_data):
            if not isinstance(recipient, dict):
                failures.append(
                    ValidationFailure(
                        field=f"recipients_data[{i}]",
                        message="Each recipient must be a dictionary with 'phone' and optional 'template_data'.",
                    )
                )
                continue

            phone = recipient.get("phone")
            if not phone:
                failures.append(
                    ValidationFailure(
                        field=f"recipients_data[{i}].phone", message="Phone number is required for each recipient."
                    )
                )
            else:
                phone_failures = SMSParams._validate_phone_number(phone, f"recipients_data[{i}].phone")
                failures.extend(phone_failures)

            template_data = recipient.get("template_data")
            if template_data is not None and not isinstance(template_data, dict):
                failures.append(
                    ValidationFailure(
                        field=f"recipients_data[{i}].template_data", message="Template data must be a dictionary."
                    )
                )

        return failures

    @staticmethod
    def _validate_message_body(message_body: str) -> List[ValidationFailure]:
        failures = []

        if not message_body or not message_body.strip():
            failures.append(ValidationFailure(field="message_body", message="Please specify a non-empty message body."))
        elif len(message_body) > SMSParams.MAX_MESSAGE_LENGTH:
            failures.append(
                ValidationFailure(
                    field="message_body",
                    message=f"Message body cannot exceed {SMSParams.MAX_MESSAGE_LENGTH} characters.",
                )
            )

        return failures

    @staticmethod
    def _validate_message_template(message_template: str) -> List[ValidationFailure]:
        failures = []

        if not message_template or not message_template.strip():
            failures.append(
                ValidationFailure(field="message_template", message="Please specify a non-empty message template.")
            )
        elif len(message_template) > SMSParams.MAX_MESSAGE_LENGTH:
            failures.append(
                ValidationFailure(
                    field="message_template",
                    message=f"Message template cannot exceed {SMSParams.MAX_MESSAGE_LENGTH} characters.",
                )
            )

        return failures
