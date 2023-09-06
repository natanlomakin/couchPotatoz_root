from api.v1.schemas.group_message import *
from api.v1.serializers.group_massageSerializer import group_massageEntitny
from api.deps.database import group_message_collection
from api.v1.websockets.group_messages.connection_manager import ConectionManager as GroupConectionManager
from fastapi import WebSocket, WebSocketDisconnect
from json import dumps


group_message_manager = GroupConectionManager()


async def retrive_group_masseges(id: str) -> GroupMessageBase:
    group_massages = []
    cursor = group_message_collection.find({"group_id": str(id)})
    for document in cursor:
        group_massages.append(GroupMessageBase(**document))
    return group_massages


async def retrive_single_group_massage(groupId: str, userId: str) -> GroupMessageBase:
    group_massage = []
    cursor = group_message_collection.find({"group_id": str(groupId)})
    for document in cursor:
        if document["user_id"] == str(userId):
            group_massage.append(GroupMessageBase(**document))
    return group_massage


async def create_group_massage(massage: GroupMessageBase) -> GroupMessageBase:
    massage.createdAt = datetime.utcnow()
    _id = group_message_collection.insert_one(dict(massage))
    new_massage = group_message_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_massage = group_massageEntitny(new_massage)
    return new_massage


async def delete_group_massage_data(groupId: str):
    deleted_group_massage = group_message_collection.find_one_and_delete(
        {"_id": ObjectId(str(groupId))})
    if deleted_group_massage:
        return True
    return False


async def group_message_websocket(websocket: WebSocket):
    await group_message_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await group_message_manager.broadcast(dumps(data))

    except WebSocketDisconnect:
        group_message_manager.disconect(websocket)
