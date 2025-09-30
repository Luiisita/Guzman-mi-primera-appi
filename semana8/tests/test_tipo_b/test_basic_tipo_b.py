import pytest
from datetime import datetime, timedelta
from fastapi import status

# Rutas adaptadas para la Clínica Dental
API_PATH_RECURSOS = "/api/v1/recursos/odontologos" # Recurso: Odontólogo o Sala
API_PATH_RESERVAS = "/api/v1/citas"              # Reserva: Cita del Paciente

@pytest.mark.tipo_b
@pytest.mark.integration
class TestRecursosCitasOdontologos:
    """Tests para la gestión de recursos programables (Odontólogos/Salas) y Citas."""

    def test_crear_recurso_odontologo_valido(self, client, auth_headers):
        """Test: Crear un recurso programable (ej. un Odontólogo con horario)"""
        recurso_data = {
            "nombre": "Dr. Guzmán - Sala 1",
            "descripcion": "Odontólogo General asignado a Sala 1",
            "capacidad": 1,
            "disponible": True,
            "hora_inicio": "08:00",
            "hora_fin": "18:00",
            "dias_disponibles": ["lunes", "martes", "miércoles", "jueves", "viernes"],
            "duracion_minima": 30, # Citas mínimas de 30 minutos
            "tipo_recurso": "odontologo"
        }
        
        response = client.post(
            API_PATH_RECURSOS,
            json=recurso_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == recurso_data["nombre"]
        assert data["hora_inicio"] == "08:00"

    def test_consultar_disponibilidad_odontologo(self, client, auth_headers):
        """Test: Consultar la disponibilidad de un Odontólogo para una fecha futura."""
        # 1. Crear recurso (Odontólogo/Sala)
        recurso_data = {
            "nombre": "Dra. Álvarez - Sala 2",
            "capacidad": 1,
            "disponible": True,
            "hora_inicio": "09:00",
            "hora_fin": "17:00"
        }

        create_response = client.post(
            API_PATH_RECURSOS,
            json=recurso_data,
            headers=auth_headers
        )
        recurso_id = create_response.json()["id"]

        # 2. Consultar disponibilidad para mañana
        fecha_consulta = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d") # Solo la fecha
        
        response = client.get(
            f"{API_PATH_RECURSOS}/{recurso_id}/disponibilidad",
            params={"fecha": fecha_consulta},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "disponible" in data
        assert isinstance(data["horarios_libres"], list)
        assert len(data["horarios_libres"]) > 0 # Debería haber horarios libres inicialmente

    def test_crear_cita_valida(self, client, auth_headers):
        """Test: Crear una Cita válida (Reserva) para un Odontólogo."""
        # 1. Crear recurso (Odontólogo)
        recurso_data = {
            "nombre": "Odontólogo Test",
            "capacidad": 1,
            "disponible": True
        }

        recurso_response = client.post(
            API_PATH_RECURSOS,
            json=recurso_data,
            headers=auth_headers
        )
        recurso_id = recurso_response.json()["id"]

        # 2. Crear Cita (Reserva)
        start_time = (datetime.now() + timedelta(days=2)).replace(hour=11, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(minutes=45)

        reserva_data = {
            "recurso_id": recurso_id,
            "paciente_id": 1, # Asume un paciente con ID 1 ya existe o se crea
            "tratamiento": "Blanqueamiento",
            "fecha_inicio": start_time.isoformat(),
            "fecha_fin": end_time.isoformat(),
            "estado": "programada",
            "descripcion": "Cita para blanqueamiento láser"
        }

        response = client.post(
            API_PATH_RESERVAS,
            json=reserva_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["recurso_id"] == recurso_id
        assert data["estado"] == "programada"
        assert data["tratamiento"] == "Blanqueamiento"

@pytest.mark.tipo_b
@pytest.mark.integration
class TestConflictosCitas:
    """Tests de conflictos de programación y superposición de Citas."""

    def test_reserva_conflicto_horario(self, client, auth_headers):
        """Test: Detectar conflicto de horarios al agendar dos citas para el mismo Odontólogo."""
        # 1. Crear recurso (Odontólogo con capacidad 1)
        recurso_data = {
            "nombre": "Odontólogo Conflicto",
            "capacidad": 1,
            "disponible": True
        }

        recurso_response = client.post(
            API_PATH_RECURSOS,
            json=recurso_data,
            headers=auth_headers
        )
        recurso_id = recurso_response.json()["id"]

        # Definir el horario de conflicto
        fecha_base = (datetime.now() + timedelta(days=3)).replace(hour=14, minute=0, second=0, microsecond=0)

        # 2. Primera Cita (14:00 a 15:00)
        reserva1 = {
            "recurso_id": recurso_id,
            "paciente_id": 2, 
            "fecha_inicio": fecha_base.isoformat(),
            "fecha_fin": (fecha_base + timedelta(hours=1)).isoformat(),
            "descripcion": "Limpieza (Primera reserva)"
        }

        response1 = client.post(API_PATH_RESERVAS, json=reserva1, headers=auth_headers)
        assert response1.status_code == status.HTTP_201_CREATED

        # 3. Segunda Cita con conflicto (14:30 a 15:30)
        reserva2 = {
            "recurso_id": recurso_id,
            "paciente_id": 3, 
            "fecha_inicio": (fecha_base + timedelta(minutes=30)).isoformat(), # Empieza 30 min después
            "fecha_fin": (fecha_base + timedelta(hours=1, minutes=30)).isoformat(),
            "descripcion": "Endodoncia (Conflicto)"
        }

        response2 = client.post(API_PATH_RESERVAS, json=reserva2, headers=auth_headers)
        
        # Se espera un status 409 (Conflict)
        assert response2.status_code == status.HTTP_409_CONFLICT
        assert "conflicto" in response2.json()["detail"].lower()
        assert "horario" in response2.json()["detail"].lower()
