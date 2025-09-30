import pytest
from fastapi import status

# Rutas estándar de autenticación, asumiendo /auth/register y /auth/login
API_PATH_REGISTER = "/api/v1/auth/register"
API_PATH_LOGIN = "/api/v1/auth/login"
# Usaremos una ruta protegida genérica para verificar el acceso (ej. listar pacientes)
API_PATH_PROTECTED = "/api/v1/pacientes" 

@pytest.mark.auth
@pytest.mark.integration
class TestAutenticacionSmileCenter:
    """Tests de autenticación adaptados al dominio de la Clínica Dental"""

    def test_registro_empleado_exitoso(self, client, sample_user_generic):
        """Test: Registro de un nuevo empleado/administrador (Creación de usuario)"""
        
        # Modificamos el usuario genérico para que sea un administrador de la clínica
        admin_data = sample_user_generic.copy()
        admin_data["username"] = "admin_smile"
        admin_data["email"] = "admin@smilecenter.co"
        admin_data["role"] = "administrador" # Asumiendo que el modelo tiene un campo 'role'

        response = client.post(API_PATH_REGISTER, json=admin_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "admin_smile"
        assert data["is_active"] is True
        assert "password" not in data # La contraseña no debe regresar en la respuesta

    def test_login_credenciales_validas(self, client, sample_user_generic):
        """Test: Login con credenciales válidas para obtener el Token de Acceso"""
        
        # 1. Asegurar que el usuario existe (registrarlo primero)
        client.post(API_PATH_REGISTER, json=sample_user_generic)

        # 2. Intentar login
        login_data = {
            "username": sample_user_generic["username"],
            "password": sample_user_generic["password"]
        }

        response = client.post(API_PATH_LOGIN, json=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
    def test_login_credenciales_invalidas(self, client):
        """Test: Login con credenciales inexistentes o incorrectas (espera 401)"""
        login_data = {
            "username": "recepcionista_fantasma",
            "password": "mala_clave"
        }

        response = client.post(API_PATH_LOGIN, json=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "credenciales inválidas" in response.json()["detail"].lower()

    def test_acceso_sin_token_a_ruta_protegida(self, client):
        """Test: Intentar listar Pacientes sin proporcionar un token de autenticación"""
        response = client.get(API_PATH_PROTECTED) # Endpoint de Pacientes

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "no autenticado" in response.json()["detail"].lower()

    def test_acceso_token_invalido_o_expirado(self, client):
        """Test: Acceso a ruta protegida con un formato de token incorrecto"""
        headers = {"Authorization": "Bearer token.completamente.falso"}
        response = client.get(API_PATH_PROTECTED, headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "token inválido" in response.json()["detail"].lower()
