def platformEntitny(platform) -> dict:
    return {
        "id": str(platform["_id"]),
        "createdAt": platform["createdAt"],
        "platformType": platform["platformType"]
    }
