"""Modelos del endpoint de salud.

Propósito: representar el estado general del servicio de forma tipada.
Ejemplo de uso: responder si la API está viva y en qué entorno se está ejecutando.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Respuesta del health check."""

    status: str
    app: str
    environment: str