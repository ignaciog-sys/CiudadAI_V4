from fastapi.testclient import TestClient

from app import app


def test_home_redirects_to_login():
    client = TestClient(app)
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"
