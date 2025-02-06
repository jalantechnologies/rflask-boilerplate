from pymongo.collection import Collection

from modules.task.internal.store.task_model import TaskModel
from modules.application.repository import ApplicationRepository


class TaskRepository(ApplicationRepository):
    collection_name = TaskModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("account")
        return True
