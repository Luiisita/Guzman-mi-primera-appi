from pydantic import BaseModel, Field, validator, model_validator
from typing import Optional, List, Set
from datetime import date

class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., description="The title of the book")
    author: str = Field(..., description="The author of the book")
    isbn: str = Field(..., description="The ISBN-13 of the book")
    year: int = Field(..., description="The publication year of the book")
    rating: float = Field(..., description="The rating of the book (0.0 to 5.0)")
    is_available: bool = Field(True, description="Is the book available for borrowing?")
    is_bestseller: bool = Field(False, description="Is the book a bestseller?")
    tags: Set[str] = Field(set(), description="Set of unique tags for the book")

    @validator('title')
    def validate_title(cls, v):
        return v.title()

    @validator('author')
    def validate_author(cls, v):
        if v.isdigit():
            raise ValueError('El autor no puede ser solo números')
        return v.title()

    @validator('rating')
    def validate_rating(cls, v):
        if not 0.0 <= v <= 5.0:
            raise ValueError('El rating debe estar entre 0.0 y 5.0')
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Los tags no pueden tener duplicados')
        return v

    @model_validator(mode='after')
    def check_bestseller_rating(self):
        if self.is_bestseller and self.rating < 4.0:
            raise ValueError('Los libros bestseller deben tener un rating de al menos 4.0')
        return self