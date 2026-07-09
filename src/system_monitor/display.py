from rich.table import Table
from rich.console import Group
from rich.text import Text
from rich.align import Align
from rich import box

from .monitor import SystemMetrics

def create_metrics_table(metrics: SystemMetrics, summary: dict[str, float]) -> Group:
    table = Table(title="System Monitor", box=box.ROUNDED)

    table.add_column("Metric")
    table.add_column("Usage", justify="right")
    table.add_column("Bar")
    table.add_column("Status")

    cpu_status, cpu_color = get_status(metrics.cpu, 50, 80)
    ram_status, ram_color = get_status(metrics.memory, 70, 90)
    disk_status, disk_color = get_status(metrics.disk, 80, 90)

    table.add_row("CPU", f"{metrics.cpu:.1f}%", f"[{cpu_color}]{create_bar(metrics.cpu)}[/{cpu_color}]", f"[{cpu_color}]{cpu_status}[/{cpu_color}]")
    table.add_row("RAM", f"{metrics.memory:.1f}%", f"[{ram_color}]{create_bar(metrics.memory)}[/{ram_color}]", f"[{ram_color}]{ram_status}[/{ram_color}]")
    table.add_row("Disk", f"{metrics.disk:.1f}%", f"[{disk_color}]{create_bar(metrics.disk)}[/{disk_color}]", f"[{disk_color}]{disk_status}[/{disk_color}]")

    timestamp = Text(f"Last updated: {metrics.timestamp.strftime("%Y-%m-%d %H:%M:%S")}", justify="center")

    summary_table = Table(title="History summary", box=box.ROUNDED)

    summary_table.add_column("Metric")
    summary_table.add_column("Average", justify="right")

    summary_table.add_row("CPU", f"{summary['avg_cpu']:.1f}%")
    summary_table.add_row("RAM", f"{summary['avg_memory']:.1f}%")
    summary_table.add_row("Disk", f"{summary['avg_disk']:.1f}%")
    
    return Align.center(Group(table, summary_table, timestamp))

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