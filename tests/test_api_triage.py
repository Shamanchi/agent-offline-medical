"""API-тесты без сети: TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_symptoms(client: TestClient) -> None:
    resp = client.get("/api/v1/symptoms")
    assert resp.status_code == 200
    assert "fever" in resp.json()["symptoms"]


def test_triage(client: TestClient) -> None:
    resp = client.post("/api/v1/triage", json={"symptoms": "fever and dry cough"})
    assert resp.status_code == 200
    assert resp.json()["urgency"] == "routine"
    assert "disclaimer" in resp.json()


def test_triage_rejects_empty(client: TestClient) -> None:
    resp = client.post("/api/v1/triage", json={"symptoms": "   "})
    assert resp.status_code == 422


@pytest.mark.integration()
def test_emergency_shape(client: TestClient) -> None:
    """Интеграционный по маркеру: emergency-форма, без сети."""
    resp = client.post("/api/v1/triage", json={"symptoms": "severe bleeding after fall"})
    assert resp.status_code == 200
    assert resp.json()["urgency"] == "emergency"
