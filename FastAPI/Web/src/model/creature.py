from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.data.init import Base
from src.model.explorer import Explorer

class Creature(Base):
    __tablename__ = "creature"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True)
    country = Column(String, index=True)
    area = Column(String, index=True)
    description = Column(String, index=True)
    aka = Column(String, index=True)
    explorer_id = Column(Integer, ForeignKey('explorer.id'))
    explorer = relationship(Explorer)
