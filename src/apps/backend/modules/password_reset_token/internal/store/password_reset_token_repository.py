from pymongo import MongoClient 
from pymongo.collection import Collection 
from pymongo.server_api import ServerApi 

from modules.password_reset_token.internal.store.password_reset_token_model import PasswordResetTokenModel  
from modules.config.config_service import ConfigService
from modules.logger.logger import Logger

class PasswordResetTokenRepository:
    __collection_name__ = PasswordResetTokenModel.get_collection_name()
    password_reset_token_db: Collection

    @staticmethod
    def create_db_connection() -> Collection:
        connection_uri = ConfigService.get_db_uri()
        Logger.info(message=f"Connecting to db:: {connection_uri}")
        client = MongoClient(connection_uri, server_api=ServerApi('1'))
        database = client.get_database()
        collection = database[PasswordResetTokenRepository.__collection_name__]
        collection.create_index("token") 

        PasswordResetTokenRepository.password_reset_token_db = collection
        return client
