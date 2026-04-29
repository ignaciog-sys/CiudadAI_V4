"""Modelos relacionados con autenticación.

Propósito: definir cómo viajan las credenciales y el usuario autenticado por la API.
Ejemplo de uso: `TokenResponse` representa la respuesta del login mock.
"""

from pydantic import BaseModel, Field


class LoginInput(BaseModel):
    """Credenciales básicas para el login de ejemplo."""

    username: str = Field(example="api_user")
    password: str = Field(example="change_me")


class TokenResponse(BaseModel):
    """Respuesta mock que simula un access token OAuth2/JWT."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class CurrentUser(BaseModel):
    """Usuario autenticado disponible dentro de endpoints protegidos."""

    username: str
    role: str = "member"