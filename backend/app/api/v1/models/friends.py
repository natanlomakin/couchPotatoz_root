from api.v1.schemas.friend import *
from api.v1.serializers.friendSerializer import friendEntitny, updateFriendEntity
from api.deps.database import friend_collection
from pymongo import ReturnDocument


async def retrive_all_friends(userId: str):
    friends = []
    cursor = friend_collection.find({"source_id": str(userId)})
    for document in cursor:
        friends.append(FriendBase(**document))
    return friends


async def retrive_friend(id: str) -> FriendBase:
    friend = friend_collection.find_one(
        {'_id': ObjectId(str(id))})
    friend = friendEntitny(friend)
    return friend


async def create_friend(new_friend: FriendBase) -> FriendBase:
    new_friend.createdAt = datetime.utcnow()
    _id = friend_collection.insert_one(dict(new_friend))
    friend = friend_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    friend = friendEntitny(friend)
    return friend


async def update_friend_data(id: str, data: UpdateFriend):
    friend = friend_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if friend:
        friend = updateFriendEntity(friend)
        return friend
    return False


async def remove_friendship(id: str) -> bool:
    friend = friend_collection.find_one({'_id': ObjectId(str(id))})
    if friend:
        friend_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False
