from fastapi import FastAPI
from routers.books import router as books_router
from routers.borrowing import router as borrowing_router
from handlers import configure_exception_handlers

app = FastAPI(
    title="Library Management API",
    description="API para gestionar una biblioteca",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url=None
)

configure_exception_handlers(app)

app.include_router(books_router, prefix="/api/v1")
app.include_router(borrowing_router, prefix="/api/v1")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}