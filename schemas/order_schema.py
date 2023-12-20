from typing import List, Optional
from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    order_status: str = "PENDING"
    total: float = 0.0


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    food_item_id: int
    quantity: int
    total: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True


class OrderWithItems(Order):
    order_items: List[OrderItem]

    class Config:
        orm_mode = True
