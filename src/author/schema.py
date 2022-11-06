from graphene import List, InputObjectType, String, Int, Date
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.init import db
from src.author.table import Author
from src.book.table import Book


class AuthorModel(SQLAlchemyObjectType):
    class Meta:
        model = Author
    
    books = List("src.book.schema.BookModel")

    def resolve_books(self, info):
        return db.get_all_filtered(self.id, Book, Book.author_id)


class CreateAuthorModel(InputObjectType):
    name = String(required=True)
    photo_link = String(required=True)
    birth_date = Date(required=True)
    death_date = Date()

class UpdateAuthorModel(InputObjectType):
    name = String()
    photo_link = String()
    birth_date = Date()
    death_date = Date()
