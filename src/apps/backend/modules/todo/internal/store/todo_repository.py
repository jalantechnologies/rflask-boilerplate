from pymongo.collection import Collection

from modules.application.repository import ApplicationRepository
from modules.todo.internal.store.todo_model import TodoModel


class TodoRepository(ApplicationRepository):
    collection_name = TodoModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("account_id")
        return True
