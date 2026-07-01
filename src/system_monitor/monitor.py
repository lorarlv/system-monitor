import psutil

def get_cpu_usage():
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent()

def get_memory_usage():
    """Returns the current memory usage as a percentage."""
    return psutil.virtual_memory().percent

def get_disk_usage():
    """Returns the current disk usage as a percentage."""
    return psutil.disk_usage('/').percent

def get_system_metrics() -> dict:
    """Returns all current system metrics."""
    return {
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage()
    }
