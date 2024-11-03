from db.databaseUtil import get_database, get_Item_Collection
from datetime import datetime
from fastapi import HTTPException
from typing import Optional

def getUNIXtimestamp():
    dt = datetime.now() 
    timestamp_seconds = int(dt.timestamp())
    timestamp_milliseconds = timestamp_seconds * 1000
    return timestamp_milliseconds

def insertNewItemInItemsCollection(newItem):
    collection = get_Item_Collection()
    try:
        newItem = dict(newItem)
        newItem["insert_ts"] = getUNIXtimestamp()
        collection.insert_one(newItem)
        return {
            "msg": "New item inserted successfully",
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Request")

def getItemFromItemId(id):
    collection = get_Item_Collection()
    try:
        res_cursor = collection.aggregate([
            {"$match": {"item_id": id}},
            {"$project": {"_id": 0}}
        ])
        res_list = list(res_cursor)
        return {
            "msg": "Item data retrieved successfully",
            "result": res_list[0],
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")
    
def filterItemsBasedOnKey(email: Optional[str], expiry_date: Optional[str], insert_ts: Optional[int], quantity: Optional[int]):
    filters = []
    if email:
        filters.append({"email": email})
    if expiry_date:
        exp_date_obj = datetime.strptime(expiry_date, "%d/%m/%y")
        filters.append({"expiry_date": {"$gt": exp_date_obj}})
    if insert_ts:
        filters.append({"insert_ts": {"$gt": insert_ts}})
    if quantity:
        filters.append({"quantity": {"$gte": quantity}})
    
    pipeline = [
        {"$match": {"$and": filters}} if filters else {"$match": {}},  # Apply filters
        {
            "$group": {
                "_id": "$email",        # Group by email
                "count": {"$sum": 1},   # Count the number of items for each email
            }
        },
        {
            "$project": {
                "_id": 0,
                "email": "$_id",
                "count": 1
            }
        }
    ]
    collection = get_Item_Collection()
    res_cursor = collection.aggregate(pipeline)
    result = list(res_cursor)
    
    return {"filtered_items": result}

def deleteItemBasedOnItemId(id):
    collection = get_Item_Collection()
    try:
        res = collection.find_one_and_delete({"item_id": id}, {"_id": 0})
        return {
            "msg": "Item deleted successfully",
            "res": res,
            "status_code": 200
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")
    
def updateItemRecord(id: int, name: Optional[str], email: Optional[str], expiry_date: Optional[str], quantity: Optional[int]):
    filter_query = {"item_id": id}
    update_query = {}
    if email:
        update_query["email"] = email
    if expiry_date:
        update_query["expiry_date"] = expiry_date
    if quantity:
        update_query["quantity"] = quantity

    try:
        collection = get_Item_Collection()
        collection.update(filter_query, {"$set": update_query})
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")