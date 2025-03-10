from bson import ObjectId

from modules.account.internal.store.account_repository import AccountRepository
from modules.comment.errors import CommentCreationError
from modules.task.internal.store.task_repository import TaskRepository


def validate_task_and_user_exists(task_id: str, user_id: str):
    try:
        task_id = ObjectId(task_id)
        user_id = ObjectId(user_id)

        task = TaskRepository.collection().find_one({"_id": task_id})
        if not task:
            raise CommentCreationError(f"Task with ID {task_id} not found.")
        user = AccountRepository.collection().find_one({"_id": user_id})
        if not user:
            raise CommentCreationError(f"User with ID {user_id} not found.")

    except Exception as e:
        raise CommentCreationError(f"Error validating task and user: {str(e)}")
