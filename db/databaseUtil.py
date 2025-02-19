import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from app.constants.constants import db_name, item_collection_name

load_dotenv()

def createMongoUri():
    uriString = "mongodb+srv://" + os.getenv("MONGO_USER_NAME") + ":" + os.getenv("MONGO_USER_PASSWORD") + "@" + os.getenv("MONGO_CLUSTER_NAME") + ".l8vsp.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPractice" if os.getenv("IS_DB_HOSTED") == "TRUE" else os.getenv("LOCAL_MONGO_URI")
    return uriString if os.getenv("IS_DB_HOSTED") == "TRUE" else os.getenv("LOCAL_MONGO_URI")

def get_mongo_client():
    mongo_url = createMongoUri()
    client = MongoClient(mongo_url, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)

def get_database():
    client = get_mongo_client()
    return client[db_name]

def get_Item_Collection():
    db = get_database()
    collection = db[item_collection_name]
    return collection