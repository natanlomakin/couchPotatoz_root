def group_memberEntitny(group_member) -> dict:
    return {
        "id": str(group_member["_id"]),
        "user_id": group_member["user_id"],
        "group_id": group_member["group_id"],
        "createdAt": group_member["createdAt"],
        "role": group_member["role"],
        "status": group_member["status"],
    }

def updateGroup_memberEntity(group_member) -> dict:
    return{
        "role": group_member["role"],
        "status": group_member["status"]
    }

def listGroup_memberEntitny(group_members):
    return [group_memberEntitny(group_member) for group_member in group_members]
