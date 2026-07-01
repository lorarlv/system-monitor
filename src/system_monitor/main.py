import time
from .monitor import get_system_metrics

def main():
    while True:
        metrics = get_system_metrics()
        print(
            f"\rCPU: {metrics['cpu']:5.1f}% | "
            f"Memory: {metrics['memory']:6.2f}% | "
            f"Disk Space Used: {metrics['disk']:5.1f}%",
            end="",
            flush=True,
        )
        time.sleep(1)


if __name__ == "__main__":
    main()