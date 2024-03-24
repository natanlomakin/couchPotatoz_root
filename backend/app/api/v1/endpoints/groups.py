from fastapi import APIRouter
from api.v1.models.groups import retrive_searched_group, retrive_all_groups, retrive_all_groups_chat_ids, retrive_single_group, create_group, update_group_data, remove_group
from api.v1.schemas.group import GroupBase, UpadateGroupBase

router = APIRouter()


@router.get("/", response_description="Retrive all groups")
async def get_groups():
    groups = await retrive_all_groups()
    if groups:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all groups from database",
            "data": groups[0],
            "groups_ids": groups[1]
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no groups",
        "data": False
    }


@router.get("/{id}", response_description="Retrived single group data")
async def get_group(id: str):
    group = await retrive_single_group(id)
    if group:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived group with id {id} from database",
            "data": group
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no group with id {id}",
        "data": False
    }


@router.get("/search/{searchValue}", response_description="Retrived single group data by search value")
async def get_group_by_search(searchValue: str):
    groups = await retrive_searched_group(searchValue)
    if groups:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived group with id {id} from database",
            "data": groups[0],
            "groups_ids": groups[1]
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no group with id {id}",
        "data": False
    }

@router.get("/chat/ids", response_description="Retrive all groups chat ids")
async def get_groups_chat_ids():
    groupsChatIds = await retrive_all_groups_chat_ids()
    if groupsChatIds:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all groups from database",
            "data": groupsChatIds,
            
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no groups",
        "data": False
    }

@router.post("/", response_description="Addede new group data to database")
async def add_group(group: GroupBase):
    new_group = await create_group(group)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"Added new group to the database",
        "data": new_group
    }


@router.put("/{id}", response_description="Group with id {id} was updated")
async def update_group(id: str, data: UpadateGroupBase):
    updated_group = await update_group_data(id, data)
    if updated_group:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Group with ID: {id} was updated",
            "data": updated_group
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Gruop with id {id} doesn't exist",
        "data": False
    }


@router.delete("/{id}", response_description="Delted group data from database")
async def delete_group(id: str):
    deleted_group = await remove_group(id)
    if deleted_group:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Group with ID: {id} was deleted",
            "data": deleted_group
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Gruop with id {id} doesn't exist",
        "data": deleted_group
    }
