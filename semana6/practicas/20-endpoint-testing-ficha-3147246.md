# Práctica 20: Testing de Endpoints - FICHA 3147246 🚀

## 🎯 Objetivo

Implementar tests CRUD específicos para tu entidad principal del dominio asignado en la **FICHA 3147246**.

## 🚨 **IMPORTANTE: USAR SOLO TU DOMINIO ASIGNADO**

### **📋 Recordatorio:**

- 🔍 Consulta tu dominio en `ASIGNACION-DOMINIOS-FICHA-3147246.md`
- 📝 Usa SOLO tu prefijo y entidad específica
- 🚫 Prohibido copiar ejemplos de otros estudiantes

---

## 📋 Pre-requisitos

- ✅ Práctica 19 completada (pytest configurado)
- ✅ Tu dominio específico identificado
- ✅ API con endpoints CRUD funcionando

## 🚀 Desarrollo

### Paso 1: Tests de Creación (POST)

```python
# tests/test_{tu_prefijo}.py - Agregar al archivo existente

def test_create_{tu_entidad}_complete(self, client, auth_headers):
    \"\"\"Test completo de creación para {tu_dominio}\"\"\"
    data = {
        # PERSONALIZAR según tu dominio específico
        # Ejemplo para Clínica Dental (AMAYA BEJARANO):
        # \"nombre\": \"Ana Martínez López\",
        # \"edad\": 28,
        # \"telefono\": \"3001234567\",
        # \"historial_medico\": \"Alergia a penicilina\"

        # TUS CAMPOS ESPECÍFICOS:
        \"campo_principal\": \"valor_específico_tu_dominio\",
        \"campo_secundario\": \"valor_específico_tu_dominio\"
    }

    response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=data, headers=auth_headers)

    assert response.status_code == 201
    created = response.json()

    # Validaciones específicas de tu dominio
    assert created[\"campo_principal\"] == data[\"campo_principal\"]
    assert \"id\" in created

def test_create_{tu_entidad}_duplicate(self, client, auth_headers):
    \"\"\"Test de creación duplicada específico para {tu_dominio}\"\"\"
    data = {
        # Datos que causarían conflicto en tu dominio específico
    }

    # Crear primera vez
    client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=data, headers=auth_headers)

    # Intentar crear duplicado
    response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=data, headers=auth_headers)

    assert response.status_code == 400
    assert \"ya existe\" in response.json()[\"detail\"].lower()
```

### Paso 2: Tests de Consulta (GET)

```python
def test_get_{tu_entidad}_by_id(self, client, auth_headers):
    \"\"\"Test de consulta por ID específico para {tu_dominio}\"\"\"
    # Crear entidad primero
    create_data = {
        # Datos específicos de tu dominio
    }
    create_response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=create_data, headers=auth_headers)
    created_id = create_response.json()[\"id\"]

    # Consultar por ID
    response = client.get(f\"/{tu_prefijo}{tu_entidad}s/{created_id}\", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data[\"id\"] == created_id

def test_get_all_{tu_entidad}s(self, client, auth_headers):
    \"\"\"Test de consulta de todas las entidades en {tu_dominio}\"\"\"
    response = client.get(f\"/{tu_prefijo}{tu_entidad}s/\", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_{tu_entidad}_not_found(self, client, auth_headers):
    \"\"\"Test de entidad no encontrada en {tu_dominio}\"\"\"
    response = client.get(f\"/{tu_prefijo}{tu_entidad}s/99999\", headers=auth_headers)

    assert response.status_code == 404
    assert f\"{tu_entidad} no encontrado\" in response.json()[\"detail\"].lower()
```

### Paso 3: Tests de Actualización (PUT)

