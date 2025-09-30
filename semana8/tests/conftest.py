import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import json
# Importa tus componentes de la aplicación. Asegúrate de que las rutas sean correctas.
from app.main import app
from app.database import get_db, Base
from app.auth.auth_handler import create_access_token

# Configuración genérica de base de datos de prueba
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test_generic.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

fake = Faker('es_ES') # Usamos Faker en español

@pytest.fixture(scope="session")
def event_loop():
    """Configuración del loop de eventos para tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Fixture de sesión de base de datos genérica"""
    # Crear tablas
    Base.metadata.create_all(bind=engine_test)

    # Crear sesión
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Limpiar después de cada test
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture de cliente de prueba genérico"""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Fixture para headers de autenticación genérica (asume un dentista/admin)"""
    # Token genérico para tests
    token_data = {"sub": "dr_guzman_test", "rol": "dentista"}
    token = create_access_token(token_data)

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_user_generic():
    """Fixture para usuario genérico de prueba (puede ser un empleado o admin)"""
    return {
        "username": "admin_smilecenter",
        "email": "admin@smilecenter.com",
        "password": "passwordSeguro123",
        "is_active": True,
        "role": "administrador"
    }

# =======================================================
# FIXTURES TIPO A - ESPECÍFICAS (Clínica Dental SmileCenter)
# Enfocadas en Gestión de Datos: Pacientes, Citas, Historiales
# =======================================================

@pytest.fixture
def sample_paciente():
    """Fixture para un objeto Paciente de la Clínica Dental"""
    return {
        "nombre": fake.first_name(),
        "apellido": fake.last_name(),
        "cedula": fake.bothify(text='V-########'),
        "telefono": fake.phone_number(),
        "email": fake.email(),
        "fecha_nacimiento": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "direccion": fake.address().replace('\n', ', '),
        "activo": True,
        "alergias": fake.random_element(["Penicilina", "Látex", "Ninguna"]),
        "historial_medico_inicial": "Hipertenso controlado."
    }

@pytest.fixture
def sample_cita_tipo_a(sample_paciente):
    """Fixture para una Cita Médica de la Clínica Dental (Gestión de Datos temporal)"""
    start_time = datetime.now() + timedelta(days=fake.random_int(1, 30), hours=fake.random_int(9, 17))
    end_time = start_time + timedelta(minutes=fake.random_element([30, 45, 60]))

    return {
        # Usamos datos de un paciente ya creado para el test
        "paciente_id": 1, 
        "doctor_asignado": fake.name(),
        "tratamiento": fake.random_element(["Limpieza Profunda", "Blanqueamiento Láser", "Revisión General", "Extracción Molar"]),
        "fecha_inicio": start_time.isoformat(),
        "fecha_fin": end_time.isoformat(),
        "estado": fake.random_element(["programada", "confirmada", "cancelada"]),
        "costo_estimado": fake.random_int(50, 500) * 10,
    }
@pytest.fixture
def sample_entidad_tipo_a():
    """Fixture para entidad genérica tipo A"""
    return {
        "nombre": fake.company(),
        "descripcion": fake.text(max_nb_chars=200),
        "categoria": fake.random_element(["categoria_1", "categoria_2", "categoria_3"]),
        "estado": "activo",
        "fecha_registro": fake.date_time_this_year().isoformat(),
        "codigo": fake.uuid4(),
        "propiedades": {
            "propiedad_1": fake.word(),
            "propiedad_2": fake.random_int(1, 100),
            "propiedad_3": fake.boolean()
        }
    }

@pytest.fixture
def multiple_entidades_tipo_a():
    """Fixture para múltiples entidades tipo A"""
    return [
        {
            "nombre": fake.company(),
            "descripcion": fake.text(max_nb_chars=100),
            "categoria": "categoria_1",
            "estado": "activo"
        }
        for _ in range(5)
    ]

# ========================
# FIXTURES TIPO B - Programación Temporal
# ========================

@pytest.fixture
def sample_recurso_tipo_b():
    """Fixture para recurso programable genérico tipo B"""
    return {
        "nombre": fake.word() + "_recurso",
        "descripcion": fake.text(max_nb_chars=150),
        "capacidad": fake.random_int(1, 50),
        "disponible": True,
        "hora_inicio": "09:00",
        "hora_fin": "17:00",
        "dias_disponibles": ["lunes", "martes", "miercoles", "jueves", "viernes"],
        "duracion_minima": 30,
        "tipo_recurso": fake.random_element(["sala", "equipo", "servicio"])
    }

