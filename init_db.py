from database import engine, Base
from models.food_item_model import FoodItem
from models.user_model import User
from models.order_model import Order
from models.order_item import OrderItem

Base.metadata.create_all(bind=engine)
