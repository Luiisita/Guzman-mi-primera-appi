from fastapi.testclient import TestClient
from semana6.main import app
import pytest

client = TestClient(app)

def test_create_book_success():
    response = client.post(
        "/api/v1/books",
        json={
            "title": "New Test Book",
            "author": "Test Author",
            "isbn": "978-9876543210",
            "year": 2023,
            "rating": 4.5
        },
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["title"] == "New Test Book"
    assert data["isbn"] == "978-9876543210"

def test_create_book_duplicate_isbn():
    client.post(
        "/api/v1/books",
        json={
            "title": "Another Book",
            "author": "Test Author",
            "isbn": "978-1234567890",
            "year": 2024,
            "rating": 4.0
        },
    )
    response = client.post(
        "/api/v1/books",
        json={
            "title": "Another Book",
            "author": "Test Author",
            "isbn": "978-1234567890",
            "year": 2024,
            "rating": 4.0
        },
    )
    assert response.status_code == 409
    assert response.json()["error_code"] == "DUPLICATE_ISBN"

def test_get_book_not_found():
    response = client.get("/api/v1/books/999")
    assert response.status_code == 404
    assert response.json()["error_code"] == "BOOK_NOT_FOUND"

def test_search_books_with_filters():
    response = client.get("/api/v1/books/search?title=dune&genre=scifi")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Dune"