```python
def test_update_{tu_entidad}_complete(self, client, auth_headers):
    \"\"\"Test de actualización completa para {tu_dominio}\"\"\"
    # Crear entidad
    create_data = {
        # Datos iniciales específicos de tu dominio
    }
    create_response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=create_data, headers=auth_headers)
    entity_id = create_response.json()[\"id\"]

    # Datos de actualización específicos de tu dominio
    update_data = {
        # Campos modificados específicos de tu negocio
    }

    response = client.put(f\"/{tu_prefijo}{tu_entidad}s/{entity_id}\", json=update_data, headers=auth_headers)

    assert response.status_code == 200
    updated = response.json()

    # Validar cambios específicos de tu dominio

def test_update_{tu_entidad}_partial(self, client, auth_headers):
    \"\"\"Test de actualización parcial específica para {tu_dominio}\"\"\"
    # Implementar actualización parcial con PATCH si tu API lo soporta
```

### Paso 4: Tests de Eliminación (DELETE)

```python
def test_delete_{tu_entidad}_success(self, client, auth_headers):
    \"\"\"Test de eliminación exitosa en {tu_dominio}\"\"\"
    # Crear entidad
    create_data = {
        # Datos específicos de tu dominio
    }
    create_response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=create_data, headers=auth_headers)
    entity_id = create_response.json()[\"id\"]

    # Eliminar
    response = client.delete(f\"/{tu_prefijo}{tu_entidad}s/{entity_id}\", headers=auth_headers)

    assert response.status_code == 200

    # Verificar que ya no existe
    get_response = client.get(f\"/{tu_prefijo}{tu_entidad}s/{entity_id}\", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_{tu_entidad}_not_found(self, client, auth_headers):
    \"\"\"Test de eliminación de entidad inexistente en {tu_dominio}\"\"\"
    response = client.delete(f\"/{tu_prefijo}{tu_entidad}s/99999\", headers=auth_headers)

    assert response.status_code == 404
```

### Paso 5: Tests de Validaciones Específicas

```python
def test_{tu_entidad}_business_rules(self, client, auth_headers):
    \"\"\"Test de reglas de negocio específicas para {tu_dominio}\"\"\"
    # Ejemplos específicos por dominio:

    # Si eres AMAYA BEJARANO (Clínica Dental):
    # - Validar que la edad sea mayor a 0
    # - Validar formato de teléfono
    # - Validar que el historial médico no esté vacío

    # Si eres BAYONA RODRIGUEZ (Centro Estético):
    # - Validar que la duración del tratamiento sea razonable
    # - Validar que el precio sea mayor a 0
    # - Validar que los productos sean compatibles

    # TUS VALIDACIONES ESPECÍFICAS:
    invalid_data = {
        # Datos que violan reglas de tu dominio específico
    }

    response = client.post(f\"/{tu_prefijo}{tu_entidad}s/\", json=invalid_data, headers=auth_headers)

    assert response.status_code == 422
    # Validar mensaje de error específico
```

## ✅ Criterios de Aceptación

### **Tests CRUD Completos (50%)**

- ✅ Tests de CREATE con datos específicos de tu dominio
- ✅ Tests de READ (individual y lista)
- ✅ Tests de UPDATE (completo y parcial)
- ✅ Tests de DELETE con verificación

### **Validaciones Específicas (30%)**

- ✅ Tests de reglas de negocio únicas de tu dominio
- ✅ Tests de validaciones específicas de tu industria
- ✅ Manejo de errores contextualizado

### **Calidad de Tests (20%)**

- ✅ Nombres de tests reflejan tu dominio específico
- ✅ Datos de prueba realistas para tu industria
- ✅ Assertions específicas y relevantes

## 🎯 Entregables

1. **Tests CRUD completos** en `tests/test_{tu_prefijo}.py`
2. **Documentación** de casos de prueba específicos
3. **Ejecución exitosa** de todos los tests

## 🚨 **Verificación Final**

```bash
# Ejecutar todos tus tests
pytest tests/test_{tu_prefijo}.py -v

# Verificar cobertura
pytest --cov=. tests/test_{tu_prefijo}.py
```

**¡Tus tests deben ser únicos para tu dominio de negocio!** 🎯
