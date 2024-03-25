from api.v1.schemas.game import *
from api.v1.serializers.gameSerializer import gameEntitny, UpdateGameEntity
from api.deps.database import game_collection
from pymongo import ReturnDocument


async def retrive_games() -> GameBase:
    games = []
    game_Ids = []
    cursor = game_collection.find()
    for document in cursor:
        game_Ids.append(str(document["_id"]))
        games.append(GameBase(**document))
    return games, game_Ids


async def retrive_single_game(id: str) -> GameBase:
    game = game_collection.find_one({"_id": ObjectId(str(id))})
    if game:
        game = gameEntitny(game)
        return game
    return False

async def retrive_searched_game(searchValue: str):
    games = []
    cursor = game_collection.find(
        {"title": {"$regex": searchValue, "$options": "i"}})
    print(cursor.retrieved)
    for document in cursor:
        games.append(GameBase(**document))
    return games


async def create_game(game: GameBase) -> GameBase:
    game.createdAt = datetime.utcnow()
    _id = game_collection.insert_one(dict(game))
    new_game = game_collection.find_one(
        {"_id": ObjectId(str(_id.inserted_id))})
    new_game = gameEntitny(new_game)
    return new_game


async def update_game_data(id: str, data: UpdateGameBase):
    game = game_collection.find_one_and_update({'_id': ObjectId(str(id))}, {
        "$set": data.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if game:
        game = UpdateGameEntity(game)
        return game
    return False


async def remove_game(id: str):
    deleted_game = game_collection.find_one_and_delete(
        {"_id": ObjectId(str(id))})
    if deleted_game:
        return True
    return False
