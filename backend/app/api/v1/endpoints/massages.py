from datetime import datetime
import json
from fastapi import WebSocketDisconnect, WebSocket, APIRouter, Depends, HTTPException, status, Body
from api.deps.database import personal_message_websocket, retrive_all_massages, retrive_single_massage, create_massage, remove_massage, update_massage_data
from api.v1.schemas.massage import MassageBase, UpadateMassage
from api.v1.serializers.massageSerializer import massageEntitny
from ...deps.auth_bearer import JWTBearer
from ..websockets.personal_messages.connection_manager import ConectionManager

router = APIRouter()
message_manager = ConectionManager()


@router.get("/", dependencies=[Depends(JWTBearer())], response_description="retrived all massages")
async def get_massages():
    massages = await retrive_all_massages()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Massages data retrieved successfully",
        "data": massages
    }


@router.get("/{id}", dependencies=[Depends(JWTBearer())], response_description="retrived spacific massage")
async def get_massage(id: str):
    massage = await retrive_single_massage(id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Massage data retrieved successfully",
        "data": massage
    }


@router.post("/", dependencies=[Depends(JWTBearer())], response_description="New massage created")
async def create_new_massage(massage: MassageBase):
    new_massage = await create_massage(massage)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Massage created successfully",
        "data": new_massage
    }


@router.put("/{id}", dependencies=[Depends(JWTBearer())], response_description="Massage data has been updated")
async def update_massage(id: str, massage: UpadateMassage):
    updated_massage = await update_massage_data(id, massage)
    if updated_massage:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Massage with ID: {id} updated",
            "data": updated_massage
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Massage with id {id} doesn't exist",
        "data": False
    }


@router.delete("/{id}", dependencies=[Depends(JWTBearer())], response_description="Massage data delted")
async def delete_massage(id: str):
    deleted_massage = await remove_massage(id)
    if deleted_massage:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Massage with ID: {id} removed",
            "data": deleted_massage
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Massage with id {id} doesn't exist",
        "data": False
    }


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    message = await personal_message_websocket(websocket, client_id)
    print(message)
