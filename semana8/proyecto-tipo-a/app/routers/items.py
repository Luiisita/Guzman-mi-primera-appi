from fastapi import APIRouter, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime

from ..models.schemas import (
    ElementoTipoACreate,
    ElementoTipoAUpdate,
    ElementoTipoAResponse,
    ListaElementosResponse,
    ErrorResponse,
    StatusEnum
)
from ..docs.descriptions import (
    ENDPOINT_DESCRIPTIONS,
    RESPONSE_DESCRIPTIONS,
    RESPONSE_EXAMPLES
)

router = APIRouter(
    prefix="/elementos",
    tags=["elementos"],
    responses={
        404: {
            "model": ErrorResponse,
            "description": RESPONSE_DESCRIPTIONS[404],
            "content": {
                "application/json": {
                    "examples": {
                        "no_encontrado": RESPONSE_EXAMPLES["error_no_encontrado"]
                    }
                }
            }
        },
        422: {
            "model": ErrorResponse,
            "description": RESPONSE_DESCRIPTIONS[422],
            "content": {
                "application/json": {
                    "examples": {
                        "validacion": RESPONSE_EXAMPLES["error_validacion"]
                    }
                }
            }
        }
    }
)

# Simulación de base de datos
elementos_db = []
contador_id = 1

@router.post(
    "/",
    response_model=ElementoTipoAResponse,
    status_code=201,
    summary="Registrar nuevo dato clínico",
    description=ENDPOINT_DESCRIPTIONS["crear_elemento"],
    response_description="Dato clínico registrado exitosamente",
    responses={
        201: {
            "model": ElementoTipoAResponse,
            "description": RESPONSE_DESCRIPTIONS[201],
            "content": {
                "application/json": {
                    "examples": {
                        "creado": RESPONSE_EXAMPLES["elemento_creado"]
                    }
                }
            }
        }
    }
)
async def crear_elemento(elemento: ElementoTipoACreate):
    """
    Registrar un nuevo elemento clínico en el sistema.

    - **codigo**: Código único siguiendo patrón (PAC-001, TRAT-123, CITA-456)
    - **nombre**: Nombre descriptivo (ej: "Paciente Juan Pérez", "Ortodoncia Correctiva")
    - **valor_numerico**: Valor relacionado al dato (ej: costo del tratamiento en COP)
    - **categoria**: Categoría del elemento (pacientes, citas, tratamientos)
    """
    global contador_id

    # Verificar código único
    if any(e["codigo"] == elemento.codigo for e in elementos_db):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "CODIGO_DUPLICADO",
                "mensaje": f"El código {elemento.codigo} ya existe",
                "codigo_http": 400,
                "timestamp": datetime.now()
            }
        )

    nuevo_elemento = {
        "id": contador_id,
        **elemento.model_dump(),
        "fecha_creacion": datetime.now(),
        "fecha_actualizacion": datetime.now(),
        "status": StatusEnum.ACTIVO
    }

    elementos_db.append(nuevo_elemento)
    contador_id += 1

    return ElementoTipoAResponse(**nuevo_elemento)

@router.get(
    "/",
    response_model=ListaElementosResponse,
    summary="Listar datos clínicos con filtros",
    description=ENDPOINT_DESCRIPTIONS["listar_elementos"],
    responses={
        200: {
            "model": ListaElementosResponse,
            "description": RESPONSE_DESCRIPTIONS[200],
            "content": {
                "application/json": {
                    "examples": {
                        "lista": RESPONSE_EXAMPLES["lista_elementos"]
                    }
                }
            }
        }
    }
)
async def listar_elementos(
    pagina: int = Query(
        1,
        ge=1,
        description="Número de página",
        example=1
    ),
    limite: int = Query(
        10,
        ge=1,
        le=100,
        description="Registros por página (máximo 100)",
        example=10
    ),
    activo: Optional[bool] = Query(
        None,
        description="Filtrar por estado activo/inactivo",
        example=True
    ),
    categoria: Optional[str] = Query(
        None,
        description="Filtrar por categoría específica",
        example="tratamientos"
    ),
    buscar: Optional[str] = Query(
        None,
        min_length=3,
        description="Buscar en nombre o descripción",
        example="Ortodoncia"
    ),
    orden_por: str = Query(
        "fecha_creacion",
        regex="^(nombre|fecha_creacion|valor_numerico)$",
        description="Campo para ordenar",
        example="fecha_creacion"
    ),
    direccion: str = Query(
        "desc",
        regex="^(asc|desc)$",
        description="Dirección del ordenamiento",
        example="desc"
    )
):
    """
    Obtener lista paginada de elementos clínicos con filtros opcionales.

    Soporta filtrado por:
    - Estado activo/inactivo
    - Categoría específica (pacientes, citas, tratamientos)
    - Búsqueda por texto en nombre/descripción

    Y ordenamiento por:
    - Nombre, fecha de creación, o valor numérico (ej: costo tratamiento)
    - Dirección ascendente o descendente
    """
    # Aplicar filtros
    elementos_filtrados = elementos_db.copy()

    if activo is not None:
        elementos_filtrados = [e for e in elementos_filtrados if e["activo"] == activo]

    if categoria:
        elementos_filtrados = [e for e in elementos_filtrados if e["categoria"] == categoria]

    if buscar:
        buscar_lower = buscar.lower()
        elementos_filtrados = [
            e for e in elementos_filtrados
            if buscar_lower in e["nombre"].lower() or
               (e.get("descripcion") and buscar_lower in e["descripcion"].lower())
        ]

    # Ordenamiento
    reverse_order = direccion == "desc"
    if orden_por == "nombre":
        elementos_filtrados.sort(key=lambda x: x["nombre"], reverse=reverse_order)
    elif orden_por == "valor_numerico":
        elementos_filtrados.sort(key=lambda x: x["valor_numerico"], reverse=reverse_order)
    else:  # fecha_creacion
        elementos_filtrados.sort(key=lambda x: x["fecha_creacion"], reverse=reverse_order)

    # Paginación
    total = len(elementos_filtrados)
    inicio = (pagina - 1) * limite
    fin = inicio + limite
    elementos_pagina = elementos_filtrados[inicio:fin]

    return ListaElementosResponse(
        elementos=[ElementoTipoAResponse(**e) for e in elementos_pagina],
        total=total,
        pagina=pagina,
        por_pagina=limite
    )

