import time
from .monitor import get_cpu_usage

def main():
    while True:
        cpu = get_cpu_usage()
        print(f"\rCurrent CPU usage: {cpu:5.1f}%", end="", flush=True)
        time.sleep(1)


if __name__ == "__main__":
    main()