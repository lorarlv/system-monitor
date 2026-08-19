# System monitor
A modular system monitoring application built with Python to practice backend and frontend development, software design, and system programming.

## Overview
System monitor is a personal learning project that has gradually grown from a simple CPU monitor into a full-stack monitoring application.

It collects real-time system information, stores historical data in SQLite, exposes data through a REST API, and provides both a terminal dashboard, as well as a React web dashboard.

---

## Download

Windows builds are available from the GitHub Releases page.

Download the ZIP, extract it, and run `SystemMonitor.exe`.

### Hardware sensor support
Temperature readings depend on hardware support and system permissions.

Some sensors may require running the application as administrator.

## Current features

### Monitoring
- CPU usage
- CPU temperature
- GPU usage
- GPU temperature (if supported)
- VRAM usage
- RAM usage
- disk usage
- network upload/download speed

### Web dashboard
- live system metrics
- temperature indicators
- usage and network activity bars
- active alerts
- historical metric charts
- selectable history time ranges

### Terminal dashboard
- live terminal dashboard built with Rich
- color-coded health indicators
- usage bars
- historical summary
- recent samples
- threshold-based alerts

### Data
- SQLite metric storage
- automatic cleanup of old history
- historical averages
- recent metric retrieval

### API
- FastAPI REST API
- current system metrics
- historical metric data
- alert status
- OpenAPI/Swagger documentation

---

## Tech stack

### Backend
- Python
- FastAPI
- Rich
- psutil
- LibreHardwareMonitor
- SQLite

### Frontend
- React
- TypeScript
- Recharts

### Tools
- Git
- GitHub

---

## Roadmap
Main monitoring features are now in place, so future work will mostly focus on improving the project without adding more metrics.

Things I may add:
- Docker support
- Linux support
- configurable alert thresholds
- exporting metrics to CSV/JSON
- automated testing with CI