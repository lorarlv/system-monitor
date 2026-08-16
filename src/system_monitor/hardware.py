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

if __name__ == "__main__":
    print_cpu_sensors()

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