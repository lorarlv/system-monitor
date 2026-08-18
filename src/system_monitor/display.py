from rich import box
from rich.align import Align
from rich.console import Group
from rich.table import Table
from rich.text import Text

from .alerts import AlertStatus
from .monitor import SystemMetrics

NETWORK_BAR_MAX_MBPS = 50

def create_metrics_table(
    metrics: SystemMetrics,
    summary: dict[str, float],
    recent_metrics: list[SystemMetrics],
    alerts: AlertStatus,
) -> Group:
    table = Table(title="System Monitor", box=box.ROUNDED)

    table.add_column("Metric", justify="center")
    table.add_column("Usage", justify="center")
    table.add_column("Bar", justify="center")
    table.add_column("Status", justify="center")

    cpu_status, cpu_color = get_status(metrics.cpu, 50, 80)
    ram_status, ram_color = get_status(metrics.memory, 70, 90)
    disk_status, disk_color = get_status(metrics.disk, 80, 90)

    if metrics.cpu_temperature is None:
        cpu_temperature_value = "N/A"
        cpu_temperature_status = "[dim]Unavailable[/dim]"
    else:
        temp_status, temp_color = get_temperature_status(metrics.cpu_temperature)

        cpu_temperature_value = f"{metrics.cpu_temperature:.1f}°C"
        cpu_temperature_status = f"[{temp_color}]{temp_status}[/{temp_color}]"

    if metrics.gpu_usage is None:
        gpu_usage_value = "N/A"
        gpu_status = "Unavailable"
        gpu_color = "dim"
    else:
        gpu_usage_value = f"{metrics.gpu_usage:.1f}%"
        gpu_status, gpu_color = get_status(
            metrics.gpu_usage,
            50,
            80,
        )

    if metrics.gpu_temperature is None:
        gpu_temperature_value = "N/A"
        gpu_temperature_status = "[dim]Unavailable[/dim]"
    else:
        gpu_temp_status, gpu_temp_color = get_temperature_status(metrics.gpu_temperature)

        gpu_temperature_value = f"{metrics.gpu_temperature:.1f}°C"
        gpu_temperature_status = (f"[{gpu_temp_color}]{gpu_temp_status}[/{gpu_temp_color}]")

    if (
        metrics.gpu_memory_used is not None
        and metrics.gpu_memory_total is not None
        and metrics.gpu_memory_total > 0
    ):
        gpu_memory_percent = (
            metrics.gpu_memory_used / metrics.gpu_memory_total
        ) * 100

        gpu_memory_value = (
            f"{metrics.gpu_memory_used:.0f} / "
            f"{metrics.gpu_memory_total:.0f} MB"
        )
    else:
        gpu_memory_percent = None
        gpu_memory_value = "N/A"

    if gpu_memory_percent is not None:
        gpu_memory_status, gpu_memory_color = get_status(
            gpu_memory_percent,
            70,
            90,
        )
    else:
        gpu_memory_status = "Unavailable"
        gpu_memory_color = "dim"

    download_percent = network_percent(metrics.download_rate)
    upload_percent = network_percent(metrics.upload_rate)

    table.add_row(
        "CPU",
        f"{metrics.cpu:.1f}%",
        f"[{cpu_color}]{create_bar(metrics.cpu)}[/{cpu_color}]",
        f"[{cpu_color}]{cpu_status}[/{cpu_color}]",
    )

    table.add_row(
        "CPU Temp",
        cpu_temperature_value,
        "",
        cpu_temperature_status,
    )

    table.add_row(
        "GPU",
        gpu_usage_value,
        (
            f"[{gpu_color}]"
            f"{create_bar(metrics.gpu_usage)}"
            f"[/{gpu_color}]"
            if metrics.gpu_usage is not None
            else ""
        ),
        f"[{gpu_color}]{gpu_status}[/{gpu_color}]",
    )

    table.add_row(
        "GPU Temp",
        gpu_temperature_value,
        "",
        gpu_temperature_status,
    )

    table.add_row(
        "VRAM",
        gpu_memory_value,
        (
            f"[{gpu_memory_color}]"
            f"{create_bar(gpu_memory_percent)}"
            f"[/{gpu_memory_color}]"
            if gpu_memory_percent is not None
            else ""
        ),
        (
            f"[{gpu_memory_color}]"
            f"{gpu_memory_status}"
            f"[/{gpu_memory_color}]"
        ),
    )

    table.add_row(
        "RAM",
        f"{metrics.memory:.1f}%",
        f"[{ram_color}]{create_bar(metrics.memory)}[/{ram_color}]",
        f"[{ram_color}]{ram_status}[/{ram_color}]",
    )

    table.add_row(
        "Disk",
        f"{metrics.disk:.1f}%",
        f"[{disk_color}]{create_bar(metrics.disk)}[/{disk_color}]",
        f"[{disk_color}]{disk_status}[/{disk_color}]",
    )

    table.add_row(
        "Download",
        format_network_rate(metrics.download_rate),
        f"[blue]{create_bar(download_percent)}[/blue]",
        "",
    )

    table.add_row(
        "Upload",
        format_network_rate(metrics.upload_rate),
        f"[blue]{create_bar(upload_percent)}[/blue]",
        "",
    )

    timestamp = Text(
        f"Last updated: "
        f"{metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        justify="center",
    )

    summary_table = Table(
        title="History summary",
        box=box.ROUNDED,
    )

    summary_table.add_column("Metric", justify="center")
    summary_table.add_column("Average", justify="center")

    summary_table.add_row(
        "CPU",
        f"{summary['avg_cpu']:.1f}%",
    )

    summary_table.add_row(
        "CPU Temp",
        f"{summary['avg_cpu_temperature']:.1f}°C",
    )

    summary_table.add_row(
        "RAM",
        f"{summary['avg_memory']:.1f}%",
    )

    summary_table.add_row(
        "Disk",
        f"{summary['avg_disk']:.1f}%",
    )

    recents_table = Table(
        title="Recent Samples",
        box=box.ROUNDED,
    )

    recents_table.add_column("Time", justify="center")
    recents_table.add_column("CPU", justify="center")
    recents_table.add_column("CPU Temp", justify="center")
    recents_table.add_column("RAM", justify="center")
    recents_table.add_column("Disk", justify="center")

    for metric in recent_metrics:
        cpu_temp = (
            f"{metric.cpu_temperature:.1f}°C"
            if metric.cpu_temperature is not None
            else "N/A"
        )

        recents_table.add_row(
            metric.timestamp.strftime("%H:%M:%S"),
            f"{metric.cpu:.1f}%",
            cpu_temp,
            f"{metric.memory:.1f}%",
            f"{metric.disk:.1f}%",
        )

    alerts_table = Table(title="Active Alerts", box=box.ROUNDED)

    alerts_table.add_column("Alert", justify="center")

    if alerts.cpu:
        alerts_table.add_row(
            "[bold red]"
            "CPU usage has remained critically high"
            "[/bold red]"
        )

    if alerts.temperature:
        alerts_table.add_row(
            "[bold red]"
            "CPU temperature has remained critically high"
            "[/bold red]"
        )

    if alerts.ram:
        alerts_table.add_row(
            "[bold red]"
            "RAM usage has remained critically high"
            "[/bold red]"
        )

    if alerts.disk:
        alerts_table.add_row(
            "[bold red]"
            "Disk usage has remained critically high"
            "[/bold red]"
        )

    if not any((alerts.cpu, alerts.temperature, alerts.ram, alerts.disk)):
        alerts_table.add_row("[green]No active alerts[/green]")

    return Group(
        Align.center(table),
        Align.center(summary_table),
        Align.center(recents_table),
        Align.center(alerts_table),
        Align.center(timestamp),
    )


def create_bar(
    value: float,
    width: int = 20,
) -> str:
    value = max(0.0, min(value, 100.0))

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


def get_temperature_status(temperature: float) -> tuple[str, str]:
    if temperature >= 90:
        return "Hot", "bold italic red"

    if temperature >= 75:
        return "Warm", "italic orange1"

    return "Normal", "italic green"


def format_network_rate(rate_bytes_per_sec: float) -> str:
    if rate_bytes_per_sec < 1024:
        return f"{rate_bytes_per_sec:.0f} B/s"

    if rate_bytes_per_sec < 1024**2:
        return f"{rate_bytes_per_sec / 1024:.1f} KB/s"

    if rate_bytes_per_sec < 1024**3:
        return f"{rate_bytes_per_sec / (1024**2):.2f} MB/s"

    return f"{rate_bytes_per_sec / (1024**3):.2f} GB/s"


def network_percent(rate_bytes_per_sec: float) -> float:
    rate_mbps = rate_bytes_per_sec * 8 / 1_000_000

    percent = rate_mbps / NETWORK_BAR_MAX_MBPS * 100

    return min(percent, 100.0)