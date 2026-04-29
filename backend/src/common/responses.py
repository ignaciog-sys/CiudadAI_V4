"""Respuestas HTTP comunes para documentar errores de forma consistente.

Propósito: reutilizar descripciones de respuestas en varios endpoints sin duplicar diccionarios.
Ejemplo de uso: `responses=COMMON_ERROR_RESPONSES` en un decorador de router.
"""

from fastapi import status

COMMON_ERROR_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "No autenticado o token inválido.",
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Recurso no encontrado.",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Error interno no controlado.",
    },
}