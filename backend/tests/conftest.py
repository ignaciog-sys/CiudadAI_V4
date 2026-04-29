"""Fixtures compartidas para pruebas.

Propósito: crear un cliente de pruebas reutilizable para todos los tests.
Ejemplo de uso: cualquier test puede pedir la fixture `client` para invocar endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client() -> TestClient:
    """Cliente de pruebas síncrono para endpoints FastAPI."""

    return TestClient(app)