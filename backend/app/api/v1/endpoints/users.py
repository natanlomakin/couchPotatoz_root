from fastapi import APIRouter, Depends
from api.v1.models.users import retrive_users, retrive_single_user_friend, add_new_user, retrive_single_user, remove_user, update_user_data, login_user
from api.v1.schemas.user import UserBase, CreateUser, User, LoginUser, ListUser, CreateUser, UpdateUser
from api.v1.serializers.userSerializer import listUserEntity
from ...deps.auth_bearer import JWTBearer

router = APIRouter()


@router.get("/", response_description="Users retrived")
async def get_users():
    users = await retrive_users()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": users
    }


@router.get("/{id}", dependencies=[Depends(JWTBearer())], response_description="retrive single user data")
async def get_user(id: str):
    user = await retrive_single_user(id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User data retrieved successfully",
        "data": user
    }


@router.get("/friend/{id}", response_description="retrive single user data")
async def get_user(id: str):
    user = await retrive_single_user_friend(id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User data retrieved successfully",
        "data": user
    }


@router.post("/signup", response_description="New user data add to the database")
async def add_user(user: CreateUser):
    new_user = await add_new_user(user)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User created successfully",
        "data": new_user
    }


@router.post("/login", response_description="Login user")
async def add_user(user: LoginUser):
    new_user = await login_user(user)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User logged in successfully",
        "data": new_user
    }


@router.delete("/{id}", response_description="User data deleted")
async def delete_user(id: str):
    deleted_user = await remove_user(id)
    if deleted_user:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Student with ID: {id} removed",
            "data": deleted_user
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Student with id {id} doesn't exist",
        "data": False
    }


@router.put("/{id}", dependencies=[Depends(JWTBearer())], response_description="User data has been updated")
async def update_user(id: str, data: UpdateUser):
    updated_user = await update_user_data(id, data)
    if updated_user:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Student with ID: {id} updated",
            "data": updated_user
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Student with id {id} doesn't exist",
        "data": False
    }
