"""Router de administración.

Propósito: exponer rutas exclusivas para administradores: dashboard con
estadísticas, listado de tickets pendientes y revisión de predicciones.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.responses import COMMON_ERROR_RESPONSES
from src.constants import API_TAGS
from src.db.session import get_db
from src.deps import require_admin
from src.models.auth import CurrentUser
from src.models.tickets import (
    TicketAdminDecision,
    TicketAnonymizedRecord,
    TicketDashboardStats,
    TicketStatus,
    TicketSummary,
)
from src.services import ticket_service

admin_router = APIRouter(prefix="/admin", tags=[API_TAGS["admin"]])


@admin_router.get(
    "/dashboard",
    status_code=status.HTTP_200_OK,
    responses=COMMON_ERROR_RESPONSES,
    summary="Dashboard del administrador",
)
async def admin_dashboard(user: CurrentUser = Depends(require_admin)) -> dict:
    """Información básica del panel de admin."""

    return {
        "message": "⚠️ ERES ADMIN - CONTENIDO CONFIDENCIAL",
        "username": user.username,
        "role": user.role,
        "content": {
            "title": "Panel de administración",
            "description": "Revisa incidencias, estadísticas y el estado de la ciudad desde aquí.",
        },
    }


@admin_router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    responses=COMMON_ERROR_RESPONSES,
    summary="Estadísticas agregadas de tickets",
)
async def admin_stats(
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(require_admin),
) -> TicketDashboardStats:
    """Devuelve métricas agregadas: totales, por estado, urgencia y categoría."""

    return await ticket_service.get_dashboard_stats(db)


@admin_router.get(
    "/tickets",
    status_code=status.HTTP_200_OK,
    responses=COMMON_ERROR_RESPONSES,
    summary="Listar tickets pendientes de revisión",
)
async def admin_list_tickets(
    status_filter: TicketStatus | None = Query(
        default=TicketStatus.pending_review, alias="status"
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(require_admin),
) -> list[TicketSummary]:
    """Lista tickets filtrando por estado (por defecto: pending_review)."""

    return await ticket_service.list_tickets(db, status_filter, skip, limit)


@admin_router.get(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_200_OK,
    responses=COMMON_ERROR_RESPONSES,
    summary="Detalle de un ticket",
)
async def admin_get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(require_admin),
) -> TicketAnonymizedRecord:
    """Devuelve el detalle completo de un ticket para revisión."""

    record = await ticket_service.get_ticket(db, ticket_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket #{ticket_id} no encontrado.",
        )
    return record


@admin_router.patch(
    "/tickets/{ticket_id}/review",
    status_code=status.HTTP_200_OK,
    responses=COMMON_ERROR_RESPONSES,
    summary="Revisar y clasificar un ticket",
)
async def admin_review_ticket(
    ticket_id: int,
    body: TicketAdminDecision,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
) -> TicketAnonymizedRecord:
    """El admin acepta o modifica la predicción del modelo sobre urgencia y categoría."""

    record = await ticket_service.admin_review_ticket(db, ticket_id, body, user.username)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket #{ticket_id} no encontrado.",
        )
    return record
