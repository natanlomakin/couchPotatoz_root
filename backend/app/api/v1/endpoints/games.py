from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.database import retrive_games, retrive_single_game, create_game, update_game_data, remove_game
from api.v1.schemas.game import GameBase, UpdateGameBase
from api.v1.serializers.gameSerializer import gameEntitny

router = APIRouter()


@router.get("/", response_description="Retrive all the games from database")
async def get_games():
    games = await retrive_games()
    if games:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived all games from database",
            "data": games
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There are no games",
        "data": False
    }


@router.get("/{id}", response_description="Retrive single game from database")
async def get_game(id: str):
    game = await retrive_single_game(id)
    if game:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Retrived game with id {id} from database",
            "data": game
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"There is no game with id {id}",
        "data": False
    }


@router.post("/", response_description="Added new game data to the database")
async def add_game(game: GameBase):
    new_game = await create_game(game)
    if game:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Added new game data to the database",
            "data": game
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Data given is not valid",
        "data": False
    }


@router.put("/{id}", response_description="Updated game with id {id}")
async def update_game(id: str, game: UpdateGameBase):
    updated_game = await update_game_data(id, game)
    if game:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Updated game with id {id}",
            "data": updated_game
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Error while trying to update game with id {id}",
        "data": False
    }

@router.delete("/{id}", response_description="Game with id {id} removed from database")
async def delete_game(id: str):
    deleted_game = await remove_game(id)
    if deleted_game:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": f"Game with ID: {id} was deleted",
            "data": deleted_game
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": f"Game with id {id} doesn't exist",
        "data": deleted_game
    }