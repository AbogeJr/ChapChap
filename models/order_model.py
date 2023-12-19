from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


order_meal_association = Table(
    "order_meal_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("meal_id", Integer, ForeignKey("meal.id")),
)


class Order(Base):
    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIVERED", "delivered"),
    )

    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    total = Column(Integer)  # Added the total field
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    meals = relationship(
        "Meal", secondary=order_meal_association, back_populates="orders"
    )

    def __repr__(self):
        return f"<Order {self.id}>"

    # Use a property to calculate the total based on meal prices and quantity
    @property
    def calculate_total(self):
        return sum(meal.price for meal in self.meals) * self.quantity
