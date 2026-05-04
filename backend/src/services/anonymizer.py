import re
import logging
from src.models.tickets import TicketCreateInput

logger = logging.getLogger(__name__)

def anonimizar_valor(texto: str, tipo: str) -> str:
    if not texto: return ""
    texto = str(texto).strip()
    if not texto: return ""

    if tipo in ["nombre", "apellidos"]:
        return f"{texto[0]}***"
    if tipo == "nif":
        return "[NIF_OCULTO]"
    if tipo == "telefono":
        return f"{texto[0]}***"
    if tipo == "email":
        try:
            usuario, dominio_completo = texto.split('@')
            partes_dominio = dominio_completo.rsplit('.', 1)
            tld = partes_dominio[1] if len(partes_dominio) == 2 else ""
            return f"{usuario[0]}***@***.{tld}" if tld else f"{usuario[0]}***@***"
        except:
            return "[EMAIL_OCULTO]"
    return texto

def limpiar_descripcion(descripcion: str, ticket: TicketCreateInput) -> str:
    if not descripcion: return ""
    texto_limpio = descripcion
    # Reemplazo contextual basado en los datos del ticket
    if ticket.nif:
        texto_limpio = re.sub(re.escape(ticket.nif), "[NIF_OCULTO]", texto_limpio, flags=re.IGNORECASE)
    if ticket.email:
        texto_limpio = re.sub(re.escape(ticket.email), anonimizar_valor(ticket.email, "email"), texto_limpio, flags=re.IGNORECASE)
    if ticket.telefono:
        texto_limpio = re.sub(re.escape(ticket.telefono), anonimizar_valor(ticket.telefono, "telefono"), texto_limpio, flags=re.IGNORECASE)
    if ticket.nombre and len(ticket.nombre) > 2:
        texto_limpio = re.sub(r'\b' + re.escape(ticket.nombre) + r'\b', anonimizar_valor(ticket.nombre, "nombre"), texto_limpio, flags=re.IGNORECASE)
    if ticket.apellidos and len(ticket.apellidos) > 2:
        texto_limpio = re.sub(r'\b' + re.escape(ticket.apellidos) + r'\b', anonimizar_valor(ticket.apellidos, "apellidos"), texto_limpio, flags=re.IGNORECASE)
    
    # Reemplazo general para otros posibles correos o DNIs
    texto_limpio = re.sub(r'\b\d{8}\s*[A-Za-z]?\b', '[NRO_OCULTO]', texto_limpio)
    texto_limpio = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', lambda m: anonimizar_valor(m.group(0), "email"), texto_limpio)
    return texto_limpio

def anonymize_ticket(ticket_input: TicketCreateInput) -> dict:
    letra_inicial = ticket_input.nombre[0] if ticket_input.nombre else "*"
    logger.info(f"Procesando anonimización para: {letra_inicial}***")
    return {
        "nombre": anonimizar_valor(ticket_input.nombre, "nombre"),
        "apellidos": anonimizar_valor(ticket_input.apellidos, "apellidos"),
        "nif": anonimizar_valor(ticket_input.nif, "nif"),
        "telefono": anonimizar_valor(ticket_input.telefono, "telefono"),
        "email": anonimizar_valor(ticket_input.email, "email"),
        "categoria": ticket_input.categoria,
        "description": limpiar_descripcion(ticket_input.description, ticket_input),
        "direccion_persona": ticket_input.direccion_persona,
        "ubicacion_incidencia": ticket_input.ubicacion_incidencia,
        "fecha": ticket_input.fecha,
    }