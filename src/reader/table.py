from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db import DeclarativeBase


class Reader(DeclarativeBase):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    fine = Column(Integer)
    rents = relationship("src.rent.table.Rent", cascade="all, delete-orphan")