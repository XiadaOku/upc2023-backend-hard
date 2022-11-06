from graphene import Mutation, Argument, Int, Boolean

from src.init import db
from src.author.schema import AuthorModel, CreateAuthorModel, UpdateAuthorModel
from src.author.table import Author
from src.book.table import Book


class Create(Mutation):
    class Arguments():
        details = Argument(CreateAuthorModel, required=True)

    Output = AuthorModel
    
    @staticmethod
    def mutate(parent, info, details):
        author = Author(
            name=details.name,
            photo_link=details.photo_link,
            birth_date=details.birth_date,
            death_date=details.death_date,
            books_available=0
        )
        db.add(author)
        return author

class Update(Mutation):
    class Arguments():
        id = Int(required=True)
        details = Argument(UpdateAuthorModel, required=True)

    Output = AuthorModel
    
    @staticmethod
    def mutate(parent, info, id, details):
        author = db.get(id, Author, Author.id)
        if author is None:
            raise Exception(f"No author found with id={id}")

        db.update(author, details)
        return db.get(id, Author, Author.id)

class Delete(Mutation):
    class Arguments():
        id = Int(required=True)

    Output = Boolean
    
    @staticmethod
    def mutate(parent, info, id):
        author = db.get(id, Author, Author.id)
        if author is None:
            raise Exception(f"No author found with id={id}")
        
        db.delete(author)
        return True


class Mutation():
    create_author = Create.Field()
    update_author = Update.Field()
    delete_author = Delete.Field()