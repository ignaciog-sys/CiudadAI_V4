"""Stub de anonimización de datos personales — pendiente de implementación.

⚠️  ESTE MÓDULO LO IMPLEMENTA EL COMPAÑERO RESPONSABLE DE ANONIMIZACIÓN.

Propósito: recibir el payload crudo del ciudadano y devolver un diccionario
con los mismos campos pero con los datos personales anonimizados, listo para
persistir en la base de datos.

Contrato esperado de la función `anonymize_ticket`:
    - Entrada: instancia de TicketCreateInput
    - Salida: dict con los mismos campos que TicketCreateInput pero con los
      campos sensibles sustituidos por sus versiones anonimizadas:
        · nombre   → e.g. "A***"
        · apellidos → e.g. "G***** L****"
        · nif      → "***"
        · telefono → "***"
        · email    → "***@***.***"
    - Los campos no sensibles (categoria, description, etc.) deben
      pasarse sin modificar al dict de salida.

Mientras no se implemente la lógica real, la función actúa como identidad
(pasa los datos SIN anonimizar) para que el resto del backend pueda arrancar.
El status del ticket se fuerza a `pending_classification` igual que en el
flujo real, así que no hay diferencia funcional en el resto del código.

TODO: implementar la lógica de anonimización real aquí.
"""

import logging

from src.models.tickets import TicketCreateInput

logger = logging.getLogger(__name__)


def anonymize_ticket(ticket_input: TicketCreateInput) -> dict:
    """Anonimiza los datos personales de un ticket antes de persistirlo.

    ⚠️  STUB: actualmente pasa los datos sin modificar.
    Reemplazar con la lógica de anonimización real.

    Args:
        ticket_input: Payload original del ciudadano con datos personales.

    Returns:
        Diccionario con los campos del ticket listos para persistir.
        Los campos sensibles deben estar anonimizados en la implementación real.
    """

    logger.warning(
        "anonymize_ticket: usando stub sin anonimización real. "
        "El compañero debe implementar este módulo."
    )

    # --- STUB: se devuelven los datos tal cual hasta que el compañero implemente esto ---
    return {
        "nombre": ticket_input.nombre,        # TODO: anonimizar
        "apellidos": ticket_input.apellidos,  # TODO: anonimizar
        "nif": ticket_input.nif,              # TODO: anonimizar
        "telefono": ticket_input.telefono,    # TODO: anonimizar
        "email": ticket_input.email,          # TODO: anonimizar
        # Campos no sensibles — pasar sin modificar
        "categoria": ticket_input.categoria,
        "description": ticket_input.description,
        "direccion_persona": ticket_input.direccion_persona,
        "ubicacion_incidencia": ticket_input.ubicacion_incidencia,
        "fecha": ticket_input.fecha,
    }
