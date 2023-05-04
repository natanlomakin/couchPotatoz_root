from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class GroupMemberBase(BaseModel):
    role: str
    status: str
    user_id: str
    group_id: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateGroupMemberBase(BaseModel):
    role: str | None = None
    status: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListGroupMembers(BaseModel):
    result: List[GroupMemberBase]
