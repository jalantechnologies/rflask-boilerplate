from datetime import datetime, timezone

from bson import ObjectId

from modules.comment.errors import CommentCreationError, CommentUpdateError
from modules.comment.internal.comment_util import validate_task_and_user_exists
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import Comment, CreateCommentParams


class CommentWriter:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        try:
            validate_task_and_user_exists(params.task_id, params.user_id)
            comment_model = CommentModel(
                id=None, task_id=params.task_id, user_id=params.user_id, content=params.content
            )

            comment_bson = comment_model.to_bson()

            query = CommentRepository.collection().insert_one(comment_bson)

            comment_bson = CommentRepository.collection().find_one({"_id": query.inserted_id})

            return CommentModel.from_bson(comment_bson)

        except Exception as e:
            raise CommentCreationError(f"An error occurred while creating the comment: {str(e)}")

    @staticmethod
    def update_comment(comment_id: str, new_content: str) -> bool:
        try:
            comment = CommentRepository.collection().find_one({"_id": ObjectId(comment_id)})
            if not comment:
                raise CommentUpdateError(f"Comment with ID {comment_id} not found.")

            updated_data = {"content": new_content, "updated_at": datetime.now(timezone.utc)}

            result = CommentRepository.collection().update_one({"_id": ObjectId(comment_id)}, {"$set": updated_data})

            return result.modified_count > 0

        except Exception as e:
            raise CommentUpdateError(f"An error occurred while updating the comment: {str(e)}")
