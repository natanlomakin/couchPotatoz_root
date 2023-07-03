from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.database import retrive_all_librarys, retrive_single_library, create_library, delete_library
from api.v1.schemas.library import LibraryBase
from api.v1.serializers.librarySerializer import libraryEntitny
from ...deps.auth_bearer import JWTBearer
from ...deps.auth import decodeJWT

router = APIRouter()


@router.get("/{userId}", dependencies=[Depends(JWTBearer())], response_description="Retrive all user librarys")
async def get_librarys(userId: str):
    librarys = await retrive_all_librarys(userId)
    if librarys:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all librarys from database",
            "data": librarys[0],
            "library_ids": librarys[1]}
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no librarys",
        "data": False
    }


@router.get("/{id}", dependencies=[Depends(JWTBearer())], response_description="Retrived specific library from database")
async def get_single_library(id: str):
    library = await retrive_single_library(id)
    if library:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived library with id {id} from database",
            "data": library
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no library with id {id}",
        "data": False
    }


@router.post("/", dependencies=[Depends(JWTBearer())], response_description="New library created")
async def add_library(library: LibraryBase):
    new_library = await create_library(library)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"New library created in the database",
        "data": new_library
    }


@router.delete("/{id}", dependencies=[Depends(JWTBearer())], response_description="Removed library from database")
async def remove_library(id: str):
    deleted_library = await delete_library(id)
    if deleted_library:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Deleted library with id {id} from database",
            "data": deleted_library
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no library with id {id}",
        "data": False
    }
