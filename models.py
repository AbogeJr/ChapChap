from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean, String, Text, ForeignKey
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(25), unique = True)
    email = Column(String(80), unique = True)
    password = Column(Text, nullable = False)
    is_staff = Column(Boolean, default = False)
    is_active = Column(Boolean, default = False)
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}>"
    

class Order(Base):

    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('INT-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered')
    )

    ORDER_SIZE = (
        ('SMALL', 'small'),
        ('MEDIUM', 'medium'),
        ('LARGE', 'large')
    )


    __tablename__ = 'order'
    id = Column(Integer, primary_key = True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    order_size = Column(ChoiceType(choices=ORDER_SIZE), default="SMALL")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}>"