from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.database import retrive_all_friends, retrive_friend, create_friend, update_friend_data, remove_friendship
from api.v1.schemas.friend import FriendBase, UpdateFriend, CreateFriend
from api.v1.serializers.friendSerializer import friendEntitny

router = APIRouter()


@router.get("/", response_description="Retrive all friendships in the database")
async def get_all_friends():
    friends = await retrive_all_friends()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": friends
    }


@router.get("/{id}", response_description="Retrive friendship in the database")
async def get_friend(id: str):
    friend = await retrive_friend(id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Student data retrieved successfully",
        "data": friend
    }


@router.post("/", response_description="New friendship data added to the database")
async def add_friend(friend: FriendBase):
    new_friend = await create_friend(friend)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User created successfully",
        "data": new_friend
    }


@router.put("/{id}", response_description="Friendship data has been updated")
async def update_friendship(id: str, data: UpdateFriend):
    updated_friend = await update_friend_data(id, data)
    if updated_friend:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Friendship with ID: {id} updated",
            "data": updated_friend
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Friendship with id {id} doesn't exist",
        "data": False
    }


@router.delete("/{id}", response_description="Friendship data deleted")
async def delete_friendship(id: str):
    deleted_friendship = await remove_friendship(id)
    if deleted_friendship:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Friendship with ID: {id} removed",
            "data": deleted_friendship
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Friendship with id {id} doesn't exist",
        "data": False
    }
