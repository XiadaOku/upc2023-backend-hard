from graphene import ObjectType, Field, Int

from src.init import db
from src.reader.table import Reader
from src.reader.schema import ReaderModel


class Query(ObjectType):
    get_reader = Field(ReaderModel, id=Int())

    @staticmethod
    def resolve_get_reader(parent, info, id):
        reader = db.get(id, Reader, Reader.id)
        if reader is None:
            raise Exception(f"No reader found with id={id}")

        return reader