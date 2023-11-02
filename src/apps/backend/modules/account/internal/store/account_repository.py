from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore

from modules.account.internal.store.account_model import AccountModel
from modules.config.config_service import ConfigService


class AccountRepository:
  __collection_name__ = AccountModel.get_collection_name()
  account_db: Collection

  @staticmethod
  def create_db_connection() -> Collection:
    connection_uri = ConfigService.get_db_uri()
    db_name = ConfigService.get_db_name()
    client = MongoClient(connection_uri)
    collection = client[db_name][AccountRepository.__collection_name__]
    # Create index if not exist
    collection.create_index("username")

    AccountRepository.account_db = collection

    return client
