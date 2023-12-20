from typing import List, Optional
from pydantic import BaseModel


class OrderCreate(BaseModel):
    order_status: str = "PENDING"
    user_id: int

    class Config:
        orm_mode = True
