import pytest
from fastapi import status
from datetime import datetime, timedelta
import json

# Rutas de la API adaptadas al dominio de la clínica
API_PATH_DOCTORES = "/api/v1/doctores"
API_PATH_CITAS = "/api/v1/citas"

@pytest.mark.tipo_b
@pytest.mark.integration
class TestCitasYHorarios:
    """Tests completos para la programación temporal de Citas y Doctores."""

    def test_crud_completo_doctor_y_horario(self, authenticated_client, sample_doctor):
        """Test CRUD completo para la entidad Doctor (Recurso Programable)."""

        # --- CREATE - Crear Doctor (Recurso) ---
        create_response = authenticated_client.post(
            API_PATH_DOCTORES,
            json=sample_doctor
        )
        assert create_response.status_code == status.HTTP_201_CREATED

        created_data = create_response.json()
        doctor_id = created_data["id"]

        # Validar datos de creación
        assert created_data["nombre"] == sample_doctor["nombre"]
        assert created_data["especialidad"] == sample_doctor["especialidad"]
        assert "horario_laboral" in created_data

        # --- READ ---
        read_response = authenticated_client.get(f"{API_PATH_DOCTORES}/{doctor_id}")
        assert read_response.status_code == status.HTTP_200_OK

        # --- UPDATE - Cambiar Horario de la Tarde ---
        update_data = {
            "especialidad": "Ortodoncia Avanzada",
            "hora_inicio_laboral": "07:00",
            "hora_fin_laboral": "19:00" # Horario extendido
        }

        update_response = authenticated_client.put(
            f"{API_PATH_DOCTORES}/{doctor_id}",
            json=update_data
        )
        assert update_response.status_code == status.HTTP_200_OK

        updated_data = update_response.json()
        assert updated_data["especialidad"] == "Ortodoncia Avanzada"
        assert updated_data["hora_inicio_laboral"] == "07:00"

        # --- DELETE ---
        delete_response = authenticated_client.delete(f"{API_PATH_DOCTORES}/{doctor_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    def test_consultar_disponibilidad_doctor(self, authenticated_client, sample_doctor, sample_paciente):
        """Test consulta de disponibilidad del doctor y cómo las citas la bloquean."""

        # 1. Crear Doctor con horario 9:00 a 17:00
        doctor_data = sample_doctor.copy()
        doctor_data["hora_inicio_laboral"] = "09:00"
        doctor_data["hora_fin_laboral"] = "17:00"

        create_response = authenticated_client.post(API_PATH_DOCTORES, json=doctor_data)
        doctor_id = create_response.json()["id"]
        
        # 2. Crear un Paciente para la cita
        paciente_id = authenticated_client.post("/api/v1/pacientes", json=sample_paciente).json()["id"]

        # 3. Crear una Cita que ocupe de 10:00 a 12:00
        fecha_consulta = (datetime.now() + timedelta(days=7)).date().isoformat()
        
        fecha_inicio_cita = datetime.fromisoformat(f"{fecha_consulta}T10:00:00")
        fecha_fin_cita = datetime.fromisoformat(f"{fecha_consulta}T12:00:00")
        
        cita_data = {
            "doctor_id": doctor_id,
            "paciente_id": paciente_id,
            "fecha_inicio": fecha_inicio_cita.isoformat(),
            "fecha_fin": fecha_fin_cita.isoformat(),
            "motivo": "Limpieza y Diagnóstico",
        }
        authenticated_client.post(API_PATH_CITAS, json=cita_data)

        # 4. Consultar disponibilidad del Doctor para ese día, esperando brechas
        # Se debe esperar disponibilidad antes de las 10:00 y después de las 12:00.
        disponibilidad_response = authenticated_client.get(
            f"{API_PATH_DOCTORES}/{doctor_id}/disponibilidad",
            params={
                "fecha": fecha_consulta,
                "duracion_minutos": 60 # Citas de 1 hora
            }
        )

        assert disponibilidad_response.status_code == status.HTTP_200_OK
        disponibilidad_data = disponibilidad_response.json()

        assert "horarios_libres" in disponibilidad_data
        horarios = disponibilidad_data["horarios_libres"]
        
        # Debe haber horarios libres antes de las 10:00 (ej. 09:00-10:00)
        assert any(h["hora_inicio"] < "10:00" for h in horarios)
        
        # Debe haber horarios libres después de las 12:00 (ej. 12:00-13:00)
        assert any(h["hora_inicio"] >= "12:00" for h in horarios)
        
        # NO debe haber horarios entre 10:00 y 11:00
        assert not any("10:00" <= h["hora_inicio"] < "12:00" for h in horarios)


    def test_citas_con_conflictos(self, authenticated_client, sample_doctor, sample_paciente):
        """Test gestión completa de Citas con detección de solapamiento (conflictos)."""

        # 1. Crear Doctor y Paciente
        doctor_id = authenticated_client.post(API_PATH_DOCTORES, json=sample_doctor).json()["id"]
        paciente_id = authenticated_client.post("/api/v1/pacientes", json=sample_paciente).json()["id"]

        # 2. Crear primera Cita (10:00 - 11:00)
        fecha_base = datetime.now() + timedelta(days=3)
        fecha_inicio1 = fecha_base.replace(hour=10, minute=0, second=0, microsecond=0)
        fecha_fin1 = fecha_inicio1 + timedelta(hours=1)

        cita1_data = {
            "doctor_id": doctor_id,
            "paciente_id": paciente_id,
            "fecha_inicio": fecha_inicio1.isoformat(),
            "fecha_fin": fecha_fin1.isoformat(),
            "motivo": "Cita Base",
        }

        cita1_response = authenticated_client.post(API_PATH_CITAS, json=cita1_data)
        assert cita1_response.status_code == status.HTTP_201_CREATED

        # 3. Intentar segunda Cita con conflicto total (también 10:00 - 11:00)
        cita2_data = cita1_data.copy()
        cita2_data["motivo"] = "Cita con conflicto total"

        cita2_response = authenticated_client.post(API_PATH_CITAS, json=cita2_data)
        assert cita2_response.status_code == status.HTTP_409_CONFLICT
        assert "conflicto de horario" in reserva2_response.json()["detail"].lower()

        # 4. Intentar tercera Cita con conflicto parcial (10:30 - 11:30)
        fecha_inicio3 = fecha_inicio1 + timedelta(minutes=30)
        fecha_fin3 = fecha_fin1 + timedelta(minutes=30)

        cita3_data = {
            "doctor_id": doctor_id,
            "paciente_id": paciente_id,
            "fecha_inicio": fecha_inicio3.isoformat(),
            "fecha_fin": fecha_fin3.isoformat(),
            "motivo": "Cita con conflicto parcial"
        }

        cita3_response = authenticated_client.post(API_PATH_CITAS, json=cita3_data)
        assert cita3_response.status_code == status.HTTP_409_CONFLICT
        
        # 5. Crear Cita sin conflicto (11:00 - 12:00)
        fecha_inicio4 = fecha_fin1 
        fecha_fin4 = fecha_inicio4 + timedelta(hours=1)

        cita4_data = {
            "doctor_id": doctor_id,
            "paciente_id": paciente_id,
            "fecha_inicio": fecha_inicio4.isoformat(),
            "fecha_fin": fecha_fin4.isoformat(),
            "motivo": "Cita sin conflicto, justo después"
        }

        cita4_response = authenticated_client.post(API_PATH_CITAS, json=cita4_data)
        assert cita4_response.status_code == status.HTTP_201_CREATED

    def test_cancelacion_y_modificacion_citas(self, authenticated_client, sample_doctor, sample_paciente):
        """Test cancelación y modificación de una Cita existente."""

        # 1. Crear Doctor, Paciente y Cita inicial
        doctor_id = authenticated_client.post(API_PATH_DOCTORES, json=sample_doctor).json()["id"]
        paciente_id = authenticated_client.post("/api/v1/pacientes", json=sample_paciente).json()["id"]
        
        fecha_inicio = (datetime.now() + timedelta(days=2)).replace(hour=14, minute=0)
        fecha_fin = fecha_inicio + timedelta(minutes=45) # Cita de 45 minutos

        cita_data = {
            "doctor_id": doctor_id,
            "paciente_id": paciente_id,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "motivo": "Control de Ortodoncia"
        }

        cita_response = authenticated_client.post(API_PATH_CITAS, json=cita_data)
        cita_id = cita_response.json()["id"]

        # 2. Modificar Cita (cambiar la hora de inicio y el motivo)
        modificacion_data = {
            "fecha_inicio": (fecha_inicio + timedelta(hours=1)).isoformat(), # Mover 1 hora después
            "fecha_fin": (fecha_fin + timedelta(hours=1)).isoformat(),
            "motivo": "Control de Ortodoncia - Modificado a la tarde"
        }

        mod_response = authenticated_client.put(
            f"{API_PATH_CITAS}/{cita_id}",
            json=modificacion_data
        )
        assert mod_response.status_code == status.HTTP_200_OK

        # 3. Cancelar Cita
        cancel_response = authenticated_client.patch(
            f"{API_PATH_CITAS}/{cita_id}/cancelar"
        )
        assert cancel_response.status_code == status.HTTP_200_OK

        # 4. Verificar estado cancelado
        get_response = authenticated_client.get(f"{API_PATH_CITAS}/{cita_id}")
        assert get_response.json()["estado"] == "CANCELADA"

@pytest.mark.tipo_b
@pytest.mark.unit
class TestValidacionesHorarios:
    """Tests de validaciones lógicas para Citas y Doctores."""

    def test_validacion_horario_laboral_doctor(self, authenticated_client, sample_doctor):
        """Test validación de horario laboral: hora fin antes que hora inicio."""

        # Hora fin anterior a hora inicio
        invalid_data = sample_doctor.copy()
        invalid_data["hora_inicio_laboral"] = "17:00"
        invalid_data["hora_fin_laboral"] = "09:00"  # Inválido

        response = authenticated_client.post(API_PATH_DOCTORES, json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_validacion_cita_en_el_pasado(self, authenticated_client, sample_doctor, sample_paciente):
        """Test validación de que no se pueden crear citas en el pasado."""

        # Crear Doctor y Paciente
        doctor_id = authenticated_client.post(API_PATH_DOCTORES, json=sample_doctor).json()["id"]
        paciente_id = authenticated_client.post("/api/v1/pacientes", json=sample_paciente).json()["id"]
        
        # Cita en el pasado
        fecha_pasado = datetime.now() - timedelta(days=1)

        reserva_pasado = {
            "doctor_id": doctor_id,
            "paciente_id": paciente_id,
            "fecha_inicio": fecha_pasado.isoformat(),
            "fecha_fin": (fecha_pasado + timedelta(hours=1)).isoformat(),
            "motivo": "Cita en el pasado",
        }

        response = authenticated_client.post(API_PATH_CITAS, json=reserva_pasado)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pasado" in response.json()["detail"].lower()
