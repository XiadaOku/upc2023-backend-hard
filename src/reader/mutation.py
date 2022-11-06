from graphene import Mutation, Argument, Int, Boolean

from src.init import db
from src.reader.schema import ReaderModel, CreateReaderModel, UpdateReaderModel
from src.reader.table import Reader


class Create(Mutation):
    class Arguments():
        details = Argument(CreateReaderModel, required=True)

    Output = ReaderModel
    
    @staticmethod
    def mutate(parent, info, details):
        reader = Reader(
            name=details.name,
            email=details.email,
            fine=0
        )
        db.add(reader)
        return reader

class Update(Mutation):
    class Arguments():
        id = Int(required=True)
        details = Argument(UpdateReaderModel, required=True)

    Output = ReaderModel
    
    @staticmethod
    def mutate(parent, info, id, details):
        reader = db.get(id, Reader, Reader.id)
        if reader is None:
            raise Exception(f"No reader found with id={id}")

        db.update(reader, details)
        return db.get(id, Reader, Reader.id)

class Delete(Mutation):
    class Arguments():
        id = Int(required=True)

    Output = Boolean
    
    @staticmethod
    def mutate(parent, info, id):
        reader = db.get(id, Reader, Reader.id)
        if reader is None:
            raise Exception(f"No reader found with id={id}")
        
        db.delete(reader)
        return True


class Mutation():
    create_reader = Create.Field()
    update_reader = Update.Field()
    delete_reader = Delete.Field()