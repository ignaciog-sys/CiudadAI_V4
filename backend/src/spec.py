"""Opcional: composición de metadatos OpenAPI.

Propósito: centralizar los metadatos del servicio cuando el proyecto crece
y se quieren separar de app.py para mantener el punto de entrada limpio.

Ejemplo de uso:
    from src.spec import build_openapi_metadata
    metadata = build_openapi_metadata()
"""

from src.config import settings


def build_openapi_metadata() -> dict:
    """Construye un diccionario reutilizable para inicializar FastAPI."""

    return {
        "title": settings.app_name,
        "description": settings.app_description,
        "version": settings.app_version,
        "docs_url": settings.docs_url,
        "openapi_url": settings.openapi_url,
        "redoc_url": settings.redoc_url,
    }
