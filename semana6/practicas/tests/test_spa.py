# tests/test_spa.py
import pytest
from fastapi.testclient import TestClient

class TestSpaAPI:
    """
    Tests específicos para el dominio Spa - FICHA 3147246
    """

    def test_create_reserva_success(self, client, sample_reserva_data, auth_headers):
        """Test de creación exitosa de reserva en Spa"""
        response = client.post(
            "/spa_reservas/",
            json=sample_reserva_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        # Validaciones específicas de tu dominio Spa
        assert data["cliente"] == sample_reserva_data["cliente"]
        assert data["servicio"] == sample_reserva_data["servicio"]
        assert data["fecha"] == sample_reserva_data["fecha"]
        assert data["hora"] == sample_reserva_data["hora"]
        assert data["duracion"] == sample_reserva_data["duracion"]
        assert data["precio"] == sample_reserva_data["precio"]

    def test_get_reserva_not_found(self, client, auth_headers):
        """Test de reserva no encontrada en Spa"""
        response = client.get("/spa_reservas/999", headers=auth_headers)

        assert response.status_code == 404
        assert "reserva no encontrada" in response.json()["detail"].lower()

    def test_reserva_validation_error(self, client, auth_headers):
        """Test de validación de datos inválidos en reserva de Spa"""
        # Datos inválidos
        invalid_data = {
            "cliente": "",              # cliente vacío
            "servicio": "Masaje",       # ok
            "fecha": "fecha_invalida",  # formato incorrecto
            "hora": "99:99",            # hora inválida
            "duracion": -5,             # duración negativa
            "precio": "gratis"          # precio inválido (debería ser numérico)
        }

        response = client.post(
            "/spa_reservas/",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code == 422
        errors = response.json()["detail"]

        # Validar que al menos uno de los errores corresponda a los campos esperados
        assert any("cliente" in str(error) for error in errors)
        assert any("fecha" in str(error) for error in errors)
        assert any("hora" in str(error) for error in errors)
