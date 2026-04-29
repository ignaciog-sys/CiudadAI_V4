"""Servicio de autenticación mock.

Propósito: separar login y validación de token de la capa HTTP.
Ejemplo de uso: authenticate_demo_user permite bootstrap de seguridad sin integrar aún un IdP.
"""

from src.config import settings


def authenticate_demo_user(username: str, password: str) -> dict | None:
    """Valida credenciales contra valores mock definidos en la configuración."""

    # Este bloque simula validación de credenciales. En producción se reemplaza por JWT/OIDC.
    if (
        username == settings.mock_auth_username
        and password == settings.mock_auth_password
    ):
        return {
            "access_token": settings.mock_auth_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
        }
    return None


def decode_demo_token(token: str) -> dict | None:
    """Decodifica un token de ejemplo y devuelve un usuario ficticio.

    En un proyecto real, aquí se validaría firma, expiración, audiencia y claims.
    """

    # En producción se validan firma, expiración, audiencia y claims.
    if token != settings.mock_auth_token:
        return None
    return {
        "username": settings.mock_auth_username,
        "role": "member",
    }