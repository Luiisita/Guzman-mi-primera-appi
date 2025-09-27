from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List, Dict
from datetime import datetime
from models import Product, ProductCategory, ProductStatus
from schemas import product_schemas

router = APIRouter()

# Base de datos en memoria (aquí simulamos la persistencia de datos)
products_db: Dict[int, Product] = {}
next_id: int = 1

def get_current_time() -> datetime:
    return datetime.now()

def product_not_found(product_id: int):
    """Helper para error 404"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Producto con ID {product_id} no encontrado"
    )

def validation_error(message: str):
    """Helper para errores de validación custom"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )

def create_product_record(product_data: product_schemas.ProductCreate) -> Product:
    """Crear registro de producto con timestamp"""
    global next_id
    
    # Verificar si ya existe un producto con el mismo nombre (bonus)
    for existing_product in products_db.values():
        if existing_product.name.lower() == product_data.name.lower():
            validation_error(f"Ya existe un producto con el nombre '{product_data.name}'")
    
    new_product = Product(
        id=next_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category,
        status=product_data.status,
        created_at=get_current_time(),
        updated_at=get_current_time()
    )
    
    products_db[next_id] = new_product
    next_id += 1
    return new_product

# ==================== CRUD ENDPOINTS ====================

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: product_schemas.ProductCreate):
    """Crear un nuevo producto"""
    new_product = create_product_record(product)
    return new_product

@router.get("/", response_model=List[Product])
def get_products(
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    category: Optional[ProductCategory] = Query(None, description="Filtrar por categoría"),
    status: Optional[ProductStatus] = Query(None, description="Filtrar por estado"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados")
):
    """Listar productos con filtros opcionales"""
    products = list(products_db.values())
    
    # Aplicar filtros
    if min_price is not None:
        products = [p for p in products if p.price >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p.price <= max_price]
    
    if category is not None:
        products = [p for p in products if p.category == category]
    
    if status is not None:
        products = [p for p in products if p.status == status]
    
    # Validar rango de precios
    if min_price is not None and max_price is not None and min_price > max_price:
        validation_error("El precio mínimo no puede ser mayor que el precio máximo")
    
    # Limitar resultados
    products = products[:limit]
    
    return products

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Obtener un producto específico por ID"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    return products_db[product_id]

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: product_schemas.ProductCreate):
    """Actualizar un producto completamente"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    # Verificar nombre único excluyendo el producto actual
    for existing_id, existing_product in products_db.items():
        if (existing_id != product_id and 
            existing_product.name.lower() == product_update.name.lower()):
            validation_error(f"Ya existe otro producto con el nombre '{product_update.name}'")
    
    # Actualizar con todos los datos nuevos
    current_product = products_db[product_id]
    current_product.name = product_update.name
    current_product.description = product_update.description
    current_product.price = product_update.price
    current_product.stock = product_update.stock
    current_product.category = product_update.category
    current_product.status = product_update.status
    current_product.updated_at = get_current_time()
    
    return current_product

@router.patch("/{product_id}", response_model=Product)
def update_product_partial(product_id: int, product_update: product_schemas.ProductUpdate):
    """Actualizar un producto parcialmente"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    # Verificar nombre único si se está actualizando
    if product_update.name is not None:
        for existing_id, existing_product in products_db.items():
            if (existing_id != product_id and 
                existing_product.name.lower() == product_update.name.lower()):
                validation_error(f"Ya existe otro producto con el nombre '{product_update.name}'")
    
    # Actualizar solo los campos proporcionados
    current_product = products_db[product_id]
    update_data = product_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(current_product, key, value)
    
    current_product.updated_at = get_current_time()
    
    return current_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    """Eliminar un producto"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    del products_db[product_id]

# ==================== FUNCIÓN DE INICIALIZACIÓN ====================

def add_sample_data():
    """Agregar datos de ejemplo al iniciar la aplicación"""
    sample_products_data = [
        {
            "name": "laptop gamer",
            "description": "Laptop para gaming con RTX 4060",
            "price": 899.99,
            "stock": 5,
            "category": ProductCategory.electronics,
            "status": ProductStatus.active
        },
        {
            "name": "camiseta básica",
            "description": "Camiseta de algodón 100%",
            "price": 19.99,
            "stock": 25,
            "category": ProductCategory.clothing,
            "status": ProductStatus.active
        },
        {
            "name": "python cookbook",
            "description": "Recetas de programación en Python",
            "price": 45.50,
            "stock": 0,
            "category": ProductCategory.books,
            "status": ProductStatus.out_of_stock
        },
        {
            "name": "mouse inalámbrico",
            "description": "Mouse ergonómico inalámbrico",
            "price": 29.99,
            "stock": 15,
            "category": ProductCategory.electronics,
            "status": ProductStatus.active
        },
        {
            "name": "jean clásico",
            "description": "Jean azul talla 32",
            "price": 49.99,
            "stock": 8,
            "category": ProductCategory.clothing,
            "status": ProductStatus.inactive
        }
    ]
    
    for product_data in sample_products_data:
        product_create = product_schemas.ProductCreate(**product_data)
        create_product_record(product_create)

# Agregar datos de ejemplo al cargar el router
add_sample_data()