"""Contratos de dominio para incidencias y tickets.

Propósito: definir la base lógica de tickets, el payload del ciudadano, la
versión anonimizada que se persiste y los metadatos de revisión.
"""

import re
import unicodedata
from datetime import datetime, timezone
from enum import IntEnum, StrEnum

from pydantic import BaseModel, Field


def _normalize_category(value: str) -> str:
    normalized = value.strip().lower()
    normalized = unicodedata.normalize("NFKD", normalized)
    normalized = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    normalized = normalized.replace("-", "_").replace(" ", "_")
    normalized = re.sub(r"_+", "_", normalized)
    return normalized


class TicketCategory(StrEnum):
    """Taxonomía base para clasificar incidencias urbanas."""

    movilidad = "movilidad"
    limpieza = "limpieza"
    alumbrado_publico = "alumbrado_publico"
    parques_y_jardines = "parques_y_jardines"
    mobiliario_urbano = "mobiliario_urbano"

    @classmethod
    def _missing_(cls, value: object):
        if not isinstance(value, str):
            return None

        normalized = _normalize_category(value)

        # Acepta el nombre del miembro (p.ej. "alumbrado_publico"),
        # el valor canónico (p.ej. "parques_y_jardines") y variantes
        # con espacios/acentos (p.ej. "Parques y jardines").
        for member in cls:
            if normalized == member.name or normalized == member.value:
                return member

        return None


class TicketChannel(StrEnum):
    """Canal por el que entra una incidencia."""

    web = "web"
    mobile = "mobile"
    phone = "phone"
    email = "email"
    app = "app"


class TicketUrgency(IntEnum):
    """Escala de urgencia usada por el modelo y la revisión manual."""

    minimum = 1
    low = 2
    medium = 3
    high = 4
    maximum = 5


class TicketStatus(StrEnum):
    """Estado operativo de un ticket."""

    pending_classification = "pending_classification"
    pending_review = "pending_review"
    accepted = "accepted"
    in_progress = "in_progress"
    resolved = "resolved"


class TicketCreateInput(BaseModel):
    """Payload que envía el ciudadano antes de anonimizar y persistir."""

    nombre: str = Field(min_length=1, max_length=120)
    apellidos: str = Field(min_length=1, max_length=180)
    nif: str = Field(min_length=5, max_length=32)
    telefono: str = Field(min_length=5, max_length=24)
    email: str = Field(min_length=5, max_length=254)
    categoria: TicketCategory
    description: str = Field(min_length=1, max_length=4000)
    canal: TicketChannel
    direccion_persona: str = Field(min_length=1, max_length=255)
    ubicacion_incidencia: str = Field(min_length=1, max_length=255)
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TicketAnonymizedRecord(BaseModel):
    """Versión que se persiste en BD después de anonimizar los datos sensibles.

    Los campos personales se mantienen en el contrato de almacenamiento, pero el
    valor que se debe escribir siempre es el resultado anonimizado.
    """

    id: int | None = None
    nombre: str = Field(description="Nombre ya anonimizado")
    apellidos: str = Field(description="Apellidos ya anonimizado")
    nif: str = Field(description="NIF ya anonimizado")
    telefono: str = Field(description="Teléfono ya anonimizado")
    email: str = Field(description="Email ya anonimizado")
    categoria: TicketCategory
    description: str = Field(min_length=1, max_length=4000)
    urgencia: TicketUrgency | None = None
    fecha: datetime
    canal: TicketChannel
    direccion_persona: str = Field(min_length=1, max_length=255)
    ubicacion_incidencia: str = Field(min_length=1, max_length=255)
    model_urgencia: TicketUrgency | None = None
    model_categoria: TicketCategory | None = None
    final_urgencia: TicketUrgency | None = None
    final_categoria: TicketCategory | None = None
    status: TicketStatus = TicketStatus.pending_classification
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None


class TicketClassificationResult(BaseModel):
    """Salida del servicio de inferencia para urgencia y categoría."""

    urgency: TicketUrgency = Field(description="Urgencia predicha por el modelo")
    category: TicketCategory = Field(description="Categoría predicha por el modelo")
    model_name: str = Field(min_length=1, max_length=120)
    model_version: str = Field(min_length=1, max_length=60)
    scored_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TicketAdminDecision(BaseModel):
    """Decisión final del administrador sobre un ticket."""

    urgency: TicketUrgency = Field(description="Urgencia final decidida por admin")
    category: TicketCategory = Field(description="Categoría final decidida por admin")
    notes: str | None = Field(default=None, max_length=2000)
    status: TicketStatus = TicketStatus.accepted


class TicketSummary(BaseModel):
    """Resumen mínimo del ticket para listados y dashboards."""

    id: int
    category: TicketCategory
    urgency: TicketUrgency | None = None
    status: TicketStatus
    fecha: datetime
    canal: TicketChannel
    ubicacion_incidencia: str
    model_urgencia: TicketUrgency | None = None
    model_categoria: TicketCategory | None = None
    final_urgencia: TicketUrgency | None = None
    final_categoria: TicketCategory | None = None


class TicketDashboardStats(BaseModel):
    """Estadísticas agregadas para el dashboard del admin."""

    total: int = 0
    pending_review: int = 0
    open: int = 0
    resolved: int = 0
    by_urgency: dict[TicketUrgency, int] = Field(default_factory=dict)
    by_category: dict[TicketCategory, int] = Field(default_factory=dict)


class TicketContractSpec(BaseModel):
    """Contrato resumido para documentar la base del dominio de tickets."""

    input_fields: list[str]
    persisted_fields: list[str]
    anonymized_fields: list[str]
    urgency_scale: list[int]
    categories: list[TicketCategory]
    channels: list[TicketChannel]
    statuses: list[TicketStatus]