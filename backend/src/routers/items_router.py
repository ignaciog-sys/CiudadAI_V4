"""Router de recursos de ejemplo protegidos por autenticación.

Propósito: enseñar un endpoint funcional con datos mock y dependencia de usuario.
Ejemplo de uso: reemplazar `DEFAULT_ITEMS` por llamadas a servicios o persistencia real.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.common.responses import COMMON_ERROR_RESPONSES
from src.constants import API_TAGS, DEFAULT_ITEMS
from src.deps import get_current_user
from src.models.auth import CurrentUser

items_router = APIRouter(prefix="/items", tags=[API_TAGS["items"]])


@items_router.get("", responses=COMMON_ERROR_RESPONSES)
async def list_items(user: CurrentUser = Depends(get_current_user)) -> dict:
    """Lista recursos mock junto con el usuario autenticado.

    Patrón recomendado: el router solo coordina y delega lógica de negocio a servicios.
    """

    return {"items": DEFAULT_ITEMS, "requested_by": user.username}


@items_router.get("/{item_id}", responses=COMMON_ERROR_RESPONSES)
async def get_item(item_id: int, user: CurrentUser = Depends(get_current_user)) -> dict:
    """Busca un recurso mock por identificador.

    En proyectos reales conviene reemplazar el loop local por una llamada a capa de servicio.
    """

    for item in DEFAULT_ITEMS:
        if item["id"] == item_id:
            return {"item": item, "requested_by": user.username}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el recurso con id {item_id}.",
    )