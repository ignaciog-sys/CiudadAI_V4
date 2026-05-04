"""Tests unitarios del stub de anonimización.

Propósito: verificar que el stub devuelve los campos correctos y que cuando
el compañero lo implemente, los campos sensibles quedan modificados.
"""

from datetime import datetime

from src.models.tickets import TicketCategory, TicketCreateInput
from src.services.anonymizer import anonymize_ticket


def sample_input() -> TicketCreateInput:
    return TicketCreateInput(
        nombre="Ana",
        apellidos="García López",
        nif="12345678A",
        telefono="+34 600123456",
        email="ana@example.com",
        categoria=TicketCategory.movilidad,
        description="Hay un bache enorme en la Calle Mayor.",
        direccion_persona="Calle Mayor 1",
        ubicacion_incidencia="Esquina con la Plaza Central",
    )


def test_anonymize_returns_dict():
    """El stub debe devolver un diccionario con las claves del contrato."""

    result = anonymize_ticket(sample_input())

    assert isinstance(result, dict)
    expected_keys = {
        "nombre",
        "apellidos",
        "nif",
        "telefono",
        "email",
        "categoria",
        "description",
        "direccion_persona",
        "ubicacion_incidencia",
        "fecha",
    }
    assert expected_keys == set(result.keys())


def test_anonymize_preserves_non_sensitive_fields():
    """Campos no sensibles deben llegar sin modificar al resultado."""

    sample = sample_input()
    result = anonymize_ticket(sample)

    assert result["categoria"] == TicketCategory.movilidad
    assert result["description"] == sample.description
    assert result["direccion_persona"] == sample.direccion_persona
    assert result["ubicacion_incidencia"] == sample.ubicacion_incidencia


def test_anonymize_fecha_is_datetime():
    """El campo fecha debe ser un datetime con tzinfo."""

    result = anonymize_ticket(sample_input())

    assert isinstance(result["fecha"], datetime)
    assert result["fecha"].tzinfo is not None


# ---------------------------------------------------------------------------
# Este test fallará cuando el compañero implemente la anonimización real.
# En ese momento, reemplazar este test por uno que verifique el enmascarado.
# ---------------------------------------------------------------------------


def test_stub_warning_fields_are_not_yet_anonymized():
    """STUB: este test documenta que los campos sensibles aún no están anonimizados.

    Cuando el compañero implemente la lógica real, este test debe fallar y
    reemplazarse por aserciones que verifiquen el enmascarado correcto.
    """

    sample = sample_input()
    result = anonymize_ticket(sample)

    # Verificamos que los campos sensibles se enmascaran según la implementación
    assert result["nombre"] == "A***"
    assert result["apellidos"] == "G***"
    assert result["nif"] == "[NIF_OCULTO]"
    assert result["telefono"].endswith("***")
    assert "@***" in result["email"]
