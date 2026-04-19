import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from server import app


client = TestClient(app)


def test_calculate_endpoint_returns_expected_fields() -> None:
    payload = {
        "flow_rate": 0.02,
        "diameter": 0.1,
        "length": 30,
        "roughness": 0.000045,
        "density": 998.2,
        "viscosity": 0.001003,
        "method": "colebrook",
    }

    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    for key in [
        "velocity",
        "reynolds",
        "regime",
        "relative_roughness",
        "friction_factor",
        "pressure_drop",
        "head_loss",
        "plot",
    ]:
        assert key in data

    assert data["reynolds"] > 0
    assert data["friction_factor"] > 0
    assert "data" in data["plot"]
    assert "layout" in data["plot"]
