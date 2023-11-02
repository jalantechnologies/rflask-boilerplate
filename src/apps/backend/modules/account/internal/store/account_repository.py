from pymongo import MongoClient  # type: ignore
from pymongo.collection import Collection  # type: ignore

from .account_model import AccountModel


class AccountRepository:
  __collection_name__ = AccountModel.get_collection_name()
  account_db: Collection

  @staticmethod
  def create_db_connection() -> Collection:
    # todo get this from config
    connection_uri = "mongodb+srv://aks97cs:5HCKHGcnIRquGJmd@cluster0.ddn1klz.mongodb.net/?retryWrites=true&w=majority"
    db_name = "airbnd"
    client = MongoClient(connection_uri)
    collection = client[db_name][AccountRepository.__collection_name__]
    # Create index if not exist
    collection.create_index("username")

    AccountRepository.account_db = collection

    return client
