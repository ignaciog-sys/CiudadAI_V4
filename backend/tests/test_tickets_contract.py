"""Pruebas del contrato base de tickets.

Propósito: asegurar que el dominio de incidencias acepta el formato esperado y
que el endpoint de especificación expone la base funcional del ticketing.
"""

from datetime import datetime

from src.models.tickets import (
    TicketAnonymizedRecord,
    TicketCategory,
    TicketChannel,
    TicketCreateInput,
    TicketStatus,
    TicketUrgency,
)


def test_ticket_create_input_builds_with_defaults():
    """El payload base del ciudadano debe aceptar el formato definido."""

    ticket = TicketCreateInput(
        nombre="Ana",
        apellidos="García López",
        nif="12345678A",
        telefono="600123123",
        email="ana@example.com",
        categoria=TicketCategory.roads,
        description="Hay un bache grande en la calle principal.",
        canal=TicketChannel.web,
        direccion_persona="Calle Mayor 1",
        ubicacion_incidencia="Esquina con Plaza Central",
    )

    assert ticket.nombre == "Ana"
    assert ticket.categoria == TicketCategory.roads
    assert ticket.fecha.tzinfo is not None


def test_ticket_anonymized_record_contains_control_fields():
    """La versión persistida debe incluir campos de control para ML y revisión."""

    record = TicketAnonymizedRecord(
        id=1,
        nombre="A***",
        apellidos="G***** L****",
        nif="***",
        telefono="***",
        email="***",
        categoria=TicketCategory.lighting,
        description="Farola apagada desde hace días.",
        urgencia=TicketUrgency.high,
        fecha=datetime.now().astimezone(),
        canal=TicketChannel.mobile,
        direccion_persona="Avenida del Parque 2",
        ubicacion_incidencia="Frente al portal 10",
        model_urgencia=TicketUrgency.medium,
        model_categoria=TicketCategory.lighting,
        final_urgencia=TicketUrgency.high,
        final_categoria=TicketCategory.lighting,
        status=TicketStatus.pending_review,
        reviewed_by=None,
        reviewed_at=None,
    )

    assert record.model_urgencia == TicketUrgency.medium
    assert record.final_urgencia == TicketUrgency.high
    assert record.status == TicketStatus.pending_review


def test_ticket_urgency_scale_matches_expected_range():
    """La escala de urgencia base debe ser de 1 a 5."""

    assert TicketUrgency.minimum == 1
    assert TicketUrgency.maximum == 5