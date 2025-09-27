from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from services import product_service
from models.product import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
def read_products():
    return product_service.get_products()

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int):
    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    return product_service.create_product(product)

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    updated = product_service.update_product(product_id, product)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    if not product_service.delete_product(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return

@router.get("/search/", response_model=List[Product])
def search_products(
    name: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
) -> List[Product]:
    """Buscar productos por nombre y rango de precio"""
    try:
        results = product_service.get_products()

        if name:
            name_lower = name.lower().strip()
            if len(name_lower) < 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El término de búsqueda debe tener al menos 2 caracteres"
                )
            results = [p for p in results if name_lower in p.name.lower()]

        if min_price is not None:
            if min_price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio mínimo no puede ser negativo"
                )
            results = [p for p in results if p.price >= min_price]

        if max_price is not None:
            if max_price is not None and max_price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio máximo no puede ser negativo"
                )
            results = [p for p in results if p.price <= max_price]
        
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio mínimo no puede ser mayor al máximo"
                )

        return results

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )