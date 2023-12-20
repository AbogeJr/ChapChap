from database import Base
from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
    String,
)
from sqlalchemy.orm import relationship


class FoodItem(Base):
    __tablename__ = "food_item"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    available = Column(Boolean, default=True)
    price = Column(Float, nullable=False)
    orders_items = relationship("OrderItem", back_populates="food_items")
