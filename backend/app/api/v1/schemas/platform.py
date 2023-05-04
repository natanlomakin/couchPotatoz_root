from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class PlatformBase(BaseModel):
    platformType: str
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
