from typing import List

from modules.comment.errors import CommentCreationError, CommentNotFoundError, CommentServiceError, CommentUpdateError
from modules.comment.internal.comment_reader import CommentReader
from modules.comment.internal.comment_writer import CommentWriter
from modules.comment.types import Comment, CreateCommentParams


class CommentService:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        try:
            comment = CommentWriter.create_comment(params=params)
            return comment

        except CommentCreationError as e:
            raise e

        except Exception as e:
            raise CommentCreationError(f"An unexpected error occurred while creating the comment: {str(e)}")

    @staticmethod
    def get_comments_by_task_id(task_id: str) -> List[Comment]:
        try:
            comment_list = CommentReader.get_comments_by_task_id(task_id=task_id)
            if not comment_list:
                raise CommentNotFoundError(f"No comments found for task ID {task_id}.")
            return comment_list

        except CommentNotFoundError as e:
            raise e

        except Exception as e:
            raise CommentServiceError(f"Error occurred in CommentService: {str(e)}")

    @staticmethod
    def update_comment(comment_id: str, new_content: str) -> bool:
        try:
            return CommentWriter.update_comment(comment_id=comment_id, new_content=new_content)
        except CommentUpdateError as e:
            raise e
        except Exception as e:
            raise CommentUpdateError(f"An unexpected error occurred while updating the comment: {str(e)}")
