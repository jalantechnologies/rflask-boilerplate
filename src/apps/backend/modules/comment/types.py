from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateCommentParams:
    task_id: str
    user_id: str
    content: str


@dataclass(frozen=True)
class Comment:
    id: str
    task_id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CommentErrorCode:
    NOT_FOUND = "COMMENT_NOT_FOUND"
    BAD_REQUEST = "COMMENT_BAD_REQUEST"
    UPDATE_ERROR = "COMMENT_UPDATE_ERROR"
    CREATION_ERROR = "COMMENT_CREATION_ERROR"
    SERVICE_ERROR = "COMMENT_SERVICE_ERROR"
    DATABASE_ERROR = "COMMENT_DATABASE_ERROR"
