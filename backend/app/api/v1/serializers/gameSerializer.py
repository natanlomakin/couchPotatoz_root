def gameEntitny(game) -> dict:
    return {
        "id": str(game["_id"]),
        "platform_id": game["platform_id"],
        "createdAt": game["createdAt"],
        "title": game["title"],
        "thumbnail_url": game["thumbnail_url"],
    }


def UpdateGameEntity(game) -> dict:
    return {
        "id": str(game["_id"]),
        "thumbnail_url": game["thumbnail_url"]
    }


def listGameEntitny(games):
    return [gameEntitny(game) for game in games]
