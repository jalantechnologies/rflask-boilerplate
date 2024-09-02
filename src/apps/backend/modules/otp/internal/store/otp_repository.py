from modules.application.repository import ApplicationRepository
from modules.otp.internal.store.otp_model import OtpModel

from pymongo.collection import Collection

class OtpRepository(ApplicationRepository):
    collection_name = OtpModel.get_collection_name()
    
    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        collection.create_index("phone_number")
        return True
