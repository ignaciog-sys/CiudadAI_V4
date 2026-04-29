"""Router base para el dominio de tickets.

Propósito: exponer el contrato funcional mínimo del nuevo dominio sin acoplarlo
todavía a persistencia o a inferencia real.
"""

from fastapi import APIRouter, status

from src.common.responses import COMMON_ERROR_RESPONSES
from src.constants import API_TAGS
from src.models.tickets import (
    TicketCategory,
    TicketChannel,
    TicketContractSpec,
    TicketStatus,
)

tickets_router = APIRouter(prefix="/tickets", tags=[API_TAGS["tickets"]])


@tickets_router.get("/spec", status_code=status.HTTP_200_OK, responses=COMMON_ERROR_RESPONSES)
async def ticket_spec() -> TicketContractSpec:
    """Devuelve el contrato base del dominio de tickets."""

    return TicketContractSpec(
        input_fields=[
            "nombre",
            "apellidos",
            "nif",
            "telefono",
            "email",
            "categoria",
            "description",
            "canal",
            "direccion_persona",
            "ubicacion_incidencia",
            "fecha",
        ],
        persisted_fields=[
            "id",
            "nombre",
            "apellidos",
            "nif",
            "telefono",
            "email",
            "categoria",
            "description",
            "urgencia",
            "fecha",
            "canal",
            "direccion_persona",
            "ubicacion_incidencia",
            "model_urgencia",
            "model_categoria",
            "final_urgencia",
            "final_categoria",
            "status",
            "reviewed_by",
            "reviewed_at",
        ],
        anonymized_fields=["nombre", "apellidos", "nif", "telefono", "email"],
        urgency_scale=[1, 2, 3, 4, 5],
        categories=[
            TicketCategory.roads,
            TicketCategory.lighting,
            TicketCategory.waste,
            TicketCategory.water,
            TicketCategory.parks,
            TicketCategory.mobility,
            TicketCategory.safety,
            TicketCategory.other,
        ],
        channels=[
            TicketChannel.web,
            TicketChannel.mobile,
            TicketChannel.phone,
            TicketChannel.email,
            TicketChannel.app,
        ],
        statuses=[
            TicketStatus.pending_classification,
            TicketStatus.pending_review,
            TicketStatus.accepted,
            TicketStatus.in_progress,
            TicketStatus.resolved,
        ],
    )