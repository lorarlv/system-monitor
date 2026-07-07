from rich.table import Table

from .monitor import SystemMetrics

def create_metrics_table(metrics: SystemMetrics) -> Table:
    table = Table(title="System Monitor")

    table.add_column("Metric")
    table.add_column("Usage")

    table.add_row("CPU", f"{metrics.cpu:.2f}%")
    table.add_row("RAM", f"{metrics.memory:.2f}%")
    table.add_row("Disk", f"{metrics.disk:.2f}%")

    return table