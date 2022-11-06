from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from src.db import DeclarativeBase


class Author(DeclarativeBase):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo_link = Column(String)
    birth_date = Column(Date)
    death_date = Column(Date, nullable=True)
    books = relationship("src.book.table.Book", cascade="all, delete-orphan")
    books_available = Column(Integer)