@pytest.fixture
def sample_reserva_tipo_b():
    """Fixture para reserva genérica tipo B"""
    return {
        "recurso_id": 1,
        "fecha_inicio": fake.future_datetime(end_date="+30d").isoformat(),
        "fecha_fin": fake.future_datetime(end_date="+30d").isoformat(),
        "descripcion": fake.text(max_nb_chars=100),
        "participantes": fake.random_int(1, 10),
        "estado": "confirmada"
    }

# ========================
# FIXTURES TIPO C - Servicios de Usuario
# ========================

@pytest.fixture
def sample_asignacion_tipo_c():
    """Fixture para asignación genérica tipo C"""
    return {
        "usuario_id": 1,
        "elemento_id": 1,
        "tipo_asignacion": fake.random_element(["temporal", "permanente", "condicional"]),
        "fecha_inicio": fake.date_time_this_year().isoformat(),
        "fecha_vencimiento": fake.future_datetime(end_date="+1y").isoformat(),
        "activo": True,
        "prioridad": fake.random_element(["alta", "media", "baja"]),
        "configuracion": {
            "notificaciones": True,
            "acceso_completo": fake.boolean(),
            "limite_uso": fake.random_int(1, 100)
        }
    }

@pytest.fixture
def sample_perfil_usuario_tipo_c():
    """Fixture para perfil de usuario genérico tipo C"""
    return {
        "nombre_completo": fake.name(),
        "telefono": fake.phone_number(),
        "direccion": fake.address(),
        "fecha_nacimiento": fake.date_of_birth().isoformat(),
        "preferencias": {
            "tema": fake.random_element(["claro", "oscuro"]),
            "idioma": fake.random_element(["es", "en"]),
            "notificaciones": True
        }
    }

# ========================
# FIXTURES TIPO D - Catálogo de Elementos
# ========================

@pytest.fixture
def sample_elemento_tipo_d():
    """Fixture para elemento de catálogo genérico tipo D"""
    return {
        "nombre": fake.word() + "_producto",
        "descripcion": fake.text(max_nb_chars=200),
        "categoria": fake.random_element(["electronica", "ropa", "hogar", "deportes"]),
        "precio": round(fake.random.uniform(10.0, 1000.0), 2),
        "stock": fake.random_int(0, 100),
        "sku": fake.uuid4()[:8].upper(),
        "dimensiones": {
            "largo": fake.random.uniform(1.0, 100.0),
            "ancho": fake.random.uniform(1.0, 100.0),
            "alto": fake.random.uniform(1.0, 100.0)
        },
        "peso": fake.random.uniform(0.1, 50.0),
        "disponible": True
    }

@pytest.fixture
def sample_transaccion_tipo_d():
    """Fixture para transacción genérica tipo D"""
    return {
        "elemento_id": 1,
        "cantidad": fake.random_int(1, 10),
        "tipo_transaccion": fake.random_element(["compra", "venta", "devolucion"]),
        "precio_unitario": round(fake.random.uniform(10.0, 500.0), 2),
        "fecha_transaccion": fake.date_time_this_year().isoformat(),
        "metodo_pago": fake.random_element(["efectivo", "tarjeta", "transferencia"]),
        "referencia": fake.uuid4()
    }

# ========================
# FIXTURES DE UTILIDAD GENÉRICA
# ========================

@pytest.fixture
def pagination_params():
    """Fixture para parámetros de paginación estándar"""
    return {
        "skip": 0,
        "limit": 10,
        "sort_by": "id",
        "sort_order": "asc"
    }

@pytest.fixture
def search_params():
    """Fixture para parámetros de búsqueda genérica"""
    return {
        "query": fake.word(),
        "filters": {
            "activo": True,
            "categoria": "test"
        }
    }


@pytest.fixture(scope="function")
def client_with_db_rollback(db_session):
    """Cliente que hace rollback automático después de cada test"""

    def override_get_db():
        try:
            # Iniciar transacción
            transaction = db_session.begin()
            yield db_session
        finally:
            # Rollback automático
            transaction.rollback()
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_client(client, sample_user_generic, auth_headers):
    """Cliente pre-autenticado para tests rápidos"""
    # Crear usuario si no existe
    client.post("/api/v1/auth/register", json=sample_user_generic)

    # Cliente con headers de autenticación automáticos
    class AuthenticatedClient:
        def __init__(self, base_client, headers):
            self.client = base_client
            self.headers = headers

        def get(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.get(url, **kwargs)

        def post(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.post(url, **kwargs)

        def put(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.put(url, **kwargs)

        def delete(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.delete(url, **kwargs)

    return AuthenticatedClient(client, auth_headers)

@pytest.fixture
def mock_external_api():
    """Mock para APIs externas durante testing"""
    with patch('app.external.api_client') as mock:
        mock.get_data.return_value = {"status": "success", "data": "mocked"}
        yield mock