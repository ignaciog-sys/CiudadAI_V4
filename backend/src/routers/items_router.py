"""Router de items de ejemplo.

Propósito: exponer un endpoint simple para el frontend de dashboard.
"""

from fastapi import APIRouter

from src.constants import API_TAGS, DEFAULT_ITEMS

items_router = APIRouter(prefix="/items", tags=[API_TAGS["items"]])


@items_router.get("", status_code=200)
async def list_items() -> dict:
    """Devuelve una respuesta de items con metadatos mínimos para la UI."""
    return {
        "items": DEFAULT_ITEMS,
        "requested_by": "frontend",
    }
