from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer, ForeignKey("order.id", ondelete="CASCADE"), nullable=False
    )
    food_item_id = Column(
        Integer, ForeignKey("food_item.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, default=1)
    total = Column(Integer, default=0)
    food_item = relationship("FoodItem", cascade="delete", back_populates="order_items")
    order = relationship("Order", cascade="delete", back_populates="order_items")

    def __repr__(self):
        return f"<Order {self.id}>"

    @property
    def calculate_total(self):
        self.total = self.food_item.price * self.quantity if self.food_item else 0
        return self.total
