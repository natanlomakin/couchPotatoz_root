from fastapi import APIRouter
from api.v1.endpoints import users, platforms, friends, massages, librarys, groups, games, group_members, group_messages, private_chat

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    platforms.router, prefix="/platforms", tags=["platforms"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(
    massages.router, prefix="/messages", tags=["massages"])
api_router.include_router(
    librarys.router, prefix="/librarys", tags=["librarys"])
api_router.include_router(
    groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(
    games.router, prefix="/games", tags=["games"])
api_router.include_router(
    group_members.router, prefix="/group/members", tags=["group_members"])
api_router.include_router(
    group_messages.router, prefix="/group/messages", tags=["group_massages"])
api_router.include_router(
    private_chat.router, prefix="/chat/private", tags=["private_chat"])
