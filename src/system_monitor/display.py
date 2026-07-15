from rich.table import Table
from rich.console import Group
from rich.text import Text
from rich.align import Align
from rich import box

from datetime import datetime

from .monitor import SystemMetrics
from .alerts import AlertStatus

def create_metrics_table(metrics: SystemMetrics, summary: dict[str, float], recent_metrics: list[SystemMetrics], alerts: AlertStatus) -> Group:
    table = Table(title="System Monitor", box=box.ROUNDED)

    table.add_column("Metric", justify="center")
    table.add_column("Usage", justify="center")
    table.add_column("Bar", justify="center")
    table.add_column("Status", justify="center")

    cpu_status, cpu_color = get_status(metrics.cpu, 50, 80)
    ram_status, ram_color = get_status(metrics.memory, 70, 90)
    disk_status, disk_color = get_status(metrics.disk, 80, 90)

    table.add_row("CPU", f"{metrics.cpu:.1f}%", f"[{cpu_color}]{create_bar(metrics.cpu)}[/{cpu_color}]", f"[{cpu_color}]{cpu_status}[/{cpu_color}]")
    table.add_row("RAM", f"{metrics.memory:.1f}%", f"[{ram_color}]{create_bar(metrics.memory)}[/{ram_color}]", f"[{ram_color}]{ram_status}[/{ram_color}]")
    table.add_row("Disk", f"{metrics.disk:.1f}%", f"[{disk_color}]{create_bar(metrics.disk)}[/{disk_color}]", f"[{disk_color}]{disk_status}[/{disk_color}]")

    timestamp = Text(f"Last updated: {metrics.timestamp.strftime("%Y-%m-%d %H:%M:%S")}", justify="center")

    summary_table = Table(title="History summary", box=box.ROUNDED)

    summary_table.add_column("Metric", justify="center")
    summary_table.add_column("Average", justify="center")

    summary_table.add_row("CPU", f"{summary['avg_cpu']:.1f}%")
    summary_table.add_row("RAM", f"{summary['avg_memory']:.1f}%")
    summary_table.add_row("Disk", f"{summary['avg_disk']:.1f}%")
    
    recents_table = Table(title="Recent Samples", box=box.ROUNDED)

    recents_table.add_column("Time", justify="center")
    recents_table.add_column("CPU", justify="center")
    recents_table.add_column("RAM", justify="center")
    recents_table.add_column("Disk", justify="center")

    for metric in recent_metrics:
        recents_table.add_row(
            metric.timestamp.strftime("%H:%M:%S"),
            f"{metric.cpu:.1f}%",
            f"{metric.memory:.1f}%",
            f"{metric.disk:.1f}%"
        )

    alerts_table = Table(title="Active Alerts", box=box.ROUNDED)

    alerts_table.add_column("Alert", justify="center")

    if alerts.cpu:
        alerts_table.add_row("[bold red]CPU usage has remained critically high[/bold red]")

    if alerts.ram:
        alerts_table.add_row("[bold red]RAM usage has remained critically high[/bold red]")

    if alerts.disk:
        alerts_table.add_row("[bold red]Disk usage has remained critically high[/bold red]")

    if not any((alerts.cpu, alerts.ram, alerts.disk)):
        alerts_table.add_row("[green]No active alerts[/green]")
    
    return Group(
        Align.center(table),
        Align.center(summary_table),
        Align.center(recents_table),
        Align.center(alerts_table),
        Align.center(timestamp)
    )

def create_bar(value: float, width: int = 20) -> str:
    filled = int((value / 100) * width)
    empty = width - filled
    return "█" * filled + "░" * empty

def get_status(value: float, warning: float, critical: float) -> tuple[str, str]:
    """Categorizes health status and color codes it"""
    if value >= critical:
        return "Critical", "bold italic red"
    if value >= warning:
        return "Busy", "italic orange1"
    return "Healthy", "italic green"