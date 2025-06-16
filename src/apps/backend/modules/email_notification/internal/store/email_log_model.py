from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId


@dataclass
class EmailLogModel:
    """Data model for email logs stored in the database"""

    id: Optional[str]
    message_id: str
    sender_email: str
    sender_name: Optional[str]
    recipient_emails: List[Dict[str, str]]
    subject: str
    body: str
    content_type: str
    status: str
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def get_collection_name() -> str:
        """
        Get the name of the MongoDB collection for this model

        Returns:
            Collection name as string
        """
        return "email_logs"

    def to_bson(self) -> Dict[str, Any]:
        """
        Convert model to BSON document for MongoDB storage

        Returns:
            Dict representing the model in BSON-compatible format
        """
        result = asdict(self)

        if self.id:
            result["_id"] = ObjectId(self.id)
            del result["id"]
        else:
            del result["id"]

        return result

    @staticmethod
    def from_bson(data: Dict[str, Any]) -> "EmailLogModel":
        """
        Create model from BSON document

        Args:
            data: BSON document from MongoDB

        Returns:
            EmailLogModel instance
        """
        if "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]

        return EmailLogModel(**data)
