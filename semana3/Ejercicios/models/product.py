from pydantic import BaseModel, Field, validator
from typing import Optional

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    is_available: bool = Field(True)

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.title()

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser un número positivo')
        return v