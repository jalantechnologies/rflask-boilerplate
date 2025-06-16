from typing import Any, Dict, List, Optional

from pymongo.collection import Collection
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.email_notification.internal.store.email_log_model import EmailLogModel
from modules.logger.logger import Logger

EMAIL_LOG_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [
            "message_id",
            "sender_email",
            "recipient_emails",
            "subject",
            "content_type",
            "status",
            "created_at",
            "updated_at",
        ],
        "properties": {
            "message_id": {"bsonType": "string"},
            "sender_email": {"bsonType": "string"},
            "sender_name": {"bsonType": ["string", "null"]},
            "recipient_emails": {"bsonType": "array"},
            "subject": {"bsonType": "string"},
            "body": {"bsonType": "string"},
            "content_type": {"bsonType": "string"},
            "status": {"bsonType": "string"},
            "error": {"bsonType": ["string", "null"]},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
            "_id": {"bsonType": "objectId"},
        },
    }
}


class EmailLogRepository(ApplicationRepository):
    """Repository for email logs in MongoDB"""

    collection_name = EmailLogModel.get_collection_name()

    RECIPIENT_EMAIL_FIELD = "recipient_emails.email"
    MESSAGE_ID_FIELD = "message_id"
    STATUS_FIELD = "status"
    CREATED_AT_FIELD = "created_at"

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index(cls.MESSAGE_ID_FIELD, unique=True)
        collection.create_index(cls.STATUS_FIELD)
        collection.create_index(cls.CREATED_AT_FIELD)
        collection.create_index(cls.RECIPIENT_EMAIL_FIELD)

        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": EMAIL_LOG_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }

        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=EMAIL_LOG_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"OperationFailure occurred for collection email_logs: {e.details}")
        return True

    @classmethod
    def find_by_recipient(cls, recipient_email: str) -> List[Dict[str, Any]]:
        """
        Find email logs by recipient email

        Args:
            recipient_email: Email address of the recipient

        Returns:
            List of matching email logs
        """
        return list(cls.collection().find({cls.RECIPIENT_EMAIL_FIELD: recipient_email}).sort(cls.CREATED_AT_FIELD, -1))

    @classmethod
    def find_by_status(cls, status: str) -> List[Dict[str, Any]]:
        """
        Find email logs by status

        Args:
            status: Email delivery status

        Returns:
            List of matching email logs
        """
        return list(cls.collection().find({cls.STATUS_FIELD: status}).sort(cls.CREATED_AT_FIELD, -1))

    @classmethod
    def find_by_message_id(cls, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Find email log by message ID

        Args:
            message_id: Unique message ID assigned by email provider

        Returns:
            Email log or None if not found
        """
        return cls.collection().find_one({cls.MESSAGE_ID_FIELD: message_id})

    @classmethod
    def update_status(cls, message_id: str, status: str, error: Optional[str] = None) -> bool:
        """
        Update email status

        Args:
            message_id: Unique message ID assigned by email provider
            status: New status
            error: Error message if applicable

        Returns:
            True if update was successful, False otherwise
        """
        update_data = {cls.STATUS_FIELD: status}
        if error:
            update_data["error"] = error

        result = cls.collection().update_one({cls.MESSAGE_ID_FIELD: message_id}, {"$set": update_data})

        return result.modified_count > 0
