# Práctica 21: Testing de Autenticación - FICHA 3147246 🔐

## 🎯 Objetivo

Implementar tests de autenticación y autorización específicos para los roles de tu dominio de negocio asignado.

## 🚨 **IMPORTANTE: ROLES ESPECÍFICOS DE TU DOMINIO**

Cada dominio tiene roles únicos según su industria. No uses roles genéricos.

---

## 📋 Pre-requisitos

- ✅ Prácticas 19 y 20 completadas
- ✅ Sistema de autenticación con roles implementado
- ✅ Tu dominio específico identificado

## 🚀 Desarrollo

### Paso 1: Tests de Autenticación Básica

```python
# tests/test_{tu_prefijo}_auth.py

def test_register_{tu_dominio}_user(self, client):
    \"\"\"Test de registro específico para {tu_dominio}\"\"\"
    data = {
        \"username\": \"usuario_{tu_prefijo}_test\",
        \"password\": \"password123\",
        \"role\": \"rol_específico_tu_dominio\"  # Personalizar según tu industria
    }

    response = client.post(\"/auth/register\", json=data)
    assert response.status_code == 201

def test_login_{tu_dominio}_user(self, client):
    \"\"\"Test de login específico para {tu_dominio}\"\"\"
    # Registrar usuario primero
    register_data = {
        \"username\": \"admin_{tu_prefijo}\",
        \"password\": \"admin123\",
        \"role\": \"admin_{tu_dominio}\"
    }
    client.post(\"/auth/register\", json=register_data)

    # Login
    login_data = {
        \"username\": \"admin_{tu_prefijo}\",
        \"password\": \"admin123\"
    }
    response = client.post(\"/auth/login\", data=login_data)

    assert response.status_code == 200
    assert \"access_token\" in response.json()
```

### Paso 2: Tests de Roles Específicos por Dominio

#### Ejemplos por dominio:

**🦷 Si eres AMAYA BEJARANO (Clínica Dental):**

```python
def test_dentist_permissions(self, client):
    \"\"\"Test de permisos específicos para dentista\"\"\"
    # Roles: dentista, asistente_dental, recepcionista, administrador

def test_patient_access_restrictions(self, client):
    \"\"\"Test de restricciones de acceso para pacientes\"\"\"
    # Solo pueden ver sus propios datos
```

**💄 Si eres BAYONA RODRIGUEZ (Centro Estético):**

```python
def test_beautician_permissions(self, client):
    \"\"\"Test de permisos para esteticista\"\"\"
    # Roles: esteticista, terapeuta, recepcionista, gerente

def test_client_booking_permissions(self, client):
    \"\"\"Test de permisos de reserva para clientes\"\"\"
```

### Paso 3: Tests de Autorización por Endpoints

```python
def test_create_{tu_entidad}_requires_auth(self, client):
    \"\"\"Test que crear {tu_entidad} requiere autenticación\"\"\"
    data = {
        # Datos específicos de tu dominio
    }

    response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=data)
    assert response.status_code == 401

def test_admin_can_delete_{tu_entidad}(self, client):
    \"\"\"Test que solo admin puede eliminar en {tu_dominio}\"\"\"
    # Crear token de admin específico para tu dominio
    admin_headers = self.get_admin_headers(client)

    # Crear entidad para eliminar
    # ... lógica específica de tu dominio

def test_regular_user_cannot_delete_{tu_entidad}(self, client):
    \"\"\"Test que usuario regular no puede eliminar en {tu_dominio}\"\"\"
    # Lógica específica de restricciones en tu dominio
```

## ✅ Criterios de Aceptación

- ✅ Tests de registro/login específicos para tu dominio
- ✅ Tests de roles únicos de tu industria
- ✅ Tests de autorización por endpoints
- ✅ Validaciones de permisos específicas

## 🎯 Entregables

1. **Tests de autenticación** en `tests/test_{tu_prefijo}_auth.py`
2. **Documentación de roles** específicos de tu dominio
3. **Tests de autorización** funcionando correctamente