@router.get(
    "/{elemento_id}",
    response_model=ElementoTipoAResponse,
    summary="Obtener dato clínico por ID",
    description=ENDPOINT_DESCRIPTIONS["obtener_elemento"],
    responses={
        200: {
            "model": ElementoTipoAResponse,
            "description": RESPONSE_DESCRIPTIONS[200]
        }
    }
)
async def obtener_elemento(
    elemento_id: int = Path(
        ...,
        gt=0,
        description="ID único del elemento clínico",
        example=1
    )
):
    """
    Obtener un elemento específico por su ID único.

    Retorna el dato clínico completo con metadatos como
    fechas de creación y actualización.
    """
    elemento = next((e for e in elementos_db if e["id"] == elemento_id), None)

    if not elemento:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "ELEMENTO_NO_ENCONTRADO",
                "mensaje": f"El elemento con ID {elemento_id} no fue encontrado",
                "codigo_http": 404,
                "timestamp": datetime.now()
            }
        )

    return ElementoTipoAResponse(**elemento)

@router.put(
    "/{elemento_id}",
    response_model=ElementoTipoAResponse,
    summary="Actualizar dato clínico existente",
    description=ENDPOINT_DESCRIPTIONS["actualizar_elemento"],
    responses={
        200: {
            "model": ElementoTipoAResponse,
            "description": RESPONSE_DESCRIPTIONS[200]
        }
    }
)
async def actualizar_elemento(
    elemento_data: ElementoTipoAUpdate,
    elemento_id: int = Path(
        ...,
        gt=0,
        description="ID único del elemento a actualizar",
        example=1
    )
):
    """
    Actualizar un registro clínico existente de forma parcial.

    Solo los campos enviados en el request serán modificados.
    La fecha de actualización se actualiza automáticamente.
    """
    elemento_idx = next(
        (i for i, e in enumerate(elementos_db) if e["id"] == elemento_id),
        None
    )

    if elemento_idx is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "ELEMENTO_NO_ENCONTRADO",
                "mensaje": f"El elemento con ID {elemento_id} no fue encontrado",
                "codigo_http": 404,
                "timestamp": datetime.now()
            }
        )

    # Actualizar solo campos enviados
    update_data = elemento_data.model_dump(exclude_unset=True)
    elementos_db[elemento_idx].update(update_data)
    elementos_db[elemento_idx]["fecha_actualizacion"] = datetime.now()

    return ElementoTipoAResponse(**elementos_db[elemento_idx])

@router.delete(
    "/{elemento_id}",
    status_code=204,
    summary="Eliminar dato clínico",
    description=ENDPOINT_DESCRIPTIONS["eliminar_elemento"],
    responses={
        204: {
            "description": RESPONSE_DESCRIPTIONS[204]
        }
    }
)
async def eliminar_elemento(
    elemento_id: int = Path(
        ...,
        gt=0,
        description="ID único del elemento a eliminar",
        example=1
    )
):
    """
    Eliminar permanentemente un registro clínico del sistema.

    ⚠️ **Advertencia**: Esta operación es irreversible.
    """
    elemento_idx = next(
        (i for i, e in enumerate(elementos_db) if e["id"] == elemento_id),
        None
    )

    if elemento_idx is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "ELEMENTO_NO_ENCONTRADO",
                "mensaje": f"El elemento con ID {elemento_id} no fue encontrado",
                "codigo_http": 404,
                "timestamp": datetime.now()
            }
        )

    elementos_db.pop(elemento_idx)
    return JSONResponse(status_code=204, content=None)

# Endpoint adicional para estadísticas
@router.get(
    "/estadisticas/resumen",
    tags=["reportes"],
    summary="Obtener estadísticas clínicas",
    description="Obtiene un resumen estadístico de pacientes, citas y tratamientos"
)
async def obtener_estadisticas():
    """
    Obtener estadísticas generales del sistema.

    Incluye conteos por estado, categorías (pacientes, citas, tratamientos)
    y valores promedio (ej: costo de tratamientos).
    """
    if not elementos_db:
        return {
            "total_elementos": 0,
            "elementos_activos": 0,
            "elementos_inactivos": 0,
            "valor_promedio": 0,
            "categorias": {}
        }

    activos = sum(1 for e in elementos_db if e["activo"])
    valores = [e["valor_numerico"] for e in elementos_db]

    # Contar por categorías
    categorias = {}
    for elemento in elementos_db:
        cat = elemento["categoria"]
        categorias[cat] = categorias.get(cat, 0) + 1

    return {
        "total_elementos": len(elementos_db),
        "elementos_activos": activos,
        "elementos_inactivos": len(elementos_db) - activos,
        "valor_promedio": sum(valores) / len(valores),
        "valor_minimo": min(valores),
        "valor_maximo": max(valores),
        "categorias": categorias
    }
