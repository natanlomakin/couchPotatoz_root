from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class GroupMassageBase(BaseModel):
    group_id: str
    user_id: str
    massage_content: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListGroupMassages(BaseModel):
    result: List[GroupMassageBase]
