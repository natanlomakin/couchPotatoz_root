from api.v1.serializers.privateChatSerializer import privateChatEntitny
from api.v1.schemas.private_chat import *
from api.deps.database import private_chat_collection
from fastapi import HTTPException
import random


async def retrive_single_private_chat(user1: str, user2: str):
    chat = private_chat_collection.find_one(
        {'user1': str(user1), 'user2': str(user2)})
    if chat:
        print(chat)
        chat = privateChatEntitny(chat)
        return chat
    chat = private_chat_collection.find_one(
        {'user1': str(user2), 'user2': str(user1)})
    if chat:
        print(chat)
        chat = privateChatEntitny(chat)
        return chat
    return HTTPException(status_code=404, detail="chat not found")


async def create_private_chat(new_chat: PrivateChatBase) -> PrivateChatBase:
    new_chat.createdAt = datetime.utcnow()
    new_chat.chatId = str(random.randrange(1000, 9999))
    _id = private_chat_collection.insert_one(dict(new_chat))
    chat = private_chat_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    chat = privateChatEntitny(chat)
    return chat


async def delete_private_chat(user1: str, user2: str):
    chat = private_chat_collection.find_one(
        {'user1': str(user1), 'user2': str(user2)})
    if chat:
        private_chat_collection.delete_one({"_id": ObjectId(str(chat['_id']))})
        return True
    chat = private_chat_collection.find_one(
        {'user1': str(user2), 'user2': str(user1)})
    if chat:
        private_chat_collection.delete_one({"_id": ObjectId(str(chat['_id']))})
        return True
    return False
