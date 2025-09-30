from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import time
from datetime import datetime

from .routers import items
from .docs.descriptions import TAGS_METADATA

# Configuración avanzada de la aplicación
app = FastAPI(
    title="API Clínica Dental SmileCenter - Gestión de Pacientes y Tratamientos",
    description="""
    ## API Clínica Dental SmileCenter

    Esta API proporciona funcionalidades completas para gestionar **pacientes, citas y tratamientos** 
    en la Clínica Dental SmileCenter.

    ### Características principales:

    * **CRUD Completo**: Crear, leer, actualizar y eliminar pacientes, citas y tratamientos
    * **Paginación**: Listado eficiente con paginación
    * **Filtrado**: Múltiples opciones de filtrado y búsqueda
    * **Validación**: Validación robusta con Pydantic
    * **Documentación**: Documentación interactiva completa
    * **Estándares**: Cumple con OpenAPI 3.0

    ### Tipos de datos soportados:

    La API trabaja con elementos del dominio dental que representan:
    - **Pacientes**: Información básica y clínica
    - **Citas**: Registro y control de agendas
    - **Tratamientos**: Procedimientos odontológicos disponibles
    - **Pagos**: Valores asociados a los servicios

    ### Autenticación

    La API utiliza autenticación basada en tokens (en producción).
    Para desarrollo, no se requiere autenticación.

    ### Versionado

    Esta es la versión 2.0 de la API con soporte para:
    - Nuevos campos de metadatos clínicos
    - Mejores validaciones específicas del dominio
    - Respuestas más descriptivas para pacientes y citas
    """,
    version="2.0.0",
    terms_of_service="https://smilecenter.com/terminos",
    contact={
        "name": "Equipo de Desarrollo - Clínica Dental SmileCenter",
        "url": "https://smilecenter.com/contacto",
        "email": "api-support@smilecenter.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
        "identifier": "MIT",
    },
    openapi_tags=TAGS_METADATA,
    docs_url=None,  # Deshabilitamos para personalizar
    redoc_url=None,  # Deshabilitamos para personalizar
    openapi_url="/api/v2/openapi.json"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://app.smilecenter.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiables
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "*.smilecenter.com"]
)

# Middleware personalizado para logging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Timestamp"] = datetime.now().isoformat()
    return response

# Incluir routers
app.include_router(items.router, prefix="/api/v2")

# Endpoint de salud
@app.get(
    "/health",
    tags=["sistema"],
    summary="Verificar estado del sistema",
    description="Endpoint para verificar que la API de la Clínica Dental SmileCenter está funcionando correctamente"
)
async def health_check():
    """
    Verificar estado de salud de la API.

    Retorna información básica sobre el estado del sistema.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "2.0.0",
        "api_name": "API Clínica Dental SmileCenter"
    }

# Configuración personalizada de OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
    )

    # Personalizar esquema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://smilecenter.com/logo-api.png"
    }

    # Agregar información de servidores
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Servidor de desarrollo"
        },
        {
            "url": "https://api-staging.smilecenter.com",
            "description": "Servidor de staging"
        },
        {
            "url": "https://api.smilecenter.com",
            "description": "Servidor de producción"
        }
    ]

    # Agregar esquemas de seguridad
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Token JWT para autenticación"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API Key para autenticación"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Documentación personalizada
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://smilecenter.com/favicon.ico",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js",
        redoc_favicon_url="https://smilecenter.com/favicon.ico",
    )

# Manejador de errores personalizado
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "RECURSO_NO_ENCONTRADO",
            "mensaje": f"El recurso solicitado '{request.url.path}' no fue encontrado",
            "codigo_http": 404,
            "timestamp": datetime.now().isoformat(),
            "sugerencias": [
                "Verificar la URL solicitada",
                "Consultar la documentación en /docs",
                "Verificar la versión de la API"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "ERROR_INTERNO_SERVIDOR",
            "mensaje": "Ocurrió un error interno en el servidor",
            "codigo_http": 500,
            "timestamp": datetime.now().isoformat(),
            "contacto": "api-support@smilecenter.com"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
