from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ecommerce.db import Base
from .hashing import get_password_hash, verify_password


class User(Base):
    __tablename__: str = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    cart = relationship('Cart', back_populates='user_cart')
    order = relationship('Order', back_populates='user_info')

    def __int__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = get_password_hash(password)

    def check_password(self, password):
        return verify_password(self.password, password)
