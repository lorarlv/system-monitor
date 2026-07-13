import time

from .storage import init_storage, save_metrics, get_history_summary
from rich.live import Live

from .display import create_metrics_table
from .monitor import get_system_metrics
from .storage import (
    get_history_summary,
    get_recent_metrics,
    init_storage,
    save_metrics,
    trim_history
)

def main():
    init_storage()
    trim_history()

    with Live(refresh_per_second=4) as live:
        while True:
            metrics = get_system_metrics()
            save_metrics(metrics)
            summary = get_history_summary()
            recent_metrics = get_recent_metrics()
            table = create_metrics_table(metrics, summary, recent_metrics)
            live.update(table)
            time.sleep(1)


if __name__ == "__main__":
    main()