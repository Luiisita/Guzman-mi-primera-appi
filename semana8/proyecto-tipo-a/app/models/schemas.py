from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    """Estados disponibles para elementos tipo A"""
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    PENDIENTE = "pendiente"

class ElementoTipoABase(BaseModel):
    """Esquema base para elementos tipo A"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "codigo": "PAC-001",
                "nombre": "Paciente Juan Pérez",
                "descripcion": "Paciente con cita inicial para revisión odontológica",
                "valor_numerico": 150.75,
                "activo": True,
                "categoria": "pacientes"
            }
        }
    )

    codigo: str = Field(
        ...,
        description="Código único del elemento",
        min_length=3,
        max_length=20,
        pattern="^[A-Z]{2,5}-[0-9]{3,6}$",
        examples=["PAC-001", "TRAT-123", "CITA-456"]
    )

    nombre: str = Field(
        ...,
        description="Nombre descriptivo del elemento",
        min_length=5,
        max_length=100,
        examples=["Paciente Juan Pérez", "Tratamiento Ortodoncia", "Cita Inicial"]
    )

    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada opcional",
        max_length=500,
        examples=["Paciente remitido para tratamiento dental integral"]
    )

    valor_numerico: float = Field(
        ...,
        description="Valor numérico asociado (ej: costo de tratamiento, saldo paciente)",
        ge=0,
        le=10000,
        examples=[100.5, 250.75, 999.99]
    )

    activo: bool = Field(
        True,
        description="Indica si el elemento está activo",
        examples=[True, False]
    )

    categoria: str = Field(
        ...,
        description="Categoría del elemento",
        examples=["pacientes", "tratamientos", "citas"]
    )

class ElementoTipoACreate(ElementoTipoABase):
    """Esquema para crear elementos tipo A"""
    pass

class ElementoTipoAUpdate(BaseModel):
    """Esquema para actualizar elementos tipo A"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Paciente Ana Gómez",
                "descripcion": "Actualización de historial clínico",
                "valor_numerico": 200.50,
                "activo": True
            }
        }
    )

    nombre: Optional[str] = Field(None, min_length=5, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    valor_numerico: Optional[float] = Field(None, ge=0, le=10000)
    activo: Optional[bool] = None
    categoria: Optional[str] = None

class ElementoTipoAResponse(ElementoTipoABase):
    """Esquema de respuesta para elementos tipo A"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "codigo": "PAC-001",
                "nombre": "Paciente Juan Pérez",
                "descripcion": "Paciente con cita inicial para revisión odontológica",
                "valor_numerico": 150.75,
                "activo": True,
                "categoria": "pacientes",
                "fecha_creacion": "2024-01-15T10:30:00",
                "fecha_actualizacion": "2024-01-15T10:30:00",
                "status": "activo"
            }
        }
    )

    id: int = Field(
        ...,
        description="ID único generado automáticamente",
        examples=[1, 2, 100]
    )

    fecha_creacion: datetime = Field(
        ...,
        description="Fecha y hora de creación",
        examples=["2024-01-15T10:30:00"]
    )

    fecha_actualizacion: datetime = Field(
        ...,
        description="Fecha y hora de última actualización",
        examples=["2024-01-15T14:45:00"]
    )

    status: StatusEnum = Field(
        ...,
        description="Estado actual del elemento",
        examples=["activo", "inactivo", "pendiente"]
    )

class ListaElementosResponse(BaseModel):
    """Respuesta para lista de elementos"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "elementos": [
                    {
                        "id": 1,
                        "codigo": "PAC-001",
                        "nombre": "Paciente Juan Pérez",
                        "valor_numerico": 100.0,
                        "activo": True,
                        "status": "activo"
                    }
                ],
                "total": 1,
                "pagina": 1,
                "por_pagina": 10
            }
        }
    )

    elementos: List[ElementoTipoAResponse] = Field(
        ...,
        description="Lista de elementos tipo A"
    )

    total: int = Field(
        ...,
        description="Total de elementos encontrados",
        examples=[25, 100, 500]
    )

    pagina: int = Field(
        ...,
        description="Página actual",
        examples=[1, 2, 5]
    )

    por_pagina: int = Field(
        ...,
        description="Elementos por página",
        examples=[10, 20, 50]
    )

class ErrorResponse(BaseModel):
    """Esquema estándar para respuestas de error"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "PACIENTE_NO_ENCONTRADO",
                "mensaje": "El paciente con ID 999 no fue encontrado",
                "codigo_http": 404,
                "timestamp": "2024-01-15T10:30:00"
            }
        }
    )

    error: str = Field(..., description="Código de error")
    mensaje: str = Field(..., description="Mensaje descriptivo del error")
    codigo_http: int = Field(..., description="Código HTTP del error")
    timestamp: datetime = Field(..., description="Momento del error")
