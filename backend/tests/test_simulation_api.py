"""
Integration tests for the TDOS backend simulation API.
"""

from fastapi.testclient import TestClient

from api import app


def test_simulation_create_and_run():
    client = TestClient(app)

    payload = {
        "name": "Backend Integration Test",
        "total_steps": 5,
        "assets": [
            {
                "asset_id": "AST-API-001",
                "asset_name": "API Test Rail",
                "asset_type": "RAIL",
                "latitude": 13.0,
                "longitude": 80.0,
                "health_score": 95.0,
                "degradation_rate": 0.05,
                "age_days": 30,
            }
        ],
        "scenarios": [],
    }

    created = client.post("/simulations", json=payload)
    assert created.status_code == 200

    simulation_id = created.json()["simulation_id"]
    assert simulation_id.startswith("SIM-")

    result = client.post(f"/simulations/{simulation_id}/run")
    assert result.status_code == 200

    body = result.json()
    assert body["simulation_id"] == simulation_id
    assert body["success"] is True
    assert body["simulation_steps"] == 5
    assert body["total_assets"] == 1

    status = client.get(f"/simulations/{simulation_id}")
    assert status.status_code == 200
    assert status.json()["completed"] is True
