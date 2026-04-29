"""Plantilla de router para nuevos dominios.

Propósito: estandarizar cómo se definen nuevos endpoints sin duplicar estructura.
Ejemplo de uso: copiar este archivo a orders_router.py o users_router.py.
"""

from fastapi import APIRouter, status

from src.common.responses import COMMON_ERROR_RESPONSES

router = APIRouter(prefix="/template", tags=["template"])


@router.get("", status_code=status.HTTP_200_OK, responses=COMMON_ERROR_RESPONSES)
async def template_endpoint() -> dict:
    """Endpoint base para iniciar un nuevo dominio.

    Reemplaza este contenido por la lógica real o por una llamada a services.
    """

    return {"message": "Reemplaza este endpoint al crear tu dominio."}
