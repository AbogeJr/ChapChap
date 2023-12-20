from database import engine, Base
from models import FoodItem, User, Order, OrderItem


Base.metadata.create_all(bind=engine)
