from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class FriendBase(BaseModel):
    source_id: str
    target_id: str
    status: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateFriend(BaseModel):
    status: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListFriends(BaseModel):
    result: List[FriendBase]


class CreateFriend(BaseModel):
    source_id: ObjectId
    target_id: ObjectId
    status: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {str: ObjectId}
