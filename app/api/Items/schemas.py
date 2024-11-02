from pydantic import BaseModel

class newItem(BaseModel):
    item_id: int
    name: str
    email: str
    quantity: int
    expiry_date: str