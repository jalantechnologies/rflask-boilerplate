import json
from typing import Any, Dict, List, cast

import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.errors import FCMServiceError, InvalidFCMTokenError
from modules.notification.internals.device_token_reader import DeviceTokenReader
from modules.notification.internals.device_token_writer import DeviceTokenWriter
from modules.notification.types import FCMNotificationData, SendFCMParams


class FCMService:
    _app = None
    BATCH_SIZE = 500  # FCM allows up to 500 tokens per multicast request
    USE_MULTICAST_FALLBACK = True  # Fallback to individual sends if multicast fails

    @staticmethod
    def _initialize_app() -> None:
        """Initialize Firebase Admin SDK if not already initialized"""
        if FCMService._app is None:
            try:
                # Check if Firebase is enabled
                firebase_enabled = ConfigService[bool].get_value(key="firebase.enabled", default=False)
                if not firebase_enabled:
                    Logger.warn(message="Firebase is disabled. FCM notifications will not be sent.")
                    raise FCMServiceError("Firebase is disabled in configuration")

                # Get the service account key JSON string from environment variable
                service_account_json = ConfigService[str].get_value(key="firebase.service_account_key")

                if not service_account_json or service_account_json.strip() == "":
                    raise FCMServiceError("Firebase service account key is not configured")

                # Parse the JSON string to a dictionary
                try:
                    cred_dict = json.loads(service_account_json)
                except json.JSONDecodeError as e:
                    raise FCMServiceError(f"Invalid Firebase service account JSON: {str(e)}")

                # Validate required fields
                required_fields = ["type", "project_id", "private_key", "client_email"]
                missing_fields = [field for field in required_fields if field not in cred_dict]

                if missing_fields:
                    raise FCMServiceError(f"Missing required fields in service account JSON: {missing_fields}")

                if cred_dict.get("type") != "service_account":
                    raise FCMServiceError("Service account type must be 'service_account'")

                # Create credentials from the dictionary
                cred = credentials.Certificate(cred_dict)

                # Initialize the app with the credentials
                FCMService._app = firebase_admin.initialize_app(cred)

                Logger.info(
                    message=f"Firebase Admin SDK initialized successfully for project: {cred_dict.get('project_id')}"
                )

            except FCMServiceError:
                raise
            except Exception as e:
                Logger.error(message=f"Failed to initialize Firebase Admin SDK: {str(e)}")
                raise FCMServiceError(f"Failed to initialize Firebase Admin SDK: {str(e)}")

    @staticmethod
    def send_notification(params: SendFCMParams) -> Dict[str, int]:
        """
        Send FCM notifications based on the provided parameters.
        Returns counts of successful and failed notifications.
        """
        try:
            FCMService._initialize_app()
        except FCMServiceError as e:
            Logger.error(message=f"FCM initialization failed: {str(e)}")
            return {"successful": 0, "failed": 0}

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
            success = FCMService._send_to_topic(params.notification, params.topic)
            return {"successful": 1 if success else 0, "failed": 0 if success else 1}

        # Send to tokens
        if not tokens:
            Logger.warn(message="No tokens found for FCM notification")
            return {"successful": 0, "failed": 0}

        return FCMService._send_to_tokens(params.notification, tokens)

    @staticmethod
    def _send_to_tokens(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, int]:
        """Send notifications to multiple tokens with multicast fallback"""
        result: Dict[str, Any] = {"successful": 0, "failed": 0, "failed_tokens": []}

        # Try multicast first, fall back to individual sends if it fails
        try:
            return FCMService._send_multicast_with_fallback(notification, tokens)
        except Exception as e:
            Logger.error(message=f"Both multicast and fallback failed: {str(e)}")
            return {"successful": 0, "failed": len(tokens)}

    @staticmethod
    def _send_multicast_with_fallback(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, int]:
        """Try multicast first, fall back to individual sends if multicast fails"""

        # First, try multicast approach
        try:
            Logger.info(message=f"Attempting FCM multicast for {len(tokens)} tokens")
            return FCMService._send_multicast_direct(notification, tokens)

        except FirebaseError as e:
            error_str = str(e).lower()

            if "404" in error_str or "not found" in error_str or "multicast" in error_str:
                Logger.warn(message="FCM multicast not available, falling back to individual sends")
                return FCMService._send_individual_messages(notification, tokens)
            else:
                raise e

        except Exception as e:
            error_str = str(e).lower()

            if "404" in error_str or "not found" in error_str:
                Logger.warn(message="FCM multicast failed with 404, using individual sends")
                return FCMService._send_individual_messages(notification, tokens)
            else:
                raise e

    @staticmethod
    def _send_multicast_direct(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, int]:
        """Send using FCM multicast API directly"""
        result: Dict[str, Any] = {"successful": 0, "failed": 0, "failed_tokens": []}

        # Process tokens in batches
        for i in range(0, len(tokens), FCMService.BATCH_SIZE):
            batch = tokens[i : i + FCMService.BATCH_SIZE]

            # Create the multicast message
            fcm_message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=notification.title, body=notification.body, image=notification.image_url
                ),
                data=notification.data,
                tokens=batch,
            )

            # Send the multicast message
            batch_response = messaging.send_multicast(fcm_message)

            # Process the responses
            success_count = batch_response.success_count
            failure_count = batch_response.failure_count

            result["successful"] = int(result["successful"]) + success_count
            result["failed"] = int(result["failed"]) + failure_count

            # Extract failed tokens
            if failure_count > 0:
                failed_tokens: List[str] = []
                for idx, resp in enumerate(batch_response.responses):
                    if not resp.success:
                        failed_tokens.append(batch[idx])
                        Logger.warn(message=f"FCM token {batch[idx][:20]}... failed: {resp.exception}")

                existing_failed = result.get("failed_tokens", [])
                if isinstance(existing_failed, list):
                    result["failed_tokens"] = existing_failed + failed_tokens
                else:
                    result["failed_tokens"] = failed_tokens

        # Clean up invalid tokens
        FCMService._handle_failed_tokens(cast(List[str], result.get("failed_tokens", [])))

        Logger.info(message=f"FCM multicast completed: {result['successful']} successful, {result['failed']} failed")
        return {"successful": int(result["successful"]), "failed": int(result["failed"])}

    @staticmethod
    def _send_individual_messages(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, int]:
        """Send individual messages as fallback when multicast is not available"""
        successful = 0
        failed = 0
        failed_tokens: List[str] = []

        Logger.info(message=f"Sending {len(tokens)} individual FCM messages")

        for token in tokens:
            try:
                # Create individual message
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=notification.title, body=notification.body, image=notification.image_url
                    ),
                    data=notification.data,
                    token=token,
                )

                # Send individual message
                response = messaging.send(message)
                successful += 1
                Logger.debug(message=f"FCM message sent successfully: {response}")

            except FirebaseError as e:
                failed += 1
                failed_tokens.append(token)
                Logger.warn(message=f"FCM individual send failed for token {token[:20]}...: {str(e)}")
            except Exception as e:
                failed += 1
                failed_tokens.append(token)
                Logger.error(message=f"Unexpected error sending to token {token[:20]}...: {str(e)}")

        # Clean up failed tokens
        FCMService._handle_failed_tokens(failed_tokens)

        Logger.info(message=f"FCM individual sends completed: {successful} successful, {failed} failed")
        return {"successful": successful, "failed": failed}

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
            response = messaging.send(message)
            Logger.info(message=f"FCM topic message sent successfully: {response}")
            return True

        except FirebaseError as e:
            error_code = getattr(e, "code", "unknown")
            Logger.error(message=f"FCM topic request failed [{error_code}]: {str(e)}")
            raise FCMServiceError(f"Failed to send notification to topic {topic}: {str(e)}")
        except Exception as e:
            Logger.error(message=f"Unexpected FCM topic error: {str(e)}")
            raise FCMServiceError(f"Failed to send notification to topic {topic}: {str(e)}")

    @staticmethod
    def _handle_failed_tokens(failed_tokens: List[str]) -> None:
        """Handle failed tokens by removing them from the database"""
        for token in failed_tokens:
            try:
                DeviceTokenWriter.remove_device_token(token)
                Logger.info(message=f"Removed invalid FCM token: {token[:20]}...")
            except Exception as e:
                Logger.error(message=f"Failed to remove invalid token: {str(e)}")

    @staticmethod
    def validate_token(token: str) -> bool:
        """Validate a FCM token by sending a silent notification"""
        try:
            FCMService._initialize_app()
        except FCMServiceError:
            return False

        # Create a message with minimal payload for validation
        message = messaging.Message(data={"type": "token_validation"}, token=token)

        try:
            messaging.send(message, dry_run=True)  # Use dry_run for validation
            return True

        except FirebaseError as e:
            error_code = getattr(e, "code", "unknown")
            Logger.warn(message=f"FCM token validation failed [{error_code}]: {str(e)}")
            raise InvalidFCMTokenError(f"Invalid FCM token: {str(e)}")
        except Exception as e:
            Logger.error(message=f"FCM token validation error: {str(e)}")
            raise InvalidFCMTokenError(f"Token validation failed: {str(e)}")
