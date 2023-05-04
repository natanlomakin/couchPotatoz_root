from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class MassageBase(BaseModel):
    massage_content: str
    source_id: str
    target_id: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpadateMassage(BaseModel):
    massage_content: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListMassages(BaseModel):
    result: List[MassageBase]
