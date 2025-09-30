from typing import Dict, Any, List
from fastapi.testclient import TestClient
import pytest
from datetime import datetime

class APITestHelper:
    """Helper genérico para testing de APIs.
    Centraliza lógica común como la creación de recursos y validación de estructuras de respuesta.
    """

    def __init__(self, client: TestClient, auth_headers: Dict[str, str]):
        self.client = client
        self.auth_headers = auth_headers

    def create_and_get_id(self, endpoint: str, data: Dict[str, Any]) -> int:
        """Crear recurso mediante POST y retornar el ID del recurso creado.
        
        Args:
            endpoint: La ruta de la API (ej. /api/v1/pacientes).
            data: El payload JSON para la creación.
            
        Returns:
            El ID (int) del recurso recién creado.
        """
        response = self.client.post(endpoint, json=data, headers=self.auth_headers)
        # Se espera 200 (OK) o 201 (Created)
        assert response.status_code in [200, 201], f"Fallo al crear recurso en {endpoint}. Status: {response.status_code}, Detalle: {response.text}"
        return response.json()["id"]

    def assert_pagination_response(self, response_data: Dict[str, Any]):
        """Validar estructura de respuesta paginada estándar (items, total, page, limit)."""
        assert "items" in response_data, "Falta el campo 'items' en la respuesta paginada."
        assert "total" in response_data, "Falta el campo 'total' en la respuesta paginada."
        assert "page" in response_data, "Falta el campo 'page' en la respuesta paginada."
        assert "limit" in response_data, "Falta el campo 'limit' en la respuesta paginada."
        assert isinstance(response_data["items"], list)
        assert isinstance(response_data["total"], int)

    def assert_error_response(self, response_data: Dict[str, Any], error_code: str = None):
        """Validar estructura de respuesta de error (debe contener 'detail')."""
        assert "detail" in response_data, "Falta el campo 'detail' en la respuesta de error."
        if error_code:
            assert error_code in response_data.get("error_code", ""), f"Código de error esperado '{error_code}' no encontrado."

    def create_multiple_resources(self, endpoint: str, data_list: List[Dict[str, Any]]) -> List[int]:
        """Crear múltiples recursos secuencialmente y retornar sus IDs."""
        ids = []
        for data in data_list:
            resource_id = self.create_and_get_id(endpoint, data)
            ids.append(resource_id)
        return ids

def assert_valid_datetime_format(datetime_string: str):
    """Validar formato de datetime ISO 8601 (con o sin Z)."""
    try:
        # Reemplazar 'Z' por '+00:00' para compatibilidad completa con fromisoformat
        datetime.fromisoformat(datetime_string.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        pytest.fail(f"Formato de datetime inválido: {datetime_string}")

def assert_response_schema(response_data: Dict[str, Any], required_fields: List[str]):
    """Validar que la respuesta de la API contiene todos los campos requeridos."""
    for field in required_fields:
        assert field in response_data, f"Campo requerido '{field}' no encontrado en response: {response_data}"

def generate_test_pagination_params():
    """Generar una lista de parámetros de paginación comunes para usar en parametrize."""
    return [
        {"skip": 0, "limit": 10},
        {"skip": 5, "limit": 5},
        {"skip": 0, "limit": 1},
        {"skip": 10, "limit": 10}
    ]
