from api.v1.schemas.library import *
from api.v1.serializers.librarySerializer import libraryEntitny
from api.deps.database import library_collection


async def retrive_all_librarys(userId: str):
    librarys = []
    library_ids = []
    cursor = library_collection.find({"user_id": str(userId)})
    for document in cursor:
        librarys.append(LibraryBase(**document))
        library_ids.append(str(document["_id"]))
    return librarys, library_ids


async def retrive_single_library(id: str) -> LibraryBase:
    library = library_collection.find_one({"_id": ObjectId(str(id))})
    if library:
        library = libraryEntitny(library)
        return library
    return False


async def create_library(library: LibraryBase) -> LibraryBase:
    library.createdAt = datetime.utcnow()
    _id = library_collection.insert_one(dict(library))
    new_library = library_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_library = libraryEntitny(new_library)
    return new_library


async def delete_library(id: str) -> bool:
    library = library_collection.find_one({'_id': ObjectId(str(id))})
    if library:
        library_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False
