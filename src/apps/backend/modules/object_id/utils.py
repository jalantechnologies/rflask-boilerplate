from bson import ObjectId


def object_id_validate(v: ObjectId | str) -> ObjectId:
    if isinstance(v, str):
        if not ObjectId.is_valid(v):
            raise ValueError(f"{v} is not a valid ObjectId")
        return ObjectId(v)
    elif isinstance(v, ObjectId):
        return v
