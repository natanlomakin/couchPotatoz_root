from fastapi import APIRouter
from api.v1.models.platforms import get_platforms, get_platform, create_platform, remove_platform
from api.v1.schemas.platform import PlatformBase

router = APIRouter()


@router.get("/", response_description="Platforms retrived")
async def get_all_platforms():
    platforms = await get_platforms()

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Platforms data retrieved successfully",
        "data": platforms
    }


@router.get("/{id}", response_description="Single platform retrived")
async def get_single_platform(id: str):
    platform = await get_platform(id)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Platform data retrieved successfully",
        "data": platform
    }


@router.post("/", response_description="New platform data added to the database")
async def add_platform(platform: PlatformBase):
    new_platform = await create_platform(platform)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Platform created successfully",
        "data": new_platform
    }


@router.delete("/{id}", response_description="Platform data deleted")
async def delete_platform(id: str):
    deleted_platform = await remove_platform(id)
    if deleted_platform:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Platform with ID: {id} removed",
            "data": deleted_platform
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Platform with id {id} doesn't exist",
        "data": False
    }
