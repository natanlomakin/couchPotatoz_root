def groupEntitny(group) -> dict:
    return {
        "id": str(group["_id"]),
        "createdBy_id": str(group["createdBy_id"]),
        "createdAt": group["createdAt"],
        "title": group["title"],
        "chatId": group["chatId"],
        "status": group["status"],
        "summery": group["summery"],
        "mainImage": group["mainImage"]
    }


def updateGroupEntity(group) -> dict:
    return {
        "id": str(group["_id"]),
        "title": group["title"],
        "status": group["status"],
        "summery": group["summery"],
        "mainImage": group["mainImage"]
    }

def returnGroupIdEntity(group) -> dict:
    return {
        "id": str(group["_id"]),
    }


def listGroupEntity(groups):
    return [groupEntitny(group) for group in groups]
