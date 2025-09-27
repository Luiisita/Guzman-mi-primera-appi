# Práctica 19: Pytest Setup - FICHA 3147246 🧪

## 🎯 Objetivo

Configurar **pytest** con metodología personalizada para la **FICHA 3147246**, donde cada estudiante implementa tests específicos para su dominio de negocio único.

## 🚨 **IMPORTANTE FICHA 3147246: METODOLOGÍA PERSONALIZADA**

### **📋 ANTES DE EMPEZAR:**

1. **🔍 Consulta tu dominio** en `ASIGNACION-DOMINIOS-FICHA-3147246.md`
2. **📝 Anota tu información:**

   - Dominio: ******\_Spa\_******
   - Entidad Principal: ******\_reserva\_******
   - Prefijo Test: ******\_spa\_******
   - Módulo Test: ******\_test_spa\_******

3. **🚫 PROHIBIDO usar ejemplos genéricos** - Todo debe ser específico a TU dominio

---

## 📋 Pre-requisitos

- ✅ Proyecto FastAPI funcionando (Semana 1-5 completada)
- ✅ API con autenticación implementada
- ✅ **Tu dominio específico identificado** de la tabla de asignaciones
- ✅ Entorno virtual activado

## 🚀 Desarrollo Paso a Paso

### Paso 1: Instalación de Dependencias

#### Instalar librerías de testing

```bash
# En tu directorio del proyecto
pip install pytest httpx pytest-asyncio coverage pytest-mock

# Verificar instalación
pytest --version
coverage --version
```

#### Actualizar requirements.txt

```text
# Dependencias existentes de semanas 1-5
fastapi==0.104.1
uvicorn==0.24.0
# Agregar nuevas dependencias para testing
pytest==7.4.3
httpx==0.25.0
pytest-asyncio==0.21.1
coverage==7.3.2
pytest-mock==3.12.0
```

### Paso 2: Configuración Base de Pytest

#### Crear archivo `pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --strict-config
    --disable-warnings
markers =
    unit: Tests unitarios
    integration: Tests de integración
    slow: Tests que tardan mucho
```

#### Crear directorio de tests

```bash
mkdir tests
touch tests/__init__.py
```

### Paso 3: Configuración Personalizada (conftest.py)

**🚨 PERSONALIZAR TODO SEGÚN TU DOMINIO:**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

# Base de datos de prueba
SQLALCHEMY_DATABASE_URL = \"sqlite:///./test_{TU_PREFIJO}.db\"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={\"check_same_thread\": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope=\"session\")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# FIXTURE ESPECÍFICA PARA TU DOMINIO
@pytest.fixture
def sample_{TU_ENTIDAD}_data():
    \"\"\"
    Datos de ejemplo específicos para {TU_DOMINIO}
    🚨 PERSONALIZAR COMPLETAMENTE SEGÚN TU NEGOCIO
    \"\"\"
    return {
        # Ejemplo para AMAYA BEJARANO (Clínica Dental):
        # \"nombre\": \"María García Rodríguez\",
        # \"edad\": 35,
        # \"telefono\": \"3001234567\",
        # \"historial_medico\": \"Sin alergias conocidas\",
        # \"tipo_sangre\": \"O+\",
        # \"contacto_emergencia\": \"3007654321\"

        # TUS CAMPOS ESPECÍFICOS AQUÍ:
        \"campo1\": \"valor_específico_tu_dominio\",
        \"campo2\": \"valor_específico_tu_dominio\",
        # Agregar más campos según tu entidad
    }

@pytest.fixture
def auth_headers(client):
    \"\"\"Headers de autenticación para tests\"\"\"
    # Crear usuario de prueba específico para tu dominio
    response = client.post(\"/auth/register\", json={
        \"username\": \"admin_{tu_prefijo}\",
        \"password\": \"test123\",
        \"role\": \"admin\"  # Rol específico de tu dominio
    })

    login_response = client.post(\"/auth/login\", data={
        \"username\": \"admin_{tu_prefijo}\",
        \"password\": \"test123\"
    })
    token = login_response.json()[\"access_token\"]
    return {\"Authorization\": f\"Bearer {token}\"}
```

### Paso 4: Primer Test Específico de Tu Dominio

