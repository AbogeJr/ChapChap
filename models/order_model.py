from database import Base
from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from . import OrderItem


class Order(Base):
    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIVERED", "delivered"),
    )

    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    total = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Order {self.id}>"

    @property
    def calculate_total(self):
        self.total = sum(order_item.total for order_item in self.order_items)
        return self.total
