from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.database import retrive_group_members, retrive_single_group_member, create_group_member, update_group_member_data, delete_group_member_data
from api.v1.schemas.group_member import GroupMemberBase, UpdateGroupMemberBase
from api.v1.serializers.group_memberSerializer import group_memberEntitny, updateGroup_memberEntity

router = APIRouter()


@router.get("/{id}", response_description="Retrive all group members from group with id {id}")
async def get_all_group_members(id: str):
    group_members = await retrive_group_members(id)
    if group_members:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all group members of group with id {id} from database",
            "data": group_members
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no group members in this group",
        "data": False
    }


@router.get("/{groupId}/{memberId}", response_description="Retrived a group member")
async def get_single_group_member(memberId: str, groupId: str):
    group_member = await retrive_single_group_member(memberId, groupId)
    if group_member:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived member with id {memberId} of group with id {groupId} from database",
            "data": group_member
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no group member with id {memberId} in this group",
        "data": False
    }


@router.post("/", response_description="Added new group member to the database")
async def add_group_member(member: GroupMemberBase):
    new_member = await create_group_member(member)
    if new_member:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Added new member to a group",
            "data": new_member
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Error while adding new group member",
        "data": False
    }


@router.put("/{groupId}/{memberId}", response_description="Member with id {memberId} from group with id {groupId} has been updated")
async def update_group_member(groupId: str, memberId: str, data: UpdateGroupMemberBase):
    updated_member = await update_group_member_data(groupId, memberId, data)
    if updated_member:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Member with id {memberId} from group with id {groupId} has been updated",
            "data": updated_member
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Error while updating group member",
        "data": False
    }


@router.delete("/{groupId}/{memberId}", response_description="Deleted member from group")
async def delete_group_member(groupId: str, memberId: str):
    deleted_member = await delete_group_member_data(groupId, memberId)
    if deleted_member:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Member with id {memberId} from group with id {groupId} has been deleted",
            "data": deleted_member
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Error while deleting group member",
        "data": False
    }
