"""Registro de middlewares de la aplicación.

Propósito: aislar la configuración transversal, por ejemplo CORS o logging HTTP.
Ejemplo de uso: `register_middlewares(app)` desde `app.py`.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings


def _parse_cors_origins(raw_origins: str) -> list[str]:
    if raw_origins.strip() == "*":
        return ["*"]
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def register_middlewares(app: FastAPI) -> None:
    """Aplica middlewares básicos adecuados para una plantilla inicial."""

    allow_origins = _parse_cors_origins(settings.cors_allow_origins)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )