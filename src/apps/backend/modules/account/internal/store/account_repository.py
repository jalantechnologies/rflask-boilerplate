from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore
from pymongo.server_api import ServerApi # type: ignore


from modules.account.internal.store.account_model import AccountModel
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger

class AccountRepository:
  __collection_name__ = AccountModel.get_collection_name()
  account_db: Collection

  @staticmethod
  def create_db_connection() -> Collection:
    connection_uri = ConfigService.get_value("URI", "MONGODB")
    Logger.info(message=f"Connecting to db:: {connection_uri}")
    client = MongoClient(connection_uri, server_api=ServerApi('1'))
    database = client.get_database()
    collection = database[AccountRepository.__collection_name__]
    # Create index if not exist
    collection.create_index("username")

    AccountRepository.account_db = collection
    return client
