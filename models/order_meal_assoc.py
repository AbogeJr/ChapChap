from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table


# Define a association table to represent the many-to-many relationship
order_meal_association = Table(
    "order_meal_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id")),
    Column("meal_id", Integer, ForeignKey("meal.id")),
)
