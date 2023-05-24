from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import List
from bson.objectid import ObjectId


class UserBase(BaseModel):
    _id: ObjectId
    userName: str
    email: EmailStr
    firstName: str | None = None
    lastName: str | None = None
    isActive: bool | None = None
    profile_image_url: str | None = None
    createdAt: datetime | None = None

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    password: constr(min_length=8)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UpdateUser(BaseModel):
    userName: str | None = None
    email: EmailStr | None = None
    firstName: str | None = None
    lastName: str | None = None
    isActive: bool | None = None
    createdAt: datetime | None = None
    profile_image_url: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class LoginUser(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class User(UserBase):
    _id: str


class ListUser(BaseModel):
    result: List[UserBase]
