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
            memory REAL NOT NULL,
            disk REAL NOT NULL
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
            INSERT INTO metrics (timestamp, cpu, memory, disk)
            VALUES (?, ?, ?, ?)
            """,
        (
            metrics.timestamp.isoformat(),
            metrics.cpu,
            metrics.memory,
            metrics.disk,
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
                AVG(memory),
                AVG(disk)
            FROM metrics
            """
        ).fetchone()

    if row is None or row[0] is None:
        return {
            "avg_cpu": 0.0,
            "avg_memory": 0.0,
            "avg_disk": 0.0,
        }
    
    return {
        "avg_cpu": float(row[0]),
        "avg_memory": float(row[1]),
        "avg_disk": float(row[2]),
    }

def get_recent_metrics(limit: int = 5) -> list[SystemMetrics]:
    with sqlite3.connect(DB_FILE) as connection:
        rows = connection.execute(
            """
            SELECT timestamp, cpu, memory, disk
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
            memory=memory,
            disk=disk,
        )
        for timestamp, cpu, memory, disk in reversed(rows)
    ]