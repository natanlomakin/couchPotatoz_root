from api.v1.schemas.massage import *
from api.v1.serializers.massageSerializer import massageEntitny, updateMassageEntity
from api.deps.database import message_collection
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from api.v1.websockets.personal_messages.connection_manager import ConectionManager as PersonalConectionManager
from json import dumps


personal_message_manager = PersonalConectionManager()


def sort_by_createdAt(obj):
    return obj.createdAt


async def retrive_user_messages(source_id: str, target_id: str):
    messages_source = []
    messages_target = []
    messages = []
    cursor_source = message_collection.find(
        {"source_id": str(source_id), "target_id": str(target_id)})
    cursor_target = message_collection.find(
        {"target_id": str(source_id), "source_id": str(target_id)})
    for document in cursor_source:
        messages_source.append(MassageBase(**document))
    for document in cursor_target:
        messages_target.append(MassageBase(**document))
    messages = messages_source + messages_target
    sorted_messages = sorted(messages, key=sort_by_createdAt)
    return sorted_messages


async def retrive_single_massage(id: str):
    message = message_collection.find_one({"_id": ObjectId(str(id))})
    if message:
        message = massageEntitny(message)
        return message
    return HTTPException(status_code=404, detail="Massage not found")


async def create_massage(new_massage: MassageBase) -> MassageBase:
    new_massage.createdAt = datetime.utcnow()
    print(new_massage)
    _id = message_collection.insert_one(dict(new_massage))
    massage = message_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    massage = massageEntitny(massage)
    return massage


async def update_massage_data(id: str, data: UpadateMassage):
    massage = message_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
                                                     "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if massage:
        massage = updateMassageEntity(massage)
        return massage
    return False


async def remove_massage(id: str) -> bool:
    massage = message_collection.find_one({'_id': ObjectId(str(id))})
    if massage:
        message_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False


personal_message_manager = PersonalConectionManager()


async def personal_message_websocket(websocket: WebSocket):
    await personal_message_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await personal_message_manager.broadcast(dumps(data))

    except WebSocketDisconnect:
        personal_message_manager.disconect(websocket)
