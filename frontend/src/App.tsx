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
          />
          <MetricCard
            title="CPU temperature"
            value={
              metrics.cpu_temperature === null
                ? "Unavailable"
                : `${metrics.cpu_temperature.toFixed(1)}°C`
            }
          />
          <MetricCard 
            title="RAM"
            value={`${metrics.memory_percent.toFixed(1)}%`}
            percent={metrics.memory_percent}
            status={getStatus(metrics.memory_percent, 70, 90)}
          />
          <MetricCard 
            title="Disk"
            value={`${metrics.disk_percent.toFixed(1)}%`}
            percent={metrics.disk_percent}
            status={getStatus(metrics.disk_percent, 80, 90)}
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