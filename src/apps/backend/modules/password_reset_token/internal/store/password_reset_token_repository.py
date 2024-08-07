from pymongo.collection import Collection

from modules.application.repository import ApplicationRepository
from modules.password_reset_token.internal.store.password_reset_token_model import PasswordResetTokenModel


class PasswordResetTokenRepository(ApplicationRepository):
    collection_name = PasswordResetTokenModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("token")
        return True
