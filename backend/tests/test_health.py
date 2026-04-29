"""Pruebas del router de salud.

Propósito: verificar que la API responde y devuelve información básica del servicio.
Ejemplo de uso: sirve como primer test sencillo para enseñar el flujo de pytest.
"""


def test_health_endpoint_returns_ok(client):
    """El health check debe responder 200 con datos mínimos."""

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"