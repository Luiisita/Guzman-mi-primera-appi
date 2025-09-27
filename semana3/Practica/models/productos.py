from fastapi import APIRouter, HTTPException, status
from typing import List
from models.products import ProductResponse, ProductCreate, ProductUpdate
from services.products_service import ProductService

# Crear el router
router = APIRouter(tags=["Productos"])

@router.get("/products", response_model=List[ProductResponse])
def get_products():
    """
    Obtiene la lista de todos los productos.
    """
    return ProductService.get_all_products()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """
    Obtiene un producto específico por su ID.
    """
    product = ProductService.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate):
    """
    Crea un nuevo producto.
    """
    try:
        new_product = ProductService.create_product(product_data)
        return new_product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate):
    """
    Actualiza un producto existente por su ID.
    """
    updated_product = ProductService.update_product(product_id, product_data)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return updated_product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    """
    Elimina un producto por su ID.
    """
    if not ProductService.delete_product(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return {}