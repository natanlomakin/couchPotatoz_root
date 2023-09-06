from api.v1.schemas.user import *
from api.deps.database import user_collection
from api.v1.serializers.userSerializer import userFriendEntity, userEntitny, userUpdatedEntity, signupUserEntity
from fastapi.security import OAuth2PasswordRequestForm
from api.deps.auth import get_hashed_password, verify_password, create_access_token, create_refresh_token
from fastapi import status, Depends
from fastapi.responses import RedirectResponse


async def retrive_users() -> List[UserBase]:
    users = []
    cursor = user_collection.find()
    for document in cursor:
        users.append(User(**document))
    return users


async def retrive_single_user(id: str) -> UserBase:
    user = user_collection.find_one(
        {'_id': ObjectId(str(id))})
    user = userEntitny(user)
    return user


async def retrive_single_user_friend(id: str) -> UserFriend:
    user = user_collection.find_one(
        {'_id': ObjectId(str(id))})
    user = userFriendEntity(user)
    return user


async def add_new_user(new_user: CreateUser) -> CreateUser:
    new_user.createdAt = datetime.utcnow()
    new_user.password = get_hashed_password(new_user.password)
    _id = user_collection.insert_one(dict(new_user))
    user = user_collection.find_one({"_id": ObjectId(str(_id.inserted_id))})
    user = signupUserEntity(user)
    return user


async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"email": str(form_data.email)})
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_401_UNAUTHORIZED)
    hashed_password = user['password']
    if not verify_password(form_data.password, hashed_password):
        raise Exception(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="incorrect email or password")
    tokens = {"access_token": create_access_token(
        str(user['_id'])), "refresh_token": create_refresh_token(str(user['_id']))}
    return tokens


async def remove_user(id: str) -> bool:
    user = user_collection.find_one({'_id': ObjectId(str(id))})
    if user:
        user_collection.delete_one({'_id': ObjectId(str(id))})
        return True
    return False


async def update_user_data(id: str, data: UpdateUser):
    user = user_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
                                               "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if user:
        user = userUpdatedEntity(user)
        return user
    return False
