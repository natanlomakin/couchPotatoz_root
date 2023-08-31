from pymongo import mongo_client, ReturnDocument
from fastapi import HTTPException, status, WebSocket, WebSocketDisconnect
from typing import List, Union
from json import dumps
import random
from config.settings import settings
from api.v1.schemas.user import *
from api.v1.schemas.platform import *
from api.v1.schemas.friend import *
from api.v1.schemas.massage import *
from api.v1.schemas.library import *
from api.v1.schemas.group import *
from api.v1.schemas.game import *
from api.v1.schemas.group_member import *
from api.v1.schemas.group_message import *
from api.v1.schemas.private_chat import *
from api.v1.serializers.userSerializer import userFriendEntity, userEntitny, listUserEntity, userUpdatedEntity, signupUserEntity
from api.v1.serializers.platformSerializer import platformEntitny
from api.v1.serializers.friendSerializer import friendEntitny, updateFriendEntity
from api.v1.serializers.massageSerializer import massageEntitny, updateMassageEntity
from api.v1.serializers.librarySerializer import libraryEntitny
from api.v1.serializers.groupSerializer import groupEntitny, updateGroupEntity
from api.v1.serializers.gameSerializer import gameEntitny, UpdateGameEntity
from api.v1.serializers.group_memberSerializer import group_memberEntitny, updateGroup_memberEntity
from api.v1.serializers.group_massageSerializer import group_massageEntitny
from api.v1.serializers.privateChatSerializer import privateChatEntitny
from bson.objectid import ObjectId
from api.deps.auth import get_hashed_password, verify_password, create_access_token, create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, status, HTTPException, Depends
from ..v1.websockets.personal_messages.connection_manager import ConectionManager as PersonalConectionManager
from ..v1.websockets.group_messages.connection_manager import ConectionManager as GroupConectionManager
import re

client = mongo_client.MongoClient(settings.DATABASE_URL)
db = client.potato
#############################################
user_collection = db.user


async def retrive_users() -> List[UserBase]:
    users = []
    cursor = user_collection.find()
    for document in cursor:
        users.append(User(**document))
    return users


async def retrive_single_user(id: str) -> UserBase:
    user = user_collection.find_one(
        {'_id': ObjectId(str(id))})
    user = userEntitny(user)
    return user


async def retrive_single_user_friend(id: str) -> UserFriend:
    user = user_collection.find_one(
        {'_id': ObjectId(str(id))})
    user = userFriendEntity(user)
    return user


async def add_new_user(new_user: CreateUser) -> CreateUser:
    new_user.createdAt = datetime.utcnow()
    new_user.password = get_hashed_password(new_user.password)
    _id = user_collection.insert_one(dict(new_user))
    user = user_collection.find_one({"_id": ObjectId(str(_id.inserted_id))})
    user = signupUserEntity(user)
    return user


async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"email": str(form_data.email)})
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_401_UNAUTHORIZED)
    hashed_password = user['password']
    if not verify_password(form_data.password, hashed_password):
        raise Exception(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="incorrect email or password")
    tokens = {"access_token": create_access_token(
        str(user['_id'])), "refresh_token": create_refresh_token(str(user['_id']))}
    return tokens


async def remove_user(id: str) -> bool:
    user = user_collection.find_one({'_id': ObjectId(str(id))})
    if user:
        user_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False


async def update_user_data(id: str, data: UpdateUser):
    user = user_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
                                               "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if user:
        user = userUpdatedEntity(user)
        return user
    return False
#############################################
platform_collection = db.platform


async def get_platforms():
    platforms = []
    cursor = platform_collection.find()
    for document in cursor:
        platforms.append(PlatformBase(**document))
    return platforms


async def get_platform(id: str) -> PlatformBase:
    platform = platform_collection.find_one(
        {'_id': ObjectId(str(id))})
    platform = platformEntitny(platform)
    return platform


async def create_platform(new_platform: PlatformBase) -> PlatformBase:
    new_platform.createdAt = datetime.utcnow()
    _id = platform_collection.insert_one(dict(new_platform))
    platform = platform_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    platform = platformEntitny(platform)
    return platform


