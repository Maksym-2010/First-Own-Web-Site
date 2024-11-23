from .database import BASE, session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean
from flask_login import UserMixin

class User(UserMixin, BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(30), nullable=False, unique=True)
    password = Column(String(250), nullable=False, unique=True)
    
