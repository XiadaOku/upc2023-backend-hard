from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db import DeclarativeBase


class Rent(DeclarativeBase):
    __tablename__ = "rents"
    id = Column(Integer, primary_key=True)
    rent_time = Column(DateTime)
    rented_for_days = Column(Integer)
    fine_per_day = Column(Integer)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("src.book.table.Book")
    reader_id = Column(Integer, ForeignKey("readers.id"))
