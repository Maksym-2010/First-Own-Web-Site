from .database import BASE
from sqlalchemy import Column, Integer, Float, Text, ForeignKey, String, DateTime
from datetime import datetime


class Comment(BASE):
    __tablename__ = "comments"
    

    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    create_dt = Column(DateTime, default=datetime.utcnow)
    
    