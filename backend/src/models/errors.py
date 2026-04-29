"""Excepciones y respuestas de error de la aplicación.

Propósito: definir errores propios para separar problemas de dominio de errores genéricos.
Ejemplo de uso: lanzar `AuthenticationError` desde un servicio y traducirlo en `app.py`.
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Formato simple de error para respuestas HTTP."""

    detail: str


class AuthenticationError(Exception):
    """Error usado cuando las credenciales o el token no son válidos."""


class ItemNotFoundError(Exception):
    """Error usado cuando un recurso mock no existe."""