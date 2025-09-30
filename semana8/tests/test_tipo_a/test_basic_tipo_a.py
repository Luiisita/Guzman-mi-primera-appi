import pytest
from fastapi import status
from datetime import datetime, timedelta

# Nota: Se asume que las rutas de tu API para Tipo A son /pacientes y /citas
API_PATH_PACIENTES = "/api/v1/pacientes"
API_PATH_CITAS = "/api/v1/citas"

@pytest.mark.tipo_a
@pytest.mark.integration
class TestGestionPacientesCRUD:
    """Tests básicos para el CRUD de Pacientes (Gestión de Datos Tipo A)"""

    def test_crear_paciente_valido(self, client, sample_paciente, auth_headers):
        """Test: Crear un nuevo Paciente con datos válidos"""
        response = client.post(
            API_PATH_PACIENTES,
            json=sample_paciente,
            headers=auth_headers
        )

        # Se espera un status 201 (Created)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == sample_paciente["nombre"]
        assert "id" in data
        assert data["activo"] is True
        assert "fecha_registro" in data

    def test_obtener_paciente_existente(self, client, auth_headers):
        """Test: Obtener un Paciente por ID que existe previamente"""
        # 1. Crear un Paciente de prueba
        create_data = {
            "nombre": "Ismael", "apellido": "Guzmán", "cedula": "V-11223344",
            "telefono": "555-0001", "email": "ismael.guzman@test.com",
            "fecha_nacimiento": "1990-01-01T00:00:00", "activo": True
        }

        create_response = client.post(
            API_PATH_PACIENTES,
            json=create_data,
            headers=auth_headers
        )
        paciente_id = create_response.json()["id"]

        # 2. Luego obtenerlo por ID
        response = client.get(f"{API_PATH_PACIENTES}/{paciente_id}", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == paciente_id
        assert data["nombre"] == create_data["nombre"]

    def test_actualizar_datos_paciente(self, client, auth_headers):
        """Test: Actualizar el correo y teléfono de un Paciente existente"""
        # 1. Crear un Paciente
        create_data = {
            "nombre": "Laura", "apellido": "Álvarez", "cedula": "V-22334455",
            "telefono": "555-1111", "email": "laura@original.com",
            "fecha_nacimiento": "1995-05-05T00:00:00", "activo": True
        }

        create_response = client.post(
            API_PATH_PACIENTES,
            json=create_data,
            headers=auth_headers
        )
        paciente_id = create_response.json()["id"]

        # 2. Datos de actualización
        update_data = {
            "telefono": "555-9999",
            "email": "laura.alvarez@nuevo.com",
            # Nota: Solo enviamos campos a modificar
        }

        response = client.put(
            f"{API_PATH_PACIENTES}/{paciente_id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == update_data["email"]
        assert data["telefono"] == update_data["telefono"]
        # Verificar que el nombre no cambió
        assert data["nombre"] == create_data["nombre"]

    def test_eliminar_paciente_existente(self, client, auth_headers):
        """Test: Eliminar un registro de Paciente (asumiendo eliminación lógica o física)"""
        # 1. Crear Paciente a eliminar
        create_data = {
            "nombre": "Jorge", "apellido": "Reyes", "cedula": "V-33445566",
            "telefono": "555-3333", "email": "jorge@delete.com",
            "fecha_nacimiento": "1985-06-06T00:00:00", "activo": True
        }

        create_response = client.post(
            API_PATH_PACIENTES,
            json=create_data,
            headers=auth_headers
        )
        paciente_id = create_response.json()["id"]

        # 2. Eliminar Paciente
        response = client.delete(f"{API_PATH_PACIENTES}/{paciente_id}", headers=auth_headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 3. Verificar que no existe (o ha cambiado de estado a inactivo)
        get_response = client.get(f"{API_PATH_PACIENTES}/{paciente_id}", headers=auth_headers)
        # Asumiendo que la eliminación es física o retorna 404 si no está activo
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.tipo_a
@pytest.mark.integration
class TestGestionCitas:
    """Tests enfocados en la Cita Médica, un objeto de datos relacional clave en Tipo A"""

    def test_crear_cita_valida(self, client, sample_paciente, sample_cita_tipo_a, auth_headers):
        """Test: Crear una Cita. Requiere que exista un paciente previamente."""
        # 1. Crear un paciente (requisito de foreign key)
        paciente_response = client.post(
            API_PATH_PACIENTES,
            json=sample_paciente,
            headers=auth_headers
        )
        paciente_id = paciente_response.json()["id"]

        # 2. Actualizar el ID de la cita para usar el paciente creado
        cita_data = sample_cita_tipo_a.copy()
        cita_data["paciente_id"] = paciente_id

        # 3. Crear la Cita
        response = client.post(
            API_PATH_CITAS,
            json=cita_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["paciente_id"] == paciente_id
        assert data["estado"] == cita_data["estado"]
        assert "id" in data

    def test_crear_cita_con_id_paciente_inexistente(self, client, sample_cita_tipo_a, auth_headers):
        """Test: Intentar crear una cita para un paciente que no existe (Validación FK)"""
        cita_data = sample_cita_tipo_a.copy()
        cita_data["paciente_id"] = 999999  # ID que no existe

        response = client.post(
            API_PATH_CITAS,
            json=cita_data,
            headers=auth_headers
        )

        # Se espera un 404 (Not Found) o 422 (Unprocessable Entity) o 400 (Bad Request)
        # Esto depende de cómo implementaste la validación de Foreign Key en tu API.
        assert response.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST)
        assert "paciente" in response.json()["detail"].lower()


@pytest.mark.tipo_a
@pytest.mark.unit
class TestValidacionesGenericas:
    """Tests de validaciones generales para la gestión de datos"""

    def test_obtener_recurso_inexistente(self, client, auth_headers):
        """Test: Intentar obtener un paciente con ID inexistente (ejemplo de 404)"""
        response = client.get(f"{API_PATH_PACIENTES}/99999", headers=auth_headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrado" in response.json()["detail"].lower()

    def test_crear_paciente_sin_datos_obligatorios(self, client, auth_headers):
        """Test: Crear Paciente con campos obligatorios faltantes (e.g., nombre, cédula)"""
        invalid_data = {
            "nombre": "",  # Nombre vacío
            "cedula": "123", # Cédula muy corta
            "email": "correo-invalido" # Email mal formateado
        }

        response = client.post(
            API_PATH_PACIENTES,
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        # Verificar que se captura el error de nombre vacío y/o email inválido
        assert any("nombre" in str(error) for error in errors)
        assert any("email" in str(error) for error in errors)
