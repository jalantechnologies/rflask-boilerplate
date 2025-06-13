import json
import os
from typing import Any, Dict, Optional

import firebase_admin
from firebase_admin import credentials, messaging

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.errors import NotificationConfigurationError, NotificationServiceError
from modules.notification.types import SendNotificationParams


class FirebaseNotificationProvider:
    """
    Firebase Cloud Messaging (FCM) implementation of notification provider

    Handles initialization of Firebase Admin SDK and sending push notifications
    through the Firebase Cloud Messaging service
    """

    _app: Optional[firebase_admin.App] = None
    _initialized: bool = False

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize Firebase Admin SDK with service account credentials

        Credentials are loaded from one of these sources (in priority order):
        1. Service account JSON file in project root
        2. Environment variable containing service account JSON
        3. Configuration service value

        Raises:
            NotificationConfigurationError: If no valid credentials are found
            NotificationServiceError: If initialization fails for other reasons
        """
        if cls._initialized:
            return

        try:
            # Option 1: Using service account key file
            if os.path.exists("firebase-service-account.json"):
                cred = credentials.Certificate("firebase-service-account.json")
                cls._app = firebase_admin.initialize_app(cred)
                Logger.info(message="Firebase initialized with service account file")

            # Option 2: Using environment variables (recommended for production)
            elif os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"):
                service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON"))
                cred = credentials.Certificate(service_account_info)
                cls._app = firebase_admin.initialize_app(cred)
                Logger.info(message="Firebase initialized with environment variables")

            # Option 3: Using config service (specific to this application)
            elif ConfigService.has_value("firebase.service_account_json"):
                service_account_json = ConfigService[str].get_value(key="firebase.service_account_json")
                service_account_info = json.loads(service_account_json)
                cred = credentials.Certificate(service_account_info)
                cls._app = firebase_admin.initialize_app(cred)
                Logger.info(message="Firebase initialized with configuration service")

            else:
                # We need credentials to proceed - fail fast to prevent runtime errors
                Logger.error(message="Firebase configuration is missing or invalid")
                raise NotificationConfigurationError()

            cls._initialized = True

        except Exception as e:
            Logger.error(message=f"Failed to initialize Firebase: {str(e)}")
            raise NotificationServiceError(str(e))

    @classmethod
    def lazy_initialize(cls) -> None:
        """
        Initialize Firebase only if it hasn't been initialized yet

        This allows components to ensure Firebase is ready without
        knowing the initialization state
        """
        if not cls._initialized:
            cls.initialize()

    @classmethod
    def send_notification(cls, params: SendNotificationParams) -> Dict[str, Any]:
        """
        Send notification to a specific FCM token

        Performs basic validation and handles common FCM error cases
        with appropriate error responses

        Args:
            params: Contains recipient FCM token and notification content

        Returns:
            Response containing success status and message ID or error details
        """
        # Make sure Firebase is initialized
        try:
            cls.lazy_initialize()
        except Exception as e:
            Logger.error(message=f"Firebase initialization failed: {str(e)}")
            return {"success": False, "error": "Firebase initialization failed", "message": str(e)}

        try:
            # Basic token validation to fail fast before making API call
            if not params.recipient.fcm_token or len(params.recipient.fcm_token.strip()) < 10:
                Logger.error(message=f"Invalid FCM token: {params.recipient.fcm_token}")
                return {
                    "success": False,
                    "error": "Invalid FCM token format",
                    "message": "The provided FCM token is invalid",
                }

            # Create notification payload
            notification = messaging.Notification(title=params.content.title, body=params.content.body)

            # Create message with platform-specific configurations
            message = messaging.Message(
                notification=notification,
                data=params.content.data or {},
                token=params.recipient.fcm_token,
                # Configure Android and iOS specific settings for better user experience
                android=messaging.AndroidConfig(
                    ttl=3600,  # Time to live in seconds
                    priority="high",
                    notification=messaging.AndroidNotification(
                        icon="stock_ticker_update", color="#f45342", sound="default"
                    ),
                ),
                apns=messaging.APNSConfig(payload=messaging.APNSPayload(aps=messaging.Aps(badge=1, sound="default"))),
            )

            # Send message and get message ID
            response = messaging.send(message)
            Logger.info(message=f"Successfully sent notification: {response}")

            return {"success": True, "message_id": response, "message": "Notification sent successfully"}

        except messaging.InvalidArgumentError as e:
            # Handle invalid token or message format errors
            Logger.error(message=f"Invalid argument error: {str(e)}")
            return {"success": False, "error": "Invalid FCM token or message format", "message": str(e)}

        except messaging.UnregisteredError as e:
            # Handle token no longer registered (app uninstalled, etc.)
            Logger.error(message=f"Unregistered token error: {str(e)}")
            return {"success": False, "error": "FCM token is not registered or expired", "message": str(e)}

        except Exception as e:
            # Catch-all for unexpected errors
            Logger.error(message=f"Failed to send notification: {str(e)}")
            return {"success": False, "error": "Internal server error", "message": str(e)}