#### Crear archivo test\_{tu_prefijo}.py

```python
# tests/test_{TU_PREFIJO}.py
import pytest
from fastapi.testclient import TestClient

class Test{TuDominio}API:
    \"\"\"
    Tests específicos para {TU_DOMINIO} - FICHA 3147246
    🚨 PERSONALIZAR TODO SEGÚN TU NEGOCIO
    \"\"\"

    def test_create_{tu_entidad}_success(self, client, sample_{tu_entidad}_data, auth_headers):
        \"\"\"Test de creación exitosa de {tu_entidad} en {tu_dominio}\"\"\"
        response = client.post(
            f\"/{tu_prefijo}{tu_entidad}s/\",
            json=sample_{tu_entidad}_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        # Validaciones específicas de tu dominio
        assert data[\"campo1\"] == sample_{tu_entidad}_data[\"campo1\"]
        assert data[\"campo2\"] == sample_{tu_entidad}_data[\"campo2\"]
        # Agregar más validaciones específicas

    def test_get_{tu_entidad}_not_found(self, client, auth_headers):
        \"\"\"Test de {tu_entidad} no encontrado en {tu_dominio}\"\"\"
        response = client.get(f\"/{tu_prefijo}{tu_entidad}s/999\", headers=auth_headers)

        assert response.status_code == 404
        assert \"{tu_entidad} no encontrado\" in response.json()[\"detail\"]

    def test_{tu_entidad}_validation_error(self, client, auth_headers):
        \"\"\"Test de validación específica para {tu_dominio}\"\"\"
        # Datos inválidos específicos de tu dominio
        invalid_data = {
            \"campo1\": \"\",  # Campo requerido vacío
            \"campo2\": \"valor_invalido_para_tu_dominio\"
        }

        response = client.post(
            f\"/{tu_prefijo}{tu_entidad}s/\",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code == 422
        errors = response.json()[\"detail\"]

        # Validar errores específicos de tu dominio
        assert any(\"campo1\" in str(error) for error in errors)
```

### Paso 5: Ejecutar Tests

#### Comandos básicos

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos de tu dominio
pytest tests/test_{tu_prefijo}.py

# Ejecutar con información detallada
pytest -v tests/test_{tu_prefijo}.py

# Ejecutar test específico
pytest tests/test_{tu_prefijo}.py::Test{TuDominio}API::test_create_{tu_entidad}_success
```

#### Verificar configuración

```bash
# Ver información de pytest
pytest --collect-only

# Verificar markers
pytest --markers
```

## ✅ Criterios de Aceptación

### **Configuración (40%)**

- ✅ pytest.ini configurado correctamente
- ✅ conftest.py con fixtures específicas de tu dominio
- ✅ Base de datos de prueba con prefijo único
- ✅ Dependencias instaladas y documentadas

### **Tests Específicos (40%)**

- ✅ Al menos 3 tests específicos de tu dominio
- ✅ Nombres de tests reflejan tu entidad y negocio
- ✅ Datos de prueba realistas para tu industria
- ✅ Validaciones únicas de tu contexto

### **Funcionamiento (20%)**

- ✅ Tests ejecutan sin errores
- ✅ Fixtures funcionan correctamente
- ✅ Autenticación integrada en tests

## 🎯 Entregables

1. **Configuración personalizada:**

   - `pytest.ini`
   - `tests/conftest.py` con fixtures específicas
   - `requirements.txt` actualizado

2. **Tests específicos:**

   - `tests/test_{tu_prefijo}.py` con al menos 3 tests
   - Documentación de casos de prueba

3. **Verificación:**
   - Capturas de pantalla de tests ejecutándose
   - Log de pytest mostrando tests específicos

## 🚨 **VERIFICACIÓN FINAL FICHA 3147246**

### **Antes de entregar, verificar:**

- ✅ Todos los nombres usan TU prefijo específico
- ✅ Los datos de prueba son realistas para TU dominio
- ✅ No hay ejemplos genéricos (\"Juan Pérez\", \"user123\")
- ✅ Tests reflejan la lógica específica de TU negocio

### **Comando de verificación:**

```bash
pytest tests/test_{tu_prefijo}.py -v
```

**¡Tu configuración de testing debe ser única e irrepetible!** 🎯
