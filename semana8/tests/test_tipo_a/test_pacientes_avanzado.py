import pytest
from fastapi import status
import json
from datetime import datetime, timedelta

# Ruta de la API para Pacientes (Tipo A)
API_PATH = "/api/v1/pacientes"

@pytest.mark.tipo_a
@pytest.mark.integration
class TestPacientesEndpoints:
    """Tests completos de endpoints para la gestión de Pacientes de la Clínica Dental."""

    def test_crud_completo_paciente(self, authenticated_client, sample_paciente):
        """Test CRUD completo (Create, Read, Update, Delete) para la entidad Paciente."""

        # --- CREATE - Crear Paciente ---
        create_response = authenticated_client.post(
            API_PATH,
            json=sample_paciente
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        created_data = create_response.json()
        paciente_id = created_data["id"]

        # Validar datos de creación
        assert created_data["nombre_completo"] == sample_paciente["nombre_completo"]
        assert created_data["email"] == sample_paciente["email"]
        assert "fecha_registro" in created_data
        assert "fecha_actualizacion" in created_data

        # --- READ - Obtener Paciente individual ---
        read_response = authenticated_client.get(f"{API_PATH}/{paciente_id}")
        assert read_response.status_code == status.HTTP_200_OK

        read_data = read_response.json()
        assert read_data["id"] == paciente_id
        assert read_data["nombre_completo"] == sample_paciente["nombre_completo"]
        
        # --- UPDATE - Actualizar información del Paciente ---
        update_data = {
            "nombre_completo": "Ana Torres - Actualizado",
            "telefono": "555-9876",
            "estado_ficha": "Activo",
            "alergias": ["Penicilina"]
        }

        update_response = authenticated_client.put(
            f"{API_PATH}/{paciente_id}",
            json=update_data
        )
        assert update_response.status_code == status.HTTP_200_OK

        updated_data = update_response.json()
        assert updated_data["nombre_completo"] == update_data["nombre_completo"]
        assert updated_data["alergias"] == update_data["alergias"]
        assert updated_data["fecha_actualizacion"] != created_data["fecha_actualizacion"] # Debe cambiar

        # --- DELETE - Eliminar Paciente (Soft Delete) ---
        delete_response = authenticated_client.delete(f"{API_PATH}/{paciente_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar eliminación suave (soft delete): el recurso ya no está activo
        verify_response = authenticated_client.get(f"{API_PATH}/{paciente_id}")
        # Asumiendo que un GET a un recurso con soft-delete retorna 404 o marca como inactivo
        # Para este test, verificamos que no está disponible en la vista activa (404/400) o que tiene fecha_baja
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    def test_busqueda_avanzada_pacientes(self, authenticated_client, faker):
        """Test búsqueda avanzada de Pacientes por nombre, email o estado de ficha."""

        # Crear pacientes de prueba (usando el faker para datos realistas)
        pacientes_data = [
            {"nombre_completo": "Elena Martín", "email": "elena.m@test.com", "telefono": faker.phone_number(), "estado_ficha": "Tratamiento"},
            {"nombre_completo": "Carlos Perez", "email": "carlos.p@test.com", "telefono": faker.phone_number(), "estado_ficha": "Activo"},
            {"nombre_completo": "Martín Velez", "email": "martin.v@test.com", "telefono": faker.phone_number(), "estado_ficha": "Activo"},
        ]
        
        for p_data in pacientes_data:
            authenticated_client.post(API_PATH, json=p_data)

        # Búsqueda por estado de ficha: 'Activo'
        search_response = authenticated_client.get(
            f"{API_PATH}/buscar",
            params={
                "estado_ficha": "Activo",
                "limit": 10
            }
        )

        assert search_response.status_code == status.HTTP_200_OK
        search_data = search_response.json()

        assert "items" in search_data
        assert len(search_data["items"]) == 2 # Esperamos a Carlos y Martín
        
        # Verificar que todos los resultados coinciden con el filtro
        for item in search_data["items"]:
            assert item["estado_ficha"] == "Activo"

    def test_paginacion_pacientes(self, authenticated_client, faker):
        """Test paginación completa del listado de pacientes."""

        # Crear 22 pacientes para testing de paginación
        for i in range(22):
            paciente_data = {
                "nombre_completo": faker.name(),
                "email": f"p{i}_{faker.email()}",
                "telefono": faker.phone_number(),
                "estado_ficha": "Activo" if i < 15 else "Inactivo"
            }
            authenticated_client.post(API_PATH, json=paciente_data)

        # Test página 1: skip 0, limit 10
        page1_response = authenticated_client.get(
            API_PATH,
            params={"skip": 0, "limit": 10}
        )
        assert page1_response.status_code == status.HTTP_200_OK
        page1_data = page1_response.json()

        assert len(page1_data["items"]) == 10
        assert page1_data["total"] >= 22
        
        # Test página 3: skip 20, limit 10
        page3_response = authenticated_client.get(
            API_PATH,
            params={"skip": 20, "limit": 10}
        )
        assert page3_response.status_code == status.HTTP_200_OK
        page3_data = page3_response.json()

        # Esperamos solo 2 elementos (22 total - 20 saltados = 2 restantes)
        assert len(page3_data["items"]) == 2


    def test_validacion_negocio_email_duplicado(self, authenticated_client, faker):
        """Test validación de negocio: no se permiten emails duplicados en Pacientes."""
        
        email_unico = "paciente.unico@smile.com"
        paciente_data1 = {
            "nombre_completo": "Paciente Uno",
            "email": email_unico,
            "telefono": faker.phone_number()
        }

        paciente_data2 = {
            "nombre_completo": "Paciente Dos",
            "email": email_unico,  # Mismo email
            "telefono": faker.phone_number()
        }

        # 1. Primera creación debe ser exitosa
        response1 = authenticated_client.post(API_PATH, json=paciente_data1)
        assert response1.status_code == status.HTTP_201_CREATED

        # 2. Segunda creación debe fallar por email duplicado
        response2 = authenticated_client.post(API_PATH, json=paciente_data2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "duplicado" in response2.json()["detail"].lower()
        assert "email" in response2.json()["detail"].lower()


@pytest.mark.tipo_a
@pytest.mark.unit
class TestValidacionesCamposPaciente:
    """Tests de validaciones de entrada (Pydantic) para el Paciente."""

    def test_validacion_campos_requeridos(self, authenticated_client):
        """Test validación de campos requeridos (ej. nombre_completo, email)."""

        # Faltan campos esenciales como nombre y email
        invalid_data = {
            "telefono": "999-999-999",
            "estado_ficha": "Pendiente"
        }

        response = authenticated_client.post(API_PATH, json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        errors = response.json()["detail"]
        assert any("nombre_completo" in str(error) for error in errors)
        assert any("email" in str(error) for error in errors)

    def test_validacion_tipos_datos(self, authenticated_client):
        """Test validación de tipos de datos incorrectos (ej. edad no numérica)."""

        invalid_data = {
            "nombre_completo": "Test Paciente",
            "email": "test@test.com",
            "edad": "veinte",  # La edad debe ser un entero
            "alergias": "no_es_una_lista" # Las alergias deben ser una lista (JSON array)
        }

        response = authenticated_client.post(API_PATH, json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_validacion_formato_email_invalido(self, authenticated_client):
        """Test validación de formato de email."""

        invalid_data = {
            "nombre_completo": "Test Paciente",
            "email": "email_sin_arroba_com",
            "telefono": "123-4567"
        }

        response = authenticated_client.post(API_PATH, json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
