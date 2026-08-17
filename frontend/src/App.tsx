import { useEffect, useState } from "react";

import "./App.css";

import MetricCard from "./components/MetricCard";
import type { Metrics } from "./types/metrics";
import { formatNetworkRate } from "./utils/format";

function getStatus(
  value: number,
  warning: number,
  critical: number
): "healthy" | "warning" | "critical" {
  if (value >= critical) {
    return "critical";
  }

  if (value >= warning) {
    return "warning";
  }

  return "healthy"
}

function getTemperatureStatus(
  temperature: number
): "cool" | "warm" | "hot" {
  if (temperature >= 90) {
    return "hot";
  }

  if (temperature >= 70) {
    return "warm";
  }

  return "cool";
}

function temperaturePercent(temp: number): number {
  const min = 30;
  const max = 100;

  return Math.max(
    0,
    Math.min(((temp - min) / (max - min)) * 100, 100)
  )
}

function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    const fetchMetrics = () => {
      fetch("http://127.0.0.1:8000/metrics/current")
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
      
          return response.json();
        })
        .then ((data) => {
          setMetrics(data)
        })
        .catch((error) => {
          console.error("Failed to fetch metrics:", error);
        });
      };

      fetchMetrics();

      const interval = setInterval(fetchMetrics, 1000);

      return () => clearInterval(interval);
  }, []);

  const temperatureStatus =
    metrics?.cpu_temperature != null
      ? getTemperatureStatus(metrics.cpu_temperature)
      : undefined;

  return (
    <main className="app">
      <h1 className="app-title">System Monitor</h1>
      
      {metrics ? (
        <div className="metrics-grid">
          <MetricCard 
            title="CPU"
            value={`${metrics.cpu_percent.toFixed(1)}%`}
            percent={metrics.cpu_percent}
            status={getStatus(metrics.cpu_percent, 50, 80)}
            visual="bar"
          />
          <MetricCard
            title="CPU temperature"
            value={
              metrics.cpu_temperature === null
                ? "Unavailable"
                : `${metrics.cpu_temperature.toFixed(1)}°C`
            }
            percent={
              metrics.cpu_temperature === null
                ? undefined
                : temperaturePercent(metrics.cpu_temperature)
            }
            status={temperatureStatus}
            visual="thermometer"
          />
          <MetricCard 
            title="RAM"
            value={`${metrics.memory_percent.toFixed(1)}%`}
            percent={metrics.memory_percent}
            status={getStatus(metrics.memory_percent, 70, 90)}
            visual="bar"
          />
          <MetricCard 
            title="Disk"
            value={`${metrics.disk_percent.toFixed(1)}%`}
            percent={metrics.disk_percent}
            status={getStatus(metrics.disk_percent, 80, 90)}
            visual="bar"
          />
          <MetricCard 
            title="Download"
            value={formatNetworkRate(metrics.download_rate)}
          />
          <MetricCard 
            title="Upload"
            value={formatNetworkRate(metrics.upload_rate)}
          />
        </div>
      ) : (
        <p className="loading">Loading...</p>
      )}
    </main>
  );
}

export default App;