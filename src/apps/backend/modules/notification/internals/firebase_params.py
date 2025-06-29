from typing import List

from modules.notification.errors import ValidationError
from modules.notification.types import PushNotificationParams, ValidationFailure


class PushNotificationValidator:
    @staticmethod
    def validate(params: PushNotificationParams) -> None:
        """
        Validate push notification parameters.

        Args:
            params: PushNotificationParams to validate

        Raises:
            ValidationError: If validation fails
        """
        failures: List[ValidationFailure] = []

        # Validate title
        if not params.title:
            failures.append(ValidationFailure(field="title", message="Please provide a title for the notification."))

        # Validate message
        if not params.message:
            failures.append(
                ValidationFailure(field="message", message="Please provide a message body for the notification.")
            )

        # Validate device type if specified
        if params.device_type and params.device_type.lower() not in ["android", "ios"]:
            failures.append(
                ValidationFailure(
                    field="device_type", message="Device type must be either 'android', 'ios', or not specified."
                )
            )

        # Validate topic
        if not params.topic:
            failures.append(ValidationFailure(field="topic", message="Please provide a topic for the notification."))

        if failures:
            raise ValidationError("Push notification cannot be sent due to validation errors.", failures)
