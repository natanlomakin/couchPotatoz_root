from fastapi import APIRouter
from api.v1.endpoints import users, platforms, friends, massages, librarys, groups, games, group_members, group_massages

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    platforms.router, prefix="/platforms", tags=["platforms"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(
    massages.router, prefix="/massages", tags=["massages"])
api_router.include_router(
    librarys.router, prefix="/librarys", tags=["librarys"])
api_router.include_router(
    groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(
    games.router, prefix="/games", tags=["games"])
api_router.include_router(
    group_members.router, prefix="/group/members", tags=["group_members"])
api_router.include_router(
    group_massages.router, prefix="/group/massages", tags=["group_massages"])
