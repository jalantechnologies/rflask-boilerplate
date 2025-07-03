import json
from typing import Any, Dict, List, Union, cast

import firebase_admin
from firebase_admin import credentials, messaging

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.errors import FCMServiceError, InvalidFCMTokenError
from modules.notification.internals.device_token_reader import DeviceTokenReader
from modules.notification.internals.device_token_writer import DeviceTokenWriter
from modules.notification.types import FCMNotificationData, SendFCMParams


class FCMService:
    _app = None
    BATCH_SIZE = 500  # FCM allows up to 500 tokens per multicast request

    @staticmethod
    def _initialize_app() -> None:
        """Initialize Firebase Admin SDK if not already initialized"""
        if FCMService._app is None:
            try:
                # Get the service account key JSON string from environment variable
                service_account_json = ConfigService[str].get_value(key="firebase.service_account_key")

                # Parse the JSON string to a dictionary
                cred_dict = json.loads(service_account_json)

                # Create credentials from the dictionary
                cred = credentials.Certificate(cred_dict)

                # Initialize the app with the credentials
                FCMService._app = firebase_admin.initialize_app(cred)

                Logger.info(message="Firebase Admin SDK initialized successfully")
            except Exception as e:
                Logger.error(message=f"Failed to initialize Firebase Admin SDK: {str(e)}")
                raise FCMServiceError(f"Failed to initialize Firebase Admin SDK: {str(e)}")

    @staticmethod
    def send_notification(params: SendFCMParams) -> Dict[str, int]:
        """
        Send FCM notifications based on the provided parameters.
        Returns counts of successful and failed notifications.
        """
        FCMService._initialize_app()

        if not params.tokens and not params.user_ids and not params.topic:
            raise ValueError("Either tokens, user_ids, or topic must be provided")

        # Determine tokens to use
        tokens: List[str] = []
        if params.tokens:
            tokens = params.tokens
        elif params.user_ids:
            for user_id in params.user_ids:
                user_tokens = DeviceTokenReader.get_tokens_by_user_id(user_id)
                tokens.extend(user_tokens)

        # If we have a topic, send to topic
        if params.topic:
            FCMService._send_to_topic(params.notification, params.topic)
            return {"successful": 1, "failed": 0}

        # Send to tokens in batches
        if not tokens:
            return {"successful": 0, "failed": 0}

        return FCMService._send_to_tokens(params.notification, tokens)

    @staticmethod
    def _send_to_tokens(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, int]:
        """Send notifications to multiple tokens in batches"""
        result: Dict[str, Any] = {"successful": 0, "failed": 0, "failed_tokens": []}

        # Process tokens in batches of BATCH_SIZE
        for i in range(0, len(tokens), FCMService.BATCH_SIZE):
            batch = tokens[i : i + FCMService.BATCH_SIZE]
            batch_result = FCMService._send_multicast(notification, batch)

            # Safely add values with proper type checking
            result["successful"] = int(result["successful"]) + int(batch_result.get("successful", 0))
            result["failed"] = int(result["failed"]) + int(batch_result.get("failed", 0))

            # Safely extend the failed_tokens list
            failed_tokens = batch_result.get("failed_tokens", [])
            if isinstance(failed_tokens, list):
                result_failed_tokens = result.get("failed_tokens", [])
                if isinstance(result_failed_tokens, list):
                    result["failed_tokens"] = result_failed_tokens + failed_tokens
                else:
                    result["failed_tokens"] = failed_tokens

        # Clean up invalid tokens
        FCMService._handle_failed_tokens(cast(List[str], result.get("failed_tokens", [])))

        # Return a dict with only int values for the counts
        return {"successful": int(result["successful"]), "failed": int(result["failed"])}

    @staticmethod
    def _send_multicast(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, Union[int, List[str]]]:
        """Send a notification to multiple tokens in a single request"""
        # Create the message
        fcm_message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification.title, body=notification.body, image=notification.image_url
            ),
            data=notification.data,
            tokens=tokens,
        )

        try:
            # Send the message
            batch_response = messaging.send_multicast(fcm_message)

            # Process the responses
            success_count = batch_response.success_count
            failure_count = batch_response.failure_count

            result: Dict[str, Union[int, List[str]]] = {"successful": success_count, "failed": failure_count}

            # Extract failed tokens
            if failure_count > 0:
                failed_tokens: List[str] = []
                for idx, resp in enumerate(batch_response.responses):
                    if not resp.success:
                        failed_tokens.append(tokens[idx])
                result["failed_tokens"] = failed_tokens

            return result

        except Exception as e:
            Logger.error(message=f"FCM multicast request failed: {str(e)}")
            return {"successful": 0, "failed": len(tokens), "failed_tokens": tokens}

    @staticmethod
    def _send_to_topic(notification: FCMNotificationData, topic: str) -> bool:
        """Send a notification to a topic"""
        # Create the message
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.title, body=notification.body, image=notification.image_url
            ),
            data=notification.data,
            topic=topic,
        )

        try:
            # Send the message
            messaging.send(message)
            return True

        except Exception as e:
            Logger.error(message=f"FCM topic request failed: {str(e)}")
            raise FCMServiceError(f"Failed to send notification to topic {topic}: {str(e)}")

    @staticmethod
    def _handle_failed_tokens(failed_tokens: List[str]) -> None:
        """Handle failed tokens by removing them from the database"""
        for token in failed_tokens:
            try:
                DeviceTokenWriter.remove_device_token(token)
                Logger.info(message=f"Removed invalid FCM token: {token}")
            except Exception as e:
                Logger.error(message=f"Failed to remove invalid token {token}: {str(e)}")

    @staticmethod
    def validate_token(token: str) -> bool:
        """Validate a FCM token by sending a silent notification"""
        FCMService._initialize_app()

        # Create a message with minimal payload
        message = messaging.Message(data={"type": "token_validation"}, token=token)

        try:
            messaging.send(message)
            return True

        except Exception:
            raise InvalidFCMTokenError(f"Invalid FCM token: {token}")
