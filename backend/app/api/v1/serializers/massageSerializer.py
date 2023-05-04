def massageEntitny(massage) -> dict:
    return {
        "id": str(massage["_id"]),
        "createdAt": massage["createdAt"],
        "massage_content": massage["massage_content"],
        "source_id": massage["source_id"],
        "target_id": massage["target_id"]
    }


def updateMassageEntity(massage) -> dict:
    return {
        "id": str(massage["_id"]),
        "massage_content": massage["massage_content"]
    }


def listMassageEntity(massages):
    return [massageEntitny(massage) for massage in massages]
