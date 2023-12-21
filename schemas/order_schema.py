from typing import List, Optional
from pydantic import BaseModel
from schemas import OrderItemCreate


class OrderCreate(BaseModel):
    order_status: str = "PENDING"
    user_id: int

    class Config:
        orm_mode = True


class OrderWithItems(OrderCreate):
    order_items: List[OrderItemCreate]