async def remove_platform(id: str) -> bool:
    platform = platform_collection.find_one({'_id': ObjectId(str(id))})
    if platform:
        platform_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False
#############################################

friend_collection = db.friend


async def retrive_all_friends(userId: str):
    friends = []
    cursor = friend_collection.find({"source_id": str(userId)})
    for document in cursor:
        friends.append(FriendBase(**document))
    return friends


async def retrive_friend(id: str) -> FriendBase:
    friend = friend_collection.find_one(
        {'_id': ObjectId(str(id))})
    friend = friendEntitny(friend)
    return friend


async def create_friend(new_friend: FriendBase) -> FriendBase:
    new_friend.createdAt = datetime.utcnow()
    _id = friend_collection.insert_one(dict(new_friend))
    friend = friend_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    friend = friendEntitny(friend)
    return friend


async def update_friend_data(id: str, data: UpdateFriend):
    friend = friend_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if friend:
        friend = updateFriendEntity(friend)
        return friend
    return False


async def remove_friendship(id: str) -> bool:
    friend = friend_collection.find_one({'_id': ObjectId(str(id))})
    if friend:
        friend_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False
#############################################
massage_collection = db.massage


""" async def retrive_all_massages():
    messages = []
    cursor = massage_collection.find()
    for document in cursor:
        messages.append(MassageBase(**document))
    return messages """


def sort_by_createdAt(obj):
    return obj.createdAt


async def retrive_user_messages(source_id: str, target_id: str):
    messages_source = []
    messages_target = []
    messages = []
    cursor_source = massage_collection.find(
        {"source_id": str(source_id), "target_id": str(target_id)})
    cursor_target = massage_collection.find(
        {"target_id": str(source_id), "source_id": str(target_id)})
    for document in cursor_source:
        messages_source.append(MassageBase(**document))
    for document in cursor_target:
        messages_target.append(MassageBase(**document))
    messages = messages_source + messages_target
    sorted_messages = sorted(messages, key=sort_by_createdAt)
    return sorted_messages


async def retrive_single_massage(id: str):
    message = massage_collection.find_one({"_id": ObjectId(str(id))})
    if message:
        message = massageEntitny(message)
        return message
    return HTTPException(status_code=404, detail="Massage not found")


async def create_massage(new_massage: MassageBase) -> MassageBase:
    new_massage.createdAt = datetime.utcnow()
    print(new_massage)
    _id = massage_collection.insert_one(dict(new_massage))
    massage = massage_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    massage = massageEntitny(massage)
    return massage


async def update_massage_data(id: str, data: UpadateMassage):
    massage = massage_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
                                                     "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if massage:
        massage = updateMassageEntity(massage)
        return massage
    return False


async def remove_massage(id: str) -> bool:
    massage = massage_collection.find_one({'_id': ObjectId(str(id))})
    if massage:
        massage_collection.delete_one({'_id': ObjectId(str(id))})
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
        """ await message_manager.broadcast("left the chat") """

#############################################
private_chat_collection = db.private_chat


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

""" async def personal_message_websocket(websocket: WebSocket, source_id: str, target_id: str):
    await message_manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            newMessage = await create_massage({"source_id": source_id,
                                               "target_id": target_id, "massage_content": data, "createdAt": now})
            await message_manager.broadcast(dumps(data))

    except WebSocketDisconnect:
        message_manager.disconect(websocket)
        message = {"time": current_time,
                   "clientId": source_id, "message": "offline"} """

#############################################
group_collection = db.group


async def retrive_all_groups():
    groups = []
    groupIds = []
    cursor = group_collection.find()
    for document in cursor:
        groupIds.append(str(document["_id"]))
        groups.append(GroupBase(**document))
    return groups, groupIds


async def retrive_single_group(id: str) -> GroupBase:
    group = group_collection.find_one({"_id": ObjectId(str(id))})
    if group:
        group = groupEntitny(group)
        return group
    return False


