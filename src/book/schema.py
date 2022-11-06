from graphene import Field, InputObjectType, String, Int
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.init import db
from src.book.table import Book
from src.author.table import Author


class BookModel(SQLAlchemyObjectType):
    class Meta:
        model = Book
        exclude_fields = ("author_id",)
    
    author = Field("src.author.schema.AuthorModel")

    def resolve_author(self, info):
        return db.get(self.author_id, Author, Author.id)


class CreateBookModel(InputObjectType):
    title = String(required=True)
    max_rent_days = Int(required=True)
    cover_link = String(required=True)
    author_id = Int(required=True)

class UpdateBookModel(InputObjectType):
    title = String()
    max_rent_days = Int()
    cover_link = String()