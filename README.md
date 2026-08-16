# System monitor
A modular system monitoring application built with Python to practice backend development, software design, and system programming

## Overview
Sytstem monitor is a personal learning project that has gradually grown from a simple dashboard CPU monitor into a modular application

It collects real-time system information, stores historical data in SQLite, exposes a REST API, and displays everything in a live terminal dashboard

I plan to continue expanding it with new features and improvements to the overall design

---

## Current features

### Monitoring
- CPU usage
- CPU temperature monitoring
- memory usage
- disk usage
- network upload/download speed

### Dashboard
- live terminal dashboard built with Rich
- color-coded health indicators
- usage bars
- historical summary
- recent sample history
- threshold-based alerts

### Data
- SQLite metric storage
- automatic cleanup of old history
- historical averages
- recent metric retrieval

### Interfaces
- command-line interface
- FastAPI REST API
- OpenAPI/Swagger documentation

---

## Roadmap

- React web dashboard
- Docker deployment
- Linux support
- GPU and additional hardware sensors
- configurable alert thresholds
- exporting metrics (CSV / JSON)
- Automated tests
- CI/CD pipeline

---

## Tech stack

### Backend
- Python
- FastAPI
- Rich
- psutil
- LibreHardwareMonitor
- SQLite

### Planned frontend
- React
- TypeScript

### Tools
- Git
- GitHub
- Docker