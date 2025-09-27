from fastapi import FastAPI
from routers import products

app = FastAPI(
    title="API de Productos - Semana 3",
    description="API para gestión de productos con validaciones Pydantic y manejo de errores",
    version="1.0.0"
)

# Incluir routers
app.include_router(products.router, prefix="/products", tags=["Productos"])

@app.get("/")
def read_root():
    """Endpoint de bienvenida"""
    return {
        "message": "Bienvenido a la API de Productos - Semana 3",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "CRUD completo de productos",
            "Validaciones Pydantic avanzadas",
            "Manejo de errores con HTTPException",
            "Filtros por precio y categoría"
        ]
    }