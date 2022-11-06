from graphene import ObjectType, List, Field, Int

from src.init import db
from src.author.table import Author
from src.author.schema import AuthorModel


class Query(ObjectType):
    get_author = Field(AuthorModel, id=Int())
    authors = List(AuthorModel)

    @staticmethod
    def resolve_get_author(parent, info, id):
        author = db.get(id, Author, Author.id)
        if author is None:
            raise Exception(f"No author found with id={id}")

        return author

    @staticmethod
    def resolve_authors(parent, info):
        return db.get_all(Author)