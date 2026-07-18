import argparse
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

def run_monitor(interval: float) -> None:
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
            time.sleep(interval)

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="system-monitor",
        description="Monitor system resource usage"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )
    
    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Run the live system monitor",
    )

    monitor_parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between metric samples. Default: 1",
    )

    subparsers.add_parser(
        "summary",
        help="Display historical metrics averages",
    )
    
    recent_parser = subparsers.add_parser(
        "recent",
        help="Display recent metric samples",
    )

    recent_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of recent samples to display. Default: 5"
    )

    return parser

def show_summary() -> None:
    init_storage()
    summary = get_history_summary()

    print(f"Average CPU: {summary['avg_cpu']:.1f}%")
    print(f"Average RAM: {summary['avg_memory']:.1f}%")
    print(f"Average Disk: {summary['avg_disk']:.1f}%")

def show_recent(limit: int) -> None:
    init_storage()
    recent_metrics = get_recent_metrics(limit)

    for metric in recent_metrics:
        print(
            f"{metric.timestamp:%Y-%m-%d %H:%M:%S} | "
            f"CPU {metric.cpu:.1f}% | "
            f"RAM {metric.memory:.1f}% | "
            f"Disk {metric.disk:.1f}%"
        )

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "monitor":
        run_monitor(args.interval)
    elif args.command == "summary":
        show_summary()
    elif args.command == "recent":
        show_recent(args.limit)

if __name__ == "__main__":
    main()