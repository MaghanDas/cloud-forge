from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "CloudForge"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "CloudForge"
    assert "id" in data

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "CloudForge"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "CloudForge"
    assert "id" in data