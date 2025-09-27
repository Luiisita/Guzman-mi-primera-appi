from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from exceptions import BookNotFoundError, DuplicateISBNError, BookNotAvailableError, LibraryFullError
import logging

def configure_exception_handlers(app):
    logging.basicConfig(level=logging.INFO)

    @app.exception_handler(BookNotFoundError)
    async def book_not_found_handler(request: Request, exc: BookNotFoundError):
        logging.error(f"BookNotFoundError: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"success": False, "error_code": "BOOK_NOT_FOUND", "message": exc.message}
        )

    @app.exception_handler(DuplicateISBNError)
    async def duplicate_isbn_handler(request: Request, exc: DuplicateISBNError):
        logging.error(f"DuplicateISBNError: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "error_code": "DUPLICATE_ISBN", "message": exc.message}
        )

    @app.exception_handler(BookNotAvailableError)
    async def book_not_available_handler(request: Request, exc: BookNotAvailableError):
        logging.warning(f"BookNotAvailableError: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "error_code": "BOOK_NOT_AVAILABLE", "message": exc.message}
        )
    
    @app.exception_handler(LibraryFullError)
    async def library_full_handler(request: Request, exc: LibraryFullError):
        logging.warning(f"LibraryFullError: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "error_code": "LIBRARY_FULL", "message": exc.message}
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logging.error(f"HTTPException: {exc.detail} with status {exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error_code": "HTTP_ERROR", "message": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.critical(f"Unhandled Exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error_code": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}
        )

