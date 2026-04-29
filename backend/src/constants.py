"""Constantes y mensajes reutilizables de la aplicación.

Propósito: evitar literales repetidos y centralizar valores simples del proyecto.
Ejemplo de uso: importar `API_TAGS` para mantener nombres coherentes en los routers.
"""

API_TAGS = {
    "health": "health",
    "auth": "auth",
    "items": "items",
}

DEFAULT_ITEMS = [
    {"id": 1, "name": "api-gateway", "owner": "platform-team"},
    {"id": 2, "name": "billing-service", "owner": "core-team"},
]