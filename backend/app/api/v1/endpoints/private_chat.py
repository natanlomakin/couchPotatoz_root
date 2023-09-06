from fastapi import APIRouter, Depends, HTTPException, status, Body
from api.v1.models.private_chat import create_private_chat, delete_private_chat, retrive_single_private_chat
from api.v1.schemas.private_chat import PrivateChatBase
from ...deps.auth_bearer import JWTBearer

router = APIRouter()


@router.get("/{user1}/{user2}", dependencies=[Depends(JWTBearer())], response_description="retrived spacific chat")
async def get_private_chat(user1: str, user2: str):
    chat = await retrive_single_private_chat(user1, user2)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "chat data retrieved successfully",
        "data": chat
    }


@router.post("/", dependencies=[Depends(JWTBearer())], response_description="New chat created")
async def create_new_private_chat(chat: PrivateChatBase):
    new_chat = await create_private_chat(chat)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "private chat created successfully",
        "data": new_chat
    }


@router.delete("/{user1}/{user2}", dependencies=[Depends(JWTBearer())], response_description="chat data delted")
async def remove_private_chat(user1: str, user2: str):
    deleted_private_chat = await delete_private_chat(user1, user2)
    if deleted_private_chat:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"",
            "data": deleted_private_chat
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"",
        "data": False
    }