async def retrive_searched_group(searchValue: str):
    groups = []
    groupIds = []
    cursor = group_collection.find(
        {"title": {"$regex": searchValue, "$options": "i"}})
    print(cursor.retrieved)
    for document in cursor:

        groupIds.append(str(document["_id"]))
        print(groupIds)
        groups.append(GroupBase(**document))
    return groups, groupIds

""" async def retrive_searched_group(searchValue: str) -> GroupBase:
    print(searchValue)
    group = group_collection.find_one({"title": str(searchValue)})
    print(group)
    if group:
        group = groupEntitny(group)
        return group
    return False """


async def create_group(group: GroupBase) -> GroupBase:
    group.createdAt = datetime.utcnow()
    _id = group_collection.insert_one(dict(group))
    new_group = group_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_group = groupEntitny(new_group)
    return new_group


async def update_group_data(id: str, data: UpadateGroupBase):
    group = group_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if group:
        group = updateGroupEntity(group)
        return group
    return False


async def remove_group(id: str):
    deleted_group = group_collection.find_one_and_delete(
        {"_id": ObjectId(str(id))})
    if deleted_group:
        return True
    return False


#############################################
group_massage_collection = db.group_massage
group_message_manager = GroupConectionManager()


async def retrive_group_masseges(id: str) -> GroupMessageBase:
    group_massages = []
    cursor = group_massage_collection.find({"group_id": str(id)})
    for document in cursor:
        group_massages.append(GroupMessageBase(**document))
    return group_massages


async def retrive_single_group_massage(groupId: str, userId: str) -> GroupMessageBase:
    group_massage = []
    cursor = group_massage_collection.find({"group_id": str(groupId)})
    for document in cursor:
        if document["user_id"] == str(userId):
            group_massage.append(GroupMessageBase(**document))
    return group_massage


async def create_group_massage(massage: GroupMessageBase) -> GroupMessageBase:
    massage.createdAt = datetime.utcnow()
    _id = group_massage_collection.insert_one(dict(massage))
    new_massage = group_massage_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_massage = group_massageEntitny(new_massage)
    return new_massage


async def delete_group_massage_data(groupId: str):
    deleted_group_massage = group_massage_collection.find_one_and_delete(
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
#############################################
group_member_collection = db.group_member


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
#############################################
library_collection = db.library


async def retrive_all_librarys(userId: str):
    librarys = []
    library_ids = []
    cursor = library_collection.find({"user_id": str(userId)})
    for document in cursor:
        librarys.append(LibraryBase(**document))
        library_ids.append(str(document["_id"]))
    return librarys, library_ids


async def retrive_single_library(id: str) -> LibraryBase:
    library = library_collection.find_one({"_id": ObjectId(str(id))})
    if library:
        library = libraryEntitny(library)
        return library
    return False


async def create_library(library: LibraryBase) -> LibraryBase:
    library.createdAt = datetime.utcnow()
    _id = library_collection.insert_one(dict(library))
    new_library = library_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_library = libraryEntitny(new_library)
    return new_library


async def delete_library(id: str) -> bool:
    library = library_collection.find_one({'_id': ObjectId(str(id))})
    if library:
        library_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False
#############################################
game_collection = db.game


async def retrive_games() -> GameBase:
    games = []
    game_Ids = []
    cursor = game_collection.find()
    for document in cursor:
        game_Ids.append(str(document["_id"]))
        games.append(GameBase(**document))
    return games, game_Ids


async def retrive_single_game(id: str) -> GameBase:
    game = game_collection.find_one({"_id": ObjectId(str(id))})
    if game:
        game = gameEntitny(game)
        return game
    return False


async def create_game(game: GameBase) -> GameBase:
    game.createdAt = datetime.utcnow()
    _id = game_collection.insert_one(dict(game))
    new_game = game_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_game = gameEntitny(new_game)
    return new_game


async def update_game_data(id: str, data: UpdateGameBase):
    game = game_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if game:
        game = UpdateGameEntity(game)
        return game
    return False


async def remove_game(id: str):
    deleted_game = game_collection.find_one_and_delete(
        {"_id": ObjectId(str(id))})
    if deleted_game:
        return True
    return False

#############################################
