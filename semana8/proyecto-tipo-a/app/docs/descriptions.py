"""Descripciones centralizadas para la documentación API"""

# Descripciones de tags
TAGS_METADATA = [
    {
        "name": "pacientes",
        "description": "Operaciones CRUD para la gestión de pacientes en la Clínica Dental SmileCenter. "
                       "Permite crear, leer, actualizar y eliminar información de pacientes.",
        "externalDocs": {
            "description": "Documentación externa",
            "url": "https://docs.clinicadental.com/api-pacientes",
        },
    },
    {
        "name": "tratamientos",
        "description": "Endpoints relacionados con la gestión de tratamientos odontológicos.",
    },
    {
        "name": "citas",
        "description": "Gestión de citas médicas y odontológicas de la Clínica Dental SmileCenter.",
    },
]

# Descripciones de endpoints
ENDPOINT_DESCRIPTIONS = {
    "crear_elemento": """
    ### Crear Nuevo Paciente / Tratamiento / Cita

    Crea un nuevo registro en el sistema con las siguientes características:

    - **Código único**: Debe seguir el patrón XXXX-000000
    - **Validación automática**: Todos los campos son validados
    - **Respuesta completa**: Retorna el registro creado con metadatos

    #### Ejemplo de uso:
    ```json
    {
        "codigo": "PAC-001",
        "nombre": "Paciente Juan Pérez",
        "descripcion": "Paciente remitido para tratamiento odontológico",
        "valor_numerico": 150.75,
        "categoria": "pacientes"
    }
    ```

    #### Validaciones:
    - El código debe ser único en el sistema
    - El nombre debe tener entre 5 y 100 caracteres
    - El valor numérico debe estar entre 0 y 10,000
    """,

    "obtener_elemento": """
    ### Obtener Paciente / Tratamiento / Cita por ID

    Recupera un registro específico usando su identificador único.

    #### Respuesta exitosa:
    - Retorna el registro completo con metadatos
    - Incluye fechas de creación y actualización
    - Muestra el estado actual del registro

    #### Casos de error:
    - **404**: Registro no encontrado
    - **422**: ID inválido
    """,

    "listar_elementos": """
    ### Listar Pacientes / Tratamientos / Citas con Paginación

    Obtiene una lista paginada de registros con filtros opcionales.

    #### Parámetros de filtrado:
    - **activo**: Filtrar por estado activo/inactivo
    - **categoria**: Filtrar por pacientes, tratamientos o citas
    - **buscar**: Búsqueda por nombre o descripción

    #### Paginación:
    - **pagina**: Número de página (default: 1)
    - **limite**: Registros por página (default: 10, max: 100)

    #### Ordenamiento:
    - **orden_por**: Campo para ordenar (nombre, fecha_creacion, valor_numerico)
    - **direccion**: asc (ascendente) o desc (descendente)
    """,

    "actualizar_elemento": """
    ### Actualizar Registro Existente (Paciente / Tratamiento / Cita)

    Actualiza parcialmente un registro existente. Solo los campos enviados serán modificados.

    #### Características:
    - **Actualización parcial**: Solo campos enviados son modificados
    - **Validación completa**: Todos los campos enviados son validados
    - **Timestamp automático**: Se actualiza fecha_actualizacion automáticamente

    #### Campos actualizables:
    - nombre, descripcion, valor_numerico, activo, categoria
    - El código e ID no pueden ser modificados
    """,

    "eliminar_elemento": """
    ### Eliminar Registro (Paciente / Tratamiento / Cita)

    Elimina permanentemente un registro del sistema.

    ⚠️ **Advertencia**: Esta operación es irreversible.

    #### Validaciones:
    - El registro debe existir
    - No debe tener dependencias activas
    - Requiere confirmación en producción
    """,
}

# Descripciones de respuestas comunes
RESPONSE_DESCRIPTIONS = {
    200: "Operación exitosa",
    201: "Registro creado exitosamente",
    204: "Registro eliminado exitosamente",
    400: "Solicitud inválida - Error en los datos enviados",
    404: "Registro no encontrado",
    422: "Error de validación - Datos no cumplen con los esquemas",
    500: "Error interno del servidor",
}

# Ejemplos de responses
RESPONSE_EXAMPLES = {
    "elemento_creado": {
        "summary": "Registro creado exitosamente",
        "description": "Ejemplo de respuesta cuando se crea un nuevo paciente, tratamiento o cita",
        "value": {
            "id": 1,
            "codigo": "PAC-001",
            "nombre": "Paciente Juan Pérez",
            "descripcion": "Paciente remitido para tratamiento odontológico",
            "valor_numerico": 150.75,
            "activo": True,
            "categoria": "pacientes",
            "fecha_creacion": "2024-01-15T10:30:00",
            "fecha_actualizacion": "2024-01-15T10:30:00",
            "status": "activo"
        }
    },

    "lista_elementos": {
        "summary": "Lista de registros paginada",
        "description": "Ejemplo de respuesta con lista paginada de pacientes, tratamientos o citas",
        "value": {
            "elementos": [
                {
                    "id": 1,
                    "codigo": "PAC-001",
                    "nombre": "Paciente Juan Pérez",
                    "valor_numerico": 100.0,
                    "activo": True,
                    "status": "activo"
                },
                {
                    "id": 2,
                    "codigo": "TRAT-002",
                    "nombre": "Tratamiento Ortodoncia",
                    "valor_numerico": 200.0,
                    "activo": False,
                    "status": "inactivo"
                }
            ],
            "total": 2,
            "pagina": 1,
            "por_pagina": 10
        }
    },

    "error_no_encontrado": {
        "summary": "Registro no encontrado",
        "description": "Error cuando se busca un paciente, tratamiento o cita que no existe",
        "value": {
            "error": "REGISTRO_NO_ENCONTRADO",
            "mensaje": "El paciente con ID 999 no fue encontrado",
            "codigo_http": 404,
            "timestamp": "2024-01-15T10:30:00"
        }
    },

    "error_validacion": {
        "summary": "Error de validación",
        "description": "Error cuando los datos no cumplen las validaciones",
        "value": {
            "error": "VALIDACION_FALLIDA",
            "mensaje": "El código debe seguir el patrón XXXX-000000",
            "codigo_http": 422,
            "timestamp": "2024-01-15T10:30:00"
        }
    }
}
