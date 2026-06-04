"""Phase 0 acceptance tests: FastAPI startup and /health endpoint."""


def test_health_endpoint_returns_200(client):
    """GET /health must return 200 with status 'healthy'."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_health_endpoint_contains_environment(client):
    """GET /health must include the current environment name."""
    response = client.get("/health")
    data = response.json()
    assert "environment" in data
    assert isinstance(data["environment"], str)
    assert len(data["environment"]) > 0
