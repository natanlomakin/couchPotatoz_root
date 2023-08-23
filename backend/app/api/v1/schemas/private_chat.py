from pydantic import BaseModel
from datetime import datetime
from bson.objectid import ObjectId


class PrivateChatBase(BaseModel):
    user1: str
    user2: str
    chatId: str | None = None
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
