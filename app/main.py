import os
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

APP_NAME = os.getenv("APP_NAME", "Factory API")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "dev")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://prometheus:9090")
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://grafana:3000")
APP_STARTED = time.monotonic()
STATIC_DIR = Path(__file__).parent / "static"
INDEX_HTML = (STATIC_DIR / "index.html").read_text(encoding="utf-8")

REQUESTS = Counter(
    "factory_http_requests_total",
    "Nombre total de requêtes HTTP",
    ("method", "path", "status"),
)
LATENCY = Histogram(
    "factory_http_request_duration_seconds",
    "Durée des requêtes HTTP",
    ("method", "path"),
)
DEMO_RUNS = Counter(
    "factory_demo_runs_total",
    "Nombre de démonstrations lancées depuis l'interface",
)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Application témoin de l'usine logicielle ClassLab.",
)


@app.middleware("http")
async def observe_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    REQUESTS.labels(request.method, path, str(response.status_code)).inc()
    LATENCY.labels(request.method, path).observe(time.perf_counter() - start)
    response.headers["X-App-Version"] = APP_VERSION
    return response


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    return INDEX_HTML


@app.get("/api/v1/info")
def info() -> dict[str, str]:
    return {"name": APP_NAME, "environment": APP_ENV, "version": APP_VERSION}


def _probe(url: str, path: str) -> str:
    try:
        with urlopen(f"{url}{path}", timeout=0.5) as response:  # noqa: S310
            return "up" if response.status < 400 else "down"
    except (OSError, URLError):
        return "down"


@app.get("/api/v1/demo/status")
def demo_status() -> dict[str, object]:
    return {
        "environment": APP_ENV,
        "version": APP_VERSION,
        "uptime_seconds": round(time.monotonic() - APP_STARTED),
        "services": {
            "api": "up",
            "prometheus": _probe(PROMETHEUS_URL, "/-/ready"),
            "grafana": _probe(GRAFANA_URL, "/api/health"),
        },
    }


@app.post("/api/v1/demo/run")
def demo_run() -> dict[str, str]:
    DEMO_RUNS.inc()
    return {"status": "started", "mode": "local-simulation", "version": APP_VERSION}


@app.get("/api/v1/demo/error", include_in_schema=False)
def demo_error() -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"status": "controlled-error", "detail": "Erreur volontaire de démonstration"},
    )


@app.get("/health/live", include_in_schema=False)
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", include_in_schema=False)
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
