from typing import List, Optional
from pydantic import BaseModel


class FoodItemModel(BaseModel):
    id: Optional[int]
    name: str
    price: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Pepperoni Pizza",
                "price": 10,
            }
        }
