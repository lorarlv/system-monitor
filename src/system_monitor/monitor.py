import time
from dataclasses import dataclass
from datetime import datetime

import psutil

from .hardware import get_cpu_temperature

_last_net = psutil.net_io_counters()
_last_net_time = time.time()

def get_cpu_usage() -> float:
    """returns the current CPU usage as a percentage"""
    return psutil.cpu_percent()

def get_memory_usage() -> float:
    """returns the current memory usage as a percentage"""
    return psutil.virtual_memory().percent

def get_disk_usage() -> float:
    """returns the current disk usage as a percentage"""
    return psutil.disk_usage('C:\\').percent

def get_network_usage() -> tuple[float, float]:
    global _last_net, _last_net_time

    current = psutil.net_io_counters()
    current_time = time.time()

    elapsed = current_time - _last_net_time

    if elapsed <= 0:
        return 0.0, 0.0

    download_rate = (current.bytes_recv - _last_net.bytes_recv) / elapsed
    upload_rate = (current.bytes_sent - _last_net.bytes_sent) / elapsed

    _last_net = current
    _last_net_time = current_time

    return download_rate, upload_rate

@dataclass
class SystemMetrics:
    timestamp: datetime
    cpu: float
    cpu_temperature: float | None
    memory: float
    disk: float
    download_rate: float
    upload_rate: float

def get_system_metrics() -> SystemMetrics:
    download_rate, upload_rate = get_network_usage()

    return SystemMetrics(
        timestamp=datetime.now(),
        cpu=get_cpu_usage(),
        cpu_temperature=get_cpu_temperature(),
        memory=get_memory_usage(),
        disk=get_disk_usage(),
        download_rate=download_rate,
        upload_rate=upload_rate,
    )
