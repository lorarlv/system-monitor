import time

from rich.live import Live

from .display import create_metrics_table
from .monitor import get_system_metrics

def main():
    with Live(refresh_per_second=4) as live:
        while True:
            metrics = get_system_metrics()
            table = create_metrics_table(metrics)
            live.update(table)
            time.sleep(1)


if __name__ == "__main__":
    main()