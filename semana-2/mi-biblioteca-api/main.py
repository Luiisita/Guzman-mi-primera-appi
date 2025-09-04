from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
import asyncio

app = FastAPI(title="Mi Biblioteca API")

# -----------------------
# ENUMS
# -----------------------
class StatusEnum(str, Enum):
    available = "available"
    borrowed = "borrowed"
    lost = "lost"

class GenreEnum(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    fantasy = "fantasy"
    mystery = "mystery"
    biography = "biography"

# -----------------------
# MODELO BOOK
# -----------------------
class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=2, max_length=100)
    author: str = Field(..., min_length=2, max_length=50)
    pages: Optional[int] = Field(default=None, ge=1, description="Número de páginas")
    status: StatusEnum = StatusEnum.available
    genre: GenreEnum

    # Validación custom
    @validator("title")
    def no_title_uppercase(cls, v):
        if v.isupper():
            raise ValueError("El título no puede estar completamente en mayúsculas")
        return v

# Base de datos en memoria
books: List[Book] = []
next_id = 1

# -----------------------
# ENDPOINTS CRUD
# -----------------------


@app.get("/")
def read_root():
    return {"message": "Mi Biblioteca API"}


@app.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    global next_id
    book.id = next_id
    next_id += 1
    books.append(book)
    return book

@app.get("/books", response_model=List[Book])
def get_books():
    return books

@app.get("/books/{id}", response_model=Book)
def get_book(id: int):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/books/{id}", response_model=Book)
def update_book(id: int, updated: Book):
    for i, book in enumerate(books):
        if book.id == id:
            updated.id = id
            books[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.patch("/books/{id}", response_model=Book)
def patch_book(id: int, updated: Book):
    for book in books:
        if book.id == id:
            if updated.title: book.title = updated.title
            if updated.author: book.author = updated.author
            if updated.pages: book.pages = updated.pages
            if updated.status: book.status = updated.status
            if updated.genre: book.genre = updated.genre
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/books/{id}")
def delete_book(id: int):
    for i, book in enumerate(books):
        if book.id == id:
            deleted = books.pop(i)
            return {"message": f"Libro '{deleted.title}' eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# -----------------------
# FUNCIONALIDADES AVANZADAS
# -----------------------
@app.get("/books/search/title", response_model=List[Book])
def search_by_title(q: str):
    return [book for book in books if q.lower() in book.title.lower()]

@app.get("/books/search/author", response_model=List[Book])
def search_by_author(q: str):
    return [book for book in books if q.lower() in book.author.lower()]

# -----------------------
# ENDPOINTS ASYNC
# -----------------------
@app.get("/books/async/all", response_model=List[Book])
async def get_books_async():
    await asyncio.sleep(1)  # Simulación I/O
    return books

@app.get("/books/async/{id}", response_model=Book)
async def get_book_async(id: int):
    await asyncio.sleep(1)  # Simulación I/O
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")
