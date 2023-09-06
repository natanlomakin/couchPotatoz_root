from api.v1.schemas.platform import *
from api.v1.serializers.platformSerializer import platformEntitny
from api.deps.database import platform_collection


async def get_platforms():
    platforms = []
    cursor = platform_collection.find()
    for document in cursor:
        platforms.append(PlatformBase(**document))
    return platforms


async def get_platform(id: str) -> PlatformBase:
    platform = platform_collection.find_one(
        {'_id': ObjectId(str(id))})
    platform = platformEntitny(platform)
    return platform


async def create_platform(new_platform: PlatformBase) -> PlatformBase:
    new_platform.createdAt = datetime.utcnow()
    _id = platform_collection.insert_one(dict(new_platform))
    platform = platform_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    platform = platformEntitny(platform)
    return platform


async def remove_platform(id: str) -> bool:
    platform = platform_collection.find_one({'_id': ObjectId(str(id))})
    if platform:
        platform_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False
