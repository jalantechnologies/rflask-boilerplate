import json
from typing import Dict, List, Union

import requests

from modules.config.config_service import ConfigService
from modules.logger.logger import Logger
from modules.notification.errors import FCMServiceError, InvalidFCMTokenError
from modules.notification.internals.device_token_reader import DeviceTokenReader
from modules.notification.internals.device_token_writer import DeviceTokenWriter
from modules.notification.types import FCMNotificationData, SendFCMParams


class FCMService:
    FIREBASE_API_URL = "https://fcm.googleapis.com/v1/projects/{}/messages:send"
    BATCH_SIZE = 500

    @staticmethod
    def send_notification(params: SendFCMParams) -> Dict[str, int]:
        if not params.tokens and not params.user_ids and not params.topic:
            raise ValueError("Either tokens, user_ids, or topic must be provided")

        # Determine tokens to use
        tokens = []
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
        result = {"successful": 0, "failed": 0, "failed_tokens": []}

        # Process tokens in batches of BATCH_SIZE
        for i in range(0, len(tokens), FCMService.BATCH_SIZE):
            batch = tokens[i : i + FCMService.BATCH_SIZE]
            batch_result = FCMService._send_multicast(notification, batch)

            result["successful"] += batch_result.get("successful", 0)
            result["failed"] += batch_result.get("failed", 0)

            if "failed_tokens" in batch_result:
                result["failed_tokens"].extend(batch_result["failed_tokens"])

        # Clean up invalid tokens
        FCMService._handle_failed_tokens(result.get("failed_tokens", []))

        return result

    @staticmethod
    def _send_multicast(notification: FCMNotificationData, tokens: List[str]) -> Dict[str, Union[int, List[str]]]:
        project_id = ConfigService[str].get_value(key="fcm.project_id")
        api_key = ConfigService[str].get_value(key="fcm.api_key")

        url = FCMService.FIREBASE_API_URL.format(project_id)

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

        payload = {
            "message": {
                "notification": {"title": notification.title, "body": notification.body},
                "data": notification.data,
                "tokens": tokens,
            }
        }

        if notification.image_url:
            payload["message"]["notification"]["image"] = notification.image_url

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()

            response_data = response.json()
            success_count = response_data.get("success_count", 0)
            failure_count = response_data.get("failure_count", 0)

            result = {"successful": success_count, "failed": failure_count}

            # Extract failed tokens from response
            if failure_count > 0 and "responses" in response_data:
                failed_tokens = []
                for idx, resp in enumerate(response_data["responses"]):
                    if "error" in resp:
                        failed_tokens.append(tokens[idx])
                result["failed_tokens"] = failed_tokens

            return result

        except requests.exceptions.RequestException as e:
            Logger.error(message=f"FCM multicast request failed: {str(e)}")
            return {"successful": 0, "failed": len(tokens), "failed_tokens": []}

    @staticmethod
    def _send_to_topic(notification: FCMNotificationData, topic: str) -> bool:
        project_id = ConfigService[str].get_value(key="fcm.project_id")
        api_key = ConfigService[str].get_value(key="fcm.api_key")

        url = FCMService.FIREBASE_API_URL.format(project_id)

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

        payload = {
            "message": {
                "notification": {"title": notification.title, "body": notification.body},
                "data": notification.data,
                "topic": topic,
            }
        }

        if notification.image_url:
            payload["message"]["notification"]["image"] = notification.image_url

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
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
        project_id = ConfigService[str].get_value(key="fcm.project_id")
        api_key = ConfigService[str].get_value(key="fcm.api_key")

        url = FCMService.FIREBASE_API_URL.format(project_id)

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

        payload = {"message": {"data": {"type": "token_validation"}, "token": token}}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return True

        except requests.exceptions.RequestException:
            raise InvalidFCMTokenError(f"Invalid FCM token: {token}")
