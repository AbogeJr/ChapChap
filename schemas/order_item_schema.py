from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    food_item_id: int
    quantity: int

    class Config:
        orm_mode = True
