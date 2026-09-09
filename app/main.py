import os
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

APP_NAME = os.getenv("APP_NAME", "Factory API")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "dev")

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
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{APP_NAME}</title><style>
body{{font-family:system-ui;background:#081525;color:#eef6ff;display:grid;place-items:center;min-height:100vh;margin:0}}
main{{max-width:720px;padding:3rem}}p{{color:#adc4d8;font-size:1.2rem}}code{{color:#4ee1a0}}
</style></head><body><main><p>ClassLab · Usine logicielle</p><h1>{APP_NAME}</h1>
<p>Déploiement <code>{APP_ENV}</code> · version <code>{APP_VERSION}</code></p>
<p><a href="/docs" style="color:#58b9ff">Documentation de l'API</a></p></main></body></html>"""


@app.get("/api/v1/info")
def info() -> dict[str, str]:
    return {"name": APP_NAME, "environment": APP_ENV, "version": APP_VERSION}


@app.get("/health/live", include_in_schema=False)
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", include_in_schema=False)
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
