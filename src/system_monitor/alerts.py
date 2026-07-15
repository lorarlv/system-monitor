from dataclasses import dataclass

@dataclass
class AlertState:
    consecutive_high: int = 0
    active: bool = False

@dataclass
class AlertStatus:
    cpu: bool
    ram: bool
    disk: bool

CPU_THRESHOLD = 80.0
RAM_THRESHOLD = 90.0
DISK_THRESHOLD = 90.0

REQUIRED_SAMPLES = 5

def update_alert(
        value: float,
        threshold: float,
        state: AlertState,
) -> bool:
    if value >= threshold:
        state.consecutive_high += 1
    else:
        state.consecutive_high = 0
        state.active = False

    if state.consecutive_high >= REQUIRED_SAMPLES:
        state.active = True

    return state.active