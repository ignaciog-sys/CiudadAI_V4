"""Dependencias reutilizables de FastAPI.

Propósito: centralizar piezas inyectables como el usuario autenticado actual.
Ejemplo de uso: `Depends(get_current_user)` protege endpoints sin acoplar el router a la lógica de auth.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.config import settings
from src.models.auth import CurrentUser
from src.models.errors import AuthenticationError
from src.services.auth_service import decode_demo_token

# tokenUrl se publica en OpenAPI y debe coincidir con el endpoint de login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    """Obtiene el usuario autenticado a partir de un token bearer.

    Este ejemplo no firma JWT reales. Solo enseña el patrón para sustituirlo después.
    """

    # La dependencia transforma un token bearer en un objeto de usuario tipado.
    payload = decode_demo_token(token)
    if payload is None:
        raise AuthenticationError("Token inválido o caducado en el ejemplo mock.")
    return CurrentUser(**payload)