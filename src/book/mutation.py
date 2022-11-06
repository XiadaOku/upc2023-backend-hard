from graphene import Mutation, Argument, Int, Boolean
from datetime import datetime, timedelta
from random import randint, randrange

from src.init import db
from src.book.schema import BookModel, CreateBookModel, UpdateBookModel
from src.book.table import Book
from src.author.table import Author
from src.reader.table import Reader
from src.rent.schema import RentModel
from src.rent.table import Rent


class Create(Mutation):
    class Arguments():
        details = Argument(CreateBookModel, required=True)

    Output = BookModel
    
    @staticmethod
    def mutate(parent, info, details):
        if details.max_rent_days <= 0:
            raise Exception(f"maxRentDays must be greater than 0, found {details.max_rent_days}")
            
        author = db.get(details.author_id, Author, Author.id)
        if author is None:
            raise Exception(f"No author found with id={details.author_id}")

        book = Book(
            title=details.title, 
            max_rent_days=details.max_rent_days, 
            cover_link=details.cover_link
        )
        db.append_childs(author, {"books": book})
        db.update(author, {"books_available": author.books_available + 1})
        return book

class Update(Mutation):
    class Arguments():
        id = Int(required=True)
        details = Argument(UpdateBookModel, required=True)

    Output = BookModel
    
    @staticmethod
    def mutate(parent, info, id, details):
        book = db.get(id, Book, Book.id)
        if book is None:
            raise Exception(f"No book found with id={id}")

        db.update(book, details)
        return db.get(id, Book, Book.id)

class Delete(Mutation):
    class Arguments():
        id = Int(required=True)

    Output = Boolean
    
    @staticmethod
    def mutate(parent, info, id):
        book = db.get(id, Book, Book.id)
        if book is None:
            raise Exception(f"No book found with id={id}")
        
        rent = db.get(id, Rent, Rent.book_id)
        if rent is None:
            author = db.get(book.author_id, Author, Author.id)
            db.update(author, {"books_available": author.books_available - 1})
        else:
            db.delete(rent)
        
        db.delete(book)
        return True

class RentBook(Mutation):
    class Arguments():
        book_id = Int(required=True)
        reader_id = Int(required=True)

    Output = RentModel
    
    @staticmethod
    def mutate(parent, info, book_id, reader_id):
        book = db.get(book_id, Book, Book.id)
        if book is None:
            raise Exception(f"No book found with id={book_id}")

        reader = db.get(reader_id, Reader, Reader.id)
        if reader is None:
            raise Exception(f"No reader found with id={reader_id}")

        rent = Rent(
            rent_time=datetime.today(),
            rented_for_days=randint(1, book.max_rent_days),
            fine_per_day=randint(1, 10),
            book_id=book_id
        )
        db.append_childs(reader, {"rents": rent})
        
        author = db.get(book.author_id, Author, Author.id)
        db.update(author, {"books_available": author.books_available - 1})
        
        return rent

class ReturnBook(Mutation):
    class Arguments():
        book_id = Int(required=True)
        reader_id = Int(required=True)

    fine = Int()
    reader_fine = Int()
    
    @staticmethod
    def mutate(parent, info, book_id, reader_id):
        book = db.get(book_id, Book, Book.id)
        if book is None:
            raise Exception(f"No book found with id={book_id}")

        reader = db.get(reader_id, Reader, Reader.id)
        if reader is None:
            raise Exception(f"No reader found with id={reader_id}")

        rent = None
        for reader_rent in reader.rents:
            if reader_rent.book_id == book_id:
                rent = reader_rent
                break
        
        if rent is None:
            raise Exception(f"No rent found with reader_id={reader_id},book_id={book_id}")

        fine = 0
        # should've been "today = datetime.today()" but I don't want to wait
        today = rent.rent_time + timedelta(days=randrange(0, rent.rented_for_days * 2))
        days_diff = (today - rent.rent_time).days
        if days_diff >= rent.rented_for_days:
            fine = (days_diff - rent.rented_for_days + 1) * rent.fine_per_day
            db.update(reader, {"fine": reader.fine + fine})

        db.delete(rent)

        author = db.get(book.author_id, Author, Author.id)
        db.update(author, {"books_available": author.books_available + 1})
        
        return ReturnBook(fine=fine, reader_fine=reader.fine + fine)


class Mutation():
    create_book = Create.Field()
    update_book = Update.Field()
    delete_book = Delete.Field()
    rent_book = RentBook.Field()
    return_book = ReturnBook.Field()