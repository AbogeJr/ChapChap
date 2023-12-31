from typing import List, Optional
from pydantic import BaseModel


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


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin",
            }
        }
