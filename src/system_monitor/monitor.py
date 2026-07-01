import psutil

def get_cpu_usage():
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent(interval=1)
