from dataclasses import dataclass
from datetime import datetime

import psutil

def get_cpu_usage() -> float:
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent()

def get_memory_usage() -> float:
    """Returns the current memory usage as a percentage."""
    return psutil.virtual_memory().percent

def get_disk_usage() -> float:
    """Returns the current disk usage as a percentage."""
    return psutil.disk_usage('/').percent

@dataclass
class SystemMetrics:
    timestamp: datetime
    cpu: float
    memory: float
    disk: float

def get_system_metrics() -> SystemMetrics:
    """Returns all current system metrics."""
    return SystemMetrics(
        timestamp=datetime.now(),
        cpu=get_cpu_usage(),
        memory=get_memory_usage(),
        disk=get_disk_usage(),
    )
