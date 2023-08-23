def privateChatEntitny(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "createdAt": chat["createdAt"],
        "chatId": chat["chatId"],
        "user1": chat["user1"],
        "user2": chat["user2"]
    }
