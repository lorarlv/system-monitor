import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .monitor import SystemMetrics, get_system_metrics
from .storage import (
    get_history_summary,
    get_metrics_since,
    get_recent_metrics,
    init_storage,
    save_metrics,
    trim_history,
)


class MetricsResponse(BaseModel):
    timestamp: datetime
    cpu_percent: float
    cpu_temperature: float | None
    memory_percent: float
    disk_percent: float
    download_rate: float
    upload_rate: float


def metrics_to_response(metrics: SystemMetrics) -> MetricsResponse:
    return MetricsResponse(
        timestamp=metrics.timestamp,
        cpu_percent=metrics.cpu,
        cpu_temperature=metrics.cpu_temperature,
        memory_percent=metrics.memory,
        disk_percent=metrics.disk,
        download_rate=metrics.download_rate,
        upload_rate=metrics.upload_rate,
    )


latest_metrics: SystemMetrics | None = None


async def sample_metrics() -> None:
    global latest_metrics

    while True:
        metrics = await asyncio.to_thread(get_system_metrics)

        latest_metrics = metrics

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