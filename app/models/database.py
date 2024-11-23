import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


ENGINE = create_engine(os.getenv("DATABASE"), connect_args={"check_same_thread": False})
SESSION = sessionmaker(bind=ENGINE)
session = SESSION()
BASE = declarative_base()


def create_db():
    BASE.metadata.create_all(ENGINE)

def drop_db():
    BASE.metadata.drop_all(ENGINE)