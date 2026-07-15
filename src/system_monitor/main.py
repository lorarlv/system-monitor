import time

from .storage import init_storage, save_metrics, get_history_summary
from rich.live import Live

from .alerts import AlertState, AlertStatus, update_alert
from .display import create_metrics_table
from .monitor import get_system_metrics
from .storage import (
    get_history_summary,
    get_recent_metrics,
    init_storage,
    save_metrics,
    trim_history
)

def main() -> None:
    init_storage()
    trim_history()

    cpu_alert = AlertState()
    ram_alert = AlertState()
    disk_alert = AlertState()


    with Live(refresh_per_second=4) as live:
        while True:
            metrics = get_system_metrics()
            save_metrics(metrics)
            summary = get_history_summary()
            recent_metrics = get_recent_metrics()
            alerts = AlertStatus(
                cpu = update_alert(metrics.cpu, 80.0, cpu_alert),
                ram = update_alert(metrics.memory, 90.0, ram_alert),
                disk = update_alert(metrics.disk, 90.0, disk_alert)
            )
            dashboard = create_metrics_table(metrics, summary, recent_metrics, alerts)
            live.update(dashboard)
            time.sleep(1)


if __name__ == "__main__":
    main()