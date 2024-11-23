from datetime import datetime
from .database import BASE
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey


class Post(BASE):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now())
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
   

    def __init__(self, title: str, content: str):
        self.title = title
        
        self.content = content