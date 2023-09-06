from pymongo import mongo_client
from config.settings import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
db = client.potato

user_collection = db.user


platform_collection = db.platform


friend_collection = db.friend


message_collection = db.massage


private_chat_collection = db.private_chat


group_collection = db.group


group_message_collection = db.group_massage


group_member_collection = db.group_member


library_collection = db.library


game_collection = db.game
