import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

from .monitor import SystemMetrics

DATA_DIR = Path("data")
DB_FILE = DATA_DIR / "metrics.db"

def init_storage() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu REAL NOT NULL,
            cpu_temperature REAL,
            memory REAL NOT NULL,
            disk REAL NOT NULL,
            gpu_usage REAL,
            gpu_temperature REAL,
            gpu_memory_used REAL,
            gpu_memory_total REAL,
            download_rate REAL NOT NULL,
            upload_rate REAL NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_metrics_timestamp
            ON metrics(timestamp)
            """
        )

def save_metrics(metrics: SystemMetrics) -> None:
    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            INSERT INTO metrics (
                timestamp, 
                cpu,
                cpu_temperature,
                memory,
                disk,
                gpu_usage,
                gpu_temperature,
                gpu_memory_used,
                gpu_memory_total,
                download_rate,
                upload_rate
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
        (
            metrics.timestamp.isoformat(),
            metrics.cpu,
            metrics.cpu_temperature,
            metrics.memory,
            metrics.disk,
            metrics.gpu_usage,
            metrics.gpu_temperature,
            metrics.gpu_memory_used,
            metrics.gpu_memory_total,
            metrics.download_rate,
            metrics.upload_rate,
        ),
    )

def trim_history(hours: int = 24) -> None:
    cutoff = datetime.now() - timedelta(hours=hours)

    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            DELETE FROM metrics
            WHERE timestamp < ?
            """,
            (cutoff.isoformat(),),
        )

def get_history_summary() -> dict[str, float]:
    with sqlite3.connect(DB_FILE) as connection:
        row = connection.execute(
            """
            SELECT
                AVG(cpu),
                AVG(cpu_temperature),
                AVG(memory),
                AVG(disk)
            FROM metrics
            """
        ).fetchone()

    if row is None or row[0] is None:
        return {
            "avg_cpu": 0.0,
            "avg_cpu_temperature": 0.0,
            "avg_memory": 0.0,
            "avg_disk": 0.0,
        }
    
    return {
        "avg_cpu": float(row[0]),
        "avg_cpu_temperature": float(row[1]) if row[1] is not None else 0.0,
        "avg_memory": float(row[2]),
        "avg_disk": float(row[3]),
    }

def get_metrics_since(minutes: int = 5) -> list[SystemMetrics]:
    cutoff = datetime.now() - timedelta(minutes=minutes)

    with sqlite3.connect(DB_FILE) as connection:
        rows = connection.execute(
            """
            SELECT
                timestamp,
                cpu,
                cpu_temperature,
                memory,
                disk,
                gpu_usage,
                gpu_temperature,
                gpu_memory_used,
                gpu_memory_total,
                download_rate,
                upload_rate
            FROM metrics
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
            """,
            (cutoff.isoformat(),),
        ).fetchall()

    return [
        SystemMetrics(
            timestamp=datetime.fromisoformat(timestamp),
            cpu=cpu,
            cpu_temperature=cpu_temperature,
            memory=memory,
            disk=disk,
            gpu_usage=gpu_usage,
            gpu_temperature=gpu_temperature,
            gpu_memory_used=gpu_memory_used,
            gpu_memory_total=gpu_memory_total,
            download_rate=download_rate,
            upload_rate=upload_rate,
        )
        for (
            timestamp,
            cpu,
            cpu_temperature,
            memory,
            disk,
            gpu_usage,
            gpu_temperature,
            gpu_memory_used,
            gpu_memory_total,
            download_rate,
            upload_rate,
        ) in rows
    ]

def get_recent_metrics(limit: int = 5) -> list[SystemMetrics]:
    with sqlite3.connect(DB_FILE) as connection:
        rows = connection.execute(
            """
            SELECT timestamp, cpu, cpu_temperature, memory, disk, gpu_usage, gpu_temperature, gpu_memory_used, gpu_memory_total, download_rate, upload_rate
            FROM metrics
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        SystemMetrics(
            timestamp=datetime.fromisoformat(timestamp),
            cpu=cpu,
            cpu_temperature=cpu_temperature,
            memory=memory,
            disk=disk,
            gpu_usage=gpu_usage,
            gpu_temperature=gpu_temperature,
            gpu_memory_used=gpu_memory_used,
            gpu_memory_total=gpu_memory_total,
            download_rate=download_rate,
            upload_rate=upload_rate,
        )
        for timestamp, cpu, cpu_temperature, memory, disk, gpu_usage, gpu_temperature, gpu_memory_used, gpu_memory_total, download_rate, upload_rate in reversed(rows)
    ]