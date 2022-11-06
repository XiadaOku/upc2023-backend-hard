from graphene import ObjectType, List, Field, Int

from src.init import db
from src.rent.table import Rent
from src.rent.schema import RentModel
from src.reader.table import Reader


class Query(ObjectType):
    rents = Field(List(RentModel), readerId=Int())

    @staticmethod
    def resolve_rents(parent, info, readerId):
        reader = db.get(readerId, Reader, Reader.id)
        if reader is None:
            raise Exception(f"No reader found with id={readerId}")

        return reader.rents