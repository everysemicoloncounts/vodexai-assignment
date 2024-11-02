from fastapi import APIRouter
from typing import Optional
from app.api.Items.schemas import newItem
from app.api.Items.service import insertNewItemInItemsCollection, getItemFromItemId, filterItemsBasedOnKey, deleteItemBasedOnItemId, updateItemRecord

router = APIRouter()

@router.post("/items")
async def insert_item(payload: newItem):
    return insertNewItemInItemsCollection(payload)

@router.delete("/items/{item_id}")
async def delete_an_item(item_id: int):
    return deleteItemBasedOnItemId(item_id)

@router.put("/items/{item_id}")
async def update_an_item(item_id: int, name: Optional[str] = None, email: Optional[str] = None, expiry_date: Optional[str] = None, quantity: Optional[int] = None):
    return updateItemRecord(item_id, name, email, expiry_date, quantity)

@router.get("/items/filter")
async def filter_items(email: Optional[str] = None, expiry_date: Optional[str] = None, insert_ts: Optional[int] = None, quantity: Optional[int] = None):
    return filterItemsBasedOnKey(email, expiry_date, insert_ts, quantity)

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    return getItemFromItemId(item_id)