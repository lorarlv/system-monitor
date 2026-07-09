import time

from .storage import init_storage, save_metrics, trim_log
from rich.live import Live

from .display import create_metrics_table
from .monitor import get_system_metrics

def main():
    init_storage()
    
    with Live(refresh_per_second=4) as live:
        while True:
            metrics = get_system_metrics()
            save_metrics(metrics)
            table = create_metrics_table(metrics)
            live.update(table)
            time.sleep(1)


if __name__ == "__main__":
    main()