from typing import List

from bson import ObjectId

from modules.comment.errors import CommentNotFoundError, DatabaseError
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import Comment


class CommentReader:
    @staticmethod
    def get_comments_by_task_id(task_id: str) -> List[Comment]:
        try:
            task_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
            comment_bson_list = list(CommentRepository.collection().find({"task_id": task_id}))
            if not comment_bson_list:
                raise CommentNotFoundError(f"No comments found for task with ID {task_id}.")

            return [CommentModel.from_bson(comment) for comment in comment_bson_list]

        except Exception as e:
            raise DatabaseError(f"An error occurred while fetching comments for task ID {task_id}: {str(e)}")
