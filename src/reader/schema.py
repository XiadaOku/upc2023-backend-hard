from graphene import List, InputObjectType, String, Int
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.init import db
from src.reader.table import Reader
from src.rent.table import Rent


class ReaderModel(SQLAlchemyObjectType):
    class Meta:
        model = Reader
    
    rents = List("src.rent.schema.RentModel")

    def resolve_rents(self, info):
        return db.get_all_filtered(self.id, Rent, Rent.reader_id)


class CreateReaderModel(InputObjectType):
    name = String(required=True)
    email = String(required=True)

class UpdateReaderModel(InputObjectType):
    name = String()
    email = String()