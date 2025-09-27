from pydantic import BaseModel, Field, validator
from typing import Optional
from models import ProductStatus, ProductCategory

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio debe ser mayor que 0")
    stock: int = Field(..., ge=0, description="Stock no puede ser negativo")
    category: ProductCategory = Field(default=ProductCategory.other)
    status: ProductStatus = Field(default=ProductStatus.active)

    @validator('name')
    def validate_name(cls, v):
        """Capitalizar y limpiar espacios en el nombre"""
        cleaned = v.strip().title()
        if len(cleaned) < 2:
            raise ValueError('Nombre debe tener al menos 2 caracteres después de limpiar')
        return cleaned

    @validator('price')
    def validate_price(cls, v):
        """Redondear precio a 2 decimales"""
        return round(v, 2)

    @validator('description')
    def validate_description(cls, v):
        """Limpiar descripción si existe"""
        if v is not None:
            cleaned = v.strip()
            return cleaned if cleaned else None
        return v

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[ProductCategory] = None
    status: Optional[ProductStatus] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            cleaned = v.strip().title()
            if len(cleaned) < 2:
                raise ValueError('Nombre debe tener al menos 2 caracteres')
            return cleaned
        return v

    @validator('price')
    def validate_price(cls, v):
        if v is not None:
            return round(v, 2)
        return v