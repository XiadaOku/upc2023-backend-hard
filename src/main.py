from fastapi import FastAPI
from graphene import Schema, ObjectType
from starlette_graphene3 import GraphQLApp, make_playground_handler

from src.init import engine, DeclarativeBase

from src.book.query import Query as BookQuery
from src.author.query import Query as AuthorQuery
from src.reader.query import Query as ReaderQuery
from src.rent.query import Query as RentQuery

from src.book.mutation import Mutation as BookMutation
from src.author.mutation import Mutation as AuthorMutation
from src.reader.mutation import Mutation as ReaderMutation


DeclarativeBase.metadata.create_all(bind=engine)
DeclarativeBase.metadata.bind = engine


class Query(
    BookQuery, 
    AuthorQuery, 
    ReaderQuery, 
    RentQuery
):
    pass

class Mutation(
    ObjectType,
    BookMutation, 
    AuthorMutation,
    ReaderMutation
):
    pass


app = FastAPI()
app.add_route("/", GraphQLApp(
    Schema(query=Query, mutation=Mutation), 
    on_get=make_playground_handler())
)