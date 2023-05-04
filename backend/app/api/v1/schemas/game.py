from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class GameBase(BaseModel):
    platform_id: str
    title: str
    thumbnail_url: str
    genre: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateGameBase(BaseModel):
    thumbnail_url: str | None = None

    class Config:
        orm_mode = True


class ListGames(BaseModel):
    result: List[GameBase]
