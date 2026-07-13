import csv
import os

from datetime import datetime, timedelta
from .monitor import SystemMetrics

LOG_FILE = "data/monitor_log.csv"

def init_storage() -> None:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "cpu", "memory", "disk"])
            writer.writeheader()

def save_metrics(metrics: SystemMetrics) -> None:
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "cpu", "memory", "disk"])
        writer.writerow({
            "timestamp": metrics.timestamp.isoformat(),
            "cpu": metrics.cpu,
            "memory": metrics.memory,
            "disk": metrics.disk,
        })

def trim_log() -> None:
    cutoff = datetime.now() - timedelta(hours=24)
    with open(LOG_FILE, "r") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if datetime.fromisoformat(r["timestamp"]) > cutoff]
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "cpu", "memory", "disk"])
        writer.writeheader()
        writer.writerows(rows)
    
def load_metrics() -> list[dict[str,str]]:
    with open(LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
def get_history_summary() -> dict[str, float]:
    rows = load_metrics()

    if not rows:
        return {
            "avg_cpu": 0.0,
            "avg_memory": 0.0,
            "avg_disk": 0.0,
        }
    
    return {
        "avg_cpu": sum(float(row["cpu"]) for row in rows) / len(rows),
        "avg_memory": sum(float(row["memory"]) for row in rows) / len(rows),
        "avg_disk": sum(float(row["disk"]) for row in rows) / len(rows),
    }

def get_recent_metrics(limit: int = 5) -> list[dict[str, str]]:
    rows = load_metrics()
    return rows[-limit:]