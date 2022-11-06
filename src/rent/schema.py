from graphene import Field, DateTime
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.init import db
from src.rent.table import Rent
from src.book.table import Book
from src.reader.table import Reader


class RentModel(SQLAlchemyObjectType):
    class Meta:
        model = Rent
        exclude_fields = ("book_id", "reader_id")
    
    book = Field("src.book.schema.BookModel")
    reader = Field("src.reader.schema.ReaderModel")

    def resolve_book(self, info):
        return db.get(self.book_id, Book, Book.id)
        
    def resolve_reader(self, info):
        return db.get(self.reader_id, Reader, Reader.id)

    def resolve_rent_time(self, info):
        return DateTime.parse_value(self.rent_time)