import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Lekhak" in response.json()["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_check_endpoint_valid_input():
    response = client.post("/check", json={"text": "मी घरी आहे"})
    assert response.status_code == 200
    data = response.json()
    assert "spelling" in data
    assert "grammar" in data
    assert "total_issues" in data


def test_check_endpoint_empty_input():
    response = client.post("/check", json={"text": ""})
    assert response.status_code == 422  # Pydantic validation error


def test_check_endpoint_detects_issues():
    response = client.post("/check", json={"text": "मी मी घरी जातो.  "})
    assert response.status_code == 200
    assert response.json()["total_issues"] > 0