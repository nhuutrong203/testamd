from sqlalchemy import Column, Integer, String
from src.data.init import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)  
    username = Column(String, index=True)
    hash = Column(String, index=True)
