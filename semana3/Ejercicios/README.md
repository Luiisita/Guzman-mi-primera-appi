# Library Management API
## Installation
Clona el repositorio: git clone <URL_del_repositorio> cd ejercicio-biblioteca

Crea y activa un entorno virtual: python -m venv venv source venv/bin/activate

Instala las dependencias: pip install -r requirements.txt

## Quick Start
Inicia el servidor de Uvicorn: uvicorn app.main:app --reload

La API estará disponible en http://127.0.0.1:8000.

## API Endpoints
### Libros (/api/v1/books)
GET /: Listar todos los libros con paginación.
GET /search: Búsqueda avanzada por title, author, genre, etc.
GET /stats: Estadísticas de la biblioteca.
POST /: Crear un nuevo libro.
GET /{book_id}: Obtener un libro por su ID.
PUT /{book_id}: Actualizar un libro.
DELETE /{book_id}: Eliminar un libro.
### Préstamos (/api/v1/borrowing)
POST /borrow/{book_id}: Prestar un libro.
POST /return/{book_id}: Devolver un libro.
GET /active: Listar libros prestados.
### Categorías (/api/v1/categories)
NOTA: No implementado en este código, pero la estructura está lista para su expansión.

## Ejemplos
# Crear un libro
curl -X POST "http://localhost:8000/api/v1/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "isbn": "978-0547928227",
    "year": 1937,
    "rating": 4.7
  }'

# Buscar por título y rating
curl "http://localhost:8000/api/v1/books/search?title=Lord&year_from=1950"

# Prestar un libro
curl -X POST "http://localhost:8000/api/v1/borrowing/borrow/1"