from api.v1.serializers.groupSerializer import groupEntitny, updateGroupEntity
from api.v1.schemas.group import *
from api.deps.database import group_collection
from pymongo import ReturnDocument


async def retrive_all_groups():
    groups = []
    groupIds = []
    cursor = group_collection.find()
    for document in cursor:
        groupIds.append(str(document["_id"]))
        groups.append(GroupBase(**document))
    return groups, groupIds


async def retrive_single_group(id: str) -> GroupBase:
    group = group_collection.find_one({"_id": ObjectId(str(id))})
    if group:
        group = groupEntitny(group)
        return group
    return False


async def retrive_searched_group(searchValue: str):
    groups = []
    groupIds = []
    cursor = group_collection.find(
        {"title": {"$regex": searchValue, "$options": "i"}})
    print(cursor.retrieved)
    for document in cursor:

        groupIds.append(str(document["_id"]))
        print(groupIds)
        groups.append(GroupBase(**document))
    return groups, groupIds


async def create_group(group: GroupBase) -> GroupBase:
    group.createdAt = datetime.utcnow()
    _id = group_collection.insert_one(dict(group))
    new_group = group_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_group = groupEntitny(new_group)
    return new_group


async def update_group_data(id: str, data: UpadateGroupBase):
    group = group_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if group:
        group = updateGroupEntity(group)
        return group
    return False


async def remove_group(id: str):
    deleted_group = group_collection.find_one_and_delete(
        {"_id": ObjectId(str(id))})
    if deleted_group:
        return True
    return False
