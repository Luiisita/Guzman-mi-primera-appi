from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    out_of_stock = "out_of_stock"

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"
    sports = "sports"
    other = "other"

class Product(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: ProductCategory
    status: ProductStatus
    created_at: datetime
    updated_at: datetime