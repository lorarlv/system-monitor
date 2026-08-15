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
    download_mb: float
    upload_mb: float


app = FastAPI(
    title="System Monitor API",
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/metrics/current", response_model=MetricsResponse)
def current_metrics() -> MetricsResponse:
    metrics = get_system_metrics()

    import psutil
    network = psutil.net_io_counters()

    return MetricsResponse(
        timestamp=metrics.timestamp,
        cpu_percent=metrics.cpu,
        memory_percent=metrics.memory,
        disk_percent=metrics.disk,
        download_mb=round(network.bytes_recv / (1024 * 1024), 2),
        upload_mb=round(network.bytes_sent / (1024 * 1024), 2),
    )

@app.get("/metrics/recent")
def recent_metrics(limit: int = 5):
    return get_recent_metrics(limit)

@app.get("/metrics/summary")
def metrics_summary():
    return get_history_summary()