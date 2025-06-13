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
    _app: Optional[firebase_admin.App] = None
    _initialized: bool = False

    @classmethod
    def initialize(cls) -> None:
        """Initialize Firebase Admin SDK with service account credentials"""
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
                Logger.error(message="Firebase configuration is missing or invalid")
                raise NotificationConfigurationError()

            cls._initialized = True

        except Exception as e:
            Logger.error(message=f"Failed to initialize Firebase: {str(e)}")
            raise NotificationServiceError(str(e))

    @classmethod
    def lazy_initialize(cls) -> None:
        """Initialize Firebase only if it hasn't been initialized yet"""
        if not cls._initialized:
            cls.initialize()

    @classmethod
    def send_notification(cls, params: SendNotificationParams) -> Dict[str, Any]:
        """
        Send notification to a specific FCM token

        Args:
            params: SendNotificationParams containing recipient and notification content

        Returns:
            dict: Response with success status and message ID or error
        """
        # Make sure Firebase is initialized
        try:
            cls.lazy_initialize()
        except Exception as e:
            Logger.error(message=f"Firebase initialization failed: {str(e)}")
            return {"success": False, "error": "Firebase initialization failed", "message": str(e)}

        try:
            # Validate token format (basic validation)
            if not params.recipient.fcm_token or len(params.recipient.fcm_token.strip()) < 10:
                Logger.error(message=f"Invalid FCM token: {params.recipient.fcm_token}")
                return {
                    "success": False,
                    "error": "Invalid FCM token format",
                    "message": "The provided FCM token is invalid",
                }

            # Create notification payload
            notification = messaging.Notification(title=params.content.title, body=params.content.body)

            # Create message
            message = messaging.Message(
                notification=notification,
                data=params.content.data or {},
                token=params.recipient.fcm_token,
                # Optional: Configure Android and iOS specific settings
                android=messaging.AndroidConfig(
                    ttl=3600,  # Time to live in seconds
                    priority="high",
                    notification=messaging.AndroidNotification(
                        icon="stock_ticker_update", color="#f45342", sound="default"
                    ),
                ),
                apns=messaging.APNSConfig(payload=messaging.APNSPayload(aps=messaging.Aps(badge=1, sound="default"))),
            )

            # Send message
            response = messaging.send(message)
            Logger.info(message=f"Successfully sent notification: {response}")

            return {"success": True, "message_id": response, "message": "Notification sent successfully"}

        except messaging.InvalidArgumentError as e:
            Logger.error(message=f"Invalid argument error: {str(e)}")
            return {"success": False, "error": "Invalid FCM token or message format", "message": str(e)}

        except messaging.UnregisteredError as e:
            Logger.error(message=f"Unregistered token error: {str(e)}")
            return {"success": False, "error": "FCM token is not registered or expired", "message": str(e)}

        except Exception as e:
            Logger.error(message=f"Failed to send notification: {str(e)}")
            return {"success": False, "error": "Internal server error", "message": str(e)}
