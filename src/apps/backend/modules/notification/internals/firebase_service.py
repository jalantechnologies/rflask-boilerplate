# src/apps/backend/modules/notification/internals/firebase_service.py
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

import firebase_admin
from firebase_admin import credentials, messaging

from modules.config.config_service import ConfigService
from modules.config.errors import MissingKeyError
from modules.logger.logger import Logger
from modules.notification.errors import ServiceError
from modules.notification.internals.fcm_params import FCMParams
from modules.notification.types import BulkFCMParams, FCMResponse, SendFCMParams, SendFCMToTopicParams

_FCM_SERVICE_ACCOUNT_KEY = "fcm.service_account_key"
_FCM_PROJECT_ID_KEY = "fcm.project_id"

_FCM_MAX_BATCH_SIZE = 500  # Firebase limit
_MAX_CONCURRENT_REQUESTS = 10


class FirebaseService:
    __app: Optional[firebase_admin.App] = None

    @staticmethod
    def send_fcm_to_tokens(params: SendFCMParams) -> FCMResponse:
        """Send FCM notification to specific tokens"""
        FCMParams.validate_send_params(params)

        try:
            app = FirebaseService.get_app()

            if len(params.tokens) == 1:
                return FirebaseService._send_single_message(app, params)
            else:
                return FirebaseService._send_multicast_message(app, params)

        except Exception as err:
            Logger.error(message=f"Error sending FCM notification: {str(err)}")
            raise ServiceError(err)

    @staticmethod
    def send_fcm_to_topic(params: SendFCMToTopicParams) -> FCMResponse:
        """Send FCM notification to a topic (all subscribers)"""
        FCMParams.validate_topic_params(params)

        try:
            app = FirebaseService.get_app()

            message = FirebaseService._build_topic_message(params)
            response = messaging.send(message, app=app)

            Logger.info(message=f"FCM topic message sent successfully. Message ID: {response}")

            return FCMResponse(success=True, sent_count=1, failed_count=0, message_ids=[response])

        except Exception as err:
            Logger.error(message=f"Error sending FCM topic notification: {str(err)}")
            return FCMResponse(success=False, sent_count=0, failed_count=1, errors=[str(err)])

    @staticmethod
    def send_bulk_fcm(params: BulkFCMParams) -> FCMResponse:
        """Send FCM notification to multiple tokens in batches"""
        FCMParams.validate_bulk_params(params)

        try:
            app = FirebaseService.get_app()

            # Split tokens into batches
            token_batches = FirebaseService._split_into_batches(params.tokens, _FCM_MAX_BATCH_SIZE)

            total_sent = 0
            total_failed = 0
            all_message_ids = []
            all_errors = []
            all_failure_details = []

            with ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_REQUESTS) as executor:
                future_to_batch = {
                    executor.submit(FirebaseService._send_batch, app, batch, params): batch for batch in token_batches
                }

                for future in as_completed(future_to_batch):
                    batch = future_to_batch[future]
                    try:
                        batch_response = future.result()
                        total_sent += batch_response.sent_count
                        total_failed += batch_response.failed_count
                        all_message_ids.extend(batch_response.message_ids)
                        all_errors.extend(batch_response.errors)
                        all_failure_details.extend(batch_response.failure_details)
                    except Exception as exc:
                        batch_size = len(batch)
                        total_failed += batch_size
                        error_msg = f"Batch processing failed: {str(exc)}"
                        all_errors.append(error_msg)
                        Logger.error(message=error_msg)

            success = total_sent > 0
            Logger.info(message=f"Bulk FCM completed. Sent: {total_sent}, Failed: {total_failed}")

            return FCMResponse(
                success=success,
                sent_count=total_sent,
                failed_count=total_failed,
                message_ids=all_message_ids,
                errors=all_errors,
                failure_details=all_failure_details,
            )

        except Exception as err:
            Logger.error(message=f"Error in bulk FCM send: {str(err)}")
            raise ServiceError(err)

    @staticmethod
    def _send_single_message(app: firebase_admin.App, params: SendFCMParams) -> FCMResponse:
        """Send FCM message to a single token"""
        try:
            message = FirebaseService._build_message(params.tokens[0], params)
            response = messaging.send(message, app=app)

            Logger.info(message=f"FCM message sent successfully to {params.tokens[0]}. Message ID: {response}")

            return FCMResponse(success=True, sent_count=1, failed_count=0, message_ids=[response])

        except messaging.FirebaseError as err:
            error_msg = f"Firebase error: {err.code} - {err.message}"
            Logger.error(message=error_msg)

            return FCMResponse(
                success=False,
                sent_count=0,
                failed_count=1,
                errors=[error_msg],
                failure_details=[{"token": params.tokens[0], "error_code": err.code, "error_message": err.message}],
            )
        except Exception as err:
            error_msg = f"Unexpected error: {str(err)}"
            Logger.error(message=error_msg)

            return FCMResponse(success=False, sent_count=0, failed_count=1, errors=[error_msg])

    @staticmethod
    def _send_multicast_message(app: firebase_admin.App, params: SendFCMParams) -> FCMResponse:
        """Send FCM message to multiple tokens"""
        try:
            multicast_message = FirebaseService._build_multicast_message(params)
            batch_response = messaging.send_multicast(multicast_message, app=app)

            message_ids = []
            errors = []
            failure_details = []

            for idx, response in enumerate(batch_response.responses):
                if response.success:
                    message_ids.append(response.message_id)
                else:
                    error_detail = {
                        "token": params.tokens[idx],
                        "error_code": response.exception.code if response.exception else "unknown",
                        "error_message": str(response.exception) if response.exception else "Unknown error",
                    }
                    failure_details.append(error_detail)
                    errors.append(f"Token {params.tokens[idx]}: {error_detail['error_message']}")

            success_count = batch_response.success_count
            failure_count = batch_response.failure_count

            Logger.info(message=f"FCM multicast completed. Success: {success_count}, Failed: {failure_count}")

            return FCMResponse(
                success=success_count > 0,
                sent_count=success_count,
                failed_count=failure_count,
                message_ids=message_ids,
                errors=errors,
                failure_details=failure_details,
            )

        except Exception as err:
            error_msg = f"Error in multicast send: {str(err)}"
            Logger.error(message=error_msg)

            return FCMResponse(success=False, sent_count=0, failed_count=len(params.tokens), errors=[error_msg])

    @staticmethod
    def _send_batch(app: firebase_admin.App, tokens: List[str], params: BulkFCMParams) -> FCMResponse:
        """Send a batch of FCM messages"""
        batch_params = SendFCMParams(
            tokens=tokens,
            notification=params.notification,
            data=params.data,
            android_config=params.android_config,
            apns_config=params.apns_config,
            webpush_config=params.webpush_config,
        )

        return FirebaseService._send_multicast_message(app, batch_params)

    @staticmethod
    def _build_message(token: str, params: SendFCMParams) -> messaging.Message:
        """Build a Firebase message for a single token"""
        message_kwargs = {"token": token}

        if params.notification:
            message_kwargs["notification"] = messaging.Notification(
                title=params.notification.title, body=params.notification.body, image=params.notification.image
            )

        if params.data:
            message_kwargs["data"] = params.data

        if params.android_config:
            android_config = messaging.AndroidConfig()
            if params.android_config.priority:
                android_config.priority = params.android_config.priority
            if params.android_config.ttl:
                android_config.ttl = params.android_config.ttl
            if params.android_config.collapse_key:
                android_config.collapse_key = params.android_config.collapse_key
            if params.android_config.data:
                android_config.data = params.android_config.data
            if params.android_config.notification:
                android_config.notification = messaging.AndroidNotification(**params.android_config.notification)
            message_kwargs["android"] = android_config

        if params.apns_config:
            apns_config = messaging.APNSConfig()
            if params.apns_config.headers:
                apns_config.headers = params.apns_config.headers
            if params.apns_config.payload:
                apns_config.payload = messaging.APNSPayload(**params.apns_config.payload)
            message_kwargs["apns"] = apns_config

        if params.webpush_config:
            webpush_config = messaging.WebpushConfig()
            if params.webpush_config.headers:
                webpush_config.headers = params.webpush_config.headers
            if params.webpush_config.data:
                webpush_config.data = params.webpush_config.data
            if params.webpush_config.notification:
                webpush_config.notification = messaging.WebpushNotification(**params.webpush_config.notification)
            message_kwargs["webpush"] = webpush_config

        return messaging.Message(**message_kwargs)

    @staticmethod
    def _build_multicast_message(params: SendFCMParams) -> messaging.MulticastMessage:
        """Build a Firebase multicast message"""
        message_kwargs = {"tokens": params.tokens}

        if params.notification:
            message_kwargs["notification"] = messaging.Notification(
                title=params.notification.title, body=params.notification.body, image=params.notification.image
            )

        if params.data:
            message_kwargs["data"] = params.data

        if params.android_config:
            android_config = messaging.AndroidConfig()
            if params.android_config.priority:
                android_config.priority = params.android_config.priority
            if params.android_config.ttl:
                android_config.ttl = params.android_config.ttl
            if params.android_config.collapse_key:
                android_config.collapse_key = params.android_config.collapse_key
            if params.android_config.data:
                android_config.data = params.android_config.data
            if params.android_config.notification:
                android_config.notification = messaging.AndroidNotification(**params.android_config.notification)
            message_kwargs["android"] = android_config

        if params.apns_config:
            apns_config = messaging.APNSConfig()
            if params.apns_config.headers:
                apns_config.headers = params.apns_config.headers
            if params.apns_config.payload:
                apns_config.payload = messaging.APNSPayload(**params.apns_config.payload)
            message_kwargs["apns"] = apns_config

        if params.webpush_config:
            webpush_config = messaging.WebpushConfig()
            if params.webpush_config.headers:
                webpush_config.headers = params.webpush_config.headers
            if params.webpush_config.data:
                webpush_config.data = params.webpush_config.data
            if params.webpush_config.notification:
                webpush_config.notification = messaging.WebpushNotification(**params.webpush_config.notification)
            message_kwargs["webpush"] = webpush_config

        return messaging.MulticastMessage(**message_kwargs)

    @staticmethod
    def _build_topic_message(params: SendFCMToTopicParams) -> messaging.Message:
        """Build a Firebase message for a topic"""
        message_kwargs = {"topic": params.topic}

        if params.notification:
            message_kwargs["notification"] = messaging.Notification(
                title=params.notification.title, body=params.notification.body, image=params.notification.image
            )

        if params.data:
            message_kwargs["data"] = params.data

        if params.android_config:
            android_config = messaging.AndroidConfig()
            if params.android_config.priority:
                android_config.priority = params.android_config.priority
            if params.android_config.ttl:
                android_config.ttl = params.android_config.ttl
            if params.android_config.collapse_key:
                android_config.collapse_key = params.android_config.collapse_key
            if params.android_config.data:
                android_config.data = params.android_config.data
            if params.android_config.notification:
                android_config.notification = messaging.AndroidNotification(**params.android_config.notification)
            message_kwargs["android"] = android_config

        if params.apns_config:
            apns_config = messaging.APNSConfig()
            if params.apns_config.headers:
                apns_config.headers = params.apns_config.headers
            if params.apns_config.payload:
                apns_config.payload = messaging.APNSPayload(**params.apns_config.payload)
            message_kwargs["apns"] = apns_config

        if params.webpush_config:
            webpush_config = messaging.WebpushConfig()
            if params.webpush_config.headers:
                webpush_config.headers = params.webpush_config.headers
            if params.webpush_config.data:
                webpush_config.data = params.webpush_config.data
            if params.webpush_config.notification:
                webpush_config.notification = messaging.WebpushNotification(**params.webpush_config.notification)
            message_kwargs["webpush"] = webpush_config

        return messaging.Message(**message_kwargs)

    @staticmethod
    def _split_into_batches(tokens: List[str], batch_size: int) -> List[List[str]]:
        """Split tokens into batches of specified size"""
        return [tokens[i : i + batch_size] for i in range(0, len(tokens), batch_size)]

    @staticmethod
    def get_app() -> firebase_admin.App:
        """Get or initialize Firebase app"""
        if not FirebaseService.__app:
            try:
                service_account_key = ConfigService[str].get_value(key=_FCM_SERVICE_ACCOUNT_KEY)

                # Parse service account key if it's a JSON string
                if isinstance(service_account_key, str):
                    service_account_dict = json.loads(service_account_key)
                else:
                    service_account_dict = service_account_key

                cred = credentials.Certificate(service_account_dict)
                FirebaseService.__app = firebase_admin.initialize_app(cred)

                Logger.info(message="Firebase Admin SDK initialized successfully")

            except MissingKeyError:
                raise ServiceError(Exception("Firebase service account key not found in configuration"))
            except json.JSONDecodeError:
                raise ServiceError(Exception("Invalid Firebase service account key format"))
            except Exception as e:
                raise ServiceError(Exception(f"Failed to initialize Firebase Admin SDK: {str(e)}"))

        return FirebaseService.__app
