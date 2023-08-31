def group_massageEntitny(group_massage) -> dict:
    return {
        "id": str(group_massage["_id"]),
        "user_id": group_massage["user_id"],
        "user_name": group_massage["user_name"],
        "group_id": group_massage["group_id"],
        "createdAt": group_massage["createdAt"],
        "massage_content": group_massage["massage_content"],
    }


def listGroup_massageEntitny(group_massages):
    return [group_massageEntitny(group_massage) for group_massage in group_massages]
