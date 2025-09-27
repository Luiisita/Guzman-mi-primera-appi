from typing import List, Optional
from models.product import Product

products_db = [
    Product(id=1, name="Laptop", price=1200.50),
    Product(id=2, name="Mouse", price=25.00),
    Product(id=3, name="Teclado", price=75.99),
    Product(id=4, name="Monitor", price=300.00),
    Product(id=5, name="Mouse Pad", price=15.00)
]

def get_products() -> List[Product]:
    return products_db

def get_product(product_id: int) -> Optional[Product]:
    for p in products_db:
        if p.id == product_id:
            return p
    return None

def create_product(product: Product) -> Product:
    new_id = len(products_db) + 1
    new_product = product.copy(update={"id": new_id})
    products_db.append(new_product)
    return new_product

def update_product(product_id: int, updated_product: Product) -> Optional[Product]:
    for i, p in enumerate(products_db):
        if p.id == product_id:
            products_db[i] = updated_product.copy(update={"id": product_id})
            return products_db[i]
    return None

def delete_product(product_id: int) -> bool:
    global products_db
    original_len = len(products_db)
    products_db = [p for p in products_db if p.id != product_id]
    return len(products_db) < original_len