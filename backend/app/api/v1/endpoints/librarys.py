from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps.database import retrive_all_librarys, retrive_single_library, create_library, delete_library
from app.api.v1.schemas.library import LibraryBase
from app.api.v1.serializers.librarySerializer import libraryEntitny

router = APIRouter()


@router.get("/", response_description="Retrive all librarys")
async def get_librarys():
    librarys = await retrive_all_librarys()
    if librarys:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all librarys from database",
            "data": librarys
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no librarys",
        "data": False
    }


@router.get("/{id}", response_description="Retrived specific library from database")
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


@router.post("/", response_description="New library created")
async def add_library(library: LibraryBase):
    new_library = await create_library(library)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": f"New library created in the database",
        "data": new_library
    }

@router.delete("/{id}", response_description="Removed library from database")
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