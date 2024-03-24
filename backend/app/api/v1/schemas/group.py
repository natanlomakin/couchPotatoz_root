from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class GroupBase(BaseModel):
    _id: ObjectId
    title: str
    summery: str
    createdBy_id: str
    chatId: str
    status: str
    createdAt: datetime | None = None
    mainImage: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpadateGroupBase(BaseModel):
    title: str | None = None
    status: str | None = None
    summery: str | None = None
    mainImage: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ReturnGroupIdBase(GroupBase):
    _id: ObjectId

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListGroups(BaseModel):
    result: List[GroupBase]
