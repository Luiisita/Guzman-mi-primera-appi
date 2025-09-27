from fastapi import APIRouter, HTTPException, status
from models import Book
from exceptions import BookNotFoundError, BookNotAvailableError, LibraryFullError
from utils import create_response, get_total_borrowed_books
from .books import BOOKS_DB
import logging

router = APIRouter(prefix="/borrowing", tags=["borrowing"])

MAX_BORROWED_BOOKS = 10

@router.post("/borrow/{book_id}")
def borrow_book(book_id: int):
    book = BOOKS_DB.get(book_id)
    if not book:
        raise BookNotFoundError(book_id)
    
    if not book.is_available:
        raise BookNotAvailableError(book_id)
    
    if get_total_borrowed_books() >= MAX_BORROWED_BOOKS:
        raise LibraryFullError()
    
    book.is_available = False
    BOOKS_DB[book_id] = book
    logging.info(f"Book {book_id} borrowed successfully.")
    return create_response(success=True, message=f"Book with ID {book_id} borrowed successfully.")

@router.post("/return/{book_id}")
def return_book(book_id: int):
    book = BOOKS_DB.get(book_id)
    if not book:
        raise BookNotFoundError(book_id)
    
    book.is_available = True
    BOOKS_DB[book_id] = book
    logging.info(f"Book {book_id} returned successfully.")
    return create_response(success=True, message=f"Book with ID {book_id} returned successfully.")

@router.get("/active", response_model=list[Book])
def get_active_borrowings():
    borrowed_books = [book for book in BOOKS_DB.values() if not book.is_available]
    return borrowed_books