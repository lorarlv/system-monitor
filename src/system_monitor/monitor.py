import time
from dataclasses import dataclass
from datetime import datetime

import psutil

from .hardware import (
    get_cpu_temperature,
    get_gpu_metrics,
    get_hardware_sensors,
)

_last_net = psutil.net_io_counters()
_last_net_time = time.time()

@dataclass
class HardwareMetrics:
    cpu_temperature: float | None = None
    gpu_usage: float | None = None
    gpu_temperature: float | None = None
    gpu_memory_used: float | None = None
    gpu_memory_total: float | None = None

_latest_hardware = HardwareMetrics()

def get_cpu_usage() -> float:
    return psutil.cpu_percent()

def get_memory_usage() -> float:
    return psutil.virtual_memory().percent

def get_disk_usage() -> float:
    return psutil.disk_usage("C:\\").percent

def get_network_usage() -> tuple[float, float]:
    global _last_net, _last_net_time

    current = psutil.net_io_counters()
    current_time = time.time()

    elapsed = current_time - _last_net_time

    if elapsed <= 0:
        return 0.0, 0.0

    download_rate = (
        current.bytes_recv - _last_net.bytes_recv
    ) / elapsed

    upload_rate = (
        current.bytes_sent - _last_net.bytes_sent
    ) / elapsed

    _last_net = current
    _last_net_time = current_time

    return download_rate, upload_rate

def update_hardware_metrics() -> None:
    global _latest_hardware

    sensors = get_hardware_sensors()

    cpu_temperature = get_cpu_temperature(
        sensors
    )

    (
        gpu_usage,
        gpu_temperature,
        gpu_memory_used,
        gpu_memory_total,
    ) = get_gpu_metrics(sensors)

    _latest_hardware = HardwareMetrics(
        cpu_temperature=cpu_temperature,
        gpu_usage=gpu_usage,
        gpu_temperature=gpu_temperature,
        gpu_memory_used=gpu_memory_used,
        gpu_memory_total=gpu_memory_total,
    )

@dataclass
class SystemMetrics:
    timestamp: datetime

    cpu: float
    cpu_temperature: float | None

    memory: float
    disk: float

    gpu_usage: float | None
    gpu_temperature: float | None
    gpu_memory_used: float | None
    gpu_memory_total: float | None

    download_rate: float
    upload_rate: float

def get_system_metrics() -> SystemMetrics:
    download_rate, upload_rate = (
        get_network_usage()
    )

    return SystemMetrics(
        timestamp=datetime.now(),

        cpu=get_cpu_usage(),
        cpu_temperature=(
            _latest_hardware.cpu_temperature
        ),

        memory=get_memory_usage(),
        disk=get_disk_usage(),

        gpu_usage=_latest_hardware.gpu_usage,
        gpu_temperature=(
            _latest_hardware.gpu_temperature
        ),
        gpu_memory_used=(
            _latest_hardware.gpu_memory_used
        ),
        gpu_memory_total=(
            _latest_hardware.gpu_memory_total
        ),

        download_rate=download_rate,
        upload_rate=upload_rate,
    )