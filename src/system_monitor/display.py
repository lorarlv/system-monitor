from rich.table import Table

from .monitor import SystemMetrics
from .monitor import get_status

def create_metrics_table(metrics: SystemMetrics) -> Table:
    table = Table(title="System Monitor")

    table.add_column("Metric")
    table.add_column("Usage")
    table.add_column("Status")

    cpu_status, cpu_color = get_status(metrics.cpu, 50, 80)
    ram_status, ram_color = get_status(metrics.memory, 70, 90)
    disk_status, disk_color = get_status(metrics.disk, 80, 90)

    table.add_row("CPU", f"{metrics.cpu:.1f}%", f"[{cpu_color}]{cpu_status}[/{cpu_color}]")
    table.add_row("RAM", f"{metrics.memory:.1f}%", f"[{ram_color}]{ram_status}[/{ram_color}]")
    table.add_row("Disk", f"{metrics.disk:.1f}%", f"[{disk_color}]{disk_status}[/{disk_color}]")

    return table