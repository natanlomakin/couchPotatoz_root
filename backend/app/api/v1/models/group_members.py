from api.v1.schemas.group_member import *
from api.v1.serializers.group_memberSerializer import group_memberEntitny, updateGroup_memberEntity
from api.deps.database import group_member_collection
from pymongo import ReturnDocument


async def retrive_group_members(id: str) -> GroupMemberBase:
    group_members = []
    cursor = group_member_collection.find({"group_id": str(id)})
    for document in cursor:
        group_members.append(GroupMemberBase(**document))
    return group_members


async def retrive_single_group_member(memberId: str, groupId: str) -> GroupMemberBase:
    group_member = []
    cursor = group_member_collection.find({"group_id": str(groupId)})
    for document in cursor:
        if document["user_id"] == str(memberId):
            group_member.append(GroupMemberBase(**document))
    return group_member


async def create_group_member(member: GroupMemberBase) -> GroupMemberBase:
    member.createdAt = datetime.utcnow()
    _id = group_member_collection.insert_one(dict(member))
    new_member = group_member_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_member = group_memberEntitny(new_member)
    return new_member


async def update_group_member_data(groupId: str, memberId: str, data: UpdateGroupMemberBase) -> UpdateGroupMemberBase:
    group_member = group_member_collection.find_one_and_update({'user_id': str(memberId), 'group_id': str(groupId)}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if group_member:
        group_member = updateGroup_memberEntity(group_member)
        return group_member
    return False


async def delete_group_member_data(groupId: str, memberId: str):
    deleted_group_member = group_member_collection.find_one_and_delete(
        {'user_id': str(memberId), 'group_id': str(groupId)})
    if deleted_group_member:
        return True
    return False
