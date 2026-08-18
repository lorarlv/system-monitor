import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .alerts import AlertState, AlertStatus, update_alert
from .monitor import SystemMetrics, get_system_metrics
from .paths import resource_path
from .storage import (
    get_history_summary,
    get_metrics_since,
    get_recent_metrics,
    init_storage,
    save_metrics,
    trim_history,
)

FRONTEND_DIST = resource_path(
    "frontend",
    "dist",
)

class MetricsResponse(BaseModel):
    timestamp: datetime
    cpu_percent: float
    cpu_temperature: float | None
    memory_percent: float
    disk_percent: float
    download_rate: float
    upload_rate: float

    gpu_usage: float | None
    gpu_temperature: float | None
    gpu_memory_used: float | None
    gpu_memory_total: float | None

class AlertsResponse(BaseModel):
    cpu: bool
    temperature: bool
    ram: bool
    disk: bool

def metrics_to_response(metrics: SystemMetrics) -> MetricsResponse:
    return MetricsResponse(
        timestamp=metrics.timestamp,
        cpu_percent=metrics.cpu,
        cpu_temperature=metrics.cpu_temperature,
        memory_percent=metrics.memory,
        disk_percent=metrics.disk,
        download_rate=metrics.download_rate,
        upload_rate=metrics.upload_rate,
        gpu_usage=metrics.gpu_usage,
        gpu_temperature=metrics.gpu_temperature,
        gpu_memory_used=metrics.gpu_memory_used,
        gpu_memory_total=metrics.gpu_memory_total,
    )


latest_metrics: SystemMetrics | None = None

latest_alerts = AlertStatus(
    cpu=False,
    temperature=False,
    ram=False,
    disk=False,
)

cpu_alert = AlertState()
temperature_alert = AlertState()
ram_alert = AlertState()
disk_alert = AlertState()

async def sample_metrics() -> None:
    global latest_metrics, latest_alerts

    while True:
        metrics = await asyncio.to_thread(get_system_metrics)

        latest_metrics = metrics

        temperature_is_alerting  = False

        if metrics.cpu_temperature is not None:
            temperature_is_alerting = update_alert(
                metrics.cpu_temperature,
                90.0,
                temperature_alert,
            )

        latest_alerts = AlertStatus(
            cpu=update_alert(
                metrics.cpu,
                80.0,
                cpu_alert,
            ),
            temperature=temperature_is_alerting,
            ram=update_alert(
                metrics.memory,
                90.0,
                ram_alert,
            ),
            disk=update_alert(
                metrics.disk,
                90.0,
                disk_alert,
            ),
        )

        await asyncio.to_thread(save_metrics, metrics)

        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_storage()
    trim_history()

    sampler_task = asyncio.create_task(sample_metrics())

    try:
        yield
    finally:
        sampler_task.cancel()

        try:
            await sampler_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="System Monitor API",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/metrics/current",
    response_model=MetricsResponse,
)
def current_metrics() -> MetricsResponse:
    if latest_metrics is None:
        metrics = get_system_metrics()
        return metrics_to_response(metrics)

    return metrics_to_response(latest_metrics)


@app.get(
    "/metrics/recent",
    response_model=list[MetricsResponse],
)
def recent_metrics(limit: int = 60) -> list[MetricsResponse]:
    metrics = get_recent_metrics(limit)

    return [
        metrics_to_response(metric)
        for metric in metrics
    ]


@app.get(
    "/metrics/history",
    response_model=list[MetricsResponse],
)
def metrics_history(minutes: int = 5) -> list[MetricsResponse]:
    metrics = get_metrics_since(minutes)

    return [
        metrics_to_response(metric)
        for metric in metrics
    ]


@app.get("/metrics/summary")
def metrics_summary() -> dict[str, float]:
    return get_history_summary()

@app.get(
    "/alerts",
    response_model=AlertsResponse,
)
def active_alerts() -> AlertsResponse:
    return AlertsResponse(
        cpu=latest_alerts.cpu,
        temperature=latest_alerts.temperature,
        ram=latest_alerts.ram,
        disk=latest_alerts.disk,
    )

if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(
            directory=FRONTEND_DIST / "assets"
        ),
        name="assets",
    )

@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    index_file = FRONTEND_DIST / "index.html"

    if not index_file.exists():
        return {
            "error": "Frontend build not found"
        }

    return FileResponse(index_file)