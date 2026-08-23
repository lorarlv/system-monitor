import atexit
import json
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from .paths import resource_path

HELPER_PATH = resource_path(
    "vendor",
    "HardwareHelper",
    "HardwareHelper.exe",
)

GPU_TYPES = {
    "GpuNvidia",
    "GpuAmd",
    "GpuIntel",
}

_helper_process: subprocess.Popen[str] | None = None
_helper_lock = threading.Lock()

def _start_helper() -> subprocess.Popen[str]:
    global _helper_process

    if (
        _helper_process is not None
        and _helper_process.poll() is None
    ):
        return _helper_process

    creation_flags = 0

    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW

    _helper_process = subprocess.Popen(
        [str(HELPER_PATH)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        creationflags=creation_flags,
    )

    return _helper_process

def _stop_helper() -> None:
    global _helper_process

    process = _helper_process

    if process is None:
        return

    try:
        if (
            process.poll() is None
            and process.stdin is not None
        ):
            process.stdin.write("quit\n")
            process.stdin.flush()

            process.wait(timeout=2)

    except Exception:
        try:
            process.kill()
        except Exception:
            pass

    finally:
        _helper_process = None

def _read_sensors() -> list[dict[str, Any]]:
    with _helper_lock:
        process = _start_helper()

        if (
            process.stdin is None
            or process.stdout is None
        ):
            return []

        try:
            process.stdin.write("read\n")
            process.stdin.flush()

            line = process.stdout.readline()

            if not line:
                _stop_helper()
                return []

            data = json.loads(line)

            if not isinstance(data, list):
                return []

            return data

        except (
            BrokenPipeError,
            OSError,
            json.JSONDecodeError,
        ) as exc:
            print(
                f"Hardware helper failed: {exc}",
                file=sys.stderr,
            )

            _stop_helper()

            return []

def get_hardware_sensors() -> list[dict[str, Any]]:
    return _read_sensors()

def print_cpu_sensors() -> None:
    sensors = get_hardware_sensors()

    for sensor in sensors:
        if sensor.get("hardwareType") != "Cpu":
            continue

        print(
            f"{sensor.get('hardware')} | "
            f"{sensor.get('name')} | "
            f"{sensor.get('type')} | "
            f"Value={sensor.get('value')}"
        )

def get_cpu_temperature(
    sensors: list[dict[str, Any]],
) -> float | None:
    cpu_temperatures: list[tuple[str, float]] = []

    for sensor in sensors:
        if sensor.get("hardwareType") != "Cpu":
            continue

        if sensor.get("type") != "Temperature":
            continue

        value = sensor.get("value")

        if value is None:
            continue

        name = str(sensor.get("name", ""))

        cpu_temperatures.append(
            (
                name,
                float(value),
            )
        )

    if not cpu_temperatures:
        return None

    preferred_names = [
        "CPU Package",
        "CPU Core Max",
        "Core Max",
        "CPU Core",
        "Tctl/Tdie",
        "Tdie",
    ]

    for preferred_name in preferred_names:
        for name, value in cpu_temperatures:
            if (
                preferred_name.lower()
                in name.lower()
            ):
                return value

    return max(
        value
        for _, value in cpu_temperatures
    )

def print_gpu_sensors() -> None:
    sensors = get_hardware_sensors()

    for sensor in sensors:
        if sensor.get("hardwareType") not in GPU_TYPES:
            continue

        print(
            f"{sensor.get('hardware')} | "
            f"{sensor.get('name')} | "
            f"{sensor.get('type')} | "
            f"Value={sensor.get('value')}"
        )

def _find_nvidia_smi() -> str | None:
    path = shutil.which("nvidia-smi")

    if path is not None:
        return path

    common_paths = [
        Path(
            r"C:\Program Files\NVIDIA Corporation"
            r"\NVSMI\nvidia-smi.exe"
        ),
        Path(
            r"C:\Windows\System32\nvidia-smi.exe"
        ),
    ]

    for candidate in common_paths:
        if candidate.exists():
            return str(candidate)

    return None

def get_nvidia_metrics() -> tuple[
    float | None,
    float | None,
    float | None,
    float | None,
]:
    nvidia_smi = _find_nvidia_smi()

    if nvidia_smi is None:
        return (
            None,
            None,
            None,
            None,
        )

    creation_flags = 0

    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW

    try:
        result = subprocess.run(
            [
                nvidia_smi,
                "--query-gpu="
                "utilization.gpu,"
                "temperature.gpu,"
                "memory.used,"
                "memory.total",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=3,
            creationflags=creation_flags,
        )

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        return (
            None,
            None,
            None,
            None,
        )

    lines = result.stdout.strip().splitlines()

    if not lines:
        return (
            None,
            None,
            None,
            None,
        )

    try:
        values = [
            value.strip()
            for value in lines[0].split(",")
        ]

        if len(values) < 4:
            return (
                None,
                None,
                None,
                None,
            )

        gpu_usage = float(values[0])
        gpu_temperature = float(values[1])
        gpu_memory_used = float(values[2])
        gpu_memory_total = float(values[3])

        return (
            gpu_usage,
            gpu_temperature,
            gpu_memory_used,
            gpu_memory_total,
        )

    except (
        ValueError,
        IndexError,
    ):
        return (
            None,
            None,
            None,
            None,
        )

def get_gpu_metrics(
    sensors: list[dict[str, Any]],
) -> tuple[
    float | None,
    float | None,
    float | None,
    float | None,
]:
    gpu_usage = None
    gpu_temperature = None
    gpu_memory_used = None
    gpu_memory_total = None

    usage_names = {
        "D3D 3D",
        "GPU Core",
        "GPU Total",
        "GPU Load",
    }

    memory_used_names = {
        "D3D Shared Memory Used",
        "GPU Memory Used",
        "GPU Memory",
    }

    memory_total_names = {
        "D3D Shared Memory Total",
        "GPU Memory Total",
    }

    for sensor in sensors:
        if sensor.get("hardwareType") not in GPU_TYPES:
            continue

        name = str(sensor.get("name", ""))
        sensor_type = str(sensor.get("type", ""))
        value = sensor.get("value")

        if value is None:
            continue

        if (
            sensor_type == "Load"
            and name in usage_names
        ):
            if gpu_usage is None:
                gpu_usage = float(value)
            else:
                gpu_usage = max(
                    gpu_usage,
                    float(value),
                )

        elif (
            sensor_type == "Temperature"
            and gpu_temperature is None
        ):
            gpu_temperature = float(value)

        elif name in memory_used_names:
            gpu_memory_used = float(value)

        elif name in memory_total_names:
            gpu_memory_total = float(value)

    (
        nvidia_usage,
        nvidia_temperature,
        nvidia_memory_used,
        nvidia_memory_total,
    ) = get_nvidia_metrics()

    if nvidia_usage is not None:
        gpu_usage = nvidia_usage

    if nvidia_temperature is not None:
        gpu_temperature = nvidia_temperature

    if nvidia_memory_used is not None:
        gpu_memory_used = nvidia_memory_used

    if nvidia_memory_total is not None:
        gpu_memory_total = nvidia_memory_total

    return (
        gpu_usage,
        gpu_temperature,
        gpu_memory_used,
        gpu_memory_total,
    )

atexit.register(_stop_helper)

if __name__ == "__main__":
    print_gpu_sensors()