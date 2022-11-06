from graphene import ObjectType, List, Field, Int

from src.init import db
from src.book.table import Book
from src.book.schema import BookModel


class Query(ObjectType):
    get_book = Field(BookModel, id=Int())
    books = List(BookModel)

    @staticmethod
    def resolve_get_book(parent, info, id):
        book = db.get(id, Book, Book.id)
        if book is None:
            raise Exception(f"No book found with id={id}")
        
        return book

    @staticmethod
    def resolve_books(parent, info):
        return db.get_all(Book)