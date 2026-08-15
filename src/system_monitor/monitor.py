import time
from dataclasses import dataclass
from datetime import datetime

import psutil

_last_net = psutil.net_io_counters()
_last_net_time = time.time()

def get_cpu_usage() -> float:
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent()

def get_memory_usage() -> float:
    """Returns the current memory usage as a percentage."""
    return psutil.virtual_memory().percent

def get_disk_usage() -> float:
    """Returns the current disk usage as a percentage."""
    return psutil.disk_usage('/').percent

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
    memory: float
    disk: float
    download_rate: float
    upload_rate: float

def get_system_metrics() -> SystemMetrics:
    download_rate, upload_rate = get_network_usage()

    return SystemMetrics(
        timestamp=datetime.now(),
        cpu=get_cpu_usage(),
        memory=get_memory_usage(),
        disk=get_disk_usage(),
        download_rate=download_rate,
        upload_rate=upload_rate,
    )
