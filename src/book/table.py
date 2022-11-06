from sqlalchemy import Column, Integer, String, ForeignKey

from src.db import DeclarativeBase


class Book(DeclarativeBase):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    max_rent_days = Column(Integer)
    cover_link = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))