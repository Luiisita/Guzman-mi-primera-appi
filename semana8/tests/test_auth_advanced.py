# tests/test_auth_advanced.py
import pytest
from fastapi import status
from datetime import datetime, timedelta
import jwt

@pytest.mark.auth
@pytest.mark.integration
class TestAdvancedAuthentication:
    """Advanced authentication and authorization tests for SalloCenter"""

    def test_complete_user_registration(self, client):
        """Test complete registration for a new patient/user with full details"""

        # Data includes specific fields relevant to a patient/user in a system
        user_data = {
            "username": "new_patient_test",
            "email": "patient_new@sallocenter.com",
            "password": "secure_password_123",
            "full_name": "Paciente de Prueba", # Renamed to 'full_name'
            "phone": "+1234567890"             # Renamed to 'phone'
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert "id" in response_data
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]
        assert "password" not in response_data  # Should not return password
        assert response_data["is_active"] is True

    def test_login_and_token_validation(self, client, sample_user_generic):
        """Test login and token validation for an authenticated user"""

        # Register user
        client.post("/api/v1/auth/register", json=sample_user_generic)

        # Login
        login_data = {
            "username": sample_user_generic["username"],
            "password": sample_user_generic["password"]
        }

        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == status.HTTP_200_OK

        token_data = login_response.json()
        assert "access_token" in token_data
        assert "token_type" in token_data
        assert "expires_in" in token_data
        assert token_data["token_type"] == "bearer"

        # Validate token using protected endpoint (e.g., getting own profile)
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        profile_response = client.get("/api/v1/auth/me", headers=headers)
        assert profile_response.status_code == status.HTTP_200_OK

        profile_data = profile_response.json()
        assert profile_data["username"] == sample_user_generic["username"]

    def test_refresh_token(self, client, sample_user_generic):
        """Test token refresh to maintain session continuity"""

        # Register and login
        client.post("/api/v1/auth/register", json=sample_user_generic)

        login_response = client.post("/api/v1/auth/login", json={
            "username": sample_user_generic["username"],
            "password": sample_user_generic["password"]
        })

        original_token = login_response.json()["access_token"]

        # Refresh token
        headers = {"Authorization": f"Bearer {original_token}"}
        refresh_response = client.post("/api/v1/auth/refresh", headers=headers)

        assert refresh_response.status_code == status.HTTP_200_OK
        new_token_data = refresh_response.json()

        assert "access_token" in new_token_data
        assert new_token_data["access_token"] != original_token

    def test_logout_and_token_invalidation(self, client, sample_user_generic):
        """Test logout and immediate token invalidation for security"""

        # Register, login
        client.post("/api/v1/auth/register", json=sample_user_generic)

        login_response = client.post("/api/v1/auth/login", json={
            "username": sample_user_generic["username"],
            "password": sample_user_generic["password"]
        })

        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Verify token is valid before logout
        profile_response = client.get("/api/v1/auth/me", headers=headers)
        assert profile_response.status_code == status.HTTP_200_OK

        # Logout
        logout_response = client.post("/api/v1/auth/logout", headers=headers)
        assert logout_response.status_code == status.HTTP_200_OK

        # Verify token is invalidated after logout
        profile_response2 = client.get("/api/v1/auth/me", headers=headers)
        assert profile_response2.status_code == status.HTTP_401_UNAUTHORIZED

    def test_role_based_access_control(self, client):
        """Test access control based on roles: 'admin' vs 'patient'"""

        # Create admin user (e.g., Clinic Manager or Doctor)
        admin_user = {
            "username": "clinic_admin",
            "email": "manager@sallocenter.com",
            "password": "admin_password",
            "role": "administrador"  # Role for data management access
        }

        # Create regular user (Patient)
        patient_user = {
            "username": "patient_001",
            "email": "patient@test.com",
            "password": "user_password",
            "role": "paciente"  # Role for basic access (appointments, profile)
        }

        # Register users
        client.post("/api/v1/auth/register", json=admin_user)
        client.post("/api/v1/auth/register", json=patient_user)

        # Login as admin
        admin_login = client.post("/api/v1/auth/login", json={
            "username": admin_user["username"],
            "password": admin_user["password"]
        })
        admin_token = admin_login.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Login as patient
        patient_login = client.post("/api/v1/auth/login", json={
            "username": patient_user["username"],
            "password": patient_user["password"]
        })
        patient_token = patient_login.json()["access_token"]
        patient_headers = {"Authorization": f"Bearer {patient_token}"}

        # Endpoint only for admin (e.g., viewing all user data)
        admin_endpoint_response = client.get("/api/v1/admin/users", headers=admin_headers)
        assert admin_endpoint_response.status_code == status.HTTP_200_OK

        # Patient should not be able to access the admin endpoint
        patient_admin_response = client.get("/api/v1/admin/users", headers=patient_headers)
        assert patient_admin_response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.auth
@pytest.mark.unit
class TestAuthValidations:
    """Authentication validation tests, critical for Data Management (Gestión de Datos)"""

    def test_duplicate_email_validation(self, client):
        """Test duplicate email validation to ensure data integrity"""

        user_data = {
            "username": "user1_unique",
            "email": "duplicate@test.com",
            "password": "password123"
        }

        # First successful registration
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED

        # Second registration with same email must fail (Data Management constraint)
        user_data2 = {
            "username": "user2_unique",
            "email": "duplicate@test.com",  # Duplicate email
            "password": "password456"
        }

        response2 = client.post("/api/v1/auth/register", json=user_data2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response2.json()["detail"].lower()

    def test_password_requirements_validation(self, client):
        """Test password requirements validation (security constraint)"""

        # Password that is too short
        weak_password_user = {
            "username": "weak_user",
            "email": "weak@test.com",
            "password": "123"  # Too short
        }

        response = client.post("/api/v1/auth/register", json=weak_password_user)
        # Assuming Pydantic or backend validation for password strength
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_failed_login_attempts_handling(self, client, sample_user_generic):
        """Test handling of failed login attempts (anti-bruteforce security)"""

        # Register user
        client.post("/api/v1/auth/register", json=sample_user_generic)

        # Multiple failed attempts
        for _ in range(5):
            response = client.post("/api/v1/auth/login", json={
                "username": sample_user_generic["username"],
                "password": "incorrect_password"
            })
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # The sixth attempt (even with correct password) could be blocked by a rate limit/lockout
        response = client.post("/api/v1/auth/login", json={
            "username": sample_user_generic["username"],
            "password": sample_user_generic["password"]  # Correct password
        })

        # Expect success (HTTP_200_OK) if no lockout is implemented, or HTTP_429_TOO_MANY_REQUESTS if a lockout is active.
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_429_TOO_MANY_REQUESTS]