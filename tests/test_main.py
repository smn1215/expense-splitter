import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_add_and_get_expense():
    response = client.post(
        "/api/expenses",
        json={"payer": "Alice", "amount": 50.0, "description": "Dinner"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["payer"] == "Alice"
    assert data["amount"] == 50.0

    response = client.get("/api/expenses")
    assert response.status_code == 200
    assert len(response.json()["expenses"]) > 0
