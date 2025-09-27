from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from models import Book
from exceptions import BookNotFoundError, DuplicateISBNError, InvalidBookDataError
from utils import create_response
import logging

router = APIRouter(prefix="/books", tags=["books"])

# Base de datos en memoria para el ejercicio
BOOKS_DB = {}
next_id = 1

# Datos de prueba
initial_books = [
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "isbn": "978-0618053267", "year": 1954, "rating": 4.8, "is_available": True, "is_bestseller": True, "tags": {"fantasy", "classic"}},
    {"title": "Dune", "author": "Frank Herbert", "isbn": "978-0441172719", "year": 1965, "rating": 4.5, "is_available": True, "is_bestseller": True, "tags": {"scifi", "classic"}},
    {"title": "1984", "author": "George Orwell", "isbn": "978-0451524935", "year": 1949, "rating": 4.6, "is_available": False, "is_bestseller": False, "tags": {"dystopian", "classic"}},
    {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "isbn": "978-0345391803", "year": 1979, "rating": 4.2, "is_available": True, "is_bestseller": False, "tags": {"scifi", "humor"}}
]

for book_data in initial_books:
    try:
        book = Book(**book_data)
        book.id = next_id
        BOOKS_DB[next_id] = book
        next_id += 1
    except Exception as e:
        logging.error(f"Error loading initial book data: {e}")

@router.get("/", response_model=List[Book])
def get_all_books(skip: int = 0, limit: int = 10):
    return list(BOOKS_DB.values())[skip: skip + limit]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    for existing_book in BOOKS_DB.values():
        if existing_book.isbn == book.isbn:
            raise DuplicateISBNError(book.isbn)
    
    global next_id
    new_book = book.copy(update={"id": next_id})
    BOOKS_DB[next_id] = new_book
    next_id += 1
    return create_response(success=True, data=new_book, message="Book created successfully")

@router.get("/{book_id}")
def get_book_by_id(book_id: int):
    if book_id not in BOOKS_DB:
        raise BookNotFoundError(book_id)
    return create_response(success=True, data=BOOKS_DB[book_id])

@router.put("/{book_id}")
def update_book(book_id: int, book_update: Book):
    if book_id not in BOOKS_DB:
        raise BookNotFoundError(book_id)
    
    if book_update.isbn != BOOKS_DB[book_id].isbn:
        for existing_book in BOOKS_DB.values():
            if existing_book.isbn == book_update.isbn and existing_book.id != book_id:
                raise DuplicateISBNError(book_update.isbn)

    BOOKS_DB[book_id] = book_update.copy(update={"id": book_id})
    return create_response(success=True, data=BOOKS_DB[book_id], message="Book updated successfully")

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    if book_id not in BOOKS_DB:
        raise BookNotFoundError(book_id)
    del BOOKS_DB[book_id]

@router.get("/search", response_model=List[Book])
def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    year_from: Optional[int] = Query(None, ge=1),
    year_to: Optional[int] = Query(None, ge=1),
    available_only: bool = Query(False)
):
    results = list(BOOKS_DB.values())
    if title:
        results = [b for b in results if title.lower() in b.title.lower()]
    if author:
        results = [b for b in results if author.lower() in b.author.lower()]
    if genre:
        results = [b for b in results if genre.lower() in b.tags]
    if year_from:
        results = [b for b in results if b.year >= year_from]
    if year_to:
        results = [b for b in results if b.year <= year_to]
    if available_only:
        results = [b for b in results if b.is_available]
    
    return results

@router.get("/stats")
def get_book_stats():
    total_books = len(BOOKS_DB)
    available_count = sum(1 for b in BOOKS_DB.values() if b.is_available)
    borrowed_count = total_books - available_count
    
    by_genre = {}
    for book in BOOKS_DB.values():
        for tag in book.tags:
            by_genre[tag] = by_genre.get(tag, 0) + 1
    
    total_rating = sum(b.rating for b in BOOKS_DB.values())
    avg_rating = total_rating / total_books if total_books > 0 else 0
    
    return create_response(success=True, data={
        "total_books": total_books,
        "available_count": available_count,
        "borrowed_count": borrowed_count,
        "by_genre": by_genre,
        "avg_rating": round(avg_rating, 2)
    })