from pathlib import Path
import sys

import clr

LIB_DIR = (
    Path(__file__).resolve().parents[2]
    / "vendor"
    / "LibreHardwareMonitor"
)

sys.path.append(str(LIB_DIR))

clr.AddReference("LibreHardwareMonitorLib")

from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType

computer = Computer()

computer.IsCpuEnabled = True
computer.IsGpuEnabled = True
computer.Open()

def print_cpu_sensors() -> None:
    for hardware in computer.Hardware:
        hardware.Update()
        print(hardware.Name)

        for sub in hardware.SubHardware:
            sub.Update()
            print(f" Sub: {sub.Name}")

        if hardware.HardwareType == HardwareType.Cpu:
            print(f"CPU: {hardware.Name}")

            for sensor in hardware.Sensors:
                print(
                    f"{sensor.Name} | "
                    f"{sensor.SensorType} | "
                    f"Value={sensor.Value} | "
                    f"Min={sensor.Min} | "
                    f"Max={sensor.Max}"
                )

def get_cpu_temperature() -> float | None:
    for hardware in computer.Hardware:
        hardware.Update()

        if hardware.HardwareType != HardwareType.Cpu:
            continue

        for sensor in hardware.Sensors:
            if (
                sensor.SensorType == SensorType.Temperature
                and sensor.Name == "CPU Package"
                and sensor.Value is not None
            ):
                return float(sensor.Value)

    return None

def print_gpu_sensors() -> None:
    for hardware in computer.Hardware:
        hardware.Update()

        if hardware.HardwareType in (
            HardwareType.GpuNvidia,
            HardwareType.GpuAmd,
            HardwareType.GpuIntel,
        ):
            print(f"GPU: {hardware.Name}")

            for sensor in hardware.Sensors:
                print(
                    f"{sensor.Name} | "
                    f"{sensor.SensorType} | "
                    f"Value={sensor.Value}"
                )

            for sub in hardware.SubHardware:
                sub.Update()

                for sensor in sub.Sensors:
                    print(
                        f"Sub: {sensor.Name} | "
                        f"{sensor.SensorType} | "
                        f"Value={sensor.Value}"
                    )

if __name__ == "__main__":
    print_gpu_sensors()

def get_gpu_metrics() -> tuple[
    float | None,
    float | None,
    float | None,
    float | None,
]:
    gpu_usage = None
    gpu_temperature = None
    gpu_memory_used = None
    gpu_memory_total = None

    for hardware in computer.Hardware:
        hardware.Update()

        if hardware.HardwareType not in (
            HardwareType.GpuNvidia,
            HardwareType.GpuAmd,
            HardwareType.GpuIntel,
        ):
            continue

        for sensor in hardware.Sensors:
            if (
                sensor.SensorType == SensorType.Load
                and sensor.Name == "D3D 3D"
                and sensor.Value is not None
            ):
                gpu_usage = float(sensor.Value)

            elif (
                sensor.SensorType == SensorType.Temperature
                and sensor.Value is not None
            ):
                gpu_temperature = float(sensor.Value)

            elif (
                sensor.Name == "D3D Shared Memory Used"
                and sensor.Value is not None
            ):
                gpu_memory_used = float(sensor.Value)

            elif (
                sensor.Name == "D3D Shared Memory Total"
                and sensor.Value is not None
            ):
                gpu_memory_total = float(sensor.Value)

        return (
            gpu_usage,
            gpu_temperature,
            gpu_memory_used,
            gpu_memory_total,
        )