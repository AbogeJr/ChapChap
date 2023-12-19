from pydantic import BaseModel
from typing import Optional, List


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405"
    )


class LoginModel(BaseModel):
    username: str
    password: str


class MealModel(BaseModel):
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


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    user_id: Optional[int]
    meals: List[MealModel]  # List of meals associated with the order

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "meals": [
                    {"name": "Pizza", "price": 10},
                    {"name": "Burger", "price": 8},
                ],
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {"example": {"order_status": "PENDING"}}
