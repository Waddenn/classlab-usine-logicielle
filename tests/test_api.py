from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_is_available() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Factory API" in response.text
    assert response.headers["X-App-Version"] == "dev"


def test_info_exposes_deployment_metadata() -> None:
    assert client.get("/api/v1/info").json() == {
        "name": "Factory API",
        "environment": "development",
        "version": "dev",
    }


def test_health_checks() -> None:
    assert client.get("/health/live").json() == {"status": "ok"}
    assert client.get("/health/ready").json() == {"status": "ready"}


def test_metrics_are_prometheus_compatible() -> None:
    client.get("/api/v1/info")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "factory_http_requests_total" in response.text
    assert "factory_http_request_duration_seconds" in response.text
