import os
from pymongo import MongoClient
from dotenv import load_dotenv
from app.constants.constants import db_name, item_collection_name

load_dotenv()

client = None
db = None

def createMongoUri():
    uriString = ""
    uriString += "mongodb+srv://" + os.getenv("MONGO_USER_NAME") + ":" + os.getenv("MONGO_USER_PASSWORD") + "@" + os.getenv("MONGO_CLUSTER_NAME") + ".l8vsp.mongodb.net/"
    return uriString

def connect_to_mongo():
    global client, db
    mongo_url = createMongoUri() if os.getenv("IS_DB_HOSTED") == "TRUE" else os.getenv("LOCAL_MONGO_URI")
    print("mongo_url", mongo_url)
    try:
        client = MongoClient(mongo_url)
        db = client[db_name]
        print("Connected to MongoDB!")
    except Exception as e:
        print("pyMongo connection error")

def get_database():
    connect_to_mongo()
    global db
    return db

def get_Item_Collection():
    db = get_database()
    collection = db[item_collection_name]
    return collection