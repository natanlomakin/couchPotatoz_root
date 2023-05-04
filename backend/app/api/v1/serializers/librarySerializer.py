def libraryEntitny(library) -> dict:
    return {
        "id": str(library["_id"]),
        "createdAt": library["createdAt"],
        "user_id": library["user_id"],
        "game_id": library["game_id"],
        "platform_id": library["platform_id"]
    }


def listLibraryEntity(librarys):
    return [libraryEntitny(library) for library in librarys]
