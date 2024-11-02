import os
from pymongo import MongoClient
from dotenv import load_dotenv
from app.constants.constants import db_name

load_dotenv()

client = None
db = None

def connect_to_mongo():
    global client, db
    mongo_url = os.getenv("MONGO_URI")
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

def get_collection():
    db = get_database()
    collection = db['Items_Collection']
    return collection