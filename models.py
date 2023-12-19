from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

# Define a association table to represent the many-to-many relationship
order_meal_association = Table(
    "order_meal_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("meal_id", Integer, ForeignKey("meal.id")),
)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    price = Column(Integer, nullable=False)
    orders = relationship(
        "Order", secondary=order_meal_association, back_populates="meals"
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
