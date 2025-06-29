import json
import os
from typing import Optional

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.errors import ServiceError
from modules.notification.internals.firebase_params import PushNotificationValidator
from modules.notification.types import PushNotificationParams

# Conditional import to handle environments without firebase-admin
try:
    import firebase_admin
    from firebase_admin import credentials, messaging

    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    Logger.warn(message="firebase-admin package not installed. Push notifications will be logged but not sent.")


class FirebaseService:
    _app = None
    _initialized = False
    _initialized_attempted = False

    @staticmethod
    def initialize_app() -> bool:
        """
        Initialize the Firebase Admin SDK app.

        Returns:
            bool: True if initialization was successful, False otherwise
        """
        # Skip if already initialized or attempted
        if FirebaseService._initialized or FirebaseService._initialized_attempted:
            return FirebaseService._initialized

        FirebaseService._initialized_attempted = True

        if not FIREBASE_AVAILABLE:
            Logger.warn(message="Firebase SDK not available. Push notifications will be simulated.")
            return False

        try:
            # Check if Firebase is enabled
            firebase_enabled = ConfigService[bool].get_value(key="firebase.enabled", default=False)
            if not firebase_enabled:
                Logger.info(message="Firebase is disabled in configuration")
                return False

            # Get the service account credentials
            cred = None

            # First try service account key directly from config
            service_account_key = ConfigService[str].get_value(key="firebase.service_account_key", default="")
            if service_account_key:
                try:
                    # Try to parse as JSON string
                    service_account_dict = json.loads(service_account_key)
                    cred = credentials.Certificate(service_account_dict)
                except json.JSONDecodeError:
                    Logger.warn(message="Service account key is not a valid JSON string")

            # If no credentials yet, try service account key path
            if cred is None:
                service_account_key_path = ConfigService[str].get_value(
                    key="firebase.service_account_key_path", default=""
                )
                if service_account_key_path and os.path.isfile(service_account_key_path):
                    cred = credentials.Certificate(service_account_key_path)

            # If still no credentials, try default app credentials
            if cred is None:
                # Try application default credentials
                FirebaseService._app = firebase_admin.initialize_app()
            else:
                # Initialize the app with credentials
                FirebaseService._app = firebase_admin.initialize_app(cred)

            Logger.info(message="Firebase app initialized successfully")
            FirebaseService._initialized = True
            return True

        except Exception as e:
            Logger.error(message=f"Failed to initialize Firebase app: {str(e)}")
            return False

    @staticmethod
    def send_push_notification(params: PushNotificationParams) -> Optional[str]:
        """
        Send a push notification using Firebase Cloud Messaging.

        Args:
            params: PushNotificationParams containing notification details

        Returns:
            str: The message ID from FCM or None if sending failed
        """
        # Validate parameters
        PushNotificationValidator.validate(params)

        # Initialize app if not already initialized
        if not FirebaseService.initialize_app():
            # If initialization failed, log notification details and return
            Logger.info(message=f"Simulating push notification: {params.title} - {params.message}")
            if params.device_type:
                Logger.info(message=f"Would target device type: {params.device_type}")
            return None

        try:
            # Build notification message
            notification = messaging.Notification(title=params.title, body=params.message, image=params.image_url)

            # Additional data
            data = params.data or {}
            android_config = None
            apns_config = None

            # Convert data values to strings (FCM requirement)
            string_data = {k: str(v) for k, v in data.items()}

            # Create platform-specific configurations if needed
            if params.device_type == "android":
                android_config = messaging.AndroidConfig(
                    priority="high",
                    notification=messaging.AndroidNotification(
                        sound="default", click_action="FLUTTER_NOTIFICATION_CLICK"
                    ),
                )
            elif params.device_type == "ios":
                apns_config = messaging.APNSConfig(
                    payload=messaging.APNSPayload(aps=messaging.Aps(sound="default", badge=1))
                )

            # Determine the message target based on device type
            topic = params.topic
            if params.device_type:
                topic = f"{topic}_{params.device_type.lower()}"

            # Create the message
            message = messaging.Message(
                notification=notification, data=string_data, topic=topic, android=android_config, apns=apns_config
            )

            # Send the message
            response = messaging.send(message)
            Logger.info(message=f"Successfully sent push notification: {response}")
            return response

        except Exception as e:
            Logger.error(message=f"Error sending push notification: {str(e)}")
            raise ServiceError(e)
