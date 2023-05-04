def groupEntitny(group) -> dict:
    return {
        "id": str(group["_id"]),
        "createdBy_id": str(group["createdBy_id"]),
        "createdAt": group["createdAt"],
        "title": group["title"],
        "status": group["status"],
        "summery": group["summery"]
    }

def updateGroupEntity(group) -> dict:
    return{
        "id": str(group["_id"]),
        "title": group["title"],
        "status": group["status"],
        "summery": group["summery"]
    }


def listGroupEntity(groups):
    return [groupEntitny(group) for group in groups]
