# src/apps/backend/modules/notification/fcm_service.py
from typing import Dict, List, Optional

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.internals.firebase_service import FirebaseService
from modules.notification.types import (
    BulkFCMParams,
    FCMAndroidConfig,
    FCMApnsConfig,
    FCMNotification,
    FCMResponse,
    FCMWebpushConfig,
    SendFCMParams,
    SendFCMToTopicParams,
)

_FCM_ENABLED_KEY = "fcm.enabled"

_FCM_DISABLED_ERROR = "FCM service is disabled"


class FCMService:
    @staticmethod
    def send_fcm_to_token(
        *,
        token: str,
        notification: Optional[FCMNotification] = None,
        data: Optional[Dict[str, str]] = None,
        android_config: Optional[FCMAndroidConfig] = None,
        apns_config: Optional[FCMApnsConfig] = None,
        webpush_config: Optional[FCMWebpushConfig] = None,
    ) -> FCMResponse:
        """Send FCM notification to a single token"""
        is_fcm_enabled = ConfigService[bool].get_value(key=_FCM_ENABLED_KEY)
        if not is_fcm_enabled:
            Logger.warn(message=f"FCM is disabled. Could not send notification to token: {token}")
            return FCMResponse(success=False, sent_count=0, failed_count=1, errors=[_FCM_DISABLED_ERROR])

        params = SendFCMParams(
            tokens=[token],
            notification=notification,
            data=data,
            android_config=android_config,
            apns_config=apns_config,
            webpush_config=webpush_config,
        )

        return FirebaseService.send_fcm_to_tokens(params)

    @staticmethod
    def send_fcm_to_tokens(
        *,
        tokens: List[str],
        notification: Optional[FCMNotification] = None,
        data: Optional[Dict[str, str]] = None,
        android_config: Optional[FCMAndroidConfig] = None,
        apns_config: Optional[FCMApnsConfig] = None,
        webpush_config: Optional[FCMWebpushConfig] = None,
    ) -> FCMResponse:
        """Send FCM notification to multiple tokens"""
        is_fcm_enabled = ConfigService[bool].get_value(key=_FCM_ENABLED_KEY)
        if not is_fcm_enabled:
            Logger.warn(message=f"FCM is disabled. Could not send notification to {len(tokens)} tokens")
            return FCMResponse(success=False, sent_count=0, failed_count=len(tokens), errors=[_FCM_DISABLED_ERROR])

        params = SendFCMParams(
            tokens=tokens,
            notification=notification,
            data=data,
            android_config=android_config,
            apns_config=apns_config,
            webpush_config=webpush_config,
        )

        return FirebaseService.send_fcm_to_tokens(params)

    @staticmethod
    def send_fcm_to_all(
        *,
        topic: str = "all",
        notification: Optional[FCMNotification] = None,
        data: Optional[Dict[str, str]] = None,
        android_config: Optional[FCMAndroidConfig] = None,
        apns_config: Optional[FCMApnsConfig] = None,
        webpush_config: Optional[FCMWebpushConfig] = None,
    ) -> FCMResponse:
        """Send FCM notification to all users via topic"""
        is_fcm_enabled = ConfigService[bool].get_value(key=_FCM_ENABLED_KEY)
        if not is_fcm_enabled:
            Logger.warn(message=f"FCM is disabled. Could not send notification to topic: {topic}")
            return FCMResponse(success=False, sent_count=0, failed_count=1, errors=[_FCM_DISABLED_ERROR])

        params = SendFCMToTopicParams(
            topic=topic,
            notification=notification,
            data=data,
            android_config=android_config,
            apns_config=apns_config,
            webpush_config=webpush_config,
        )

        return FirebaseService.send_fcm_to_topic(params)

    @staticmethod
    def send_bulk_fcm(
        *,
        tokens: List[str],
        notification: Optional[FCMNotification] = None,
        data: Optional[Dict[str, str]] = None,
        android_config: Optional[FCMAndroidConfig] = None,
        apns_config: Optional[FCMApnsConfig] = None,
        webpush_config: Optional[FCMWebpushConfig] = None,
    ) -> FCMResponse:
        """Send FCM notification to multiple tokens in bulk"""
        is_fcm_enabled = ConfigService[bool].get_value(key=_FCM_ENABLED_KEY)
        if not is_fcm_enabled:
            Logger.warn(message=f"FCM is disabled. Could not send bulk notification to {len(tokens)} tokens")
            return FCMResponse(success=False, sent_count=0, failed_count=len(tokens), errors=[_FCM_DISABLED_ERROR])

        params = BulkFCMParams(
            tokens=tokens,
            notification=notification,
            data=data,
            android_config=android_config,
            apns_config=apns_config,
            webpush_config=webpush_config,
        )

        return FirebaseService.send_bulk_fcm(params)

    @staticmethod
    def send_simple_fcm(
        *,
        tokens: List[str] | str,
        title: str,
        body: str,
        data: Optional[Dict[str, str]] = None,
        image: Optional[str] = None,
        android_priority: Optional[str] = None,
    ) -> FCMResponse:
        """Send simple FCM notification with minimal parameters"""
        try:
            # Normalize tokens input
            if isinstance(tokens, str):
                token_list = [tokens]
            else:
                token_list = tokens

            # Create notification
            notification = FCMNotification(title=title, body=body, image=image)

            # Create Android config if priority is specified
            android_config = None
            if android_priority:
                android_config = FCMAndroidConfig(priority=android_priority)

            # Determine which method to use based on token count
            if len(token_list) == 1:
                return FCMService.send_fcm_to_token(
                    token=token_list[0], notification=notification, data=data, android_config=android_config
                )
            else:
                return FCMService.send_fcm_to_tokens(
                    tokens=token_list, notification=notification, data=data, android_config=android_config
                )

        except Exception as e:
            Logger.error(message=f"Error in send_simple_fcm: {str(e)}")
            recipient_count = len(tokens) if isinstance(tokens, list) else 1
            return FCMResponse(success=False, sent_count=0, failed_count=recipient_count, errors=[str(e)])
