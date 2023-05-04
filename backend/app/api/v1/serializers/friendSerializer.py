def friendEntitny(friend) -> dict:
    return {
        "id": str(friend["_id"]),
        "source_id": friend["source_id"],
        "target_id": friend["target_id"],
        "createdAt": friend["createdAt"],
        "status": friend["status"],
    }

def updateFriendEntity(friend) -> dict:
    return{
        "id": str(friend["_id"]),
        "status": friend["status"]
    }

def listFriendEntity(friends):
    return [friendEntitny(friend) for friend in friends]
