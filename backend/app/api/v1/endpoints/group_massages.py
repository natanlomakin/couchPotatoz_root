from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps.database import retrive_group_masseges, retrive_single_group_massage, create_group_massage, delete_group_massage_data
from app.api.v1.schemas.group_massage import GroupMassageBase
from app.api.v1.serializers.group_massageSerializer import group_massageEntitny

router = APIRouter()


@router.get("/{groupId}", response_description="Retrive all the massages in the group")
async def get_all_group_massages(groupId: str):
    group_massages = await retrive_group_masseges(groupId)
    if group_massages:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all massages from group with id {groupId} from database",
            "data": group_massages
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no massages in group with id {groupId}",
        "data": False
    }


@router.get("/{groupId}/{userId}", response_description="Retrived single massage from group")
async def get_single_groupe_massage(groupId: str, userId: str):
    group_massage = await retrive_single_group_massage(groupId, userId)
    if group_massage:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived single massage from group with id {groupId} from database",
            "data": group_massage
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no massage in group with id {groupId}",
        "data": False
    }


@router.post("/", response_description="Added new group massage to the database")
async def add_new_massage(massage: GroupMassageBase):
    new_group_massage = await create_group_massage(massage)
    if new_group_massage:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Added new massage to group",
            "data": new_group_massage
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Error adding massage to group",
        "data": False
    }


@router.delete("/{massageId}", response_description="Remove group massage from database ")
async def delete_group_massage(massageId: str):
    deleted_massage = await delete_group_massage_data(massageId)
    if deleted_massage:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Removed massage with id {massageId} from database",
            "data": deleted_massage
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Massage with id {massageId} doesn't exist",
        "data": False
    }
