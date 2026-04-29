"""Pruebas del flujo de autenticación mock.

Propósito: comprobar login, acceso autorizado y rechazo de tokens inválidos.
Ejemplo de uso: mostrar cómo se testean endpoints públicos y protegidos.
"""


def test_login_returns_token_for_valid_credentials(client):
    """El login mock debe devolver un bearer token cuando las credenciales son correctas."""

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "api_user", "password": "change_me"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_protected_endpoint_requires_valid_token(client):
    """Un endpoint protegido debe funcionar con el token mock correcto."""

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer bootstrap-token"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "api_user"


def test_protected_endpoint_rejects_invalid_token(client):
    """Un endpoint protegido debe rechazar un token no reconocido."""

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401