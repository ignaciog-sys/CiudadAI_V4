"""Pruebas del contrato publicado por el router de tickets."""


def test_ticket_spec_endpoint_returns_contract(client):
    """El endpoint de especificación debe exponer la base del dominio."""

    response = client.get("/api/v1/tickets/spec")

    assert response.status_code == 200
    payload = response.json()
    assert payload["anonymized_fields"] == [
        "nombre",
        "apellidos",
        "nif",
        "telefono",
        "email",
    ]
    assert payload["urgency_scale"] == [1, 2, 3, 4, 5]
    assert "movilidad" in payload["categories"]
    assert "limpieza" in payload["categories"]
    assert "alumbrado_publico" in payload["categories"]
    assert "parques_y_jardines" in payload["categories"]
    assert "mobiliario_urbano" in payload["categories"]
    assert "web" in payload["channels"]
    assert "pending_review" in payload["statuses"]