def userEntitny(user) -> dict:
    return {
        "id": str(user["_id"]),
        "userName": user["userName"],
        "email": user["email"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "isActive": user["isActive"],
        "createdAt": user["createdAt"],
        "password": user["password"],
        "profile_image_url": user["profile_image_url"]
    }


def userFriendEntity(user) -> dict:
    return{
        "id": str(user["_id"]),
        "userName": user["userName"]
    }


def signupUserEntity(user) -> dict:
    return{
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
    }


def userUpdatedEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "userName": user["userName"],
        "email": user["email"],
        "firstName": user["firstName"],
        "lastName": user["lastName"],
        "isActive": user["isActive"],
        "createdAt": user["createdAt"],
        "profile_image_url": user["profile_image_url"]
    }


def listUserEntity(users):
    return [userEntitny(user) for user in users]
