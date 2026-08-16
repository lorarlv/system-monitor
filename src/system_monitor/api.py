from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from .monitor import get_system_metrics
from .storage import get_recent_metrics, get_history_summary

class MetricsResponse(BaseModel):
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    download_rate: float
    upload_rate: float


app = FastAPI(
    title="System Monitor API",
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/metrics/current", response_model=MetricsResponse)
def current_metrics() -> MetricsResponse:
    metrics = get_system_metrics()

    return MetricsResponse(
        timestamp=metrics.timestamp,
        cpu_percent=metrics.cpu,
        memory_percent=metrics.memory,
        disk_percent=metrics.disk,
        download_rate=metrics.download_rate,
        upload_rate=metrics.upload_rate,
    )

@app.get("/metrics/recent")
def recent_metrics(limit: int = 5):
    return get_recent_metrics(limit)

@app.get("/metrics/summary")
def metrics_summary():
    return get_history_summary()