# src/apps/backend/modules/notification/internals/fcm_params.py
from modules.notification.errors import ValidationError
from modules.notification.types import BulkFCMParams, SendFCMParams, SendFCMToTopicParams, ValidationFailure


class FCMParams:
    @staticmethod
    def validate_send_params(params: SendFCMParams) -> None:
        """Validate SendFCMParams"""
        validation_failures = []

        # Validate tokens
        if not params.tokens:
            validation_failures.append(ValidationFailure(field="tokens", message="Tokens list cannot be empty"))
        elif not isinstance(params.tokens, list):
            validation_failures.append(ValidationFailure(field="tokens", message="Tokens must be a list"))
        else:
            for idx, token in enumerate(params.tokens):
                if not token or not isinstance(token, str):
                    validation_failures.append(
                        ValidationFailure(field=f"tokens[{idx}]", message="Token must be a non-empty string")
                    )
                elif len(token.strip()) == 0:
                    validation_failures.append(
                        ValidationFailure(field=f"tokens[{idx}]", message="Token cannot be empty or whitespace")
                    )

        # Validate notification (if provided)
        if params.notification:
            if not params.notification.title or not isinstance(params.notification.title, str):
                validation_failures.append(
                    ValidationFailure(
                        field="notification.title", message="Notification title must be a non-empty string"
                    )
                )
            elif len(params.notification.title.strip()) == 0:
                validation_failures.append(
                    ValidationFailure(field="notification.title", message="Notification title cannot be empty")
                )

            if not params.notification.body or not isinstance(params.notification.body, str):
                validation_failures.append(
                    ValidationFailure(field="notification.body", message="Notification body must be a non-empty string")
                )
            elif len(params.notification.body.strip()) == 0:
                validation_failures.append(
                    ValidationFailure(field="notification.body", message="Notification body cannot be empty")
                )

        # Validate data (if provided)
        if params.data is not None:
            if not isinstance(params.data, dict):
                validation_failures.append(ValidationFailure(field="data", message="Data must be a dictionary"))
            else:
                for key, value in params.data.items():
                    if not isinstance(key, str):
                        validation_failures.append(
                            ValidationFailure(field=f"data.{key}", message="Data keys must be strings")
                        )
                    if not isinstance(value, str):
                        validation_failures.append(
                            ValidationFailure(field=f"data.{key}", message="Data values must be strings")
                        )

        # Validate Android config (if provided)
        if params.android_config:
            if params.android_config.priority and params.android_config.priority not in ["normal", "high"]:
                validation_failures.append(
                    ValidationFailure(field="android_config.priority", message="Priority must be 'normal' or 'high'")
                )

        # At least one of notification or data must be provided
        if not params.notification and not params.data:
            validation_failures.append(
                ValidationFailure(field="message", message="Either notification or data must be provided")
            )

        if validation_failures:
            raise ValidationError(failures=validation_failures)

    @staticmethod
    def validate_topic_params(params: SendFCMToTopicParams) -> None:
        """Validate SendFCMToTopicParams"""
        validation_failures = []

        # Validate topic
        if not params.topic or not isinstance(params.topic, str):
            validation_failures.append(ValidationFailure(field="topic", message="Topic must be a non-empty string"))
        elif len(params.topic.strip()) == 0:
            validation_failures.append(ValidationFailure(field="topic", message="Topic cannot be empty or whitespace"))
        elif not params.topic.replace("_", "").replace("-", "").isalnum():
            validation_failures.append(
                ValidationFailure(
                    field="topic", message="Topic must contain only alphanumeric characters, hyphens, and underscores"
                )
            )

        # Validate notification (if provided)
        if params.notification:
            if not params.notification.title or not isinstance(params.notification.title, str):
                validation_failures.append(
                    ValidationFailure(
                        field="notification.title", message="Notification title must be a non-empty string"
                    )
                )
            elif len(params.notification.title.strip()) == 0:
                validation_failures.append(
                    ValidationFailure(field="notification.title", message="Notification title cannot be empty")
                )

            if not params.notification.body or not isinstance(params.notification.body, str):
                validation_failures.append(
                    ValidationFailure(field="notification.body", message="Notification body must be a non-empty string")
                )
            elif len(params.notification.body.strip()) == 0:
                validation_failures.append(
                    ValidationFailure(field="notification.body", message="Notification body cannot be empty")
                )

        # Validate data (if provided)
        if params.data is not None:
            if not isinstance(params.data, dict):
                validation_failures.append(ValidationFailure(field="data", message="Data must be a dictionary"))
            else:
                for key, value in params.data.items():
                    if not isinstance(key, str):
                        validation_failures.append(
                            ValidationFailure(field=f"data.{key}", message="Data keys must be strings")
                        )
                    if not isinstance(value, str):
                        validation_failures.append(
                            ValidationFailure(field=f"data.{key}", message="Data values must be strings")
                        )

        # At least one of notification or data must be provided
        if not params.notification and not params.data:
            validation_failures.append(
                ValidationFailure(field="message", message="Either notification or data must be provided")
            )

        if validation_failures:
            raise ValidationError(failures=validation_failures)

    @staticmethod
    def validate_bulk_params(params: BulkFCMParams) -> None:
        """Validate BulkFCMParams"""
        validation_failures = []

        # Validate tokens
        if not params.tokens:
            validation_failures.append(ValidationFailure(field="tokens", message="Tokens list cannot be empty"))
        elif not isinstance(params.tokens, list):
            validation_failures.append(ValidationFailure(field="tokens", message="Tokens must be a list"))
        elif len(params.tokens) > 1000:  # Reasonable limit for bulk operations
            validation_failures.append(
                ValidationFailure(field="tokens", message="Too many tokens (maximum 1000 allowed)")
            )
        else:
            for idx, token in enumerate(params.tokens):
                if not token or not isinstance(token, str):
                    validation_failures.append(
                        ValidationFailure(field=f"tokens[{idx}]", message="Token must be a non-empty string")
                    )
                elif len(token.strip()) == 0:
                    validation_failures.append(
                        ValidationFailure(field=f"tokens[{idx}]", message="Token cannot be empty or whitespace")
                    )

        # Validate notification (if provided)
        if params.notification:
            if not params.notification.title or not isinstance(params.notification.title, str):
                validation_failures.append(
                    ValidationFailure(
                        field="notification.title", message="Notification title must be a non-empty string"
                    )
                )
            elif len(params.notification.title.strip()) == 0:
                validation_failures.append(
                    ValidationFailure(field="notification.title", message="Notification title cannot be empty")
                )

            if not params.notification.body or not isinstance(params.notification.body, str):
                validation_failures.append(
                    ValidationFailure(field="notification.body", message="Notification body must be a non-empty string")
                )
            elif len(params.notification.body.strip()) == 0:
                validation_failures.append(
                    ValidationFailure(field="notification.body", message="Notification body cannot be empty")
                )

        # Validate data (if provided)
        if params.data is not None:
            if not isinstance(params.data, dict):
                validation_failures.append(ValidationFailure(field="data", message="Data must be a dictionary"))
            else:
                for key, value in params.data.items():
                    if not isinstance(key, str):
                        validation_failures.append(
                            ValidationFailure(field=f"data.{key}", message="Data keys must be strings")
                        )
                    if not isinstance(value, str):
                        validation_failures.append(
                            ValidationFailure(field=f"data.{key}", message="Data values must be strings")
                        )

        # At least one of notification or data must be provided
        if not params.notification and not params.data:
            validation_failures.append(
                ValidationFailure(field="message", message="Either notification or data must be provided")
            )

        if validation_failures:
            raise ValidationError(failures=validation_failures)
