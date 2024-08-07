from pymongo.collection import Collection

from modules.account.internal.store.account_model import AccountModel
from modules.application.repository import ApplicationRepository


class AccountRepository(ApplicationRepository):
    collection_name = AccountModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("username")
        return True
