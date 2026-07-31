from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from system_monitor.monitor import get_system_metrics

class MetricsResponse(BaseModel):
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float


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
    )