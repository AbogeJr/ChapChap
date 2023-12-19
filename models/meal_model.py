from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

order_meal_association = Table(
    "order_meal_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("meal_id", Integer, ForeignKey("meal.id")),
    extend_existing=True,
)


class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    price = Column(Integer, nullable=False)
    orders = relationship(
        "Order", secondary=order_meal_association, back_populates="meals"
    )
