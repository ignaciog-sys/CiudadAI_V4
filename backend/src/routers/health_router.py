"""Router del health check.

Propósito: ofrecer un endpoint simple para comprobar que la API responde.
Ejemplo de uso: orquestadores, pruebas o monitors consultan `/health`.
"""

from fastapi import APIRouter, status

from src.constants import API_TAGS
from src.models.health import HealthResponse
from src.config import settings

health_router = APIRouter(prefix="/health", tags=[API_TAGS["health"]])


@health_router.get("", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check() -> HealthResponse:
    """Devuelve un estado básico del servicio."""

    return HealthResponse(
        status="ok",
        app=settings.app_name,
        environment=settings.app_env,
    )