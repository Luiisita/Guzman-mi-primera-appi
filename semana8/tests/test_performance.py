import pytest
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio
from fastapi import status # Importar status para consistencia

@pytest.mark.slow
@pytest.mark.benchmark
class TestRendimientoAPI:
    """Tests avanzados de rendimiento (performance) para endpoints de SalloCenter"""

    def test_tiempo_respuesta_citas(self, authenticated_client, benchmark):
        """Test tiempo de respuesta para listar citas (Gestión de Datos)"""

        def obtener_citas():
            # Endpoint adaptado al dominio de citas
            return authenticated_client.get("/api/v1/citas")

        # Benchmark automático con pytest-benchmark
        response = benchmark(obtener_citas)
        assert response.status_code == status.HTTP_200_OK

        # El benchmark automáticamente reportará estadísticas

    def test_requests_concurrentes(self, authenticated_client):
        """Test manejo de requests concurrentes para el endpoint de citas"""

        def realizar_request():
            # Simular múltiples recepcionistas/pacientes buscando citas al mismo tiempo
            response = authenticated_client.get("/api/v1/citas")
            return response.status_code

        # Ejecutar 10 requests concurrentes
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(realizar_request) for _ in range(10)]
            results = [future.result() for future in futures]

        # Todos los requests deben ser exitosos
        assert all(status_code == 200 for status_code in results)

    def test_manejo_payload_grande(self, authenticated_client):
        """Test manejo de payloads grandes al crear un registro (Testing Integral)"""

        # Crear una 'cita' o 'historial médico' con datos grandes
        datos_grandes = {
            "nombre_paciente": "Paciente con Historial Largo",
            "motivo_cita": "Test de carga de datos",
            "observaciones": "x" * 1000,  # 1KB de observaciones
            "diagnostico_previo": {
                f"diagnostico_{i}": f"detalle_largo_{'x' * 100}"
                for i in range(50)  # 50 campos de diagnóstico
            }
        }

        start_time = time.time()
        # Endpoint para crear una nueva cita o registro
        response = authenticated_client.post("/api/v1/citas", json=datos_grandes)
        end_time = time.time()

        assert response.status_code == status.HTTP_201_CREATED
        assert (end_time - start_time) < 5.0  # Menos de 5 segundos