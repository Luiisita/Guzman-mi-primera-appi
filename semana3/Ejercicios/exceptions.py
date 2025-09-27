class BookNotFoundError(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id
        self.message = f"Book with ID {book_id} not found."

class DuplicateISBNError(Exception):
    def __init__(self, isbn: str):
        self.isbn = isbn
        self.message = f"Book with ISBN {isbn} already exists."

class InvalidBookDataError(Exception):
    def __init__(self, details: str):
        self.details = details
        self.message = f"Invalid book data: {details}"

class BookNotAvailableError(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id
        self.message = f"Book with ID {book_id} is not available for borrowing."

class LibraryFullError(Exception):
    def __init__(self):
        self.message = "The library has reached its maximum borrowing limit (10 books)."